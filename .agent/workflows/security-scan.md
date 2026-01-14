---
slug: "security-scan"
description: "依存関係脆弱性・シークレット混入・基本セキュリティ規約違反をSoT（quality-gates.yml）に従って検査し、PASS/FAIL/SKIP を根拠つきで報告する原子ワークフロー。"
trigger: "manual"
---
# 🔐 security-scan — セキュリティスキャン

このワークフローは **検査と報告のみ** を行います。
修正（依存更新・シークレット無効化など）は別ワークフローで行います。

---

## 定義（このワークフローの狙い）
- 脆弱性やシークレット混入を検査し、結果を **PASS / FAIL / SKIP** で報告する
- 実行コマンドは **quality-gates スキル** を通じて決定する
- **Source of Truth**: `assets/branding/<Product>/quality-gates.yml`（優先）

---

## 安全ガード（Convoy標準）
- `// turbo` 可
- **自動修正はしない**
- 意図しない外部ネットワークアクセスを防ぐため、許可されたコマンドのみ実行する

---

# 手順

## Step 1: セキュリティ検査 (Quality Gate) // turbo

`quality-gates` スキルを使用してチェックを実行します。
初期状態では `assets/branding/<Product>/quality-gates.yml` にコマンド定義（gitleaks, trivy, npm audit 等）が必要です。定義がない場合は SKIP されます。

```bash
python .agent/skills/quality-gates/scripts/gate_check.py --type security
```

## Step 2: 結果確認

- **PASS (Exit 0)**: 脆弱性なし。
- **SKIP (Exit 0)**: 設定なし（警告扱い）。
- **FAIL (Exit 1)**: 脆弱性検出、シークレット混入、または内部エラー。

---

# 完了報告テンプレ

出力されたレポートをそのまま使用してください。

```markdown
# Gate Report: security
Result: PASS|FAIL|SKIP
Command: <executed command>
Reason: <Category>
Log:
<output>
```
