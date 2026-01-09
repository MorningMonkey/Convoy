---
slug: "antigravity-agent-control-spec"
description: "Convoy プロダクトを安全かつ一貫した品質で運用するための最上位管制仕様書。"
trigger: "model_decision"
---

# 🛰️ ANTIGRAVITY_AGENT_CONTROL_SPEC

## 🌌 Overview
本ドキュメントは、Google Antigravity エージェントが Convoy（Mission Control）を安全かつ一貫した品質で運用するための「管制仕様書」である。
Workspace 内の Rules / Workflows をどう解釈・実行すべきかを定義し、人間とエージェントの期待値を揃えることを目的とする。

- **対象**: Convoy プロダクト（本リポジトリ）配下で動作する Google Antigravity エージェント
- **目的**: エージェント主導開発（ADE）ワークスペースとして、リポジトリ生成からリリースまでの導線を標準化する
- **範囲**: `.agent/` 配下、`workspace.config.json`、`assets/`、`docs/` および `README.md`

## ⚖️ Rules / Constraints

### 1. Source of Truth (SoT)
エージェントは以下のファイルを正本として扱い、外部情報より優先させる。
- **運用ルールの正本**: `.agent/`（Rules / Workflows / Templates / INDEX）
- **Workspace 設定の正本**: `workspace.config.json`
- **アーキテクチャ図の正本**: `docs/architecture.drawio`（GitHub上では大小文字を厳密に区別する）

### 2. 管制オブジェクト定義
| 領域                 | 役割                                           | 代表ファイル                            |
| -------------------- | ---------------------------------------------- | --------------------------------------- |
| **Rules（憲法）**    | 生成物の制約・規約（命名、禁則等）             | `.agent/rules/*`                        |
| **Workflows（SOP）** | Slash コマンドの実行手順・成果物形式           | `.agent/workflows/*`                    |
| **Templates**        | リリースノート等の定型フォーマット             | `.agent/templates/*`                    |
| **Config（設定）**   | プロジェクト工場・デフォルト言語・ライセンス等 | `workspace.config.json`                 |
| **Branding（意匠）** | アプリ別のブランド正本と派生プロンプト         | `assets/branding/<productId>/brief.md`  |
| **Docs（外部共有）** | README / アーキテクチャ図                      | `README.md`, `docs/architecture.drawio` |

### 3. 安全・品質ガード（必須遵守）
- **Safety First**: 破壊的操作（削除・上書き・強制 push 等）はユーザー確認を必須とする。
- **Secrets 禁止**: APIキーや認証情報等の機密情報は一切コミットしない。
- **言語設定**: デフォルトは日本語。思考および最終応答も日本語を正とする。
- **権利配慮**: 特定作品・固有IP（例: Transformers 等）を想起させる表現を禁止する。

## 🚀 Workflow / SOP

### 1. インターフェース運用手順
- **Slash コマンド**: `.agent/workflows/*.md` の frontmatter `slug` をトリガーに実行し、`description` は原則クオートして扱う。
- **生成物配置**: `workspace.config.json` の `paths.projectFactoryDir`（例: `CONVOY_PROJECT`）を唯一の基準とする。
- **ブランディング適用**: アプリ別の `brief.md` を正とし、README/ヘッダーを整流化する際は `update-convoy-identity` を経由する。

### 2. 推奨実行フロー (Standard Sequence)
エージェントは、通常以下の順序でタスクを提案・実行する。
1. `/create-convoy-project-complete` でリポジトリを生成。
2. `/build-app-simple` 等でアプリ実装を適用。
3. `/branding-intake` でアプリ別ブランド（brief.md）を確定。
4. `/review-repo-quality` で品質チェックを実施。
5. `/create-release` でリリースを完了。

## ✅ Checklist
エージェントはタスク終了前に以下の項目を確認しなければならない。

- [ ] すべての成果物が `workspace.config.json` で定義された SoT に準拠しているか？
- [ ] README や docs 内のリンクに参照切れ（大小文字ミス含む）はないか？
- [ ] 変更点はコミットメッセージに明確に記述され、レビュー導線が確保されているか？
- [ ] 不確実な操作を行う前に、ユーザーへの確認手順を挟んだか？