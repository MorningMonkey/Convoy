---
slug: "git-auto-commit"
description: "git statusとdiffを根拠に、Convoy標準の作業ブランチ作成・粒度の細かいコミット・マージまでを安全に自動化する。"
trigger: "model_decision"
---

# 🤖 git-auto-commit

## 🌌 Overview
本ワークフローは、リポジトリの変更内容を解析し、Convoy（Mission Control）の運用品質を崩さない形で
「作業ブランチ作成 → 変更の分割コミット → 統合ブランチへマージ → 後始末」までを一気通貫で行う。
判断の根拠は `git status` と `git diff` を SoT（Source of Truth）として固定し、意図しない混入や粗いコミットを防ぐ。

## ⚖️ Rules / Constraints
- **SoT（差分の根拠）**: 判断の根拠は `git status` と `git diff`（必要に応じて `--stat`）とする。推測で分割しない。
- **コマンド連結禁止**: Git 操作はセミコロン（`;`）で連結しない。必ず 1 コマンドずつ実行し、結果を確認して次へ進む。
- **統合ブランチ方針**: 既定は `develop` 統合。トランク運用で `develop` を使わない場合は、以後の `develop` を `main` に読み替える。
- **作業ブランチ命名**: `feature/<topic>-<YYYYMMDD>` を採用する。Issue 番号は含めない。
- **一時ファイルの混入禁止**: `COMMIT_MSG.txt` はコミット対象に含めない。必要なら削除または `.gitignore` に追加する。
- **コミット粒度**: `git diff` を分析し、作業単位ごとに分割してコミットする（「全部まとめて 1 コミット」を禁止）。
- **コミットメッセージ規律**:
  - Type は `feat|fix|docs|style|refactor|perf|test|chore` から選ぶ。
  - メッセージは **必ず日本語**、先頭に **絵文字**、本文は **3行程度の箇条書き**で具体を書く。
  - メッセージは `COMMIT_MSG.txt` に作成し、`git commit -F COMMIT_MSG.txt` で適用する。
- **マージ規律**: 統合ブランチへのマージは `--no-ff` を原則とし、マージメッセージも `COMMIT_MSG.txt` を使用する。

## 🚀 Workflow / SOP

### Step 1: 状態確認（Decision）
1. 作業ツリーの状態を確認する。
2. 差分の規模を把握し、分割コミットの粒度を設計する。

**実行**
```bash
git status
git --no-pager diff --stat
```

**出力**
- 変更対象ファイル一覧（追加/変更/削除）
- 変更の塊（例: ドキュメント更新、設定変更、実装修正など）の分割方針

---

### Step 2: 統合ブランチの準備（Decision → Action）
1. `develop` の有無を確認する（トランク運用なら `main` を統合ブランチとして扱う）。
2. 無ければ作成して push、有れば checkout して最新化する。

**実行（例）**
```bash
git branch --list develop
git checkout develop
git pull origin develop
```

**出力**
- 採用した統合ブランチ名（`develop` または `main`）
- 最新化が完了したこと（fast-forward / 競合有無）

---

### Step 3: 作業ブランチの作成（Decision → Action）
1. 差分内容から、英語のトピック語を抽出してブランチ名を提案する。
2. `feature/<topic>-<YYYYMMDD>` で作成し、チェックアウトする（Issue 番号は入れない）。

**実行（例）**
```bash
git checkout -b feature/<topic>-<YYYYMMDD>
```

**出力**
- 作業ブランチ名（確定）

---

### Step 4: 粒度の細かいコミット（Decision → Action）
1. `git diff` を見て、作業単位ごとにコミット対象ファイルを分割する。
2. 各コミットごとに `COMMIT_MSG.txt` を作成し、`-F` でコミットする。
3. `COMMIT_MSG.txt` が追跡対象に入らないように自己検閲する（必要なら `.gitignore` へ追加）。

**実行（最小手順）**
```bash
git --no-pager diff
git add <fileA> <fileB>
git commit -F COMMIT_MSG.txt
```

**COMMIT_MSG.txt（例）**
```text
📝 docs: インストール手順を更新

- 推奨ランタイムの記載を最新化
- 設定例と注意点を追記
- 手順の順序を整理
```

**出力**
- コミット一覧（ハッシュ/要約）
- 分割の根拠（どの変更をどのコミットに入れたか）

---

### Step 5: コミット完了確認（Decision）
1. 変更が残っていないか確認する。
2. 残っている場合は Step 4 に戻り、追加分割または追従コミットを作成する。

**実行**
```bash
git status
```

**出力**
- 作業ツリーがクリーンであること（または残差分の内訳）

---

### Step 6: 統合ブランチへマージ（Decision → Action）
1. 統合ブランチへ切り替える。
2. マージメッセージを `COMMIT_MSG.txt` に作成する。
3. `--no-ff` と `-F` を用いてマージする。
4. リモートへ push する。

**実行（例）**
```bash
git checkout develop
git merge --no-ff feature/<topic>-<YYYYMMDD> -F COMMIT_MSG.txt
git push origin develop
```

**出力**
- マージ結果（成功/競合の有無）
- push 成功（リモート反映済み）

---

### Step 7: 作業ブランチの後始末（Action）
1. マージ済みの作業ブランチをローカルから削除する。

**実行**
```bash
git branch -d feature/<topic>-<YYYYMMDD>
```

**出力**
- ブランチ削除完了

## ✅ Checklist
- [ ] `git status` / `git diff` を根拠に、変更を作業単位で分割してコミットできている
- [ ] `COMMIT_MSG.txt` がコミット対象に含まれておらず、必要に応じて削除または `.gitignore` 済み
- [ ] コミットメッセージが「絵文字 + 日本語 + 3行程度の箇条書き + 正しいType」を満たしている
- [ ] 統合ブランチへ `--no-ff` でマージし、push まで完了している


