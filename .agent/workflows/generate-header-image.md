---
slug: generate-header-image
description: "READMEやリリースノート用の高品質なヘッダー画像を生成します"
trigger: model_decision
---

# ヘッダー画像生成ワークフロー

このワークフローは、プロジェクト名を冠した高品質なヘッダー画像をAIで生成し、**スクリプトで最終成果物の寸法（SoT）を固定**して、README表示のブレをなくします。

---

## SoT（最終成果物の規格）
- README用バナー（標準）: **1600×420 px（約 3.8:1）**
- 生成画像（生）は任意の解像度でよいが、**最終出力は必ず固定px**に揃える

出力ファイル:
- `assets/header.png`（AI生成の“生”）
- `assets/header_cropped.png`（SoTバナーに固定）
- `assets/header_cropped_text.png`（テキスト重畳済み）

---

## Step 1: プロンプト構築
- プロジェクト名を取得（README、カレントディレクトリ等）
- スタイル選択（Standard / Mission Control など）
- `header_prompt.txt` を土台に、必要最小限の差分で生成プロンプトを作成

---

## Step 2: 生成
- AIで画像を生成し `assets/header.png` に保存

---

## Step 3: クロップ処理（寸法固定）
`pnpm header:crop` を実行し、**bannerモード（既定）**で SoT に固定します。

- 入力: `assets/header.png`
- 出力: `assets/header_cropped.png`（1600×420）

仕組み:
- `scripts/crop-header.ps1` が **coverリサイズ → 中央クロップ**で厳密に 1600×420 に揃えます。
- 互換用途として `-Mode 16x9` も利用可能（ただしREADME標準は banner）。

---

## Step 4: テキスト重畳（自動フィット）
必要に応じて `pnpm header:add-text` を実行し、テキストを重畳します。

- 出力: `assets/header_cropped_text.png`（1600×420）

仕組み:
- `scripts/add-text-to-header.ps1` は **safe area** を確保しつつ、テキストが横幅からはみ出さないように**自動縮小（fit）**します。

---

## Step 5: 完了・保存
- 生成に使用した最終プロンプトを `assets/branding/<productId>/brief.md` もしくは `assets/` 配下に履歴として残す（運用に合わせて）
- READMEは `assets/header_cropped_text.png` を参照（固定pxのため、サイズ指定は原則不要）
