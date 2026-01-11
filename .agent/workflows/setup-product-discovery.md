---
slug: "setup-product-discovery"
description: "Convoy内でプロダクトの棚卸し→MVP決定→設計を回すための成果物置き場（SoT/Docs/Decisions）を標準生成する。"
trigger: "manual"
---

# 🗂️ Product Discovery Workspace Setup (Inventory → MVP → Design)

## 🌌 Overview
本ワークフローは、Convoy 傘下プロダクト（例: AquaRitual）の「棚卸し→MVP→設計」を並列に進めるために、
成果物が散逸しない **標準の置き場（Docs/Decisions）** を先に構築します。

Antigravity 等で複数エージェントが同時に成果物を出す前提において、
「何が正本か」「どこに収束させるか」を固定し、後工程（build-app-flutter / 実装SOP）へ滑らかに接続します。

---

## ⚖️ Rules / Constraints
- **SoT（唯一の正本）**: `assets/branding/<productId>/brief.md` を唯一の正本とする。
- **成果物の正本**: 棚卸し・MVP・設計・決定ログは `docs/products/<productId>/` に集約する。
- **Artifactsは中間生成物**: Antigravity の Artifacts はレビュー・統合のために用いるが、最終版は必ず `docs/` に反映する。
- **MVPは上限を設ける**: MVP 画面数は原則 7 画面まで（超える場合は理由と分割案を必須とする）。
- **決定はログに残す**: 重要な選択（例: 状態管理・ルーティング方針・永続化有無）は ADR として残す。

---

## ✅ Inputs / Outputs

### Inputs
- `productId`（例: `aquaritual`）
- `assets/branding/<productId>/brief.md`（存在必須）

### Outputs（生成/更新）
- `docs/products/<productId>/00_mvp-scope.md`
- `docs/products/<productId>/01_screen-inventory.md`
- `docs/products/<productId>/02_user-flows.md`
- `docs/products/<productId>/03_data-contract.md`
- `docs/products/<productId>/04_quality-gates.md`
- `docs/products/<productId>/decisions/ADR-0001-initial-decisions.md`

---

## 🚀 Workflow / SOP

### Step 1: SoT の存在確認
- `assets/branding/<productId>/brief.md` の存在を確認する。
- 無い場合はこのワークフローを中止し、`brief.md` 作成を優先する。

### Step 2: 成果物ディレクトリの作成
以下を作成する：
- `docs/products/<productId>/`
- `docs/products/<productId>/decisions/`

### Step 3: ドキュメント雛形を生成（テンプレ投入）
以下のファイルを作成し、最低限のテンプレ構造（見出し）を投入する。

#### `00_mvp-scope.md`（MVP範囲）
- Purpose / Target user
- MVP Goals（デモ可能条件 3つ）
- In Scope / Out of Scope
- MVP Screens（最大7）
- MVP Data（保存する/しない）
- Risks / Open Questions

#### `01_screen-inventory.md`（画面棚卸し）
- Screen list（名称 / 目的 / 主要UI / 入出力 / 失敗パターン / 完了条件）
- 非MVP候補（理由つき）

#### `02_user-flows.md`（遷移フロー）
- MVP最短フロー（ユーザー目線）
- 例外フロー（権限NG、ネットワーク不調等）

#### `03_data-contract.md`（データ契約）
- Domain model（概念）
- State / Action / Side effects（Riverpod前提）
- 永続化（必要なら最小）

#### `04_quality-gates.md`（品質ゲート）
- local（format/analyze/test/run）
- CI最小（format/analyze/test）
- Definition of Done（PR完了条件）

#### `decisions/ADR-0001-initial-decisions.md`
- Context
- Decision
- Alternatives considered
- Consequences
- Status（Accepted）

### Step 4: brief.md へのリンクを埋める
各ドキュメント冒頭に、必ず以下を記載する。
- SoT: `assets/branding/<productId>/brief.md`

### Step 5: INDEX / ナビの更新（任意）
Convoyの運用に合わせ、以下のいずれかを行う。
- `.agent/INDEX.md` にプロダクトドキュメントへのリンクを追記
- `docs/products/<productId>/README.md` を作り、目次を置く

---

## 🧩 Template Snippets（最低限の本文テンプレ）

### 00_mvp-scope.md（例）
- SoT: `assets/branding/<productId>/brief.md`

#### Purpose
#### MVP Goals（デモ可能条件）
1.
2.
3.

#### In Scope
#### Out of Scope
#### MVP Screens（<= 7）
#### MVP Data（保存の要否）
#### Risks / Open Questions

---

## ✅ Checklist
- [ ] `assets/branding/<productId>/brief.md` が存在する
- [ ] `docs/products/<productId>/` と `decisions/` が作成されている
- [ ] 00〜04 のファイルがテンプレ付きで存在する
- [ ] 全ファイルに SoT リンクが明記されている
- [ ] ADR-0001 が作成されている（初期決定の置き場がある）
