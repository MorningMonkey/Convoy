---
slug: "create-repo-from-folder"
description: "既存のフォルダを Convoy 規格（CONVOY_PROJECT 配下）の GitHub リポジトリへ変換・整流化する。"
trigger: "model_decision"
---

# 📂 create-repo-from-folder — Repository Initialization Policy & SOP

## 🌌 Overview
本ワークフローは、既存の無秩序なフォルダを Convoy（Mission Control）の統制下へ移行し、**運用可能な品質の GitHub リポジトリ**として整流化するための手順です。

単なる `git init` に留まらず、以下を一気通貫で実施します。

- 作成先（SoT）と対象ディレクトリの適正化（`workspace.config.json` に準拠）
- コンテンツ解析に基づく命名提案（`kebab-case`）
- `.gitignore` の強制適用（Convoy 規格 + 言語スタック）
- GitHub Private リポジトリ作成 / `origin` の安全な設定
- 既定ブランチの標準化（原則 `main`）と push
- 実行結果の監査ログ（`walkthrough.md`）生成

---

## ⚖️ Rules / Constraints（憲法）

### 1) 所在地（SoT）
- 生成・管理対象の作成先は **必ず** `workspace.config.json` の `paths.projectFactoryDir` を唯一の基準とします（既定: `CONVOY_PROJECT`）。
- 対象フォルダが SoT 配下に無い場合、エージェントは作業を続行せず、**Commander（ユーザー）に警告し、移動または例外承認を求めます**。

### 2) Git 履歴の尊重（破壊禁止）
- 既に `.git` が存在する場合、**`git init` を実行しない**（再初期化の疑義を避けるため）。
- 既存履歴は保持したまま、整流化（`.gitignore` / `origin` / ブランチ名 / 既定ブランチ設定）のみ行います。

### 3) GitHub 秘匿性（既定は Private）
- 明示的な指示がない限り、GitHub リポジトリは **Private（`--private`）を既定**とします。

### 4) 除外設定の強制（.gitignore）
- 以下は **必ず** `.gitignore` で遮断します（例示、必要に応じて追加）。
  - Convoy 規格ファイル: `*_SPEC.MD`
  - OS ゴミ: `.DS_Store`, `Thumbs.db`
  - 生成物・依存物（例）: `node_modules/`, `dist/`, `build/`, `.dart_tool/`, `.gradle/`, `Pods/`, `DerivedData/`
  - 秘密情報: `.env`, `*.pem`, `*.key` 等（※秘密情報はコミット禁止）
- **親ディレクトリの資産を取り込まない**こと。対象は SoT 配下のフォルダに限定します。

### 5) 破壊的操作は必ず確認
- 以下は破壊的または復旧困難な操作のため、**実行前に必ず Commander の明示確認**を要求します。
  - 既存 `origin` の付け替え（URL が不一致・不明な場合）
  - 既存ブランチの削除（特に GitHub 側の `master` 削除）
  - 複数ブランチが存在する状況でのブランチ名の強制リネーム

### 6) 監査ログ（walkthrough.md）
- 本ワークフローの結果として、`walkthrough.md` を日本語で生成・更新し、少なくとも以下を記録します。
  - 対象ディレクトリ / 決定したリポジトリ名
  - 実行した主要コマンド（要約で可）
  - `origin` URL
  - 既定ブランチ名と push 結果
  - 重要な判断（例外承認、破壊的操作の有無）

---

## ✅ Prerequisites（前提）
- `git` が利用可能であること
- GitHub CLI `gh` が利用可能で、`gh auth status` が **ログイン済み**であること
- `workspace.config.json` が存在し、`paths.projectFactoryDir` が解決可能であること

---

## 🚀 Workflow / SOP

### Step 0: Preflight（SoT と対象の確定）
1. `workspace.config.json` を読み取り、`paths.projectFactoryDir` を解決します（既定: `CONVOY_PROJECT`）。
2. 対象フォルダが SoT 配下にあることを確認します。
3. SoT 配下に無い場合は、警告して **移動または例外承認**を求めます（承認がない限り停止）。

---

