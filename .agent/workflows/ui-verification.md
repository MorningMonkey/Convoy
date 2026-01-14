---
slug: "ui-verification"
description: "UIの視覚検証（E2E/スクリーンショット比較等）をSoT（quality-gates.yml）に従って実行し、PASS/FAIL/SKIP を根拠つきで報告する原子ワークフロー。"
trigger: "manual"
---
# 🖥️ ui-verification — UI検証

このワークフローは **検査と報告のみ** を行います。
修正や実装は別ワークフローで行います。

---

## 定義（このワークフローの狙い）
- UI検証（E2E、スクリーンショット比較など）を実行し、結果を **PASS / FAIL / SKIP** で報告する
- 実行コマンドは **quality-gates スキル** を通じて決定する
- **Source of Truth**: `assets/branding/<Product>/quality-gates.yml`（優先）

---

## 安全ガード（Convoy標準）
- `// turbo` 可
- **自動修正はしない**

---

# 手順

## Step 1: UI検証 (Quality Gate) // turbo

`quality-gates` スキルを使用してチェックを実行します。
自動テスト（Playwright/Maestro等）が設定されている場合に実行されます。手動検証が必要な場合は、別途手順を参照してください。

```bash
python .agent/skills/quality-gates/scripts/gate_check.py --type ui
```

## Step 2: 結果確認

- **PASS (Exit 0)**: テスト通過。
- **SKIP (Exit 0)**: 設定なし（警告扱い）。
- **FAIL (Exit 1)**: テスト失敗、または内部エラー。

---

# 完了報告テンプレ

出力されたレポートをそのまま使用してください。

```markdown
# Gate Report: ui
Result: PASS|FAIL|SKIP
Command: <executed command>
Reason: <Category>
Log:
<output>
```
