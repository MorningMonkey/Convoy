---
slug: "create-release"
description: "Semantic Versioning に基づくリリース作成と、バージョン入りヘッダー画像の生成を自動化する。"
trigger: "model_decision"
---
# 🚀 create-release — Release Creation Policy & SOP

## 🌌 Overview
本ワークフローは、`main` ブランチの最新状態を基点として **公式な GitHub Release** を発行する手順です。

Semantic Versioning（SemVer）に基づくバージョン判定、変更履歴の自動解析によるリリースノート編纂、ならびに（可能であれば）プロジェクトの「顔」となる **バージョン入りヘッダー画像**の生成・添付までを一気通貫で実行します。画像生成が困難な場合でも、リリース発行そのものは優先し、後続でアセット追加できる導線を維持します。

---

## ⚖️ Rules / Constraints（憲法）

### 1) コマンド実行の整合性
- Git 操作において **コマンドをセミコロン（`;`）で連結することを禁止**します。
- 状態遷移（ブランチ・タグ・差分・作業ツリー）を正確に追跡するため、**1コマンドずつ実行**し、各ステップの終了条件（`git status` / 出力）を確認します。

### 2) バージョニングの規律（SemVer）
- SemVer を原則とし、前回リリース以降の差分から **推奨バージョン**を算出します。
- 判定ルール（最低限）:
  - **BREAKING CHANGE** を含む: major
  - `feat:` を含む: minor
  - `fix:` を含む: patch
- Alpha/Beta 段階のリポジトリでは、プレリリースタグ（例: `-alpha`, `-beta`）の付与を強く推奨します。
- Commander（ユーザー）による明示指定がある場合は、それを最優先します。

### 3) 画像内言語の制約
- リリース用ヘッダー画像に含まれるテキストは **English Only** とします。
- 日本語・漢字の混入を避け、国際的な互換性と視認性を担保します。

### 4) SoT の遵守（Release Notes）
- リリースノート生成の正本（SoT）は **必ず** `.agent/templates/release_notes_template.md` とします。
- テンプレートの構造は維持しつつ、変数（例: `{{VERSION}}`, `{{COMPARE_URL}}`）へ情報を埋め込みます。

### 5) SoT の遵守（Header Prompt）
- ヘッダープロンプトの SoT 優先順位は以下とします。
  1. `assets/branding/{productId}/header_prompt.txt`（存在するなら最優先）
  2. `assets/header_prompt.txt`（フォールバック）
- どちらも無い場合は、ブランド規格の最小要件（repo名 + version + English Only）に基づきプロンプトを構築します。

### 6) 監査ログ（walkthrough.md）
- 本ワークフローの実行結果は `walkthrough.md` に日本語で記録します（最低限）:
  - 確定バージョン
  - 比較範囲（前タグ、または初回リリース扱い）
  - リリースURL
  - 添付アセット（有無、ファイル名）
  - 主要コマンド要約（失敗時はエラー要約）

---

## ✅ Prerequisites（前提）
- `git` が利用可能であること
- GitHub CLI `gh` が利用可能で、認証済みであること（例: `gh auth status` が成功）
- ローカル作業ツリーがクリーンであること（未コミット差分が無い）
- `.agent/templates/release_notes_template.md` が存在すること

---

## 🚀 Workflow / SOP

### Step 1: 🌿 準備と環境の同期
1. `main` ブランチへ切り替えます。
2. ローカルを最新へ同期します（fast-forward のみ）。
3. タグを取得し、状態を確認します。
4. 未コミット差分がある場合は **リリース作業を中断**し、Commander に「コミット」または「スタッシュ」を促します。

**実行例（例示、環境に応じて調整）**
```bash
git checkout main
git pull --ff-only
git fetch --tags
git status
```

**前回タグ取得（タグが無い場合は初回リリースとして扱う）**
```bash
git describe --tags --abbrev=0
```
- 上記が失敗する場合は、**タグ無し（初回リリース）**として扱います。
  - 比較範囲: リポジトリ開始〜`HEAD`
  - 推奨: `v0.1.0-alpha` 等のプレリリースを提案

