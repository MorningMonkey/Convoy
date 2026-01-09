---
slug: "repo-creation"
description: "Convoy（Mission Control）における新規リポジトリ作成・既存フォルダのリポジトリ化を、統一手順で強制・自動実行する。"
trigger: "model_decision"
---

# 🏗️ Repository Creation Policy

## 🌌 Overview
Convoy におけるリポジトリ作成は、単なる `git init` ではありません。それは「反復作業の重力」から解放された、標準化された開発拠点のセットアップを意味します。

本ファイルは、すべてのプロジェクトが Convoy 規格（Mission Control 準拠）で開始され、エージェント主導開発（ADE）が円滑に進行することを保証するためのガイドラインです。

## ⚖️ Rules / Constraints
エージェントは、リポジトリの生成および移行において以下の制約を「憲法」として厳守しなければなりません。

- **所在地（SoT）**: すべてのリポジトリは `workspace.config.json` の `paths.projectFactoryDir`（既定: `CONVOY_PROJECT`）直下に配置すること。
- **命名規則**: リポジトリ名は必ず **kebab-case** とし、プロジェクトの内容を具体的かつ簡潔に示す名称であること（`test`, `tmp` 等の曖昧な名称は禁止）。
- **独立性**: 各プロジェクトは独立した `.git` ディレクトリを持ち、単体で動作・完結可能であること。
- **必須構成**: 最小構成資産として、適切な `.gitignore` および `README.md` を必ず初期段階で含めること。
- **リモート同期**: GitHub 利用時は `gh repo create` 等のツールを用い、ローカルとリモートの状態を完全に同期させること。

## 🚀 Workflow / SOP
ユーザーからの要求（新規作成または既存移行）に基づき、以下の手順を自律的に実行します。

### Step 1: 準備（Preparation）
`workspace.config.json` を読み込み、展開先となる Factory パスを確定します。既存フォルダを移行する場合は、その内容を分析して最適なリポジトリ名を commander（ユーザー）へ提案します。

### Step 2: 初期化（Initialization）
ターゲットディレクトリを作成し、`git init` を実行します。続いて、プロジェクトの言語やスタックに適した `.gitignore` を生成し、プロダクトの目的を明記した `README.md` を初期生成します。

### Step 3: Convoy 化（Branding & Sync）
初回コミットを行い、履歴の基点（Initial commit）を作成します。必要に応じて GitHub リモートリポジトリを作成し、`origin` を設定して push を実行します。

※ ユーザーが一気通貫の処理を求めている場合は、上位 Workflow（例: `create-convoy-project-complete`）へ処理を委譲します。

## ✅ Checklist
エージェントは最終出力の前に、以下の項目が満たされているか確認してください。

- [ ] 作成先ディレクトリは `workspace.config.json` の設定値に準拠しているか？
- [ ] 名称は kebab-case であり、プロジェクトの内容を正しく反映しているか？
- [ ] 独立した `.git` が存在し、親（Convoy 自体）の Git 履歴と混同されていないか？
- [ ] 設定された `origin` は、既存の他プロジェクトと重複していないか？