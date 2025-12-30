<!--
Convoy テンプレート: リリースノート（Mission Control）
目的: AIエージェントが埋めやすく、人間が読みやすい GitHub Release/README 向け Markdown を提供する。

============================================================
■ 変数（推奨：できる限り埋める）
  {{PROJECT_NAME}}        プロジェクト名
  {{VERSION}}             リリースバージョン（例: v1.2.3）
  {{RELEASE_DATE}}        リリース日（例: 2025-12-30）
  {{IMAGE_URL}}           ヘッダー画像URL（任意）
  {{REPO_URL}}            リポジトリURL
  {{DOCS_URL}}            ドキュメントURL（任意）
  {{ISSUES_URL}}          Issue URL（任意）
  {{DISCUSSIONS_URL}}     Discussions URL（任意）
  {{COMPARE_URL}}         比較URL（tag間/commit間）

■ 品質ゲート（任意だが推奨）
  {{BUILD_STATUS}}        passing / failing / n/a
  {{BUILD_NOTES}}         補足（任意）
  {{TEST_STATUS}}         passing / failing / n/a
  {{TEST_NOTES}}          補足（任意）
  {{LINT_STATUS}}         passing / failing / n/a
  {{LINT_NOTES}}          補足（任意）
  {{SECURITY_STATUS}}     passing / failing / n/a
  {{SECURITY_NOTES}}      補足（任意）
  {{COVERAGE}}            例: 78%
  {{COVERAGE_NOTES}}      補足（任意）

■ 本文ブロック（任意）
  {{OVERVIEW_PARAGRAPH}}  概要（2〜5文）
  {{TLDR_ONE_LINER}}      要点1行
  {{MEDIA_BLOCK}}         スクショ/GIF等
  {{AGENT_SUMMARY}}       エージェント実行サマリ（3〜7行）
  {{CONVOY_RUN_ID}}       Run ID（任意）

■ 変更内容（必要に応じて行を増やす）
  {{NF_1}} {{NF_1_DESC}} {{NF_1_PR}} ... etc
============================================================

注意:
- これは「出力フォーマットの規格」です。Workflows 側で `{{...}}` を埋めて使用します。
- 表の行は増減して構いません（テンプレの骨格を維持することを優先）。
-->

<div align="center">
  <img src="{{IMAGE_URL}}" alt="Release Header" width="100%" />
</div>

<div align="center">

[![Version](https://img.shields.io/badge/version-{{VERSION}}-blue)]()
[![PRs](https://img.shields.io/badge/PRs-welcome-brightgreen)]()

**{{PROJECT_NAME}} {{VERSION}} をリリースしました。**  
Mission Control: Automate Everything / Agent First

[Docs]({{DOCS_URL}}) · [Issues]({{ISSUES_URL}}) · [Discussions]({{DISCUSSIONS_URL}})

</div>

---

## 概要

- リリース日: **{{RELEASE_DATE}}**
- 比較リンク: **{{COMPARE_URL}}**

{{OVERVIEW_PARAGRAPH}}

---

## ハイライト

> [!NOTE]
> **TL;DR**: {{TLDR_ONE_LINER}}

### いま何ができるようになったか
- {{HIGHLIGHT_1}}
- {{HIGHLIGHT_2}}
- {{HIGHLIGHT_3}}

### スクリーンショット / デモ
{{MEDIA_BLOCK}}

---

## 品質ゲート（Mission Control）

| Gate | Status | Notes |
|------|--------|------|
| Build | {{BUILD_STATUS}} | {{BUILD_NOTES}} |
| Tests | {{TEST_STATUS}} | {{TEST_NOTES}} |
| Lint | {{LINT_STATUS}} | {{LINT_NOTES}} |
| Security | {{SECURITY_STATUS}} | {{SECURITY_NOTES}} |
| Coverage | {{COVERAGE}} | {{COVERAGE_NOTES}} |

---

## 変更内容

### 新機能

| 機能 | 説明 | PR |
|------|------|----|
| {{NF_1}} | {{NF_1_DESC}} | {{NF_1_PR}} |
| {{NF_2}} | {{NF_2_DESC}} | {{NF_2_PR}} |

### 改善
- **{{IMP_1}}**: {{IMP_1_DESC}} ({{IMP_1_PR}})
- **{{IMP_2}}**: {{IMP_2_DESC}} ({{IMP_2_PR}})

### バグ修正
- {{FIX_1}} ({{FIX_1_PR}})
- {{FIX_2}} ({{FIX_2_PR}})

### ドキュメント
- {{DOC_1}} ({{DOC_1_PR}})

---

## 破壊的変更（該当する場合）

> [!WARNING]
> {{BREAKING_SUMMARY}}

```diff
- {{OLD_BEHAVIOR}}
+ {{NEW_BEHAVIOR}}
```

### 移行手順
1. {{MIGRATION_STEP_1}}
2. {{MIGRATION_STEP_2}}

---

## 技術詳細（任意）

<details>
  <summary>詳細を表示</summary>

### アーキテクチャ
- {{ARCH_NOTE_1}}
- {{ARCH_NOTE_2}}

### パフォーマンス

| 指標 | Before | After | 差分 |
|------|--------|-------|------|
| {{METRIC_1}} | {{BEFORE_1}} | {{AFTER_1}} | {{DELTA_1}} |
| {{METRIC_2}} | {{BEFORE_2}} | {{AFTER_2}} | {{DELTA_2}} |

</details>

---

## アップグレード手順

```bash
# 例（実際のコマンドに置き換えてください）
# pip
pip install --upgrade {{PROJECT_NAME}}

# uv
uv pip install {{PROJECT_NAME}}
```

---

## エージェント実行サマリ（任意）

Run ID: `{{CONVOY_RUN_ID}}`

{{AGENT_SUMMARY}}

---

## 貢献者

本リリースに貢献いただいた皆さま、ありがとうございます。

---

## 完全な変更履歴

**Full Changelog**: {{COMPARE_URL}}

---

<div align="center">

このプロジェクトが役に立ったら Star をお願いします。

[GitHub]({{REPO_URL}})

</div>
