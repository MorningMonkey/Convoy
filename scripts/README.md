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
