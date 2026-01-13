---
slug: "ui-system-overview"
description: "UI System ワークフロー群の概要、資産構成、実行順序を定義する。"
trigger: "user_request"
---

# UI-System Workflows Overview

## 目的
`ui-system` の資産を用いて、Figma MCP ワークフローを標準的かつ反復可能な方法で運用します。
仕様書 (Spec) からプロンプトを生成し、レビュー結果をフィードバックする一連のサイクルを定義します。

## 資産 (Source of Truth)
以下のファイルが「信頼できる唯一の情報源」として機能します。

*   **Specs**: `ui-system/specs/<productId>/<specId>.json`
*   **Base Prompt**: `ui-system/prompts/mcp_base_prompt.md`
*   **Gates (Default)**: `ui-system/rubrics/smoke_test_gates.md`
*   **Rubric (Default)**: `ui-system/rubrics/ux_scorecard.md`
*   **Template**: `ui-system/templates/review.template.md`
*   **Schema**: `ui-system/schemas/ui-spec.schema.json`

## 出力 (Generated)
各実行 (Run) ごとに以下の生成物が保存されます（Git管理外）。

*   `ui-system/runs/<productId>/<specId>/<YYYYMMDD>/<HHmmss>/mcp_prompt.md`
*   `ui-system/runs/<productId>/<specId>/<YYYYMMDD>/<HHmmss>/review.md`

## 標準フロー (Standard Flow)

### 1. Bootstrap
新規プロダクトまたはSpecのセットアップを行います。
*   Worklfow: `10_bootstrap_product.md`

### 2. Generate
Specと品質基準を結合し、Figma MCP用のプロンプトとレビューシートを生成します。
*   Workflow: `20_generate_mcp_prompt.md`

### 3. Implement (Human Action)
生成された `mcp_prompt.md` を Figma MCP に入力し、デザインまたはコードを生成します。

### 4. Review
生成結果を検証し、品質ゲートとUXスコアを記録します。
*   Workflow: `30_review_run.md`

### 5. Iterate
レビュー結果に基づいてSpecを修正し、次のサイクルへ進みます。
*   Workflow: `40_iterate_spec.md`

## 安全性 (Safety)
すべての操作は `.agent/rules/safety-terminal.md` に従う必要があります。
