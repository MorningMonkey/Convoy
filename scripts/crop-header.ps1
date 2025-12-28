#Requires -Version 7.0
param(
  # 相対パス可（ワークスペースルート基準）
  [string]$InputPath = "assets/header.png",

  # 未指定なら入力と同じ（上書き扱い）
  [string]$OutputPath,

  # 上書き許可（OutputPathが既存 or InputPathと同一の場合に必要）
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

# 安全策：同一パス上書きは -Force 必須
if (($OutputPath -eq $InputPath) -and (-not $Force)) {
  Write-Error "OutputPath equals InputPath. Use -Force to overwrite safely."
  exit 1
}
# 既存ファイル上書きは -Force 必須
if ((Test-Path $OutputPath) -and (-not $Force)) {
  Write-Error "Output file already exists: $OutputPath (use -Force to overwrite)"
  exit 1
}

$img = $null
$srcBmp = $null
$destBmp = $null
$g = $null

try {
  # ファイルロック回避：Image -> Bitmap コピー
  $img = [System.Drawing.Image]::FromFile($InputPath)
  $srcBmp = New-Object System.Drawing.Bitmap($img)

  $w = $srcBmp.Width
  $h = $srcBmp.Height

  # 元仕様：幅を維持して16:9になる高さ
  $targetH = [int]([Math]::Round($w * 9.0 / 16.0))
  $targetW = $w

  $cropX = 0
  $cropY = 0

  if ($targetH -le $h) {
    # 余った上下を中央寄せでクロップ（元の意図）
    $cropX = 0
    $cropY = [int](($h - $targetH) / 2)
  }
  else {
    # フォールバック：高さを維持して16:9になる幅を中央クロップ
    $targetH = $h
    $targetW = [int]([Math]::Round($h * 16.0 / 9.0))
    if ($targetW -gt $w) { $targetW = $w }  # 念のため
    $cropX = [int](($w - $targetW) / 2)
    $cropY = 0
  }

  # クランプ
  $cropX = [Math]::Max(0, [Math]::Min($cropX, $w - $targetW))
  $cropY = [Math]::Max(0, [Math]::Min($cropY, $h - $targetH))

  $rect = New-Object System.Drawing.Rectangle($cropX, $cropY, $targetW, $targetH)

  $destBmp = New-Object System.Drawing.Bitmap($targetW, $targetH)
  $g = [System.Drawing.Graphics]::FromImage($destBmp)
  $g.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
  $g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::HighQuality
  $g.PixelOffsetMode = [System.Drawing.Drawing2D.PixelOffsetMode]::HighQuality

  $g.DrawImage($srcBmp, 0, 0, $rect, [System.Drawing.GraphicsUnit]::Pixel)

  # 一時ファイルへ保存してからMove（元仕様を踏襲）
  $outDir = Split-Path -Parent $OutputPath
  if (-not (Test-Path $outDir)) { New-Item -ItemType Directory -Path $outDir | Out-Null }

  $tempOutput = Join-Path $outDir ("." + [IO.Path]::GetFileNameWithoutExtension($OutputPath) + ".tmp" + [IO.Path]::GetExtension($OutputPath))
  $destBmp.Save($tempOutput, [System.Drawing.Imaging.ImageFormat]::Png)

  Move-Item -Path $tempOutput -Destination $OutputPath -Force
  Write-Host "Success: Cropped to 16:9 ($targetW x $targetH) -> $OutputPath"
}
catch {
  Write-Error "Crop failed: $_"
  exit 1
}
finally {
  if ($g) { $g.Dispose() }
  if ($destBmp) { $destBmp.Dispose() }
  if ($srcBmp) { $srcBmp.Dispose() }
  if ($img) { $img.Dispose() }
}
