---
slug: "parallel-discovery-antigravity"
description: "Antigravity Managerで UI/データ/CI の3エージェントを並列稼働し、ArtifactsをConvoyの正本ドキュメント（docs/products/<productId>/）へ収束させる。"
trigger: "manual"
---
# 🧭 Parallel Discovery SOP (UI / Data / CI) via Antigravity Manager

## 🌌 Overview
本ワークフローは、Antigravity の Manager を用いて
UI / データ / CI の調査・設計を **同時進行→レビュー→方向修正** のループで実施し、
成果を Convoy の正本（`docs/products/<productId>/`）へ統合するための標準手順です。

目的は「速さ」ではなく、**並列化してもブレない意思決定と成果物の収束**です。

---

## ⚖️ Rules / Constraints
- **SoT（唯一の正本）**: `assets/branding/<productId>/brief.md`
- **成果の正本**: `docs/products/<productId>/`（Artifactsは中間成果）
- **衝突時の優先順位**: Brief > MVPスコープ（00）> 各設計（01-04）> 実装都合
- **MVP画面数上限**: 原則 7 画面（超える場合は分割案必須）
- **エージェントの作業範囲**:
  - UI: 画面/フロー/文言/完了条件まで
  - データ: 状態・イベント・永続化の最小契約まで
  - CI: 最小品質ゲートと復旧手順まで
- **危険操作の禁止**: 破壊的コマンド・広範囲ファイル変更をしない（調査・設計が目的）
- **アウトプットはArtifacts形式**で提出し、最後に統合フェーズで docs に反映する

---

## ✅ Inputs / Preconditions
- `productId`（例: `aquaritual`）
- `assets/branding/<productId>/brief.md`（必須）
- `docs/products/<productId>/` が存在（推奨: `setup-product-discovery` 実行済み）
  - `00_mvp-scope.md`
  - `01_screen-inventory.md`
  - `03_data-contract.md`
  - `04_quality-gates.md`

---

## 🎛️ Roles（Managerで立てる3エージェント）
### Agent A: UI Inventory Lead
**責務**: 画面棚卸し、MVP画面の提案、主要フロー、文言の方向性  
**成果物（Artifacts）**:
- MVP画面一覧（<=7）＋各画面の完了条件
- 主要ユーザーフロー（最短）＋例外フロー（権限NG等）
- 画面ごとの「入力/出力/エラー」粒度の下書き

### Agent B: Data Contract Lead
**責務**: Riverpod前提の状態設計、イベント設計、永続化の最小ライン  
**成果物（Artifacts）**:
- Domain概念（名詞）とState（SoT/Derived）の線引き
- Action/Event一覧（UIイベント→State変化→副作用）
- 永続化が必要なものだけを理由付きで定義（MVP最小）

### Agent C: Quality & CI Lead
**責務**: 品質最小ゲート、CIテンプレ、失敗時の復旧手順  
**成果物（Artifacts）**:
- ローカルゲート: format/analyze/test/run の順序
- CI最小: format/analyze/test（GitHub Actions想定）
- よくある失敗TOP5と復旧手順（初学者向け）

---

## 🚀 Workflow / SOP

### Step 1: Managerセットアップ（並列開始）
Managerで3エージェントを作成し、同時に以下の指示を与える。

#### A: UIエージェント指示（コピペ用）
- brief.md を読み、AquaRitualの体験を「ユーザーが得る価値」で1文に要約。
- MVP画面を最大7画面に制限して提案（Must/Should/Couldの分類）。
- 各画面について「目的・主要UI・入力・出力・失敗パターン・完了条件」を書く。
- 主要フローを1本、例外フローを2本（権限NG/ネットワーク不調等）作る。
- すべてArtifactsとして提出し、最後に docs/products/<productId>/01・02 に反映する差分案も添える。

#### B: データエージェント指示（コピペ用）
- UIエージェントのMVP画面一覧を前提に、画面ごとに State / Action / SideEffect を列挙。
- Riverpodで「SoT（保持）/ Derived（計算）」を明確に分離する方針を書く。
- 永続化が必要なデータだけを理由付きで採用し、MVP外は明確に除外。
- Artifactsとして提出し、docs/products/<productId>/03 に反映する差分案を添える。

#### C: CIエージェント指示（コピペ用）
- build-app-flutterの品質最低ラインに整合する最小ゲートを定義（format/analyze/test）。
- GitHub Actionsでの最小CI案（ジョブ名、キャッシュ、コマンド順）を提示。
- 失敗時の典型原因TOP5と、調査→復旧の手順を日本語で書く。
- Artifactsとして提出し、docs/products/<productId>/04 に反映する差分案を添える。

---

### Step 2: レビューゲート（衝突検出）
Manager（あなた or 統合エージェント）は以下をチェックし、矛盾があれば差し戻す。

- UIのMVP画面数が<=7か
- 画面の完了条件が「ユーザー達成」で書けているか
- DataがUIフローを満たす契約になっているか（不足・過剰がないか）
- CIが“実装前でも回せる最小”になっているか（重すぎないか）
- SoT（brief.md）と矛盾がないか

---

### Step 3: 統合（Convoy docsへ収束）
統合担当（あなた、または別エージェント）で、Artifactsの結論を以下へ反映する。

- `00_mvp-scope.md`（MVPゴール/範囲/やらないこと更新）
- `01_screen-inventory.md`（MVP画面棚卸しを確定）
- `02_user-flows.md`（主要フロー＋例外フロー）
- `03_data-contract.md`（State/Action/永続化の最小契約）
- `04_quality-gates.md`（format/analyze/test/CI方針）
- `decisions/ADR-0002-mvp-and-architecture.md`（主要決定をログ化）

---

## ✅ Definition of Done（このStepの完了条件）
- [ ] 3エージェントのArtifactsが揃い、相互矛盾が解消されている
- [ ] docs/products/<productId>/00〜04 が “MVP版” として更新されている
- [ ] ADR-0002 が作成され、MVP境界・状態管理・ルーティング・品質ゲートの決定が記録されている
- [ ] 次工程（build-app-flutter）に渡せる「MVPの完了条件（デモ条件）」が3つ明文化されている


