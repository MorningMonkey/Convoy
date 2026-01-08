---
slug: build-app-flutter
description: "Flutterプロジェクトを標準構成（Riverpod/go_router）で生成し、SoT（assets/branding/<productId>/brief.md）に基づく前提をREADMEへ反映、品質最小ライン（pub get/analyze/test）を満たす"
trigger: "Flutterアプリの標準雛形を生成し、初期品質とディレクトリ標準を整える"
---

# 🐦 build-app-flutter

Convoyにおける **Flutter（iOS/Android）向けの標準プロジェクト骨格**を生成し、艦隊運用のための最小統一ルール（Riverpod / go_router / ディレクトリ標準 / 品質ゲート）まで整えます。

---

## Source of Truth（分岐の正本）

- `assets/branding/<productId>/brief.md` を唯一の正本とし、以下をそこから確定します。
  - 想定プラットフォーム（最優先含む）
  - 権限（カメラ / 位置情報 / 通知 など）
  - 取り扱いメディア（画像 / 動画 / 音声 など）
  - 主要ユースケース（画面の骨格に影響する）

> `brief.md` が無い場合は、先に `/branding-intake` を実行して生成してください。

---

## 標準スタック（固定）

- 状態管理: **Riverpod**（統一）
- ルーティング: **go_router**（統一）

---

## 最小ディレクトリ標準（固定）

- `lib/app/`：アプリ起動・ルーティング・テーマ
- `lib/features/`：機能単位（例: habits, aquarium, settings）
- `lib/shared/`：共通（widgets, utils, constants）
- `assets/`：画像/動画等（briefに準拠）
- `test/`：最低限のテストが走る状態を維持

---

## 成果物（期待出力）

- Flutterプロジェクト（`flutter create`）の生成
- 依存導入（Riverpod / go_router）
- `README.md` の Quick Start を **Flutter を正**として整備
- `walkthrough.md`（日本語）に、実行手順・判断根拠・生成物を記録

---

## 手順

### Step 0: brief.md を読み、前提を固定する
1. `assets/branding/<productId>/brief.md` を確認し、以下を抜き出してメモします。
   - 最優先プラットフォーム（iOS/Android）
   - 必要権限（例: Camera / Photos / Notifications）
   - メディア（動画を含むか、ストリーミングか）
   - 画面の最低限（例: Home / Aquarium / Settings）

2. `README.md` に反映すべき項目（権限・注意事項・対象OS）を確定します。

---

### Step 1: Flutterプロジェクト生成（雛形）
- 生成例（`<app_name>` は `productId` を推奨）:

```bash
flutter create <app_name>
cd <app_name>
```

- 既にリポジトリが存在し、配下にFlutterを入れる場合は `--project-name` 等の整合に注意します（CIとbundle idに影響）。

---

### Step 2: 依存導入（Riverpod / go_router）
以下を最低ラインとして導入します。

```bash
flutter pub add flutter_riverpod go_router
flutter pub get
```

> コード生成（riverpod_generator等）は「必要になった段階で」導入します。標準骨格ではまず依存を薄く保ちます。

---

### Step 3: ディレクトリ整備（標準構造に寄せる）
`lib/` を以下の形に整えます。

```
lib/
  app/
  features/
  shared/
  main.dart
```

- `lib/main.dart`：起動のみ（Appの注入）
- `lib/app/`：router / theme / app widget

---

### Step 4: 最小実装（go_router + Riverpod）
以下を最低限の骨格として作成します（例）。

- `lib/main.dart`
- `lib/app/app.dart`
- `lib/app/router.dart`
- `lib/features/home/home_page.dart`（最小1画面）

要件（最低限）:
- `MaterialApp.router` で `go_router` を有効化
- `ProviderScope` でRiverpodを有効化
- ルート `/` でホームが表示できる

---

### Step 5: assets/ の規約適用
- `assets/` 直下に無秩序に置かず、brief.md の構成に合わせて整理します。
  - 例: `assets/images/`, `assets/video/`
- `pubspec.yaml` の `flutter: assets:` へ登録します。

大容量ファイルがある場合:
- Git LFS の利用、もしくは取得方法（ダウンロード/ストリーミング）を `README.md` に明記します。

---

### Step 6: README.md（Quick Start を Flutter 正に）
`README.md` に、最低限以下を含めます。

- `flutter --version`（任意）
- `flutter pub get`
- `flutter run`（エミュレータ/実機の前提を添える）
- （推奨）`flutter test` / `flutter analyze`

また、`brief.md` 由来の前提を README に転記します。
- 対象プラットフォーム（最優先含む）
- 必要権限（iOS/Androidの注意事項）
- 動画/音声などの扱い（ストレージ容量・ネットワーク前提）

---

### Step 7: test/（最低限のテストを通す）
- `flutter test` が通る状態を維持します（内容が薄くても可）。
- 例: ルーティングの初期画面がビルドできる程度の smoke test を1本。

---

### Step 8: ローカル品質ゲート確認（最小ライン）
以下が通ることを確認します。

```bash
flutter pub get
flutter analyze
flutter test
```

---

### Step 9: CIテンプレ導入（推奨）
アプリrepoの `.github/workflows/` に、ConvoyのCIテンプレをコピーして導入します。

- 品質ゲート（Ubuntu）: `.agent/templates/ci/flutter-quality-gates.yml`
- iOSビルド（macOS/手動・タグ起動）: `.agent/templates/ci/ios-build.yml`

導入後、PRで `flutter-quality-gates` が回り、必要時のみ `ios-build/*` タグ or 手動でiOSビルドを回します（署名はローカルMac運用）。

---

## walkthrough.md（日本語）に残す内容（必須）

- 実行したコマンド
- `brief.md` から採用した前提（プラットフォーム/権限/メディア）
- 生成・更新したファイル一覧
- 次にやるべきこと（例: 画面追加、権限実装、CI導入）