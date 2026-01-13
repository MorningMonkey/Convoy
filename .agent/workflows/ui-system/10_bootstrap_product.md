---
slug: "bootstrap-product"
description: "新規プロダクトのディレクトリ構造と初期UI Specをセットアップする。"
trigger: "user_request"
---

# 🚀 Bootstrap New Product

`ui-system` に新しいプロダクトを受け入れるための最小構成を作成します。

## 📥 入力
*   **productId**: プロダクトID (kebab-case) 例: `convoy`, `aqua-ritual`

## 👣 手順

1.  **ディレクトリ作成**
    以下のディレクトリが存在しない場合は作成します。
    *   `ui-system/specs/<productId>/`
    *   `assets/branding/<productId>/`

2.  **初期Specの作成**
    テンプレート `ui-system/templates/spec.template.json` をコピーし、デフォルトSpecとして保存します。
    *   出力先: `ui-system/specs/<productId>/ui-header.json`

3.  **Specフィールドの更新**
    作成したJSONファイルの以下のフィールドを書き換えます。
    *   `productId`: 入力されたID
    *   `specId`: "ui-header"
    *   `figma`: 既知であればURLを設定、不明ならデフォルト維持

4.  **ブランディング資産の準備 (Optional)**
    `assets/branding/<productId>/README.md` を作成し、ロゴやカラー定義の置き場所であることを示します。

5.  **コミット (Optional)**
    作成したファイルをステージングし、初期化コミットを行うコマンドを提案します。
    `git commit -m "chore(<productId>): bootstrap ui-system spec and branding"`
