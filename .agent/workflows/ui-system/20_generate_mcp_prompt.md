---
slug: "generate-mcp-prompt"
description: "UI Spec と品質基準を結合し、Figma MCP 用のコンテキスト最適化プロンプトを生成する。"
trigger: "user_request"
---

# 🏭 Generate Figma MCP Prompt

## 目的 (Goal)
以下を生成する:
*   `mcp_prompt.md` (for Figma MCP)
*   `review.md` (Smoke Gates + UX Score Skeleton)

## 入力 (Inputs)
### 必須 (Required)
*   `productId`: <kebab-case>
*   `specId`: <kebab-case>
*   `figmaPage`: 文字列 (Figma上のページ名)
*   `figmaUrl`: https://...

### オプション (Optional Overrides)
*   `gatesPath`: Gates定義ファイルパス (デフォルトは後述)
*   `rubricPath`: Rubric定義ファイルパス (デフォルトは後述)
*   `uxThreshold`: 合格閾値 (デフォルトは後述)

## デフォルト設定 (Defaults)
*   `gatesPath`: `ui-system/rubrics/smoke_test_gates.md`
*   `rubricPath`: `ui-system/rubrics/ux_scorecard.md`
*   `uxThreshold`:
    *   標準 (Standard): `75`
    *   Headerプロファイル: `80`

### Header Profile オーバーライド
(推奨: `specId` が `ui-header` の場合のみ)
*   `gatesPath`: `ui-system/rubrics/profiles/header/smoke_test_header_gates.md`
*   `rubricPath`: `ui-system/rubrics/profiles/header/ux_header_scorecard.md`
*   `uxThreshold`: `80`

## 安全性 (Safety Guardrails)
*   `.agent/rules/safety-terminal.md` を遵守してください。

## 手順 (Steps)

1.  **必須ファイルの検証**
    以下の存在を確認します:
    *   `ui-system/specs/<productId>/<specId>.json`
    *   `ui-system/prompts/mcp_base_prompt.md`
    *   選択された `gatesPath`
    *   選択された `rubricPath`
    *   `ui-system/templates/review.template.md`

2.  **Spec JSONの検証 (最小限)**
    *   Spec内に `productId`/`specId` が含まれ、入力と一致することを確認。
    *   `figma.url` が https URL であることを確認 (プレースホルダー可)。

3.  **Runディレクトリ作成**
    `ui-system/runs/<productId>/<specId>/<YYYYMMDD>/<HHmmss>/` を作成します。

4.  **mcp_prompt.md の生成 (順序厳守)**
    以下の要素を順番に結合して生成します:
    *   **A) Meta Header**:
        *   productId, specId, runId
        *   figmaPage, figmaUrl
        *   gatesPath, rubricPath, uxThreshold
    *   **B) Base Prompt**: `ui-system/prompts/mcp_base_prompt.md`
    *   **C) Spec JSON**: (Inline展開)
    *   **D) Gates**: (Inline展開)
    *   **E) UX Rubric**: (Inline展開)

5.  **review.md の生成**
    テンプレートから生成します:
    *   メタフィールド (`productId`/`specId`/`runId`/`page`/`url`) を埋める。
    *   `gatesPath`/`rubricPath`/`threshold` を埋める。
    *   チェックリストを初期化する (PASS/FAIL は空欄).

6.  **出力通知 (Output)**
    *   Runディレクトリのパスを表示。
    *   `mcp_prompt.md` の冒頭20行を表示。
    *   (Optional) クリップボードへのコピーコマンドを提示:
        `Get-Content mcp_prompt.md | Set-Clipboard`

## 期待される出力 (Expected Output)
*   `ui-system/runs/.../mcp_prompt.md`
*   `ui-system/runs/.../review.md`
