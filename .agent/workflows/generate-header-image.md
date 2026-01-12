---
slug: "generate-header-image"
description: "READMEおよびリリース向けのヘッダー画像を生成し、1600x420の規格へクロップして成果物を固定する。"
trigger: "model_decision"
---
# 🖼️ generate-header-image

## 🌌 Overview
本ワークフローは、プロジェクトの視覚的アイデンティティを担うヘッダー画像を生成し、
README 表示のブレをなくすために最終成果物の寸法（SoT）を固定する。
生成からクロップ、必要に応じたテキスト重畳までを一度で成立させる。

## ⚖️ Rules / Constraints
- **SoT（最終寸法）**: README 用バナーは **1600×420 px** を唯一の規格とする（約 3.8:1）。
- **成果物の固定**: 生成画像の解像度は任意だが、最終出力は必ず SoT に揃える。
- **出力パスの固定**: 出力ファイルは以下に限定し、勝手な命名・配置をしない。  
  - `assets/header.png`（生成の生）  
  - `assets/header_cropped.png`（SoT へ固定）  
  - `assets/header_cropped_text.png`（テキスト重畳）
- **クロップ方法の固定**: クロップは **cover リサイズ → 中央クロップ**で実行し、
  1600×420 を厳密に満たすこと。
- **README 標準**: README が参照する既定は `assets/header_cropped_text.png` とする。
  固定 px のため、README 側のサイズ指定は原則不要。
- **プロンプトの追跡性**: 生成に用いた最終プロンプトは履歴として残す
  （`assets/branding/<productId>/brief.md` または `assets/` 配下）。

## 🚀 Workflow / SOP

### Step 1: 事前確認と入力収集（Decision）
1. プロジェクト名を取得する（README、カレントディレクトリ名等）。
2. スタイルを選択する（例: Standard / Mission Control）。
3. `header_prompt.txt` を土台に、必要最小限の差分で生成プロンプトを構築する。

**出力**
- 最終生成プロンプト（テキスト）
- 取得したプロジェクト名 / スタイル

### Step 2: 画像生成（Action）
1. AI で画像を生成する。
2. 生成結果を `assets/header.png` として保存する。

**出力**
- `assets/header.png`

### Step 3: クロップで SoT 固定（Action）
1. `pnpm header:crop` を実行し、banner モード（既定）で SoT に固定する。
2. 入力と出力は以下で固定する。  
   - 入力: `assets/header.png`  
   - 出力: `assets/header_cropped.png`（1600×420）

**出力**
- `assets/header_cropped.png`（1600×420）

### Step 4: テキスト重畳（条件付き / Action）
1. 画像にタイトル等のテキストが必要な場合のみ、`pnpm header:add-text` を実行する。
2. safe area を確保しつつ、横幅からはみ出さないよう自動フィットさせる。

**出力**
- `assets/header_cropped_text.png`（1600×420）

### Step 5: 履歴保存と README 反映（Action）
1. 最終プロンプトを履歴として保存する（推奨: `assets/branding/<productId>/brief.md`）。
2. README が `assets/header_cropped_text.png` を参照することを確認する。

**出力**
- 履歴（最終プロンプト）
- README の参照先確認

## ✅ Checklist
- [ ] 最終成果物が 1600×420 px（SoT）に固定されている
- [ ] `assets/header.png` / `assets/header_cropped.png` / `assets/header_cropped_text.png`
      が所定のパスに存在する
- [ ] 生成プロンプトが履歴として保存され、後から再現できる
- [ ] README が `assets/header_cropped_text.png` を参照している


