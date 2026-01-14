---
slug: "type-check"
description: "TypeScript の型チェック（tsc 等）をSoT（quality-gates.yml）に従って実行し、PASS/FAIL/SKIP を根拠（主要エラー）を報告する原子ワークフロー。"
trigger: "manual"
---
# 🧷 type-check — 型チェック

このワークフローは **型チェックの実行と報告のみ** を行います。
修正は別ワークフローで行います。

---

## 定義（このワークフローの狙い）
- 型チェックを実行し、結果を **PASS / FAIL / SKIP** で報告する
- 実行コマンドは **quality-gates スキル** を通じて決定する
- **Source of Truth**: `assets/branding/<Product>/quality-gates.yml`（優先）

---

## 安全ガード（Convoy標準）
- `// turbo` 可（検証のみ）
- **自動修正はしない**

---

# 手順

## Step 1: 型チェック実行 (Quality Gate) // turbo

`quality-gates` スキルを使用してチェックを実行します。

```bash
python .agent/skills/quality-gates/scripts/gate_check.py --type type
```

## Step 2: 結果確認

- **PASS (Exit 0)**: 問題なし。
- **SKIP (Exit 0)**: 設定なし、または実行環境不足（警告扱い）。
- **FAIL (Exit 1)**: 型エラー、または内部エラー。

---

# 完了報告テンプレ

出力されたレポートをそのまま使用してください。

```markdown
# Gate Report: type
Result: PASS|FAIL|SKIP
Command: <executed command>
Reason: <Category>
Log:
<output>
```
