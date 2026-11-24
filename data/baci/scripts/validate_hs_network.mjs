import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
const base=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'../data_clean');
function parse(l){const a=[];let s='',q=false;for(let i=0;i<l.length;i++){if(l[i]==='"'){if(q&&l[i+1]==='"'){s+='"';i++;}else q=!q;}else if(l[i]===','&&!q){a.push(s);s='';}else s+=l[i];}a.push(s);return a;}
function read(n){const l=fs.readFileSync(path.join(base,n),'utf8').replace(/^\uFEFF/,'').trim().split(/\r?\n/);const h=parse(l.shift());return l.map(x=>Object.fromEntries(parse(x).map((v,i)=>[h[i],v])));}
function check(x,m){if(!x)throw Error(m);}
function sums(rows){const m=new Map();for(const r of rows){const k=[r.year,r.trade_flow,r.partner_code||''].join('|');m.set(k,(m.get(k)||0)+Number(r.trade_usd));}return m;}
for(const pair of [['product_year.csv','section_year.csv'],['partner_product_year.csv','partner_section_year.csv']]){
 const a=sums(read(pair[0])),b=sums(read(pair[1]));check(a.size===b.size,'Group count mismatch');let max=0;
 for(const [k,v]of a){const d=Math.abs(v-b.get(k));check(Number.isFinite(d)&&d<=Math.max(1,v*1e-10),'Section total mismatch '+k);max=Math.max(max,d);}
 console.log(pair[1]+': '+a.size+' groups reconciled; max rounding difference USD '+max);
}
for(const stem of ['product_year','partner_product_year']){
 const a=read(stem+'.csv'),b=read(stem+'_enriched.csv');check(a.length===b.length,'Row count changed');
 for(let i=0;i<a.length;i++){for(const k of Object.keys(a[i]))check(a[i][k]===b[i][k],'Original field changed');check(b[i].section_code&&b[i].section_name&&b[i].chapter_name,'Missing classification');check(!/&[a-z]+;/.test(b[i].chapter_name),'Undecoded HTML');}
 console.log(stem+': every original field preserved, all rows classified.');
}
if(!process.argv.includes('--hs-only')){
 const nodes=new Set(read('network_nodes.csv').map(r=>r.country_code)),edges=read('network_year.csv'),keys=new Set(),years=new Set();let nonVietnam=0;
 for(const r of edges){const k=[r.year,r.exporter_code,r.importer_code].join('|');check(!keys.has(k),'Duplicate edge');keys.add(k);years.add(Number(r.year));check(nodes.has(r.exporter_code)&&nodes.has(r.importer_code),'Unknown node');check(r.exporter_code!==r.importer_code,'Self trade');check(Number.isFinite(Number(r.trade_usd))&&Number(r.trade_usd)>=0,'Invalid value');if(r.exporter_code!=='704'&&r.importer_code!=='704')nonVietnam++;}
 check(years.size===20&&Math.min(...years)===2005&&Math.max(...years)===2024,'Year coverage');check(nonVietnam>0,'Missing non-Vietnam edges');
 for(const [i,j]of [['764','842'],['702','764'],['764','702']])check(keys.has(['2024',i,j].join('|')),'Missing example edge '+i+' '+j);
 console.log('Network: '+edges.length+' unique directed year-edges; '+nodes.size+' nodes; '+nonVietnam+' edges without Vietnam; 20 years verified.');
}
