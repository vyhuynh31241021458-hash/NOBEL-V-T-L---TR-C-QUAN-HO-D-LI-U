$ErrorActionPreference = 'Stop'
$project = Split-Path -Parent $PSScriptRoot
$out = Join-Path $project 'audit_results'
$culture = [System.Globalization.CultureInfo]::InvariantCulture
function Number($value) { [double]::Parse([string]$value, $culture) }
function Read-Observation($file, $reporter, $partner, $period, $flow) {
    $response = Get-Content -Raw -LiteralPath (Join-Path $out $file) | ConvertFrom-Json
    if ($response.error -or $response.count -ne 1) { throw "Invalid response: $file" }
    $row = $response.data[0]
    if ($row.reporterCode -ne $reporter -or $row.partnerCode -ne $partner -or
        $row.period -ne $period -or $row.flowCode -ne $flow -or $row.cmdCode -ne 'TOTAL') {
        throw "Unexpected observation: $file"
    }
    return $row
}
$comparison = Import-Csv -LiteralPath (Join-Path $out '03_baci_wdi_comparison.csv')
$annual = $comparison | Where-Object year -eq '2024'
$gap = (Number $annual.export_usd) - (Number $annual.wdi_merchandise_exports_usd)
$partners = Import-Csv -LiteralPath (Join-Path $out '06_export_partners_2024.csv')
$references = @(
    @{code='156';name='China';reported=61200000000;file='comtrade_chn_imports_vnm_2024_total.json'},
    @{code='842';name='USA';reported=119500000000;file='comtrade_usa_imports_vnm_2024_total.json'}
)
$source = 'https://wtocenter.vn/download/19792/bao-cao-xnk-vn-2024-1534_compressed.pdf'
$result = foreach ($reference in $references) {
    $baci = $partners | Where-Object partner_code -eq $reference.code
    if (@($baci).Count -ne 1) { throw 'Partner is not unique' }
    $mirror = Read-Observation $reference.file ([int]$reference.code) 704 '2024' 'M'
    $baciValue = Number $baci.export_usd
    [pscustomobject]@{
        year=2024
        partner=$reference.name
        baci_export_usd=$baciValue
        vn_published_export_usd_rounded=$reference.reported
        baci_minus_vn_published_usd=$baciValue-$reference.reported
        share_of_baci_wdi_total_gap_pct=100*($baciValue-$reference.reported)/$gap
        partner_reported_import_cif_usd=$mirror.cifvalue
        partner_reported_import_fob_usd=$mirror.fobvalue
        mirror_minus_vn_published_usd=(Number $mirror.primaryValue)-$reference.reported
        vn_published_source=$source
        note='Rounded national reference; diagnostic only, not an exact decomposition of the WDI total. Comtrade is a current snapshot, not the input vintage used by BACI.'
    }
}
$result | Export-Csv -NoTypeInformation -Encoding UTF8 -LiteralPath (Join-Path $out '07_export_gap_partner_evidence_2024.csv')
$products = Import-Csv -LiteralPath (Join-Path $project 'data_clean/partner_product_year.csv') |
    Where-Object { $_.year -eq '2024' -and $_.trade_flow -eq 'Export' -and $_.partner_code -in @('156','842') } |
    Sort-Object { Number $_.trade_usd } -Descending |
    Select-Object year,partner_code,hs2,trade_usd,@{n='note';e={'BACI value only; not a measured discrepancy by product'}}
$products | Export-Csv -NoTypeInformation -Encoding UTF8 -LiteralPath (Join-Path $out '08_baci_export_products_china_usa_2024.csv')
$checks = foreach ($file in @('comtrade_vnm_exports_2024_total.json','comtrade_vnm_exports_2024_H6.json','comtrade_vnm_exports_2024_H2.json')) {
    $response = Get-Content -Raw -LiteralPath (Join-Path $out $file) | ConvertFrom-Json
    if ($response.error -or $response.count -ne 0) { throw "Unexpected response: $file" }
    [pscustomobject]@{file=$file;count=$response.count;interpretation='No observation returned by this query. Not proof of absence in the historical BACI input.'}
}
$v23 = Read-Observation 'comtrade_vnm_exports_2023_total.json' 704 0 '2023' 'X'
$result | Format-Table partner,baci_export_usd,vn_published_export_usd_rounded,baci_minus_vn_published_usd
Write-Output ('Combined diagnostic difference: ' + (($result | Measure-Object baci_minus_vn_published_usd -Sum).Sum))
Write-Output ('BACI-WDI total difference: ' + $gap)
Write-Output ('Vietnam 2023 Comtrade exports, control query: ' + $v23.primaryValue)
$checks | Format-Table file,count
