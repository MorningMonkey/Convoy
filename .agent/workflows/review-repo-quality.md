---
slug: review-repo-quality
description: "リポジトリの品質（README, 構造, 設定）をチェックし、Convoy標準（Agent First / Automate Everything）に沿って改善点を提案します"
trigger: model_decision
---

# ✅ リポジトリ品質レビュー

このワークフローは、現在のリポジトリが品質基準を満たしているか確認します。

## Step 1: 📝 docs check // turbo
- **README.mdの存在確認**: ルートディレクトリに `README.md` があるか確認します。
- **READMEの品質チェック**: 以下の要素が含まれているか確認します。
  - **ヘッダー画像**: 最上部に配置されていること（タイトルより上）。
  - 中央揃えのタイトル
  - ステータスバッジ
  - **Convoy標準の導線**: `.agent/`（rules/templates/workflows）が存在し、README から運用手順へ辿れること
  - 概要、インストール手順、使用方法
  - 目次（長い場合）
- **ドキュメントの一貫性**: `examples/` などのサブフォルダがある場合、そこにもREADMEがあるか確認します。

## Step 2: ⚙️ config check
- **.gitignore**: 存在するか、および `.env` などの機密ファイルが除外されているか確認します。
- **機密情報**: コード内にAPIキーなどがハードコードされていないか簡易チェックします。
- **一時ファイル**: `COMMIT_MSG.txt` や生成物がコミットされていないか確認します。

## Step 3: 📂 structure check
- **配置場所（Convoy）**: リポジトリが `workspace.config.json` の `paths.projectFactoryDir` 配下にあり、multi-repo（各プロジェクトが独立 `.git`）前提に反していないか確認します。
- **フォルダ構造**: 構造が論理的か（`src/`, `tests/`, `docs/` などに分かれているか）確認します。
- **命名規則**: ファイルやフォルダが `kebab-case` （または言語の規則）に従っているか確認します。

## Step 4: 📊 report
- 出力は **Pass / Risk / Action** の3区分で整理し、最短で改善できる順に並べます。
- チェック結果をまとめ、改善点（TODOリスト）をユーザーに提示します。
- 修正が必要な場合は、具体的な修正案やコマンドを提案します。
