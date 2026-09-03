$ErrorActionPreference = 'Stop'
$source = 'C:\local\projects\modernize ABW\slides\authoritative\Lecture 2 - 2025-2026.pptx'
$output = 'C:\local\projects\modernize ABW\beamer\lecture-2-2026-native\powerpoint-table-dimensions.json'
$powerPoint = New-Object -ComObject PowerPoint.Application
$presentation = $null
try {
    $presentation = $powerPoint.Presentations.Open($source, $true, $false, $false)
    $tables = @()
    for ($slideIndex = 1; $slideIndex -le $presentation.Slides.Count; $slideIndex++) {
        $slide = $presentation.Slides.Item($slideIndex)
        for ($shapeIndex = 1; $shapeIndex -le $slide.Shapes.Count; $shapeIndex++) {
            $shape = $slide.Shapes.Item($shapeIndex)
            if ([int]$shape.Type -eq 19) {
                $rowHeights = @()
                for ($row = 1; $row -le $shape.Table.Rows.Count; $row++) {
                    $rowHeights += [double]$shape.Table.Rows.Item($row).Height
                }
                $columnWidths = @()
                for ($column = 1; $column -le $shape.Table.Columns.Count; $column++) {
                    $columnWidths += [double]$shape.Table.Columns.Item($column).Width
                }
                $tables += [ordered]@{
                    slide = $slideIndex
                    path = $shapeIndex.ToString('D3')
                    rowHeights = $rowHeights
                    columnWidths = $columnWidths
                }
            }
        }
    }
    $tables | ConvertTo-Json -Depth 10 | Set-Content -LiteralPath $output -Encoding UTF8
} finally {
    if ($null -ne $presentation) { $presentation.Close() }
    $powerPoint.Quit()
}
Write-Output ('Metadata: ' + $output)
Get-Content -LiteralPath $output

