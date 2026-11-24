import fs from 'node:fs';
import path from 'node:path';
import readline from 'node:readline';
import {fileURLToPath} from 'node:url';
const base=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const raw=path.join(base,'data_raw'), clean=path.join(base,'data_clean');
const source='https://www.wcoomd.org/en/topics/nomenclature/instrument-and-tools/hs_nomenclature_previous_editions/hs_nomenclature_table_2002.aspx';
function assert(ok,msg){if(!ok) throw Error(msg);}
function parse(line){const out=[];let s='',q=false;for(let i=0;i<line.length;i++){const c=line[i];if(c==='"'){if(q&&line[i+1]==='"'){s+='"';i++;}else q=!q;}else if(c===','&&!q){out.push(s);s='';}else s+=c;}out.push(s);return out;}
function read(file){const lines=fs.readFileSync(file,'utf8').replace(/^\uFEFF/,'').trim().split(/\r?\n/);const h=parse(lines.shift());return lines.map(l=>Object.fromEntries(parse(l).map((v,i)=>[h[i],v])));}
function write(name,rows,headers){const esc=v=>{const s=String(v??'');return /[",\r\n]/.test(s)?'"'+s.replaceAll('"','""')+'"':s;};fs.writeFileSync(path.join(clean,name),'\uFEFF'+[headers,...rows.map(r=>headers.map(h=>r[h]))].map(r=>r.map(esc).join(',')).join('\n')+'\n');}
function text(s){return s.replace(/<[^>]*>/g,' ').replace(/&nbsp;|&#160;/g,' ').replace(/&eacute;/g,'é').replace(/&amp;/g,'&').replace(/&quot;/g,'"').replace(/&#39;|&apos;/g,"'").replace(/\s+/g,' ').trim();}
const html=fs.readFileSync(path.join(raw,'hs2002_wco_source.html'),'utf8');
let section=null;const chapters=[];const sections=new Map();
for(const match of html.matchAll(/<tr\b[^>]*>([\s\S]*?)<\/tr>/gi)){
 const cells=[...match[1].matchAll(/<td\b[^>]*>([\s\S]*?)<\/td>/gi)].map(x=>text(x[1]));
 const sec=cells.find(c=>/^SECTION [IVX]+\s/.test(c));
 if(sec){const m=sec.match(/^SECTION ([IVX]+)\s+(.+)$/);section={section_code:m[1],section_name:m[2]};sections.set(m[1],m[2]);}
 if(cells.length>=2&&/^\d{1,2}$/.test(cells[0])&&section){const hs2=cells[0].padStart(2,'0');if(hs2==='77')continue;chapters.push({hs2,chapter_name:cells[1],...section,hs_revision:'HS2002',source_url:source});}
}
assert(chapters.length===96&&new Set(chapters.map(r=>r.hs2)).size===96,'Expected 96 unique HS chapters');
assert(sections.size===21,'Expected 21 HS sections');
const chapterMap=new Map(chapters.map(r=>[r.hs2,r]));
const hsChecks=[];
for(const filename of ['product_year','partner_product_year']){
 const rows=read(path.join(clean,filename+'.csv'));const keys=Object.keys(rows[0]);let before=0,after=0;
 const enriched=rows.map(r=>{before+=Number(r.trade_usd);const m=chapterMap.get(r.hs2.padStart(2,'0'));assert(m,'Unknown chapter '+r.hs2);const e={...r,chapter_name:m.chapter_name,section_code:m.section_code,section_name:m.section_name};after+=Number(e.trade_usd);return e;});
 assert(before===after,'Enrichment changed trade values');
 write(filename+'_enriched.csv',enriched,[...keys,'chapter_name','section_code','section_name']);
 const agg=new Map();const groupKeys=['year','trade_flow',...(filename.startsWith('partner')?['partner_code']:[]),'section_code','section_name'];
 for(const r of enriched){const k=groupKeys.map(x=>r[x]).join('|');if(!agg.has(k))agg.set(k,{...Object.fromEntries(groupKeys.map(x=>[x,r[x]])),trade_usd:0});agg.get(k).trade_usd+=Number(r.trade_usd);}
 write(filename.startsWith('partner')?'partner_section_year.csv':'section_year.csv',[...agg.values()],[...groupKeys,'trade_usd']);
 hsChecks.push({table:filename,rows:rows.length,missing_classifications:0,total_before_usd:before,total_after_usd:after});
}
write('hs_classification.csv',chapters,['hs2','chapter_name','section_code','section_name','hs_revision','source_url']);
console.log('HS: 96 chapters mapped to 21 sections; enriched tables verified.');
if(process.argv.includes('--hs-only')) process.exit(0);
const countries=read(path.join(raw,'country_codes_V202601.csv'));const countryMap=new Map(countries.map(r=>[r.country_code,r]));
const partnerRows=read(path.join(clean,'partner_year.csv'));const ranking=new Map();
for(const r of partnerRows){const y=Number(r.year);if(y>=2005&&y<=2024)ranking.set(r.partner_code,(ranking.get(r.partner_code)||0)+Number(r.trade_usd));}
const top=[...ranking].sort((a,b)=>b[1]-a[1]||Number(a[0])-Number(b[0])).slice(0,30);
// Fixed historical ASEAN-10 membership for the 2005-2024 study; not current membership.
const asean=new Set(['96','116','360','418','458','104','608','702','764','704']);
const nodes=new Set([...asean,...top.map(r=>r[0])]);
const nodeRows=[...nodes].sort((a,b)=>Number(a)-Number(b)).map(code=>{const c=countryMap.get(code);assert(c,'Missing country '+code);const rank=top.findIndex(r=>r[0]===code);return {country_code:code,country_iso3:c.country_iso3,country_name:c.country_name,is_asean_2005_2024:asean.has(code),top30_rank:rank<0?'':rank+1,vietnam_total_trade_2005_2024_usd:ranking.get(code)||0};});
write('network_nodes.csv',nodeRows,Object.keys(nodeRows[0]));
const edgeRows=[],networkChecks=[];
for(let year=2005;year<=2024;year++){
 const edges=new Map();let rawRows=0,keptRows=0;
 const input=readline.createInterface({input:fs.createReadStream(path.join(raw,`BACI_HS02_Y${year}_V202601.csv`)),crlfDelay:Infinity});let header=true;
 for await(const line of input){if(header){assert(line.replace(/^\uFEFF/,'').trim()==='t,i,j,k,v,q','Unexpected BACI schema');header=false;continue;}if(!line.trim())continue;rawRows++;const p=line.split(',');const i=p[1],j=p[2];if(!nodes.has(i)||!nodes.has(j)||i===j)continue;assert(Number(p[0])===year,'Wrong year');const value=Number(p[4])*1000;assert(Number.isFinite(value)&&value>=0,'Invalid value');const key=i+'|'+j;edges.set(key,(edges.get(key)||0)+value);keptRows++;}
 // Independent reference: existing Vietnam partner aggregates restricted to identical nodes.
 let maxDiff=0;for(const r of partnerRows.filter(r=>Number(r.year)===year&&nodes.has(r.partner_code))){const key=r.trade_flow==='Export'?'704|'+r.partner_code:r.partner_code+'|704';const expected=Number(r.trade_usd),actual=edges.get(key)||0;const diff=Math.abs(actual-expected);assert(diff<=Math.max(1,Math.abs(expected)*1e-10),'Vietnam edge mismatch '+year+' '+key);maxDiff=Math.max(maxDiff,diff);}
 for(const [key,value]of edges){const [i,j]=key.split('|');edgeRows.push({year,exporter_code:i,importer_code:j,trade_usd:value});}
 networkChecks.push({year,raw_rows:rawRows,kept_product_rows:keptRows,directed_edges:edges.size,max_vietnam_reference_difference_usd:maxDiff});
 console.log(`Network ${year}: ${keptRows} product rows -> ${edges.size} directed edges; Vietnam checks passed.`);
}
write('network_year.csv',edgeRows,['year','exporter_code','importer_code','trade_usd']);
fs.writeFileSync(path.join(base,'audit_results','hs_network_validation.json'),JSON.stringify({hs:hsChecks,chapter_count:96,section_count:21,network_node_count:nodes.size,network:networkChecks,selection:'Historical ASEAN-10 plus top 30 Vietnam partners by cumulative nominal exports+imports, 2005-2024; fixed node list',source_url:source},null,2));
console.log('DONE. Originals unchanged. Nodes: '+nodes.size+'; directed year-edges: '+edgeRows.length);
