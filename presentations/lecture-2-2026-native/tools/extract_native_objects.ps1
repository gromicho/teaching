$ErrorActionPreference = 'Stop'

$sourcePath = 'C:\local\projects\modernize ABW\slides\authoritative\Lecture 2 - 2025-2026.pptx'
$outputRoot = 'C:\local\projects\modernize ABW\beamer\lecture-2-2026-native'
$assetRoot = Join-Path $outputRoot 'assets\source'
$metadataPath = Join-Path $outputRoot 'powerpoint-objects.json'
New-Item -ItemType Directory -Force -Path $assetRoot | Out-Null

function Get-ColorHex($colorObject) {
    try {
        $value = [int64]$colorObject.RGB
        if ($value -lt 0) { return $null }
        $red = $value -band 255
        $green = ($value -shr 8) -band 255
        $blue = ($value -shr 16) -band 255
        return ('#{0:X2}{1:X2}{2:X2}' -f $red, $green, $blue)
    } catch {
        return $null
    }
}

function Get-FontRecord($font) {
    $size = $null
    try { if ([double]$font.Size -gt 0) { $size = [double]$font.Size } } catch {}
    $name = $null
    try { $name = [string]$font.Name } catch {}
    $color = $null
    try { $color = Get-ColorHex $font.Color } catch {}
    $bold = $false
    $italic = $false
    $underline = $false
    try { $bold = ([int]$font.Bold -eq -1) } catch {}
    try { $italic = ([int]$font.Italic -eq -1) } catch {}
    try { $underline = ([int]$font.Underline -eq -1) } catch {}
    return [ordered]@{
        name = $name
        size = $size
        color = $color
        bold = $bold
        italic = $italic
        underline = $underline
    }
}

function Get-ParagraphRecords($shape) {
    $records = @()
    try {
        if ([int]$shape.HasTextFrame -ne -1 -or [int]$shape.TextFrame.HasText -ne -1) {
            return $records
        }
        $range = $shape.TextFrame.TextRange
        $count = [int]$range.Paragraphs().Count
        for ($index = 1; $index -le $count; $index++) {
            $paragraph = $range.Paragraphs($index, 1)
            $text = ([string]$paragraph.Text).TrimEnd("`r", "`n", "`t")
            $font = Get-FontRecord $paragraph.Font
            if ($null -eq $font.size -and $paragraph.Length -gt 0) {
                $font = Get-FontRecord $paragraph.Characters(1, 1).Font
            }
            $alignment = 1
            $bullet = $false
            $level = 1
            try { $alignment = [int]$paragraph.ParagraphFormat.Alignment } catch {}
            try { $bullet = ([int]$paragraph.ParagraphFormat.Bullet.Visible -eq -1) } catch {}
            try { $level = [int]$paragraph.IndentLevel } catch {}
            $records += [ordered]@{
                text = $text
                font = $font
                alignment = $alignment
                bullet = $bullet
                level = $level
            }
        }
    } catch {}
    return $records
}

