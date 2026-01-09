---
slug: "convoy-scripts"
description: "Convoy（Mission Control）ワークスペースの運用スクリプトを単一の入口として整理し、ヘッダー生成とリリース導線を再現可能にする。"
trigger: "manual"
---

# Convoy Scripts

## 🌌 Overview
本READMEは、Convoy（Mission Control）ワークスペースに含まれる運用スクリプトの入口を固定し、
「ヘッダー画像生成」「リリース作成」を迷いなく実行できる状態を提供する。
実装の詳細（Node/CLIの内部）は隠蔽し、利用者は **pnpm scripts** のみを正として扱う。

## ⚖️ Rules / Constraints
- **SoT（設定）**: `workspace.config.json` を正本とする。ローカル上書きは `workspace.config.local.json`（Git管理しない）。
- **正規導線の固定**: 入口は `header:build` / `create-release` などの **pnpm scripts** に固定する（直叩き・独自手順を増やさない）。
- **ヘッダー規格（SoT）**: README用バナー最終成果物は **1600×420 px** とする。
- **出力パスの固定**:
  - 入力: `assets/header.png`
  - 中間: `assets/header_cropped.png`
  - 最終: `assets/header_cropped_text.png`（README が参照する既定）
- **レガシー禁止**: `legacy:*` の scripts / 手順は運用で使用しない（入口を増やさない）。
- **プレースホルダー禁止**: `package.json` の scripts に `...` 等の省略記号を残さない（そのままでは実行不能となるため）。
- **Git運用**: `.gitignore` により中間生成物は除外し、最終成果物（`assets/header_cropped_text.png`）はコミットする。

## 🚀 Workflow / SOP

### Step 1: Prerequisites（環境）
- Node.js（LTS 推奨）
- pnpm（Corepack 推奨）

> 補足  
> 本READMEでは OS 依存の実装（PowerShell 等）を前提にしない。実行は `pnpm` のみを正とする。

---

### Step 2: Config（SoT）
1. `workspace.config.json` を確認する（ヘッダー入出力パス、生成先ディレクトリ等）。
2. ローカル差分が必要な場合のみ `workspace.config.local.json` を作成する（Git管理しない）。

**出力**
- SoT がどこか（`workspace.config.json`）を明確化

---

### Step 3: Header build（正規導線）
ヘッダー画像の生成・規格化・（必要なら）テキスト重畳までを一括で行う。

```bash
pnpm header:build
```

**Outputs**
- `assets/header_cropped.png`（1600×420固定）
- `assets/header_cropped_text.png`（最終・README既定）

---

### Step 4: Crop only（切り出しのみ）
入力画像（任意サイズ）を、README用の標準サイズへ規格化する。

```bash
pnpm header:crop
```

---

### Step 5: Add text only（テキストのみ）
テキスト重畳のみを実行する（前提: `assets/header_cropped.png` が存在）。

```bash
pnpm header:add-text
```

---

### Step 6: Verify / Clean（運用コスト削減）
事前チェックと後片付け（生成物の掃除）を提供する。

```bash
pnpm header:verify
pnpm header:clean
```

---

### Step 7: Header image workflow（Antigravity連携の標準手順）
1. Branding ソースを更新  
   - `assets/branding/<productId>/brief.md`  
   - `assets/branding/<productId>/header_prompt.txt`
2. Antigravity で背景画像を生成（推奨: **テキストなし**）
   - PNG で書き出し
   - 推奨: 横 1600px 以上（可能なら 3200px 以上）
3. 入力画像を差し替え  
   - `assets/header.png` として保存
4. 正規導線で生成  
   - `pnpm header:build`

**出力**
- README 表示に耐える最終ヘッダー（`assets/header_cropped_text.png`）

## ✅ Checklist
- [ ] `workspace.config.json` が SoT として参照され、ローカル差分は `workspace.config.local.json` に隔離されている
- [ ] 入口は `pnpm header:build` を正として運用し、`legacy:*` を使用していない
- [ ] `assets/header_cropped_text.png` が 1600×420 で生成され、Git管理対象としてコミットされる
- [ ] `package.json` の scripts に `...` 等の省略表記が残っておらず、実行可能になっている
