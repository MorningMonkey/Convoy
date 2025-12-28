#Requires -Version 7.0

param(
  [string]$InputPath,
  [string]$OutputPath,
  [string]$TitleText,
  [string]$SubtitleText,

  [string]$TitleFontFamily = "Yu Mincho",
  [string]$SubtitleFontFamily = "Yu Gothic",

  [double]$TitleHeightRatio = 0.25,
  [string]$GoldHex = "#E6D285",
  [int]$ShadowAlpha = 180,

  [switch]$Force
)

Set-StrictMode -Version Latest

Import-Module (Join-Path $PSScriptRoot "_lib\config.ps1") -Force
$config = Get-ConvoyConfig
$root   = Get-ConvoyWorkspaceRoot
$assetsDir = Join-Path $root "assets"

# --- defaults ---
if ([string]::IsNullOrWhiteSpace($TitleText))    { $TitleText    = $config.product.name }
if ([string]::IsNullOrWhiteSpace($SubtitleText)) { $SubtitleText = $config.product.tagline }

if ([string]::IsNullOrWhiteSpace($InputPath))  { $InputPath  = Join-Path $assetsDir "header.png" }
if ([string]::IsNullOrWhiteSpace($OutputPath)) { $OutputPath = $InputPath }

# 相対パス対応（root基準）
function Resolve-WorkspacePath([string]$p) {
  if ([System.IO.Path]::IsPathRooted($p)) { return $p }
  return (Join-Path $root $p)
}
$InputPath  = Resolve-WorkspacePath $InputPath
$OutputPath = Resolve-WorkspacePath $OutputPath

if (-not (Test-Path $InputPath)) {
  Write-Error "Input file not found: $InputPath"
  exit 1
}

# OutputPath が既存で、かつ -Force が無い場合は止める
if ((Test-Path $OutputPath) -and (-not $Force) -and ($OutputPath -ne $InputPath)) {
  Write-Error "Output file already exists: $OutputPath (use -Force to overwrite)"
  exit 1
}

# フォント存在チェック（存在しないと例外になるのでtry）
function Pick-FontFamily([string]$preferred, [string[]]$fallbacks) {
  try {
    $ff = New-Object System.Drawing.FontFamily($preferred)
    return $preferred
  } catch {
    foreach ($f in $fallbacks) {
      try {
        $ff2 = New-Object System.Drawing.FontFamily($f)
        return $f
      } catch {}
    }
  }
  # 最後の砦
  return "Segoe UI"
}

# System.Drawing（Windows前提。PS7ではWindows推奨）
Add-Type -AssemblyName System.Drawing

# 参照を確実に解放するための変数（finallyでDispose）
$bmp = $null
$g = $null
$mainBrush = $null
$shadowBrush = $null
$titleFont = $null
$subtitleFont = $null

try {
  # Load image (avoid lock)
  $tempImg = [System.Drawing.Image]::FromFile($InputPath)
  $bmp = New-Object System.Drawing.Bitmap($tempImg)
  $tempImg.Dispose()

  $g = [System.Drawing.Graphics]::FromImage($bmp)
  $g.TextRenderingHint = [System.Drawing.Text.TextRenderingHint]::AntiAliasGridFit
  $g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::HighQuality

  # Fonts
  $pickedTitleFontFamily = Pick-FontFamily $TitleFontFamily @("Yu Mincho", "Georgia", "Times New Roman")
  $pickedSubtitleFontFamily = Pick-FontFamily $SubtitleFontFamily @("Yu Gothic", "Segoe UI", "Arial")

  # Title size auto-fit by height ratio
  $targetTitleHeight = [Math]::Max(1, ($bmp.Height * $TitleHeightRatio))
  $titleFontSize = 10
  do {
    $titleFontSize++
    $probe = New-Object System.Drawing.Font($pickedTitleFontFamily, $titleFontSize, [System.Drawing.FontStyle]::Bold)
    $size = $g.MeasureString($TitleText, $probe)
    $probe.Dispose()
  } while ($size.Height -lt $targetTitleHeight)

  $titleFont = New-Object System.Drawing.Font($pickedTitleFontFamily, $titleFontSize, [System.Drawing.FontStyle]::Bold)
  $titleSize = $g.MeasureString($TitleText, $titleFont)

  $subtitleFontSize = [int][Math]::Max(8, ($titleFontSize * 0.25))
  $subtitleFont = New-Object System.Drawing.Font($pickedSubtitleFontFamily, $subtitleFontSize)
  $subtitleSize = $g.MeasureString($SubtitleText, $subtitleFont)

  # Center positions
  $centerX = $bmp.Width / 2
  $centerY = $bmp.Height / 2

  $titleX = $centerX - ($titleSize.Width / 2)
  $titleY = $centerY - ($titleSize.Height / 2) - ($titleSize.Height * 0.1)

  $subtitleX = $centerX - ($subtitleSize.Width / 2)
  $subtitleY = $titleY + $titleSize.Height - ($titleSize.Height * 0.2)

  # Colors
  $goldColor = [System.Drawing.ColorTranslator]::FromHtml($GoldHex)
  $shadowColor = [System.Drawing.Color]::FromArgb($ShadowAlpha, 0, 0, 0)

  $mainBrush = New-Object System.Drawing.SolidBrush($goldColor)
  $shadowBrush = New-Object System.Drawing.SolidBrush($shadowColor)

  # Shadow offset
  $shadowOffset = [Math]::Max(1, ($titleFontSize / 15))

  # Draw shadow
  $g.DrawString($TitleText, $titleFont, $shadowBrush, $titleX + $shadowOffset, $titleY + $shadowOffset)
  $g.DrawString($SubtitleText, $subtitleFont, $shadowBrush, $subtitleX + ($shadowOffset / 2), $subtitleY + ($shadowOffset / 2))

  # Draw main
  $g.DrawString($TitleText, $titleFont, $mainBrush, $titleX, $titleY)
  $g.DrawString($SubtitleText, $subtitleFont, $mainBrush, $subtitleX, $subtitleY)

  # Save safely: if overwrite same file, write to temp then move
  $outDir = Split-Path -Parent $OutputPath
  if (-not (Test-Path $outDir)) { New-Item -ItemType Directory -Path $outDir | Out-Null }

  $tempOut = $OutputPath
  if ($OutputPath -eq $InputPath) {
    if (-not $Force) {
      Write-Error "OutputPath equals InputPath. Use -Force to overwrite safely."
      exit 1
    }
    $tempOut = Join-Path $outDir ("." + [IO.Path]::GetFileNameWithoutExtension($OutputPath) + ".tmp" + [IO.Path]::GetExtension($OutputPath))
  }

  $bmp.Save($tempOut, [System.Drawing.Imaging.ImageFormat]::Png)

  if ($tempOut -ne $OutputPath) {
    Move-Item -Force $tempOut $OutputPath
  }

  Write-Host "Success: Added text to $OutputPath"
}
catch {
  Write-Error "Error processing image: $_"
  exit 1
}
finally {
  if ($mainBrush) { $mainBrush.Dispose() }
  if ($shadowBrush) { $shadowBrush.Dispose() }
  if ($titleFont) { $titleFont.Dispose() }
  if ($subtitleFont) { $subtitleFont.Dispose() }
  if ($g) { $g.Dispose() }
  if ($bmp) { $bmp.Dispose() }
}