function Get-ShapeRecord($shape, $slideNumber, $objectNumber, $pathTag) {
    $record = [ordered]@{
        object = $objectNumber
        path = $pathTag
        name = [string]$shape.Name
        type = [int]$shape.Type
        z = [int]$shape.ZOrderPosition
        left = [double]$shape.Left
        top = [double]$shape.Top
        width = [double]$shape.Width
        height = [double]$shape.Height
        rotation = [double]$shape.Rotation
        autoShapeType = $null
        placeholderType = $null
        fillVisible = $false
        fillColor = $null
        fillTransparency = 0.0
        lineVisible = $false
        lineColor = $null
        lineWeight = 0.0
        lineDash = $null
        beginArrow = $null
        endArrow = $null
        verticalAnchor = $null
        margins = $null
        paragraphs = @()
        table = $null
        asset = $null
        children = @()
    }

    try { $record.autoShapeType = [int]$shape.AutoShapeType } catch {}
    try { $record.placeholderType = [int]$shape.PlaceholderFormat.Type } catch {}
    try {
        $record.fillVisible = ([int]$shape.Fill.Visible -eq -1)
        if ($record.fillVisible) {
            $record.fillColor = Get-ColorHex $shape.Fill.ForeColor
            $record.fillTransparency = [double]$shape.Fill.Transparency
        }
    } catch {}
    try {
        $record.lineVisible = ([int]$shape.Line.Visible -eq -1)
        if ($record.lineVisible) {
            $record.lineColor = Get-ColorHex $shape.Line.ForeColor
            $record.lineWeight = [double]$shape.Line.Weight
            $record.lineDash = [int]$shape.Line.DashStyle
            $record.beginArrow = [int]$shape.Line.BeginArrowheadStyle
            $record.endArrow = [int]$shape.Line.EndArrowheadStyle
        }
    } catch {}
    try {
        $record.verticalAnchor = [int]$shape.TextFrame.VerticalAnchor
        $record.margins = [ordered]@{
            left = [double]$shape.TextFrame.MarginLeft
            right = [double]$shape.TextFrame.MarginRight
            top = [double]$shape.TextFrame.MarginTop
            bottom = [double]$shape.TextFrame.MarginBottom
        }
    } catch {}
    $record.paragraphs = @(Get-ParagraphRecords $shape)

    if ([int]$shape.Type -eq 6) {
        $children = @()
        for ($childIndex = 1; $childIndex -le $shape.GroupItems.Count; $childIndex++) {
            $child = $shape.GroupItems.Item($childIndex)
            $childTag = $pathTag + '-' + $childIndex.ToString('D2')
            $children += Get-ShapeRecord $child $slideNumber $objectNumber $childTag
        }
        $record.children = $children
    } elseif ([int]$shape.Type -eq 19) {
        $rows = @()
        for ($rowIndex = 1; $rowIndex -le $shape.Table.Rows.Count; $rowIndex++) {
            $cells = @()
            for ($columnIndex = 1; $columnIndex -le $shape.Table.Columns.Count; $columnIndex++) {
                $cellShape = $shape.Table.Cell($rowIndex, $columnIndex).Shape
                $cells += [ordered]@{
                    text = [string]$cellShape.TextFrame.TextRange.Text.TrimEnd("`r", "`n")
                    paragraphs = @(Get-ParagraphRecords $cellShape)
                    fillColor = $(try { Get-ColorHex $cellShape.Fill.ForeColor } catch { $null })
                }
            }
            $rows += ,$cells
        }
        $record.table = [ordered]@{
            rows = $shape.Table.Rows.Count
            columns = $shape.Table.Columns.Count
            cells = $rows
        }
    } else {
        $shouldExport = ([int]$shape.Type -in @(3, 7, 11, 13, 16, 21, 24, 28, 29, 31, 32))
        if ([int]$shape.Type -eq 14 -and $record.paragraphs.Count -eq 0) { $shouldExport = $true }
        if ($shouldExport -and $shape.Width -gt 2 -and $shape.Height -gt 2) {
            $filename = ('slide-{0:D2}-object-{1}.png' -f $slideNumber, $pathTag)
            $assetPath = Join-Path $assetRoot $filename
            try {
                $shape.Export($assetPath, 2)
                if (Test-Path -LiteralPath $assetPath) { $record.asset = 'assets/source/' + $filename }
            } catch {}
        }
    }

    return [pscustomobject]$record
}

$powerPoint = New-Object -ComObject PowerPoint.Application
$presentation = $null
try {
    $presentation = $powerPoint.Presentations.Open($sourcePath, $true, $false, $false)
    $slides = @()
    for ($slideNumber = 1; $slideNumber -le $presentation.Slides.Count; $slideNumber++) {
        $slide = $presentation.Slides.Item($slideNumber)
        $objects = @()
        for ($shapeIndex = 1; $shapeIndex -le $slide.Shapes.Count; $shapeIndex++) {
            $shape = $slide.Shapes.Item($shapeIndex)
            $objects += Get-ShapeRecord $shape $slideNumber $shapeIndex $shapeIndex.ToString('D3')
        }
        $slides += [ordered]@{
            slide = $slideNumber
            name = [string]$slide.Name
            objects = $objects
        }
        if (($slideNumber % 10) -eq 0 -or $slideNumber -eq $presentation.Slides.Count) {
            Write-Output ('Extracted ' + $slideNumber + '/' + $presentation.Slides.Count)
        }
    }
    $metadata = [ordered]@{
        source = $sourcePath
        slideWidthPoints = [double]$presentation.PageSetup.SlideWidth
        slideHeightPoints = [double]$presentation.PageSetup.SlideHeight
        slideCount = [int]$presentation.Slides.Count
        slides = $slides
    }
    $metadata | ConvertTo-Json -Depth 30 | Set-Content -LiteralPath $metadataPath -Encoding UTF8
} finally {
    if ($null -ne $presentation) { $presentation.Close() }
    $powerPoint.Quit()
}

Write-Output ('Metadata: ' + $metadataPath)
Write-Output ('Assets: ' + (Get-ChildItem -LiteralPath $assetRoot -File).Count)