### Step 1: コンテンツ分析と命名提案
1. フォルダ内の README / `package.json` / `pubspec.yaml` / `pyproject.toml` / ソースコード等を読み、プロジェクトの目的と技術スタックを把握します。
2. 現在のフォルダ名が不適切（例: `test`, `tmp`, `new`, `untitled`）な場合、**`kebab-case`** で目的が伝わるリポジトリ名を提案します。
3. リネームが必要な場合は、Commander に提案し、承認後にフォルダ名を変更します（承認なしで勝手に確定しない）。

---

### Step 2: Git 整流化（.git 判定・.gitignore）
1. `.git` の有無を確認します。
   - **無し**: `git init`
   - **有り**: `git init` は実行せず、整流化へ進む（履歴は維持）
2. `.gitignore` を生成・更新します。
   - Convoy 必須（`*_SPEC.MD`, OS ゴミ, 秘密情報）を含める
   - 技術スタックに応じて追加（例: Node / Flutter / Python など）
3. `git status` で差分を確認し、不要ファイル（秘密情報・巨大生成物）が混入していないことを自己検閲します。

---

### Step 3: 基点の作成（Commit）
1. 既存リポジトリの場合はコミット履歴を確認します。
   - **コミット無し**: 初回コミットを作成（既定メッセージ: `Initial commit`）
   - **コミット有り**: 整流化コミットを作成（例: `chore: normalize repository`）
2. 実行例（プロジェクトに応じて調整）:
   - `git add .`
   - `git commit -m "Initial commit"` または `git commit -m "chore: normalize repository"`

---

### Step 4: GitHub 連携（origin 検証 → Private 作成）
1. 既存の `origin` がある場合:
   - `git remote -v` で URL を確認
   - 期待する GitHub 組織・リポジトリと一致しない場合、誤接続防止のため **Commander の明示確認**を取った上で付け替え
2. `origin` が無い場合:
   - `gh repo create <repo-name> --private --source=. --remote=origin`
   - （必要に応じて）`gh repo view` で作成確認

> 注: `gh repo create` の挙動は環境や権限に依存します。失敗時はエラーログを `walkthrough.md` に記録し、認証・権限・org 指定の再確認を行います。

---

### Step 5: ブランチ標準化と push（原則 main）
1. ブランチ状態を確認します（例: `git branch --show-current`, `git branch -a`）。
2. 既定ブランチの整流化:
   - `main` が存在する場合: `main` を既定として採用
   - `main` が無く `master` が存在する場合: **`master → main` にリネーム**  
     - 例: `git branch -m master main`
   - 複数ブランチがあり、現在ブランチが `master` でも `main` でもない場合:  
     - **勝手にリネームしない**（破壊的変更になり得るため）  
     - Commander に「どのブランチを既定にするか」を確認し、確定後に整流化
3. push:
   - `git push -u origin main`
4. GitHub 側の既定ブランチ設定:
   - 必要に応じて `main` をデフォルトに設定（権限がある場合）
5. 旧 `master` の削除:
   - 削除は破壊的操作のため、**必ず Commander の明示確認後**に実施（標準フローでは削除しない）。

---

### Step 6: walkthrough.md の生成（日本語）
リポジトリ直下に `walkthrough.md` を作成・更新し、実行結果を記録します（最低限のテンプレートは以下）。

- 対象ディレクトリ（SoT 配下であること）
- 採用したリポジトリ名（提案・承認の有無）
- `.git` の有無と実施内容（init 実行有無）
- `.gitignore` 生成・更新の要点
- `origin` URL
- 既定ブランチ（main）と push 結果
- 破壊的操作の有無（確認取得の有無）
- 実行日時

---

## ✅ Checklist（DoD）
- [ ] 対象は `workspace.config.json` の `paths.projectFactoryDir` 配下である
- [ ] 既存 `.git` がある場合に `git init` を実行していない
- [ ] `.gitignore` に `*_SPEC.MD` / OS ゴミ / 依存物 / 秘密情報が含まれている
- [ ] GitHub リポジトリが Private で作成されている（指示がない限り）
- [ ] `origin` URL が意図した接続先である（検証済み）
- [ ] 既定ブランチが `main` に整流化され、`git push -u origin main` が成功している
- [ ] `walkthrough.md` に日本語で結果（origin URL 含む）が記録されている
