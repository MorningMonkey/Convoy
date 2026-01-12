---
slug: "verify-code"
description: "Lint / 型チェック / テスト（任意でセキュリティ）を既存の原子ワークフローで順次実行し、結果を集約してPASS/FAILを判定する統合ワークフロー。"
trigger: "manual"
---
# ✅ verify-code — コード検証（必須ワークフロー）

`verify-code` は、リポジトリの健全性を確認するための **統合チェック**です。  
Convoy では、各検証を「原子ワークフロー」に分離し、本ワークフローは **実行順序と結果集約**に責務を限定します。

---

## 定義（このワークフローの狙い）
- 変更が品質ゲートを満たしているかを短時間で判定する
- 失敗時に「どこが壊れたか」を即時に切り分けできる状態にする
- 実行結果（Evidence）を残し、レビューやリリース判断に使える形式で報告する

---

## SoT（Source of Truth）
- 原子ワークフロー:
  - `/lint-check`
  - `/type-check`
  - `/run-tests`
  - `/security-scan`（任意）
- スタック/品質ゲート: `assets/branding/<productId>/brief.md`
- コマンド一覧: `.agent/INDEX.md`
- セキュリティ規約（任意）: `.agent/rules/*security*.md`

---

## 入力（Inputs）
- 目的（任意）: `PR前` / `リリース前` / `バグ修正後` など
- 実行モード:
  - 標準: Lint → Type → Tests
  - 拡張: Lint → Type → Tests → Security
- 対象ブランチ/コミット（任意）

---

## 成果物（Outputs）
- チェック結果テーブル（各ワークフローの判定）
- 総合判定: `PASS` / `FAIL`
- 失敗がある場合の最短アクション（次に実行すべきワークフロー）

---

## 判定ルール（重要）
- `FAIL` が1つでもあれば **総合 FAIL**
- `PASS_WITH_WARNINGS` や `PASS_WITH_SKIPPED` は **総合 PASS** だが、Risk として明記する
- セキュリティスキャンは任意だが、実施した場合に `FAIL` なら総合 FAIL

---

# 手順

## Step 1: Lint チェック実行 // turbo
- 実行: `/lint-check`
- 取得: 判定（PASS / PASS_WITH_WARNINGS / FAIL）と主要所見

---

## Step 2: 型チェック実行 // turbo
- 実行: `/type-check`
- 取得: 判定（PASS / FAIL）と主要所見

---

## Step 3: テスト実行 // turbo
- 実行: `/run-tests`
- 取得: 判定（PASS / FAIL / PASS_WITH_SKIPPED）と主要所見

---

## Step 4: セキュリティスキャン（任意）
以下のいずれかを満たす場合に実行を推奨：
- リリース前
- 依存関係更新を含むPR
- 認証/課金/データ取り扱い周りの変更

実行する場合：
- 実行: `/security-scan`
- 取得: 判定（PASS / PASS_WITH_WARNINGS / FAIL）と主要所見

---

## Step 5: 結果集約と総合判定
各チェックの結果を集約し、判定ルールに従って `PASS / FAIL` を決定する。

---

## Step 6: 完了報告（Convoy標準）
```markdown
## ✅ verify-code 結果

- 目的: <PR前/リリース前/バグ修正後 など（任意）>
- 対象: <ブランチ/コミット（任意）>

| Check | Result | Notes |
|---|---|---|
| Lint | PASS / PASS_WITH_WARNINGS / FAIL | <主要所見（短く）> |
| Type | PASS / FAIL | <主要所見（短く）> |
| Tests | PASS / PASS_WITH_SKIPPED / FAIL | <passed/failed/skipped or 主要所見> |
| Security (opt) | PASS / PASS_WITH_WARNINGS / FAIL / N/A | <主要所見（短く）> |

### 総合判定
- **PASS / FAIL**

### Risk（任意）
- PASS_WITH_WARNINGS / PASS_WITH_SKIPPED がある場合は列挙

### Next Action（FAIL時）
- まず直すべきもの: <Lint / Type / Tests / Security>
- 推奨ワークフロー: `<例: /bug-fix>`
```

---

## 付録: よくある運用パターン
- PR作成前: `verify-code`（Securityは任意）
- リリース前: `verify-code` + Security必須
- バグ修正後: `verify-code` → OKなら `/git-auto-commit`


