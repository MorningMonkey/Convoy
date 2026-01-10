param(
  [string]$ManifestPath = "projects/manifest.json"
)

$ErrorActionPreference = "Stop"

function Invoke-CheckedCommand([string]$cmd, [string]$cwd) {
  Write-Host ">> $cmd"
  $p = Start-Process -FilePath "pwsh" -ArgumentList @("-NoProfile","-Command",$cmd) -WorkingDirectory $cwd -NoNewWindow -PassThru -Wait
  if ($p.ExitCode -ne 0) { throw "Command failed ($($p.ExitCode)): $cmd" }
}

function New-DirectoryIfMissing([string]$Path) {
  if (-not (Test-Path -LiteralPath $Path)) {
    New-Item -ItemType Directory -Path $Path | Out-Null
  }
}

if (-not (Test-Path -LiteralPath $ManifestPath)) {
  throw "Manifest not found: $ManifestPath"
}

$manifest = Get-Content -Raw -LiteralPath $ManifestPath | ConvertFrom-Json
if (-not $manifest.rootDir) { throw "manifest.rootDir is missing" }
if (-not $manifest.projects) { throw "manifest.projects is missing" }

$rootDir = Join-Path (Get-Location) $manifest.rootDir
New-DirectoryIfMissing $rootDir

foreach ($proj in $manifest.projects) {
  $name = $proj.name
  $repo = $proj.repo
  $branch = $proj.branch
  $onDirty = if ($proj.onDirty) { $proj.onDirty } else { "abort" }

  if (-not $name -or -not $repo -or -not $branch) {
    throw "Invalid project entry. Required: name, repo, branch. Got: $(ConvertTo-Json $proj -Compress)"
  }

  $dest = Join-Path $rootDir $name

  if (-not (Test-Path -LiteralPath $dest)) {
    Write-Host "== Clone: $name =="
    Invoke-CheckedCommand "git clone -b $branch $repo `"$dest`"" (Get-Location).Path
    continue
  }

  if (-not (Test-Path -LiteralPath (Join-Path $dest ".git"))) {
    throw "Folder exists but is not a git repo: $dest"
  }

  Write-Host "== Update: $name =="

  # Remote sanity
  $origin = (git -C $dest remote get-url origin 2>$null)
  if (-not $origin) {
    Invoke-CheckedCommand "git remote add origin $repo" $dest
  } elseif ($origin.Trim() -ne $repo.Trim()) {
    Write-Host "!! origin differs for $name"
    Write-Host "   expected: $repo"
    Write-Host "   actual:   $origin"
    Write-Host "   Fix with: git -C `"$dest`" remote set-url origin $repo"
  }

  # Fetch first
  Invoke-CheckedCommand "git fetch origin --prune" $dest

  # Dirty working tree guard
  $dirty = (git -C $dest status --porcelain)
  if ($dirty) {
    switch ($onDirty) {
      "stash" {
        Write-Host "!! Dirty tree detected, stashing: $name"
        Invoke-CheckedCommand "git stash -u" $dest
      }
      "skip" {
        Write-Host "!! Dirty tree detected, skipping: $name"
        continue
      }
      default {
        throw "Dirty working tree detected: $dest`nSet projects[].onDirty to 'stash' or 'skip' to override."
      }
    }
  }

  # Ensure branch, then fast-forward pull only
  Invoke-CheckedCommand "git switch $branch" $dest
  Invoke-CheckedCommand "git pull --ff-only origin $branch" $dest

  if ($dirty -and $onDirty -eq "stash") {
    Write-Host "!! Restoring stash: $name"
    # stash pop can conflict; surface error if so
    Invoke-CheckedCommand "git stash pop" $dest
  }
}

Write-Host "Done."