---

### Step 2: 🏷️ バージョンの確定
1. Commander がバージョンを明示指定している場合、その値を採用します。
2. 指定がない場合、前回タグ（または初回扱い）からの変更内容を解析し、推奨バージョンを算出します。
3. Alpha/Beta 段階のプロジェクトではプレリリースタグ（例: `v0.1.0-alpha`）を提案し、**承認を得て確定**します。

**比較範囲の決定**
- 前回タグがある場合: `[PREV_TAG]..HEAD`
- 初回リリースの場合: `HEAD` までの全履歴を対象（`git log` の範囲指定なし、または初回基準を明記）

---

### Step 3: 🎨 リリース用ヘッダー画像の生成（可能な場合）
1. Header Prompt の SoT 優先順位に従い、プロンプトを取得します。
2. リポジトリ名と確定バージョンを含む **DALL·E 用プロンプト**を構築します（画像内テキストは English Only）。
3. 生成後、README 規格にクロップ（1600x420）し、以下へ保存します。
   - `assets/release_header_[version].png`

> 画像生成が技術的に困難な場合は、画像添付を保留し、Step 5 のリリース作成を優先します。後から `gh release upload` で追加する導線を提示します。

---

### Step 4: 📝 リリースノートの編纂（テンプレ SoT 準拠）
1. 前回タグから `HEAD` までのコミットログを抽出し、機能追加・修正・破壊的変更に分類します。
2. テンプレートの変数へ埋め込み、概要、変更点一覧、貢献者リストを構成します。
3. Breaking Changes が含まれる場合は、必ず Migration Guide を設け、影響と移行手順を明文化します。

**差分/ログ抽出（タグがある場合の例）**
```bash
git diff --stat [PREV_TAG]..HEAD
git log --oneline --pretty=format:"%s (%h)" [PREV_TAG]..HEAD
git log --format='%an' [PREV_TAG]..HEAD | sort -u
```

**Compare URL（例）**
- `https://github.com/<ORG>/<REPO>/compare/[PREV_TAG]...[TAG]`

> 注: 初回リリース（タグ無し）の場合は Compare URL を「初回リリース」として明記し、範囲は `HEAD` までの全履歴として説明します。

---

### Step 5: 🚀 リリースの発行と公開（gh release create）
1. タグ名を確定します（例: `v1.2.3` / `v0.1.0-alpha`）。
2. `gh release create` を使用して、タグ、リリースノート、（あれば）ヘッダー画像を添付して発行します。
3. プレリリースの場合は `--prerelease` を付与します。
4. 発行後、リリース URL を確認します。

**実行例（画像添付あり）**
```bash
gh release create [TAG]   --title "[TAG]"   --notes-file release_notes.md   assets/release_header_[version].png
```

**実行例（プレリリース）**
```bash
gh release create [TAG]   --title "[TAG]"   --notes-file release_notes.md   --prerelease
```

**画像を後から追加する場合（例）**
```bash
gh release upload [TAG] assets/release_header_[version].png
```

---

### Step 6: 📢 完了報告（Commander へ日本語）
- 作成したリリースの URL、確定バージョン、添付アセット、Breaking Changes の有無を日本語で報告します。
- 併せて `walkthrough.md` を更新し、出荷工程の完了を記録します。

---

## ✅ Checklist（DoD）
- [ ] `main` が最新であり、作業ツリーがクリーンである（未コミット差分なし）
- [ ] 前回タグ取得に成功、またはタグ無し（初回）として分岐できている
- [ ] 推奨バージョン算出の根拠（feat/fix/BREAKING）を説明できる
- [ ] リリースノート Overview が 3 文以内で要点を伝えている
- [ ] Breaking Changes がある場合、Migration Guide が含まれている
- [ ] 生成ヘッダー画像のテキストが English Only で、バージョン番号が正しい
- [ ] GitHub Release が作成され、（可能なら）アセットが添付されている
- [ ] `walkthrough.md` に日本語で実行内容とリリース URL が記録されている


