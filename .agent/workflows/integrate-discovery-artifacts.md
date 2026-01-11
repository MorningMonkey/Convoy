---
slug: "integrate-discovery-artifacts"
description: "AntigravityのUI/Data/CI Artifactsをレビューし、衝突解消→Convoy docsへ収束→ADRで決定ログ化する統合SOP。"
trigger: "manual"
---

# 🧩 Discovery Artifacts Integration SOP (Artifacts → Convoy Docs)

## 🌌 Overview
本ワークフローは、Antigravity Manager で並列生成された
UI / Data / CI の Artifacts を統合し、Convoy の正本ドキュメントへ反映して
「棚卸し→MVP→設計」を確定させるための手順です。

Artifacts は中間成果であり、最終版は必ず Convoy リポジトリに収束させます。

---

## ⚖️ Rules / Constraints
- **SoT（唯一の正本）**: `assets/branding/<productId>/brief.md`
- **正本の置き場**: `docs/products/<productId>/`（Artifactsは中間成果）
- **優先順位（衝突時）**: Brief > MVP Scope（00）> UI（01/02）> Data（03）> CI（04）
- **MVP画面数上限**: 原則 7（超える場合は“分割案”を必須とし、Out of Scopeへ退避）
- **実装に踏み込まない**: この工程は設計確定であり、コード生成・大規模編集は行わない
- **必ずADRを残す**: MVP境界・状態管理・ルーティング・品質ゲートの決定は ADR 化する

---

## ✅ Inputs / Preconditions
- `productId`（例: `aquaritual`）
- Antigravity で提出された以下の Artifacts（3本）
  - UI Inventory Lead の成果
  - Data Contract Lead の成果
  - Quality & CI Lead の成果
- `docs/products/<productId>/` が存在（推奨: `setup-product-discovery` 実行済み）
  - `00_mvp-scope.md`
  - `01_screen-inventory.md`
  - `02_user-flows.md`
  - `03_data-contract.md`
  - `04_quality-gates.md`
  - `decisions/`

---

## 🎯 Integration Outputs（このStepで確定させるもの）
- `00_mvp-scope.md` を MVP確定版に更新（In/Out、デモ条件3つ）
- `01_screen-inventory.md` を MVP画面（<=7）で確定
- `02_user-flows.md` を “最短フロー1本＋例外フロー2本” で確定
- `03_data-contract.md` を “SoT/Derived、Action/Event、永続化最小” で確定
- `04_quality-gates.md` を “format/analyze/test、CI最小、DoD” で確定
- `decisions/ADR-0002-mvp-and-architecture.md` を新規作成（決定ログ）

---

## 🚀 Workflow / SOP

### Step 1: Artifacts の取り込み（入力を固定）
統合担当は、3本のArtifactsから以下を抜き出し、統合メモ（作業中メモ）に貼り付ける。

- UI: MVP画面一覧、完了条件、最短フロー、例外フロー
- Data: State分類（SoT/Derived）、Action/Event、永続化の要否
- CI: ローカルゲート、CI最小、失敗TOP5と復旧手順

> 目的: “何が出てきたか” を可視化し、衝突検出を早くする

---

### Step 2: 衝突検出（Conflict Matrixを作る）
次の観点で矛盾を検出し、表にする（最大10件まで）。

- MVP画面数超過（<=7を超える）
- UIフローに必要なデータが Data 契約にない（不足）
- Data が過剰（MVP外の永続化・複雑な副作用が増えている）
- CIが重すぎる（MVP前に運用できない構成）
- Brief と矛盾（色・プラットフォーム優先・権限方針・メディア特性）

---

### Step 3: 衝突解消（裁定ルールに従う）
以下の順で裁定する。

1) Brief に寄せる（SoT優先）
2) MVPスコープ（00）に寄せる（“やらないこと”を明文化）
3) 画面数が増える場合は分割（MVPとPost-MVPに分ける）
4) Dataは “動くための最小契約” に縮退（永続化は必要性が証明できるものだけ）
5) CIは “format/analyze/test” の最小に固定し、追加は後段へ

---

### Step 4: Convoy docs へ反映（確定ドキュメントを更新）
以下の順で更新する（順番が重要）。

1. `00_mvp-scope.md`
   - MVP Goals（デモ条件3つ）
   - In Scope / Out of Scope
   - MVP Screens（<=7）
   - MVP Data（保存する/しない）
2. `01_screen-inventory.md`
   - MVP画面のみ確定（画面ごとに完了条件を必須）
3. `02_user-flows.md`
   - 最短フロー1本、例外フロー2本
4. `03_data-contract.md`
   - SoT/Derived、Action/Event、SideEffect、永続化最小
5. `04_quality-gates.md`
   - local: format/analyze/test/run
   - CI: format/analyze/test
   - Definition of Done（PR完了条件）

---

### Step 5: ADR を作成（決定ログ化）
`docs/products/<productId>/decisions/ADR-0002-mvp-and-architecture.md` を作成し、最低限これを埋める。

- Context（並列Artifactsの前提、Briefの要点）
- Decision（MVP境界、画面数、状態管理方針、ルーティング方針、永続化有無、品質ゲート）
- Alternatives considered（捨てた案）
- Consequences（メリット/トレードオフ）
- Status（Accepted）

---

## 🧾 Integration Lead Prompt（Antigravity用コピペ）
以下を “統合担当エージェント” に渡し、この workflow の通りに実行させる。

### Prompt
あなたは統合担当（Integration Lead）です。
目的は、Antigravityで提出された UI / Data / CI のArtifactsを統合し、
Convoyリポジトリの `docs/products/<productId>/` を正本として更新し、
`ADR-0002-mvp-and-architecture.md` に主要決定を記録することです。

制約:
- SoTは `assets/branding/<productId>/brief.md`
- Artifactsは中間成果。最終版は必ず docs に収束させる
- MVP画面数は原則7まで。超える場合はOut of Scopeへ退避し、分割案を明記
- CIは最小（format/analyze/test）を先に確定。重いものは後段へ
- 実装（コード生成）に踏み込まない。設計確定のみ

手順:
1) 3つのArtifactsから要点（UI:画面/完了条件/フロー、Data:State/Action/永続化、CI:品質ゲート）を抽出
2) 矛盾を最大10件まで列挙（Conflict Matrix）
3) Brief→MVPの順で裁定し、MVPを“1ページ”に要約
4) docs/products/<productId>/00〜04 を更新する差分案を提示
5) decisions/ADR-0002 を作成し、決定・代替案・帰結を記録

出力:
- Conflict Matrix（表）
- MVP確定版サマリ（箇条書き）
- docs更新の差分案（どこに何を書くか）
- ADR-0002 の本文案

---

## ✅ Definition of Done（完了条件）
- [ ] 3本のArtifactsの要点が取り込まれ、Conflict Matrix が作られている
- [ ] 矛盾が裁定され、MVPが「画面<=7」「デモ条件3つ」で確定している
- [ ] docs/products/<productId>/00〜04 が整合した内容で更新されている
- [ ] ADR-0002 が作成され、主要決定が記録されている
- [ ] 次工程（build-app-flutter）へ渡せる状態になっている
