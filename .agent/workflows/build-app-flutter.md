---
slug: "build-app-flutter"
description: "Flutter プロジェクトを標準構成（Riverpod/go_router）で生成し、ブランド正本に基づき品質最小ラインを確保する。"
trigger: "manual"
---
# 🐦 Flutter Application Build Policy & SOP

## 🌌 Overview
本ワークフローは、Convoy 傘下における Flutter プロジェクトの骨格定義です。

単なるコード生成にとどまらず、状態管理・ルーティング・ディレクトリ構造を厳格に固定することで、複数のプロジェクトを一つの「艦隊」として捉え、運用保守性を最大化することを目的とします。

## ⚖️ Rules / Constraints
エージェントは、Flutter アプリ構築において以下の制約を「憲法」として厳守しなければなりません。

- **技術スタックの固定**: 状態管理には **Riverpod**、ルーティングには **go_router** を必ず使用すること。代替手段の採用は Commander（ユーザー）の明示的な許可がない限り禁止する。
- **SoT の遵守**: `assets/branding/<productId>/brief.md` を唯一の正本（Source of Truth）とし、権限設定やプラットフォーム優先順位を決定すること。
- **ディレクトリ構造の強制**: `lib/` 配下は `app/`, `features/`, `shared/` に分割し、無秩序な配置を厳禁とする。
- **品質の最低ライン**: `flutter analyze` および `flutter test` が警告なしで正常に通過する状態で納品すること。
- **アセット管理**: 画像や動画資産は `brief.md` の指示に従い、`assets/` 内で論理的にフォルダ分けを行うこと。

## 🚀 Workflow / SOP
エージェントは以下の手順に従い、標準化された Flutter 環境を自律的に構築します。

### Step 1: 要件の同期（Sync with Brief）
`assets/branding/<productId>/brief.md` から、最優先プラットフォーム、必要権限（カメラ、位置情報等）、およびメディア特性を抽出します。抽出した条件に基づき、プロジェクト固有の `README.md` 構成案を策定します。

### Step 2: 雛形の生成と依存関係の導入
`flutter create` を実行してプロジェクトを生成し、コアパッケージを導入します。
- `flutter pub add flutter_riverpod go_router`
その後、標準ディレクトリ（`app/`, `features/`, `shared/`）を作成し、`main.dart` を起動処理専用のコードへと整流化します。

### Step 3: 基盤実装（Routing & State）
`MaterialApp.router` を用い、`go_router` による画面遷移基盤を実装します。アプリケーション全体を `ProviderScope` で包み、Riverpod を即座に利用可能な状態にします。最後に、ホーム画面（`/`）の最小実装を行い、ビルドが正常に通ることを確認します。

### Step 4: 仕上げと品質検証
`README.md` を「Flutter 実装が正」となるよう更新し、環境構築手順を日本語で明文化します。必要に応じて GitHub Actions 用の CI テンプレートを導入し、`analyze` および `test` を実行して品質ゲートを通過させます。

## ✅ Checklist
エージェントは最終出力の前に、以下の項目が満たされているか自己検閲してください。

- [ ] `brief.md` で定義されたブランドカラーや権限設定がコードに反映されているか？
- [ ] 状態管理に Riverpod、ルーティングに go_router が正しく組み込まれているか？
- [ ] `lib/` のディレクトリ構造は Convoy 標準（app/features/shared）に準拠しているか？
- [ ] `walkthrough.md` に日本語で実行根拠と生成ファイルの一覧が記録されているか？

