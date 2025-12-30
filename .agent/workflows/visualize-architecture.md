---
slug: visualize-architecture
description: Draw.io XMLでプロジェクトの論理構成図を生成する（AI生成）
trigger: model_decision
---

# 🧩 Visualize Architecture (Draw.io)

このワークフローは、リポジトリ内容を解析し、アーキテクチャ図（Draw.io形式）を生成・保存します。

## Step 1: 🔎 プロジェクトの解析 // turbo
   - `list_dir` や `view_file` ツールを使用して、プロジェクトの構造、主要なファイル（README.md, package.json, main scripts等）を確認します。
   - アプリケーションの目的、主要なコンポーネント、データの流れ、依存関係を特定してください。
   - **重要**: 物理的なファイル構造ではなく、READMEやドキュメントから読み取れる**論理的な概念**（Mission Control, Factory, Brainなど）を優先します。

## Step 2: 🧱 Draw.io XMLの生成 // turbo
   - 解析した情報を基に、Draw.ioで読み込み可能なXMLテキストを生成します。
   - **デザイン要件 (Strict Requirements)**:
     - **言語**: **英語 (English)** で統一すること。
     - **スタイル**: **Mission Control**で対話形式での決定を基本とし、洗練されたプロフェッショナルな図にすること。
       - *配色*: ニュートラル＋アクセント1〜2色（例：slate/gray基調 + blue/redアクセント）
       - **グラデーション禁止 (Flat Design Only)**: フラットなデザインにすること。
     - **構成**:
       - **Block Diagram**: コンテナやSwimlaneを使用して明確な境界を示す。
       - **Flow**: データの流れを矢印で分かりやすく繋ぐ。
       - **Spacing (余白の美)**: 
         - **要素間は十分な余白（最低40px以上）を取ること。**
         - コンテナ内部のパディングも広めに取り、窮屈な印象を与えないこと。
         - 全体的にゆったりとした配置にすること。
     - **形式**: 完全で有効なXML形式（`<mxfile>`〜`</mxfile>`）。

## Step 3: 💾 保存 // turbo
   - 生成したXMLコンテンツを `docs/architecture.drawio` というファイル名で保存します。
     - ※ `docs` ディレクトリが存在しない場合は、ユーザーに作成を促すか、`write_to_file` で親ディレクトリ作成が可能ならそのまま保存します。
   - 保存完了後、ユーザーに通知します。

## Step 4: (Optional) SVGのエクスポートと埋め込み
   - 生成された `architecture.drawio` をDraw.ioで開き、スタイルを微調整した上で **SVG形式** としてエクスポート (`docs/architecture.svg`) することを推奨します。
   - SVG画像は `README.md` の Architecture セクションに埋め込むことで、視覚的なドキュメントとして機能します。
