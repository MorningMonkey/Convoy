---
slug: "review-repo-quality"
description: "リポジトリのREADME・設定・構造・実行ゲートを点検し、Pass/Risk/Actionで出荷可否と改善手順を提示する。"
trigger: "model_decision"
---
# ✅ review-repo-quality

## 🌌 Overview
本ワークフローは、現在のリポジトリが Convoy の最小品質ラインを満たしているかを点検し、
出荷判断を **Pass / Risk / Action** で確定する。
Web/React と Mobile/Flutter の両基準を維持し、リポジトリの実態に応じて評価観点を切り替える。

## ⚖️ Rules / Constraints
- **スタック二重基準**: Web/React と Flutter の両基準を保持し、検出結果に基づき評価観点を切り替える。
- **スタック識別のSoT**: 判定はリポジトリ内の事実（`pubspec.yaml`、`android/`・`ios/`、README の記載）に基づく。推測で決めない。
- **Convoy導線の必須**: `.agent/`（rules/templates/workflows）が存在し、README から運用手順へ到達できることを必須とする。
- **機密の排除**: `.env` 等の機密ファイル、APIキー等のハードコードが存在する場合は即 Risk とし、修正を Action 化する。
- **一時ファイル混入禁止**: `COMMIT_MSG.txt` や生成物が追跡されている場合は Risk とし、除外または削除を Action 化する。
- **配置のSoT**: リポジトリは `workspace.config.json` の `paths.projectFactoryDir` 配下（multi-repo 前提）であることを確認する。
- **実行ゲートの最小要件**:
  - Flutter: `flutter pub get` / `flutter analyze` / `flutter test` が失敗しないこと
  - Web/React: README に準拠して `install` / `lint` / `test` / `build` の最低限が通ること（可能な範囲ではなく、原則として確認する）
- **出力形式の固定**: 結果は必ず **Pass / Risk / Action** の3区分で整理し、Action は最短で改善できる順に並べる。

## 🚀 Workflow / SOP

### Step 1: スタック識別（Decision）
1. 次の条件で Flutter を推定する（複数該当可）。
   - ルートに `pubspec.yaml`
   - `android/` と `ios/` が存在
   - README に `flutter` コマンドが明記
2. いずれも該当しない場合は Web/React を主として評価する。

**出力**
- 判定スタック（Flutter / Web/React）
- 判定根拠（該当条件の列挙）

---

### Step 2: docs check（README導線の品質）
#### 2-A: 共通（全リポジトリ）
1. ルートに `README.md` が存在することを確認する。
2. README の必須要素を点検する。
   - ヘッダー画像（タイトルより上）
   - 中央揃えタイトル（または同等の視認性）
   - Convoy標準の導線（`.agent/` の存在と、README から運用へ辿れること）
   - 概要、インストール手順、使用方法
   - 長文の場合は目次
3. `examples/` 等のサブフォルダがある場合、配下の README を点検する。

#### 2-B: Flutter（追加）
- Quick Start が Flutter 前提になっていること
  - `flutter pub get`
  - `flutter run`（実機/エミュレータ前提の注記があると望ましい）
  - 推奨: `flutter analyze` / `flutter test`
- SoT 参照: `assets/branding/<productId>/brief.md` が存在する場合、README が参照し、前提（プラットフォーム/権限/動画等）が反映されていること

#### 2-C: Web/React（追加）
- Quick Start が `npm install` / `pnpm i` / `npm run dev` 等で成立していること
- 推奨: `lint` / `test` / `build` の導線が明記されていること

**出力**
- docs での Pass/Risk/Action（README不足・導線切れ・手順不備の特定）
- README の修正案（追記すべき見出し・最小テキスト案）

---

### Step 3: config check（除外・機密・一時ファイル）
1. `.gitignore` の存在と内容を点検する（`.env` 等が除外されていること）。
2. コード内に API キー等のハードコードが無いか簡易チェックする。
3. `COMMIT_MSG.txt` や生成物がコミットされていないか確認する。

**出力**
- config での Pass/Risk/Action
- 修正コマンド案（例: `.gitignore` 追記、追跡解除、秘密情報のローテーション手順）

---

### Step 4: structure check（配置・命名・スタック標準）
#### 4-A: 共通（Convoy）
1. リポジトリが `paths.projectFactoryDir` 配下にあるか確認する。
2. multi-repo 前提（各プロジェクトが独立 `.git`）に反していないか確認する。
3. 命名規則が概ね `kebab-case`（または言語規則）に従っているか点検する。

#### 4-B: Flutter（追加）
- 最小ディレクトリ標準に概ね沿っているかを確認する（厳密一致は不要、逸脱時は理由を要求）。
  - `lib/app/`（起動・ルーティング・テーマ）
  - `lib/features/`（機能単位）
  - `lib/shared/`（共通）
  - `assets/`（`pubspec.yaml` の assets 宣言がある）
  - `test/`（少なくとも `flutter test` が失敗しない）
- 大容量アセットの方針があるか確認する（無方針で巨大ファイル直コミットは Risk）。

#### 4-C: Web/React（追加）
- 構造が論理的か（例: `src/`, `tests/`, `docs/` の分離）を点検する。

**出力**
- structure での Pass/Risk/Action
- 具体的な再配置案（ディレクトリ提案、命名修正の優先順位）

---

### Step 5: quality gates（実行確認）
#### 5-A: Flutter（最低限）
- `flutter pub get`
- `flutter analyze`
- `flutter test`（空でも可。ただし `flutter test` 自体が失敗しないこと）

#### 5-B: Web/React（最低限）
- README に準拠して `install` / `lint` / `test` / `build` の最低限を実行し、結果を記録する。

**出力**
- 実行したコマンド一覧
- 成否（失敗時はエラー要約と一次原因）
- 再現手順（同じ失敗を再現できる最小コマンド）

---

### Step 6: report（出荷判断）
1. 全ステップの結果を統合し、**Pass / Risk / Action** で整理する。
2. Risk は必ず Action 化し、最短で改善できる順に並べる。
3. Action には「どこを、何を、どう直すか」を具体化する（ファイルパス、見出し、コマンド）。

**出力**
- Pass: 出荷要件を満たしている点
- Risk: 出荷を妨げる点（根拠付き）
- Action: 修正タスク（優先順位付き、最小手順）

## ✅ Checklist
- [ ] スタック識別（Flutter/Web）が根拠付きで確定し、評価観点が一致している
- [ ] README に Convoy 導線（`.agent/` への到達）があり、Quick Start が実行可能である
- [ ] 機密情報・一時ファイル・生成物の混入が無く、`.gitignore` が適切である
- [ ] 実行ゲート（Flutter または Web/React）が確認され、結果が Pass/Risk/Action に落ちている


