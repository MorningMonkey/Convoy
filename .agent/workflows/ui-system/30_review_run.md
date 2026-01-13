---
slug: "review-run"
description: "生成されたUIの検証手順をガイドし、レビューシートへの記入を支援する。"
trigger: "user_request"
---

# 🕵️ Review UI Run (Smoke Gates + UX Score)

## 目的 (Goal)
生成されたデザイン/コードを評価し、`review.md` に以下を確定させる:
*   Smoke Gates (PASS/FAIL)
*   UX Score
*   Verdict (SHIP / FIX / REDESIGN)

## 入力 (Inputs)
*   `runDir`: `ui-system/runs/<productId>/<specId>/<YYYYMMDD>/<HHmmss>/`
*   **Review Target**:
    *   (a) Figma result
    *   (b) Generated code diff
    *   (c) Both

## 安全性 (Safety Guardrails)
*   `.agent/rules/safety-terminal.md` を遵守してください。

## 手順 (Steps)

1.  **レビューファイルの確認**
    `runDir` 内の `review.md` を開きます。
    メタデータを確認します:
    *   `gatesPath` / `rubricPath` / `threshold`
    *   `figmaPage` / `figmaUrl`

2.  **Smoke Gates 実行 (Hard Gate)**
    各ゲート項目について:
    *   **PASS** または **FAIL** をマークする。
    *   **Evidence** (根拠) を1行追記する (ファイル/行、スクショ、再現手順など)。
    
    > **ルール**: 1つでも **FAIL** がある場合、Smoke Gates全体を **FAIL** とし、Verdict は自動的に **REDESIGN** となる。

3.  **UX Scoring (Rubric)**
    *   各セクションを採点する。
    *   合計スコアを算出する。
    *   **P0/P1/P2** の課題を特定する (該当する場合、各レベル少なくとも1つ)。
    *   **具体的な修正案 (Concrete fixes)** を記述する:
        *   **Spec-level**: JSONの修正点
        *   **Figma-level**: 変数、レイアウト、バリアントの修正点

4.  **判定 (Verdict Mapping)**
    以下の基準で判定を記入する:
    *   **SHIP**: Gates **PASS** かつ Score **≧ Threshold**
    *   **FIX**: Gates **PASS** かつ Score **< Threshold**
    *   **REDESIGN**: Gates **FAIL**

5.  **完了 (Save)**
    `review.md` を保存して完了とする。
