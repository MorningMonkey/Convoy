---
slug: "visualize-architecture"
description: "リポジトリの論理構成を解析し、Draw.io XMLでアーキテクチャ図を生成してdocs/へ保存する。"
trigger: "model_decision"
---

# 🧩 visualize-architecture

## 🌌 Overview
本ワークフローは、リポジトリ内容を解析し、プロジェクトの**論理構成**（目的・主要コンポーネント・依存関係・データの流れ）を
プロフェッショナルな Draw.io 図として可視化する。
ファイルツリーの写経ではなく、README・ドキュメントから読み取れる概念（例: Mission Control / Factory / Brain）を優先し、
設計の共有とオンボーディングを高速化する。

## ⚖️ Rules / Constraints
- **解析の優先順位**: 物理的なファイル構造より、READMEやドキュメントに現れる**論理概念**を優先する。fileciteturn12file0L12-L16
- **出力言語**: 図中のラベル・説明は **English only** とする。fileciteturn12file0L22-L24
- **スタイル規律**: Mission Control 風の洗練された図。ニュートラル基調 + アクセント1〜2色。グラデーションは禁止（Flat design only）。fileciteturn12file0L24-L31
- **構成要件**:
  - Block Diagram として境界を明示する（Container / Swimlane を使用）。fileciteturn12file0L31-L34
  - Flow は矢印で接続し、データ/制御の流れを明確にする。fileciteturn12file0L33-L35
  - 余白は十分に確保する（要素間 최소 40px、コンテナ内も広めのパディング）。fileciteturn12file0L35-L41
- **形式の厳守**: 出力は Draw.io で読み込める完全な XML（`<mxfile>` 〜 `</mxfile>`）。fileciteturn12file0L41-L43
- **保存先のSoT**: 生成物は `docs/architecture.drawio` を正本とする。fileciteturn12file0L46-L49
- **保存の扱い**: `docs/` が無い場合は作成して保存する（作成不可ならユーザーに作成を促す）。fileciteturn12file0L47-L49

## 🚀 Workflow / SOP

### Step 1: 🔎 プロジェクト解析（Decision）
1. `list_dir` / `view_file` 相当の手段で、README、主要設定（例: `package.json`, `pubspec.yaml`）、主要スクリプトを確認する。fileciteturn12file0L10-L13
2. 目的、主要コンポーネント、データの流れ、依存関係を特定する。fileciteturn12file0L13-L14
3. 構造は「論理概念」を中心に抽象化して整理する（ファイル階層そのものは図の中心にしない）。fileciteturn12file0L12-L16

**出力**
- 図に載せる論理ブロック一覧（名前・役割・相互関係）
- Flow（矢印）の一覧（from → to、データ/制御の種別）

---

### Step 2: 🧱 Draw.io XML 生成（Action）
1. Step 1 の結果をもとに、Draw.io で読み込み可能な XML を生成する。fileciteturn12file0L18-L22
2. 以下を必ず満たす:
   - English only（図中ラベル）
   - Flat design（no gradients）
   - Container/Swimlane で境界明示
   - 十分な余白（≥40px）
   - Flow を矢印で接続
3. 出力は `<mxfile>` で始まり `</mxfile>` で終わる完全な XML とする。fileciteturn12file0L41-L43

**出力**
- Draw.io XML（完全版）

---

### Step 3: 💾 保存（Action）
1. `docs/architecture.drawio` に保存する。fileciteturn12file0L46-L49
2. `docs/` が無い場合は作成してから保存する（できない場合は作成を依頼する）。fileciteturn12file0L47-L49
3. 保存完了を通知する。

**出力**
- `docs/architecture.drawio`

---

### Step 4: 📎 SVG エクスポートと README 埋め込み（任意）
1. `architecture.drawio` を Draw.io で開き、必要なら微調整する。fileciteturn12file0L51-L54
2. SVG としてエクスポートする（`docs/architecture.svg`）。fileciteturn12file0L52-L54
3. `README.md` の Architecture セクションに SVG を埋め込み、視覚ドキュメントとして機能させる。fileciteturn12file0L54-L55

**出力**
- `docs/architecture.svg`（任意）
- README の埋め込み（任意）

## ✅ Checklist
- [ ] 図がファイルツリーではなく論理概念を中心に構成されている
- [ ] 図中のテキストが English only で、Flat design（no gradients）を満たしている
- [ ] XML が有効（`<mxfile>`〜`</mxfile>`）で、`docs/architecture.drawio` に保存されている
- [ ] 要素間余白（≥40px）と Flow（矢印接続）が確保され、読みやすい
