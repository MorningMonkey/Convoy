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
- **解析の優先順位**: 物理的なファイル構造より、READMEやドキュメントに現れる**論理概念**を優先する。
- **出力言語**: 図中のラベル・説明は **English only** とする。
- **スタイル規律**: Mission Control 風の洗練された図。ニュートラル基調 + アクセント1〜2色。グラデーションは禁止（Flat design only）。
- **構成要件**:
  - Block Diagram として境界を明示する（Container / Swimlane を使用）。
  - Flow は矢印で接続し、データ/制御の流れを明確にする。
  - 余白は十分に確保する（要素間 最小 40px、コンテナ内も広めのパディング）。
- **形式の厳守**: 出力は Draw.io で読み込める完全な XML（`<mxfile>` 〜 `</mxfile>`）。
- **保存先のSoT**: 生成物は `docs/architecture.drawio` を正本とする。
- **保存の扱い**: `docs/` が無い場合は作成して保存する（作成不可ならユーザーに作成を促す）。

## 🚀 Workflow / SOP

### Step 1: 🔎 プロジェクト解析（Decision）
1. `list_dir` / `view_file` 相当の手段で、README、主要設定（例: `package.json`, `pubspec.yaml`）、主要スクリプトを確認する。
2. 目的、主要コンポーネント、データの流れ、依存関係を特定する。
3. 構造は「論理概念」を中心に抽象化して整理する（ファイル階層そのものは図の中心にしない）。

**出力**
- 図に載せる論理ブロック一覧（名前・役割・相互関係）
- Flow（矢印）の一覧（from → to、データ/制御の種別）

---

### Step 2: 🧱 Draw.io XML 生成（Action）
1. Step 1 の結果をもとに、Draw.io で読み込み可能な XML を生成する。
2. 以下を必ず満たす:
   - English only（図中ラベル）
   - Flat design（no gradients）
   - Container/Swimlane で境界明示
   - 十分な余白（≥40px）
   - Flow を矢印で接続
3. 出力は `<mxfile>` で始まり `</mxfile>` で終わる完全な XML とする。

**出力**
- Draw.io XML（完全版）

---

### Step 3: 💾 保存（Action）
1. `docs/architecture.drawio` に保存する。
2. `docs/` が無い場合は作成してから保存する（できない場合は作成を依頼する）。
3. 保存完了を通知する。

**出力**
- `docs/architecture.drawio`

---

### Step 4: 🎨 SVG/PNG 生成と README への反映（必須）
Draw.io XMLの生成に加え、READMEでのプレビュー用に画像ファイル（SVG/PNG）を生成し、埋め込みまでを自動化する。

1. **SVG 生成**: Pythonスクリプト or Node.js (`sharp`) 等を用いて、論理構成図と同等の内容を持つ `docs/architecture.svg` を作成する。（`class="box"` 等の属性が正しいか注意する）
2. **PNG 生成**: SVG から `docs/architecture.png` を生成する（GitHubのダークモード/ライトモード互換性やプレビュー用）。
3. **README 埋め込み**: `README.md` の Architecture セクションに `<picture>` タグを用いて埋め込む。

```markdown
## Architecture
<!-- Source: docs/architecture.drawio -->
<picture>
  <source type="image/svg+xml" srcset="docs/architecture.svg">
  <img src="docs/architecture.png" alt="Architecture Diagram" width="900">
</picture>
```

**出力**
- `docs/architecture.svg`
- `docs/architecture.png`
- `README.md` (Updated)

## ✅ Checklist
- [ ] 図がファイルツリーではなく論理概念を中心に構成されている
- [ ] 図中のテキストが English only で、Flat design（no gradients）を満たしている
- [ ] XML が有効（`<mxfile>`〜`</mxfile>`）で、`docs/architecture.drawio` に保存されている
- [ ] 要素間余白（≥40px）と Flow（矢印接続）が確保され、読みやすい


