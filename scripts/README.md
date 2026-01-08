# Convoy Scripts

## Prerequisites
- Node.js (LTS)
- pnpm (Corepack 推奨)
- Optional: PowerShell 7+ (`pwsh`) — `header:add-text`（テキスト重畳）を使う場合のみ

> Note（互換性）  
> 画像の「リサイズ/クロップ（1600×420固定）」は Node（sharp）で行うため、非Windows環境（Antigravity等）でも動作します。  
> 旧 `scripts/crop-header.ps1`（System.Drawing 依存）は legacy 扱いです。

## Config
- `workspace.config.json` is the source of truth.
- Optional: `workspace.config.local.json` (ignored by git)

## Commands

### Build header images (recommended)
背景の生成と（可能なら）テキスト重畳までを行います。

```powershell
pnpm run header:build
```

Outputs:
- `assets/header_cropped.png`（標準出力・**1600×420固定**）
- `assets/header_cropped_text.png`（任意・テキスト重畳。`pwsh` がある場合のみ）

### Crop only (always works)
入力画像（任意サイズ）から、README用の標準サイズへ規格化します。

```powershell
pnpm run header:crop
```

### Add text only (optional)
`pwsh` がある環境でのみ使用してください。

```powershell
pnpm run header:add-text
```

## Header image workflow (Antigravity)

### SoT（README用バナー規格）
- 標準サイズ: **1600 × 420 px（約3.8:1）**
- 入力画像は任意サイズでOK（後段でリサイズ/クロップして規格化）
- 重要要素は中央寄せ（左右と上下端は切れても成立する構図を推奨）

### Steps
1) Update branding sources:
- `assets/branding/convoy/brief.md`
- `assets/branding/convoy/header_prompt.txt`

2) Generate image in Antigravity（テキストなし推奨）
- Export as PNG
- 推奨: 横 1600px 以上（可能なら 3200px 以上。後段のリサイズで品質が落ちにくい）

3) Replace input image:
- Save as `assets/header.png`

4) Build header outputs:
- `pnpm run header:build`

### Notes（テキスト重畳）
- `assets/header_cropped_text.png` は、`add-text-to-header.ps1` により safe area 内へ自動フィットします。  
- `pwsh` が無い環境では、背景（`assets/header_cropped.png`）のみが生成されます。
