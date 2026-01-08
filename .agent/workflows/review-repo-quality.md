---
slug: review-repo-quality
description: "リポジトリの品質（README, 構造, 設定）をチェックし、Convoy標準（Agent First / Automate Everything）に沿って改善点を提案します"
trigger: model_decision
---

# ✅ リポジトリ品質レビュー

このワークフローは、現在のリポジトリが Convoy の最小品質ラインを満たしているか確認します。  
Web/React と モバイル/Flutter の **両基準を維持**し、対象スタックに応じて評価観点を切り替えます。

---

## 判定（スタック識別）

以下のいずれかで **Flutter と推定**します（複数該当でも可）。

- ルートに `pubspec.yaml` がある
- `android/` と `ios/` ディレクトリがある（Flutter生成物の典型）
- README に `flutter` コマンドが明記されている

上記に該当しない場合は **Web/React（既存基準）**を主として評価します。

---

## Step 1: 📝 docs check // turbo

### 1-A) 共通（全リポジトリ）
- **README.mdの存在確認**: ルートディレクトリに `README.md` があるか確認します。
- **READMEの品質チェック**: 以下の要素が含まれているか確認します。
  - **ヘッダー画像**: 最上部に配置されていること（タイトルより上）。
  - 中央揃えのタイトル
  - ステータスバッジ（任意）
  - **Convoy標準の導線**: `.agent/`（rules/templates/workflows）が存在し、README から運用手順へ辿れること
  - 概要、インストール手順、使用方法
  - 目次（長い場合）
- **ドキュメントの一貫性**: `examples/` などのサブフォルダがある場合、そこにもREADMEがあるか確認します。

### 1-B) Flutterの場合（追加チェック）
- **Quick Start が Flutter 正**になっていること
  - `flutter pub get`
  - `flutter run`（エミュレータ/実機など前提の記述があるとなお良い）
  - （推奨）`flutter analyze` / `flutter test`
- **SoT の参照**: `assets/branding/<productId>/brief.md` がある場合、README がそれを参照し、プラットフォーム/権限/動画等の前提が反映されていること

### 1-C) Web/Reactの場合（既存観点を維持）
- Quick Start に `npm install` / `pnpm i` / `npm run dev` 等の実行導線がある
- （推奨）lint/test/build の実行導線がある

---

## Step 2: ⚙️ config check
- **.gitignore**: 存在するか、および `.env` などの機密ファイルが除外されているか確認します。
- **機密情報**: コード内にAPIキーなどがハードコードされていないか簡易チェックします。
- **一時ファイル**: `COMMIT_MSG.txt` や生成物がコミットされていないか確認します。

---

## Step 3: 📂 structure check

### 3-A) 共通（Convoy）
- **配置場所（Convoy）**: リポジトリが `workspace.config.json` の `paths.projectFactoryDir` 配下にあり、multi-repo（各プロジェクトが独立 `.git`）前提に反していないか確認します。
- **命名規則**: ファイルやフォルダが `kebab-case`（または言語の規則）に従っているか確認します。

### 3-B) Flutterの場合（追加チェック）
- **最小ディレクトリ標準**に概ね沿う（厳密一致でなくて良いが、逸脱時は理由が必要）
  - `lib/app/`（起動・ルーティング・テーマ）
  - `lib/features/`（機能単位）
  - `lib/shared/`（共通）
  - `assets/`（brief準拠、`pubspec.yaml` の assets 宣言がある）
  - `test/`（少なくとも `flutter test` が通る）
- **大容量アセット**: 置き方に方針がある（Git LFS / ダウンロード手順 / ストリーミング等）。無方針で巨大ファイルが直コミットされている場合は Risk。

### 3-C) Web/Reactの場合（既存観点を維持）
- 構造が論理的か（`src/`, `tests/`, `docs/` などに分かれているか）確認します。

---

## Step 4: ✅ quality gates（実行確認）

### 4-A) Flutter（最低限）
- `flutter pub get` が通る
- `flutter analyze` が通る
- `flutter test` が通る（空でもOK、ただし `flutter test` 自体が失敗しないこと）

### 4-B) Web/React（既存基準）
- 可能なら `install` / `lint` / `test` / `build` の最低限が通る（リポジトリの README に準拠）

---

## Step 5: 📊 report
- 出力は **Pass / Risk / Action** の3区分で整理し、最短で改善できる順に並べます。
- チェック結果をまとめ、改善点（TODOリスト）をユーザーに提示します。
- 修正が必要な場合は、具体的な修正案やコマンドを提案します。
