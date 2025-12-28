Set-StrictMode -Version Latest

function Get-ConvoyWorkspaceRoot {
  # scripts/_lib/config.ps1 -> scripts/_lib -> scripts -> <root>
  return (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
}

function Get-ConvoyConfig {
  param(
    [switch]$AllowLocalOverride
  )

  $root = Get-ConvoyWorkspaceRoot
  $basePath  = Join-Path $root "workspace.config.json"
  $localPath = Join-Path $root "workspace.config.local.json"

  if (-not (Test-Path $basePath)) {
    throw "workspace.config.json not found at: $basePath"
  }

  $base = Get-Content $basePath -Raw | ConvertFrom-Json

  if ($AllowLocalOverride -and (Test-Path $localPath)) {
    # shallow merge: local のトップレベルだけ上書き
    $local = Get-Content $localPath -Raw | ConvertFrom-Json
    foreach ($p in $local.PSObject.Properties) {
      $base | Add-Member -NotePropertyName $p.Name -NotePropertyValue $p.Value -Force
    }
  }

  return $base
}