---
slug: create-convoy-project-complete
description: "リポジトリ作成→（任意）最小実装→（条件付き）ブランディング確定→Identity注入→品質レビュー→（任意）可視化/リリースまでを、Convoy標準の一気通貫導線として実行する"
trigger: model_decision
---

# 🚀 Convoy Project Complete（統合導線 / Mission Control）

このワークフローは、Convoy（Mission Control）配下で **1つのプロジェクトを「運用可能な品質」まで最短で到達**させるための統合SOPです。  
個別ワークフロー（`create-repo-from-folder` / `build-app-simple` / `branding-intake` / `update-convoy-identity` …）を **決められた順序と条件**で呼び出します。

---

## Source of Truth（必読）

- 生成先ディレクトリは `workspace.config.json` の `paths.projectFactoryDir` を唯一の基準とします（推奨: `CONVOY_PROJECT`）
- ルール/手順の正本は `.agent/` 配下です（Rules / Templates / Workflows / INDEX）
- この統合導線は「迷わない最短」を優先し、例外は **条件分岐**で扱います（勝手に省略しない）

---

## 呼び出し順（最終固定）

> 原則: 「作る → 形にする →（必要なら）意図を確定する → 整える → 点検する → 出荷する」

### 必須（必ず実行）
1. `/create-repo-from-folder`（リポジトリ化・origin/branch整備）
2. `/update-convoy-identity`（README/ヘッダー/Alerts/導線）
3. `/review-repo-quality`（Pass / Risk / Action）

### 条件付き（条件を満たす場合は実行）
- `/build-app-simple`（UI/アプリの最小実装が必要な場合）
- `/branding-intake`（アプリ固有のブランディングを確定したい、または brief.md が無い場合）

### 任意（価値がある場合のみ実行）
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
- **UI/アプリを作る**（例: ピッキング効率化アプリのような画面がある）: 実行（推奨）
- **空repoを先に作る（仕様策定/調査から）**: スキップ可（Identity→Qualityへ進む）

> 実装スタックは「Vanilla基本」。ただし画面状態が複雑な場合は **React + Tailwind（任意でTS）** を使用可。

### C) ブランディング確定（branding-intake）の要否
- **アプリの世界観/トーンを製作者から回収して固定したい**: 実行（推奨）
- **`assets/branding/{productId}/brief.md` が存在しない**: 実行（実質必須）
- **共通トーンで十分**（試作/内部検証）: スキップ可（ただし後で必ず確定）

### D) 可視化（visualize-architecture）の要否
- **複数モジュール / 複数サービス / 役割分担がある**: 実行（推奨）
- **単一ページ/単機能の小規模**: スキップ可

### E) リリース（create-release）の要否
- **外部/チームへ配布する節目**: 実行（推奨）
- **まだ破壊的変更が多い/内部試作**: スキップ可

> 初回リリースのバージョンは固定しません。  
> 既定値は `workspace.config.json` の `defaults.release`（channel / versionPrefix）に従い、状況に応じて `v0.1.0-alpha` 等を選択します。

### F) プロンプトrepo（create-prompt-repo）の要否
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

## Step 2: 🏗️ アプリケーションの実装 // turbo（条件付き）

- UI/アプリを作る場合は `/build-app-simple` を実行
- 空repoを先に作る場合はスキップ可（次へ進む）

---

## Step 3: 🎛 Branding Intake（質問→Brief確定） // turbo（条件付き・推奨）

- 次の条件のいずれかを満たす場合は `/branding-intake` を実行し、`assets/branding/{productId}/brief.md` を確定します。
  - 新規プロジェクトでブランディングが未定
  - ヘッダー/READMEのトーンをアプリ固有に寄せたい
  - `assets/branding/{productId}/brief.md` が存在しない
- 成果物:
  - `assets/branding/{productId}/brief.md`
  - `assets/branding/{productId}/header_prompt.txt`

---

## Step 4: 🧭 Convoy Identityの適用 // turbo（必須）

- `/update-convoy-identity` を実行します。
  - ヘッダー生成（または既存ヘッダーの整備）
  - README更新（導線/Alerts/運用注記）
- 注意: `brief.md` が無い場合、`update-convoy-identity` は続行しません（ブランディング一貫性のため）

---

## Step 5: 🧪 品質レビュー // turbo（必須）

- `/review-repo-quality` を実行し、結果を **Pass / Risk / Action** で受け取ります。
- Risk があれば Action として具体化し、次の一手（修正/後回し）を明確にします。

---

## Step 6: 🗺️ 構成の可視化 // turbo（任意）

- `/visualize-architecture` を実行
  - 保存先: `docs/architecture.drawio`
  - README からリンク可能にする

---

## Step 7: 🏷️ リリース作成 // turbo（任意）

- `/create-release` を実行
  - テンプレ: `.agent/templates/release_notes_template.md`
  - 画像添付が難しい場合は後から `gh release upload` で追加可
  - Breaking/Migration がある場合は必ず明記

---

## 完了条件（Definition of Done）

- README に「何のrepoか / どう起動するか / どこがルールか」が揃っている
- `.agent/INDEX.md` から主要Workflowに辿れる（Convoy本体側の導線）
- 品質レビューが Pass もしくは Risk がAction化され、次に進める状態
- （必要なら）構成図が `docs/architecture.drawio` として保存されている
