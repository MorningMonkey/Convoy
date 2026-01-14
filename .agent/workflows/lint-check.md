---
slug: "lint-check"
description: "プロジェクトのLint（スタイル/静的解析）をSoT（quality-gates.yml）に従って実行し、PASS/FAIL/SKIP を根拠つきで報告する原子ワークフロー。"
trigger: "manual"
---
# ✅ lint-check — Lintチェック

このワークフローは **読み取り＋検証のみ** を行います。
修正（--fix）や設定変更は、別ワークフロー（またはユーザー承認）で行います。

---

## 定義（このワークフローの狙い）
- リポジトリの Lint を実行し、結果を **PASS / FAIL / SKIP** で報告する
- 実行コマンドは **quality-gates スキル** を通じて決定する
- **Source of Truth**: `assets/branding/<Product>/quality-gates.yml`（優先）

---

## 安全ガード（Convoy標準）
- `// turbo` 可（読み取り/検証のみ）
- **自動修正はしない**（`--fix` 実行は承認が必要）

---

# 手順

## Step 1: Lint実行 (Quality Gate) // turbo

`quality-gates` スキルを使用してチェックを実行します。

```bash
python .agent/skills/quality-gates/scripts/gate_check.py --type lint
```

## Step 2: 結果確認

- **PASS (Exit 0)**: 問題なし。
- **SKIP (Exit 0)**: 設定なし、または実行環境不足（警告扱い）。
- **FAIL (Exit 1)**: Lint エラー、または内部エラー。

---

# 完了報告テンプレ

出力されたレポートをそのまま使用してください。

```markdown
# Gate Report: lint
Result: PASS|FAIL|SKIP
Command: <executed command>
Reason: <Category>
Log:
<output>
```
