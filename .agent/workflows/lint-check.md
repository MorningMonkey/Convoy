---
slug: "lint-check"
description: "プロジェクトのLint（スタイル/静的解析）をSoT（brief.md）に従って実行し、PASS/PASS_WITH_WARNINGS/FAIL と根拠（主要エラー）を報告する原子ワークフロー。"
trigger: "manual"
---
# ✅ lint-check — Lintチェック

このワークフローは **読み取り＋検証のみ** を行います。  
修正（--fix）や設定変更は、別ワークフロー（またはユーザー承認）で行います。

---

## 定義（このワークフローの狙い）
- リポジトリの Lint を実行し、結果を **機械的に分類**して報告する
- 失敗時に「次に何を直すべきか」が分かるよう、主要エラーを要約する
- 実行コマンドは **SoT（brief.md）** を優先し、ない場合のみフォールバックする

---

## SoT（Source of Truth）
- スタック/品質ゲート: `assets/branding/<productId>/brief.md`
- 利用可能コマンド一覧: `.agent/INDEX.md`
- 関連（任意）: `.agent/rules/*.md`（code-style / type-safety / security 等）

---

## 入力（Inputs）
- 対象ブランチ/コミット（任意）
- 実行環境（任意）：Node/Flutter/Python 等  
  ※ 最終判断は brief.md を正本とする

---

## 成果物（Outputs）
- 判定: `PASS` / `PASS_WITH_WARNINGS` / `FAIL`
- 実行したコマンド（Evidence）
- 主要エラー（最大5件）
- 推奨次アクション（例: fix-lint / format / typecheck）

---

## 安全ガード（Convoy標準）
- `// turbo` 可（読み取り/検証のみ）
- **自動修正はしない**（`--fix` 実行は承認が必要）
- 依存追加・設定変更・push は行わない

---

# 手順

## Step 1: 前提確認（軽量） // turbo
- リポジトリ直下で実行されているか
- `package.json`（Node系の場合）または該当スタックの設定があるか

（例）
```bash
pwd
ls -la
```

---

## Step 2: 実行コマンドの決定（SoT優先） // turbo
優先順位：

1. `assets/branding/<productId>/brief.md` に記載の lint コマンド
2. `package.json` scripts の `lint`
3. フォールバック（検出順で試す）

---

## Step 3: Lint 実行 // turbo
### Node（pnpm/npm/yarn）フォールバック例
```bash
pnpm -s lint || npm run -s lint || yarn -s lint
```

### Flutter の例（プロジェクトがFlutterの場合）
```bash
flutter analyze
```

### Python の例（プロジェクトがPythonの場合）
> 実際のツールは brief.md を正本とする（ruff/flake8等）

```bash
python -m ruff check . || python -m flake8 .
```

> 注意: 複数の候補を試す場合も「実行した順序」を Evidence として残す。

---

## Step 4: 結果判定（分類ルール）
- **成功**: エラーなし → `PASS`
- **警告のみ**: 警告はあるがエラーなし → `PASS_WITH_WARNINGS`
- **失敗**: エラーあり → `FAIL`

> ツールごとに “warning/ error” の扱いが異なる場合は、出力から判断し、曖昧なら `FAIL` 寄りで扱う。

---

## Step 5: 失敗時の要約（最大5件） // turbo
`FAIL` の場合は以下を報告する：

- エラー数 / 警告数（分かる範囲で）
- 代表的なエラー（最大5件、ファイルパス・行番号・ルールID）
- 自動修正可能性（`--fix` / formatter）
- “次に取るべき手” を提示（例: `fix-lint` を作る、対象ファイルを直す、ルール調整案）

---

# 完了報告テンプレ

```markdown
## ✅ lint-check 結果

- 判定: PASS / PASS_WITH_WARNINGS / FAIL
- コマンド（Evidence）: <実行したコマンド>
- 対象: <ブランチ/コミット（任意）>

### サマリー
- エラー: <N>
- 警告: <N>

### 主要エラー（最大5件）
1. <file:line> <rule-id> <message>
2. ...
3. ...

### 自動修正（提案）
- --fix: 可能 / 不可 / 不明
- 次のアクション: <推奨手順>
```


