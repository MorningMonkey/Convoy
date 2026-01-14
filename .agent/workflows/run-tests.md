---
slug: "run-tests"
description: "プロジェクトのテスト（Unit/Auto）をSoT（quality-gates.yml）に従って実行し、PASS/FAIL/SKIP を根拠つきで報告する原子ワークフロー。"
trigger: "manual"
---
# 🧪 run-tests — テスト実行

このワークフローは **実行と報告のみ** を行います。
修正や実装は別ワークフローで行います。

---

## 定義（このワークフローの狙い）
- テストを実行し、結果を **PASS / FAIL / SKIP** で報告する
- 実行コマンドは **quality-gates スキル** を通じて決定する
- **Source of Truth**: `assets/branding/<Product>/quality-gates.yml`（優先）

---

## 安全ガード（Convoy標準）
- `// turbo` 可
- **自動修正はしない**

---

# 手順

## Step 1: テスト実行 (Quality Gate) // turbo

`quality-gates` スキルを使用してチェックを実行します。

```bash
python .agent/skills/quality-gates/scripts/gate_check.py --type test
```

## Step 2: 結果確認

- **PASS (Exit 0)**: 全テスト通過。
- **SKIP (Exit 0)**: 設定なし、または実行環境不足（警告扱い）。
- **FAIL (Exit 1)**: テスト失敗、または内部エラー。

---

# 完了報告テンプレ

出力されたレポートをそのまま使用してください。

```markdown
# Gate Report: test
Result: PASS|FAIL|SKIP
Command: <executed command>
Reason: <Category>
Log:
<output>
```
