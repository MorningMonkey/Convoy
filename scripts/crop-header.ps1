param(
    [string]$InputPath = "assets/header.png",

    [string]$OutputPath,

    [ValidateSet("banner","16x9")]
    [string]$Mode = "banner",

    [int]$TargetWidth = 1600,
    [int]$TargetHeight = 420,

    [switch]$Force
)

Set-StrictMode -Version Latest

Import-Module (Join-Path $PSScriptRoot "_lib\config.ps1") -Force
$root = Get-ConvoyWorkspaceRoot

function Resolve-WorkspacePath([string]$p) {
  if ([string]::IsNullOrWhiteSpace($p)) { return $null }
  if ([System.IO.Path]::IsPathRooted($p)) { return $p }
  return (Join-Path $root $p)
}

$InputPath = Resolve-WorkspacePath $InputPath
if ([string]::IsNullOrWhiteSpace($OutputPath)) { $OutputPath = $InputPath }
$OutputPath = Resolve-WorkspacePath $OutputPath

Add-Type -AssemblyName System.Drawing

if (-not (Test-Path $InputPath)) {
  Write-Error "Input file not found: $InputPath"
  exit 1
}

if (($OutputPath -eq $InputPath) -and (-not $Force)) {
  Write-Error "OutputPath equals InputPath. Use -Force to overwrite safely."
  exit 1
}
if ((Test-Path $OutputPath) -and (-not $Force)) {
  Write-Error "Output file already exists: $OutputPath (use -Force to overwrite)"
  exit 1
}

$img = $null
$srcBmp = $null
$resizedBmp = $null
$destBmp = $null
$g = $null

try {
  $img = [System.Drawing.Image]::FromFile($InputPath)
  $srcBmp = New-Object System.Drawing.Bitmap($img)

  $w = $srcBmp.Width
  $h = $srcBmp.Height

  if ($Mode -eq "16x9") {
    $targetH = [int]([Math]::Round($w * 9.0 / 16.0))
    $targetW = $w

    $cropX = 0
    $cropY = 0

    if ($targetH -le $h) {
      $cropY = [int](($h - $targetH) / 2)
    }
    else {
      $targetH = $h
      $targetW = [int]([Math]::Round($h * 16.0 / 9.0))
      if ($targetW -gt $w) { $targetW = $w }
      $cropX = [int](($w - $targetW) / 2)
      $cropY = 0
    }

    $cropX = [Math]::Max(0, [Math]::Min($cropX, $w - $targetW))
    $cropY = [Math]::Max(0, [Math]::Min($cropY, $h - $targetH))

    $rect = New-Object System.Drawing.Rectangle($cropX, $cropY, $targetW, $targetH)
    $destBmp = New-Object System.Drawing.Bitmap($targetW, $targetH)

    $g = [System.Drawing.Graphics]::FromImage($destBmp)
    $g.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
    $g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::HighQuality
    $g.PixelOffsetMode = [System.Drawing.Drawing2D.PixelOffsetMode]::HighQuality
    $g.DrawImage($srcBmp, 0, 0, $rect, [System.Drawing.GraphicsUnit]::Pixel)

    $outW = $targetW
    $outH = $targetH
  }
  else {
    if ($TargetWidth -le 0 -or $TargetHeight -le 0) {
      throw "TargetWidth/TargetHeight must be positive integers."
    }

    $scaleW = $TargetWidth / [double]$w
    $scaleH = $TargetHeight / [double]$h
    $scale = [Math]::Max($scaleW, $scaleH)

    $scaledW = [int]([Math]::Ceiling($w * $scale))
    $scaledH = [int]([Math]::Ceiling($h * $scale))

    $resizedBmp = New-Object System.Drawing.Bitmap($scaledW, $scaledH)
    $g = [System.Drawing.Graphics]::FromImage($resizedBmp)
    $g.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
    $g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::HighQuality
    $g.PixelOffsetMode = [System.Drawing.Drawing2D.PixelOffsetMode]::HighQuality
    $g.DrawImage($srcBmp, 0, 0, $scaledW, $scaledH)
    $g.Dispose()
    $g = $null

    $cropX = [int]([Math]::Floor(($scaledW - $TargetWidth) / 2))
    $cropY = [int]([Math]::Floor(($scaledH - $TargetHeight) / 2))
    $cropX = [Math]::Max(0, [Math]::Min($cropX, $scaledW - $TargetWidth))
    $cropY = [Math]::Max(0, [Math]::Min($cropY, $scaledH - $TargetHeight))

    $srcRect = New-Object System.Drawing.Rectangle($cropX, $cropY, $TargetWidth, $TargetHeight)

    $destBmp = New-Object System.Drawing.Bitmap($TargetWidth, $TargetHeight)
    $g = [System.Drawing.Graphics]::FromImage($destBmp)
    $g.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
    $g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::HighQuality
    $g.PixelOffsetMode = [System.Drawing.Drawing2D.PixelOffsetMode]::HighQuality
    $g.DrawImage($resizedBmp, 0, 0, $srcRect, [System.Drawing.GraphicsUnit]::Pixel)

    $outW = $TargetWidth
    $outH = $TargetHeight
  }

  $outDir = Split-Path -Parent $OutputPath
  if (-not (Test-Path $outDir)) { New-Item -ItemType Directory -Path $outDir | Out-Null }

  $tempOutput = Join-Path $outDir ("." + [IO.Path]::GetFileNameWithoutExtension($OutputPath) + ".tmp" + [IO.Path]::GetExtension($OutputPath))
  $destBmp.Save($tempOutput, [System.Drawing.Imaging.ImageFormat]::Png)

  Move-Item -Path $tempOutput -Destination $OutputPath -Force
  if ($Mode -eq "banner") {
    Write-Host "Success: Cropped to banner SoT ($outW x $outH) -> $OutputPath"
  } else {
    Write-Host "Success: Cropped to 16:9 ($outW x $outH) -> $OutputPath"
  }
}
catch {
  Write-Error "Crop failed: $_"
  exit 1
}
finally {
  if ($g) { $g.Dispose() }
  if ($destBmp) { $destBmp.Dispose() }
  if ($resizedBmp) { $resizedBmp.Dispose() }
  if ($srcBmp) { $srcBmp.Dispose() }
  if ($img) { $img.Dispose() }
}
