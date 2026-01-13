---
slug: "iterate-spec"
description: "レビュー結果に基づいて UI Spec (JSON) を更新し、次回の生成品質を向上させる。"
trigger: "user_request"
---

# 🔄 Iterate Spec (Feedback -> Next Run)

## 目的 (Goal)
レビューでの発見事項を Spec の改善に変換し、ワークフロー 20 を再実行する。

## 入力 (Inputs)
*   **runDir**: 前回の実行ディレクトリ (`ui-system/runs/.../`)
*   **specPath**: `ui-system/specs/<productId>/<specId>.json`

## 安全性 (Safety Guardrails)
*   `.agent/rules/safety-terminal.md` を遵守してください。

## 手順 (Steps)

1.  **レビュー結果の分析**
    `runDir` 内の `review.md` を読み込みます:
    *   **P0 / P1** の課題を抽出する。
    *   "Concrete fixes (Spec-level)" の記述を抽出する。

2.  **Spec JSON の更新**
    抽出した課題に基づき、JSONファイルを修正します:
    *   **Acceptance Criteria**: 漏れていた基準があれば追加。
    *   **Components**: State や Props の不足を修正。
    *   **Layout**: Overflow や タップターゲットに関する制約が不足していれば追加。

3.  **コミット (Recommended)**
    変更をコミットすることを推奨します:
    ```bash
    git add ui-system/specs/<productId>/<specId>.json
    git commit -m "spec(<productId>): refine <specId> based on run review"
    ```

4.  **再実行 (Rerun)**
    *   **Workflow 20** (`generate-mcp-prompt`) を同じ入力パラメータで実行する。
    *   前回 (`runDir`) の結果と、今回の新しい生成結果を比較する。
