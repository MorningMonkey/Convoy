# Convoy Scripts

## Prerequisites
- PowerShell 7+ (`pwsh`)

## Config
- `workspace.config.json` is the source of truth.
- Optional: `workspace.config.local.json` (ignored by git)

## Commands
### Add text to header image
```powershell
pwsh ./scripts/add-text-to-header.ps1
---

## Step 5：package.json の scripts に“入口”を作る（任意だが便利）
pnpm を使っているので、PowerShell起動を固定できます。

**package.json**
```json
"scripts": {
  "header:add-text": "pwsh ./scripts/add-text-to-header.ps1 -Force"
}

## Header image workflow (Antigravity)

1) Update branding sources:
- assets/branding/convoy/brief.md
- assets/branding/convoy/header_prompt.txt

2) Generate image in Antigravity (no text overlay recommended)
- Export as PNG (16:9 recommended, e.g., 1920x1080)

3) Replace input image:
- Save as assets/header.png

4) Build header outputs:
- pnpm header:build

Outputs:
- assets/header_cropped.png
- assets/header_cropped_text.png
