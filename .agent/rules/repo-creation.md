---
slug: repo-creation
description: Convoy（Mission Control）における新規リポジトリ作成・既存フォルダのリポジトリ化を、統一手順で強制する。
trigger: model_decision
---

# 🆕 リポジトリ作成ルール（Convoy）

本ルールは、ユーザーが以下を要求した場合に必ず適用する。

- 新しいリポジトリの作成（新規プロジェクトの開始）
- 既存フォルダを Git リポジトリとして初期化（リポジトリ化）
- 既存プロジェクトを「Convoy 管理下」に移行

---

## 1. 定義（Source of Truth）

### 1.1 Project Factory ディレクトリ
Convoy 配下で生成される **すべてのリポジトリは、Project Factory ディレクトリ直下に作成する**。

- 設定ファイル: `workspace.config.json`（ワークスペース直下）
- 参照キー: `paths.projectFactoryDir`
- 推奨既定値: `CONVOY_PROJECT`

**禁止**:
- `paths.projectFactoryDir` 以外の場所に新規リポジトリを作らない
- 絶対パス（例: `d:/...`）をルールに固定しない

### 1.2 ワークスペースルート
「ワークスペースルート」は、ユーザーが作業している現在の作業ディレクトリ（リポジトリ群を包含する基点）を指す。  
パス解決は常に以下を前提とする。

`<workspace-root>/<paths.projectFactoryDir>/<repo-name>/`

---

## 2. 要点（強制事項）

### 2.1 命名規則
- リポジトリ名は **kebab-case**（例: `convoy-mission-control`）
- 「内容を表さない仮名（例: `test`, `new`, `tmp`）」は禁止
- 既存フォルダをリポジトリ化する場合も、**コード/README/設定ファイル等を分析**し、適切な名称へ変更提案を行う（必要なら実施）

### 2.2 Git の独立性（Multi-repo 前提）
- Project Factory 配下の各プロジェクトは **独立した `.git` を持つ**
- 親（`<paths.projectFactoryDir>`）はワークスペース側で ignore 対象でも良いが、**子リポジトリは常に独立運用可能**であること

### 2.3 必須ファイル
新規作成・移行いずれの場合も、最低限以下を揃える。

- `.gitignore`（言語/実行環境に合わせて）
- `README.md`（プロダクト目的・実行方法・運用手順の最小限）
- `LICENSE`（ユーザーの指示がある場合。未指定なら提案のみ）

### 2.4 GitHub（Remote 作成と同期）
ユーザーが GitHub 管理を前提としている場合、以下を徹底する。

- `gh repo create` を用いてリモートを作成（または既存リモートに接続）
- `origin` 設定と初回 push を実施し、**ローカルとリモートを同期**
- 既存リポジトリ移行の場合は、`origin` が期待通りかを検証（誤接続は重大事故）

---

## 3. 標準手順（推奨フロー）

### 3.1 新規リポジトリ作成（Bootstrap）
1. `workspace.config.json` を確認し、`paths.projectFactoryDir` を確定する  
   - 不在の場合は **既定値 `CONVOY_PROJECT` を提案**し、以後その値を Source of Truth とする
2. リポジトリ名を決める（kebab-case、内容に即す）
3. `<projectFactoryDir>/<repo-name>/` を作成
4. `git init`、`.gitignore`、`README.md` を作成
5. 初回コミット
6. GitHub リモート作成（必要なら）
7. 初回 push

### 3.2 既存フォルダのリポジトリ化（Convoy 化）
1. 対象フォルダが `Project Factory` 配下にあるか確認  
   - 配下でない場合は、**移動（または複製）計画を提示**し、原則として配下に揃える
2. 既存に `.git` がある場合
   - 既存履歴を尊重しつつ、Convoy 規約（README/ignore 等）へ整流化
3. `.git` がない場合
   - 新規リポジトリとして `git init` → 初回コミット → リモート作成/接続

---

## 4. 自動化（Automate Everything）

ユーザーが「作成」ではなく「一気通貫の整備（初期化→品質→リリース）」を求めた場合、手動作業を分解して実行するのではなく、**該当 Workflows を最優先で起動**する。

- 推奨: `project-complete`（リポジトリ作成〜Convoy化〜初回リリースまで）
- 代替: 作業を `repo-bootstrap` / `quality-check` / `release` に分割して順に実行

> 重要: Convoy は「コードを書く場所」ではなく「タスクを委任し、指揮する場所」である。  
> よって、リポジトリ作成は単体作業ではなく、必ず **運用可能な状態（再現性・品質・自動化）**まで引き上げる。

---