# ui-system (Convoy UI 生成システム)

## 概要
`ui-system/` は、UI生成とレビューのための「信頼できる唯一の情報源 (Single Source of Truth)」を集約するディレクトリです。
以下の資産を管理し、AIエージェントによる一貫したUI実装を支援します。

*   **UI Specs**: 実装要件を定義したJSONファイル
*   **Schemas**: Specの構造を検証するJSON Schema
*   **Templates**: プロンプトやレビュー記録の雛形
*   **Prompts / Rubrics**: 品質ゲートと評価基準

## セットアップ
本ディレクトリの運用には、リポジトリルートに配置されたAntigravityエージェント (`.agent/`) が必要です。
生成されたプロンプトを使用するには **Figma MCP** またはそれに準ずるAIエージェント環境が必要です。

## 使用方法

### 1. Spec（仕様書）の作成・更新
`ui-system/specs/<productId>/` 配下に、JSON形式の仕様書を作成してください。
テンプレート `ui-system/templates/spec.template.json` を参考に記述します。

### 2. Figma MCP プロンプトの生成
作成したSpecを元に、AIへの指示書（プロンプト）を生成します。
以下のワークフローを実行してください（Antigravity経由）。

*   **ワークフロー**: `.agent/workflows/ui-system/20_generate_mcp_prompt.md`
*   **出力**: `ui-system/runs/<productId>/<specId>/<日付>/<時間>/mcp_prompt.md`

### 3. 実装と適用
生成された `mcp_prompt.md` の内容をコピーし、Figma MCP（またはClaude等のAIツール）に入力してUIを作成・修正します。

### 4. レビューと改善
実装されたUIを評価し、結果をフィードバックします。
*   **レビュー**: `ui-system/rubrics/` の基準を用いて評価します。
*   **改善**: 評価結果に基づき、Spec自体を修正してサイクルを回します。

## ディレクトリ構成
```
ui-system/
  ├── README.md         # 本ファイル
  ├── specs/            # プロダクト別UI仕様書 (JSON)
  ├── schemas/          # 仕様書のバリデーションスキーマ
  ├── templates/        # 各種テンプレート
  ├── prompts/          # エージェント用プロンプト資産
  ├── rubrics/          # 品質評価基準 (Smoke Test, Scorecard)
  └── runs/             # (gitignored) 生成アーティファクト出力先
```

## ライセンス
本プロジェクトのルートディレクトリにある `LICENSE` ファイルに準拠します。
