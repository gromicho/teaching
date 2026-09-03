$ErrorActionPreference = 'Stop'

$sourcePath = 'C:\local\projects\modernize ABW\slides\authoritative\Lecture 2 - 2025-2026.pptx'
$outputRoot = 'C:\local\projects\modernize ABW\beamer\lecture-2-2026-native'
$assetRoot = Join-Path $outputRoot 'assets\template'
$metadataPath = Join-Path $outputRoot 'powerpoint-template-objects.json'
New-Item -ItemType Directory -Force -Path $assetRoot | Out-Null

function Shape-Record($shape, $scopeTag, $index) {
    $text = ''
    try {
        if ([int]$shape.HasTextFrame -eq -1 -and [int]$shape.TextFrame.HasText -eq -1) {
            $text = [string]$shape.TextFrame.TextRange.Text
        }
    } catch {}
    $filename = ('{0}-object-{1:D2}.png' -f $scopeTag, $index)
    $assetPath = Join-Path $assetRoot $filename
    $asset = $null
    try {
        if ($shape.Width -gt 2 -and $shape.Height -gt 2) {
            $shape.Export($assetPath, 2)
            if (Test-Path -LiteralPath $assetPath) { $asset = 'assets/template/' + $filename }
        }
    } catch {}
    return [ordered]@{
        index = $index
        name = [string]$shape.Name
        type = [int]$shape.Type
        left = [double]$shape.Left
        top = [double]$shape.Top
        width = [double]$shape.Width
        height = [double]$shape.Height
        text = $text
        asset = $asset
    }
}

$powerPoint = New-Object -ComObject PowerPoint.Application
$presentation = $null
try {
    $presentation = $powerPoint.Presentations.Open($sourcePath, $true, $false, $false)
    $master = $presentation.SlideMaster
    $masterObjects = @()
    for ($i = 1; $i -le $master.Shapes.Count; $i++) {
        $masterObjects += Shape-Record $master.Shapes.Item($i) 'master' $i
    }
    $layouts = @()
    for ($layoutIndex = 1; $layoutIndex -le $master.CustomLayouts.Count; $layoutIndex++) {
        $layout = $master.CustomLayouts.Item($layoutIndex)
        $layoutObjects = @()
        $tag = 'layout-' + $layoutIndex.ToString('D2')
        for ($shapeIndex = 1; $shapeIndex -le $layout.Shapes.Count; $shapeIndex++) {
            $layoutObjects += Shape-Record $layout.Shapes.Item($shapeIndex) $tag $shapeIndex
        }
        $layouts += [ordered]@{
            index = $layoutIndex
            name = [string]$layout.Name
            objects = $layoutObjects
        }
    }
    $slideLayouts = @()
    for ($slideIndex = 1; $slideIndex -le $presentation.Slides.Count; $slideIndex++) {
        $slide = $presentation.Slides.Item($slideIndex)
        $layoutIndex = $null
        for ($candidate = 1; $candidate -le $master.CustomLayouts.Count; $candidate++) {
            if ($master.CustomLayouts.Item($candidate).Name -eq $slide.CustomLayout.Name) {
                $layoutIndex = $candidate
                break
            }
        }
        $slideLayouts += [ordered]@{
            slide = $slideIndex
            layoutIndex = $layoutIndex
            layoutName = [string]$slide.CustomLayout.Name
            followMasterBackground = $(try { [int]$slide.FollowMasterBackground } catch { $null })
        }
    }
    [ordered]@{
        source = $sourcePath
        masterObjects = $masterObjects
        layouts = $layouts
        slideLayouts = $slideLayouts
    } | ConvertTo-Json -Depth 20 | Set-Content -LiteralPath $metadataPath -Encoding UTF8
} finally {
    if ($null -ne $presentation) { $presentation.Close() }
    $powerPoint.Quit()
}

Write-Output ('Metadata: ' + $metadataPath)
Get-ChildItem -LiteralPath $assetRoot -File | Select-Object Name,Length | Format-Table -AutoSize

