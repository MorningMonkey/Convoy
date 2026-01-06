---
slug: create-convoy-project-complete
description: "リポジトリ作成→実装→Identity注入→品質レビュー→（任意）可視化/リリースまでを、Convoy標準の一気通貫導線として実行する"
trigger: model_decision
---

# 🚀 Convoy Project Complete（統合導線 / Mission Control）

このワークフローは、Convoy（Mission Control）配下で **1つのプロジェクトを「運用可能な品質」まで最短で到達**させるための統合SOPです。  
個別ワークフロー（`create-repo-from-folder` / `build-app-simple` / `update-convoy-identity` …）を **決められた順序と条件**で呼び出します。

---

## Source of Truth（必読）

- 生成先ディレクトリは `workspace.config.json` の `paths.projectFactoryDir` を唯一の基準とします（推奨: `CONVOY_PROJECT`）
- ルール/手順の正本は `.agent/` 配下です（Rules / Templates / Workflows / INDEX）

---

## 呼び出し順（確定）

> **原則**: 「作る → 形にする → 整える → 点検する → 出荷する」

### 必須（必ず実行）
1. `/create-repo-from-folder`（リポジトリ化・origin/branch整備）
2. （必要なら）`/build-app-simple`（最小実装の成立）
3. `/update-convoy-identity`（README/ヘッダー/Alerts/導線）
4. `/review-repo-quality`（Pass / Risk / Action）

### 任意（条件付き）
- `/visualize-architecture`（構成が複雑、または共有が必要な場合）
- `/create-release`（バージョンを切る価値がある場合）
- `/git-auto-commit`（変更が大きく、粒度を分割したい場合）
- `/create-prompt-repo`（プロンプト資産を別repoで管理する方針の場合）

---

## 条件分岐（最終固定）

### A) 新規プロジェクトか、既存フォルダか
- **既存フォルダがある**: そのフォルダを対象に `/create-repo-from-folder`
- **既存フォルダがない**: `paths.projectFactoryDir` 配下にフォルダ作成 → `/create-repo-from-folder`

### B) 実装フェーズ（build-app-simple）の要否
- **UI/アプリを作る**（例: ピッキング効率化アプリのような画面がある）: 実行する（推奨）
- **空repoを先に作る（仕様策定/調査から）**: 実行しない（Identity→Qualityへ進む）

> 実装スタックは「Vanilla基本」。ただし画面状態が複雑な場合は **React + Tailwind（任意でTS）** を使用可。

### C) 可視化（visualize-architecture）の要否
- **複数モジュール / 複数サービス / 役割分担がある**: 実行（推奨）
- **単一ページ/単機能の小規模**: スキップ可

### D) リリース（create-release）の要否
- **外部/チームへ配布する節目**: 実行（推奨）
- **まだ破壊的変更が多い/内部試作**: スキップ可

> 初回リリースのバージョンは固定しません。  
> 既定値は `workspace.config.json` の `defaults.release`（channel / versionPrefix）に従い、状況に応じて `v0.1.0-alpha` 等を選択します。

### E) プロンプトrepo（create-prompt-repo）の要否
- **プロンプト/運用手順/評価ログを別repoで資産化する**: 実行（推奨）
- **単一repoで十分**: スキップ可

---

## 実行手順（SOP）

## Step 1: 📂 リポジトリの準備と初期化 // turbo（必須）

1. `paths.projectFactoryDir` 配下に対象フォルダを用意して移動
2. `/create-repo-from-folder` を実行
   - Private を既定
   - `main` を既定
   - 既存 `.git` がある場合は再初期化しない
   - 既存 `origin` がある場合は誤接続防止のためURLを確認

---

## Step 2: 🏗️ アプリケーションの実装（条件付き）

- **実装が必要な場合のみ** `/build-app-simple` を実行
  - 既定: Vanilla（HTML/CSS/JS）
  - 条件に応じて: React + Tailwind（任意でTS）
  - Identity適用より前に、最小動作（起動/主要画面）が成立していること

---

## Step 3: 🧭 Convoy Identityの適用 // turbo（必須）

- `/update-convoy-identity` を実行
  1. ヘッダー生成: 「リポジトリ名」を含む **Mission Control スタイル（neutral + 1–2 accents / flat / readable）**
  2. README更新: ヘッダー最上部、GitHub Alerts、導線（Docs/Workflows/Rules）を注入
  3. 生成物ポリシー: `assets/header_cropped_text.png` はコミット可／中間生成物は原則 `.gitignore`

---

## Step 4: ✅ 品質レビュー // turbo（必須）

- `/review-repo-quality` を実行し、**Pass / Risk / Action** で結果を出す
- Risk が残る場合は、先に改善してから次工程へ

---

## Step 5: 🗺️ アーキテクチャ可視化（任意）

- 構成共有が必要なら `/visualize-architecture`
  - 出力: `docs/architecture.drawio`（Draw.io XML）

---

## Step 6: 💾 コミット運用（任意だが推奨）

- 変更が大きい場合は `/git-auto-commit` を使用して粒度を整える
- **push は必須ではありません**。origin/権限/運用方針を確認してから実施する

---

## Step 7: 🚀 リリース作成（任意）

- `/create-release` を実行
  - テンプレ: `.agent/templates/release_notes_template.md`
  - 画像添付が難しい場合は後から `gh release upload` で追加可
  - Breaking/Migration がある場合は必ず明記

---

## 完了条件（Definition of Done）

- README に「何のrepoか / どう起動するか / どこがルールか」が揃っている
- `.agent/INDEX.md` から主要Workflowに辿れる
- 品質レビューが Pass もしくは Risk がAction化され、次に進める状態
- （必要なら）構成図が `docs/architecture.drawio` として保存されている
