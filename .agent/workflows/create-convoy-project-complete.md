---
slug: "create-convoy-project-complete"
description: "リポジトリ作成から品質レビュー、リリースまでを Convoy 標準の一気通貫導線で実行する統合 SOP。"
trigger: "model_decision"
---

# 🚀 Convoy Project Complete (統合導線 / Mission Control)

## 🌌 Overview
本ワークフローは、Convoy（Mission Control）配下において、単一のプロジェクトを「運用可能な品質」まで最短で到達させるための最上位統合 SOP です。

個別ワークフローを最適な順序と条件で連結し、エージェント主導開発（ADE）における「迷わない最短経路」を提供します。本手順の完遂により、リポジトリは Convoy の厳格な品質基準と意匠規格を満たした状態で出荷可能となります。

## ⚖️ Rules / Constraints

### 1. 安全性および整合性（Safety & Integrity）
エージェントは破壊的操作を避けるため、以下のルールを厳守しなければなりません。
- **Git 初期化の禁止**: 既存の `.git` が存在する場合、再初期化（git init）を行わず現状を維持すること。
- **Origin の検証**: 既存の `origin` がある場合は、誤接続防止のため必ず URL を確認すること。
- **ユーザー承認**: 上書き、強制 push、履歴改変などの非可逆的な操作が必要な場合は、必ず Commander（ユーザー）の承認を得ること。
- **所在地（SoT）**: 生成先は `workspace.config.json` の `paths.projectFactoryDir` を唯一の基準とする。

### 2. 意思決定マトリクス (Decision Matrix)
エージェントは各ステップの開始前に、以下の基準で実行の要否を判断します。

| コマンド                       | 実行条件 (Run IF...) | 判定基準                                               |
| :----------------------------- | :------------------- | :----------------------------------------------------- |
| **`/create-repo-from-folder`** | **必須**             | 全プロジェクトの基盤構築。既存フォルダ有無で分岐。     |
| **`/build-app-simple`**        | 条件付き             | UI/アプリ画面の実装が必要な場合（Vanilla/React選択）。 |
| **`/branding-intake`**         | **実質必須**         | `brief.md` が未作成、または個別の意匠が必要な場合。    |
| **`/update-convoy-identity`**  | **必須**             | README/ヘッダーの整流化。`brief.md` が必須。           |
| **`/review-repo-quality`**     | **必須**             | 出荷前の最終品質ゲート（Pass/Risk/Action判定）。       |
| **任意コマンド群**             | 任意                 | 必要に応じて可視化、リリース、プロンプト管理を実行。   |

## 🚀 Workflow / SOP
マトリクスの判定に基づき、以下のフェーズを自律的に進行します。

### Step 1: 📂 リポジトリの初期化（必須）
`paths.projectFactoryDir` 配下にフォルダを準備し、`/create-repo-from-folder` を実行します。
- **既存フォルダあり**: 内容を維持し、`.git` の再初期化は行わない。`origin` URL の整合性を確認する。
- **既存フォルダなし**: 新規作成後に初期化。Private リポジトリおよび `main` ブランチを既定とする。

### Step 2: 🏗️ アプリケーションの実装（条件付き）
UI 要素が必要な場合のみ、`/build-app-simple` を実行します。
- 実装を伴わない調査用 repo 等の場合はスキップ可能です。

### Step 3: 🎛 ブランディングの確定（推奨・実質必須）
`assets/branding/<productId>/brief.md` が存在しない場合は `/branding-intake` を実行します。
- **成果物**: `brief.md` および `header_prompt.txt` の生成。

### Step 4: 🧭 Convoy Identity の注入（必須）
`/update-convoy-identity` を実行し、ブランド正本に基づいた README 更新とヘッダー画像整備を行います。
- `brief.md` が存在しない状態での続行は不可となります。

### Step 5: 🧪 品質レビューと検証（必須）
`/review-repo-quality` を実行し、結果を **Pass / Risk / Action** で取得します。
- Risk 検出時は、Commander へ具体的な Action プランを提示します。

### Step 6: 🗺️ 仕上げと出荷（任意）
必要に応じ、構成図生成（`/visualize-architecture`）やリリース発行（`/create-release`）を提案・実行します。

## ✅ Checklist
- [ ] 既存の `.git` 履歴を破壊せず、`origin` URL は正しく検証されたか？
- [ ] 破壊的操作を行う前に、ユーザーへの明示的な確認を行ったか？
- [ ] すべての成果物は `CONVOY_PROJECT` 配下に配置されているか？
- [ ] `review-repo-quality` を通過、または Risk が Action 化されているか？