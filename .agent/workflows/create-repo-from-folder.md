---
slug: "create-repo-from-folder"
description: "既存フォルダをConvoy規格のGitHubリポジトリへ整流化し、Private作成・origin検証・main標準化までを完了する。"
trigger: "model_decision"
---
# 📂 create-repo-from-folder

## 🌌 Overview
本ワークフローは、既存フォルダを Convoy（Mission Control）の統制下へ移行し、出荷前提の GitHub リポジトリとして整流化する。
対象は `workspace.config.json` の SoT に従い、命名・除外・履歴保護・リモート同期を一度で成立させる。

## ⚖️ Rules / Constraints
- **SoT（作成先）**: 生成・運用対象は `workspace.config.json` の `paths.projectFactoryDir` を唯一の基準とする（既定: `CONVOY_PROJECT`）。
- **範囲外禁止**: 対象フォルダが SoT 配下に無い場合は続行しない。警告し、移動または例外承認を求める。
- **履歴破壊禁止**: `.git` が存在する場合は `git init` を実行しない（再初期化禁止）。履歴は保持し、整流化のみ実施する。
- **既定は Private**: 明示指示が無い限り GitHub リポジトリは `--private` を既定とする。
- **origin の安全性**: 既存 `origin` がある場合は URL を検証する。不一致・不明時の付け替えは破壊的操作として扱い、必ず確認を取る。
- **除外設定は強制**: `.gitignore` に `*_SPEC.MD`、OS ゴミ（`.DS_Store` / `Thumbs.db`）を必ず含める。依存物・生成物・秘密情報（`.env` 等）もスタックに応じて追加する。
- **ブランチ標準**: 既定ブランチは `main` を原則とする。`master` からの移行は条件付きで行う。
- **削除は確認必須**: 旧ブランチ削除（GitHub 側含む）は破壊的操作のため、必ず明示確認を取る。

## 🚀 Workflow / SOP

### Step 1: 対象確認と命名（Decision）
1. 対象フォルダが SoT（`paths.projectFactoryDir`）配下かを判定する。
2. README / ソース / 設定ファイルを読み、プロジェクトの目的とスタックを把握する。
3. フォルダ名が不適切（例: `test`, `tmp`）または改善余地がある場合、`kebab-case` の候補名を提示し、改名の是非を確認する。

**出力**
- 採用するリポジトリ名（確定）
- SoT 適合の判定結果（OK/要移動/例外）

### Step 2: Git 状態の判定と .gitignore 整流化（Decision）
1. `.git` の有無を判定する。
   - 無い場合のみ `git init` を実行する。
   - ある場合は `git init` を実行せず、履歴を保持して整流化へ進む。
2. `.gitignore` を生成/更新し、Convoy 必須除外を入れる。
   - `*_SPEC.MD`
   - `.DS_Store`, `Thumbs.db`
   - 依存物/生成物（例: `node_modules/`, `dist/`, `build/`）
   - 秘密情報（例: `.env`, `*.pem`, `*.key`）

**出力**
- 更新された `.gitignore`
- `git status` が示す差分の要約（危険物混入が無いこと）

### Step 3: 初回コミットの作成（Action）
1. 既存履歴の有無を確認する。
2. コミットが無い場合は初回コミットを作成する。既存履歴がある場合は整流化コミットとして作成する。

**出力**
- コミットハッシュ
- コミットメッセージ（例: `Initial commit` / `chore: normalize repository`）

### Step 4: GitHub リポジトリ作成と origin 設定（Decision → Action）
1. 既存 `origin` がある場合、URL を検証する。
   - 一致: 継続
   - 不一致/不明: 付け替えは確認を取ってから実施
2. `gh repo create` を用いて Private リポジトリを作成し、`origin` を設定する（未設定の場合）。

**出力**
- 作成した GitHub リポジトリ情報（owner/repo）
- `origin` URL

### Step 5: ブランチ標準化と push（Decision → Action）
1. ブランチ状況を確認し、既定ブランチを `main` に整流化する。
   - `main` が存在: そのまま `main`
   - `main` が無く `master` が存在: `master → main` をリネーム
   - その他: 既定ブランチ方針を確認し、確定後に整流化
2. `git push -u origin main` を実行し、同期を完了する。
3. 旧 `master` の削除は標準フローに含めない。実施する場合は必ず確認を取る。

**出力**
- push 結果（成功/失敗と要因）
- 既定ブランチ名（`main`）

## ✅ Checklist
- [ ] 対象が `paths.projectFactoryDir` 配下であり、範囲外で続行していない
- [ ] `.git` 既存時に `git init` を実行していない（履歴を破壊していない）
- [ ] `.gitignore` に `*_SPEC.MD` と OS ゴミの除外が含まれている
- [ ] `origin` URL を検証し、`main` で `git push -u origin main` が完了している


