---
slug: "agent-index"
description: "Convoy（Mission Control）の .agent/ 資産を単一の入口として整理し、参照SoTと推奨導線を固定する。"
trigger: "manual"
---

# 🧭 .agent/INDEX — Mission Control Entry Point

## 🌌 Overview
本ファイルは、Convoy（Mission Control）配下の `.agent/` 資産を一覧化し、運用の入口として
「参照SoT」「実行導線」「成果物の所在」を固定するインデックスである。
個別ワークフローの増減や自動生成テーブルの更新があっても、運用者とエージェントが迷わない参照点として機能させる。

## ⚖️ Rules / Constraints
- **SoT（上位契約）**: 管制仕様は `ANTIGRAVITY_AGENT_CONTROL_SPEC.md` を正本とする。
- **SoT（生成先）**: リポジトリ生成先は `workspace.config.json` の `paths.projectFactoryDir` を正本とする（推奨: `CONVOY_PROJECT`）。
- **SoT（資産の所在）**: Rules/Workflows/Templates は `.agent/` 配下に置く。
- **自動生成領域の不変**: `BEGIN: AUTO-GENERATED` 〜 `END: AUTO-GENERATED` の範囲は手編集しない（生成スクリプトで更新する）。
- **Frontmatter 規律**: Workflows/Rules の frontmatter は `slug` を kebab-case、`description` は必ず二重引用符、`trigger` は `model_decision` または `manual`。
- **テーブル整合性**: Workflows テーブルは必ず 4 列（`slug/description/trigger/file`）、Rules テーブルは 3 列（`slug/description/file`）を維持する。
- **参照の一貫性**: README 等から運用導線へ到達できるよう、リンク切れを許容しない。

## 🚀 Workflow / SOP

### Step 1: Index の整合性チェック（Decision）
1. Rules / Templates / Workflows の各テーブルが期待列数で構成されているか確認する。
2. `trigger` 列が `manual` または `model_decision` になっているか確認する（説明文が誤って混入していないか）。
3. Templates の file パスが `.agent/templates/` 配下へ統一されているか確認する。

**出力**
- 検出事項（Pass / Risk / Action の形式で列挙）
- 直すべき行（slug単位）と修正方針

### Step 2: 自動生成テーブルの更新（Action）
1. 生成スクリプト（例: `scripts/generate_agent_index.py`）を実行し、AUTO-GENERATED 範囲を再生成する。
2. `scripts/validate_agent_markdown.py` 等で frontmatter と整合性を検証する。

**出力**
- 更新後の `.agent/INDEX.md`
- 検証結果（OK / NG と理由）

### Step 3: 推奨導線の確認（Decision）
1. 推奨導線（Project Complete）が現在の運用意図と一致しているか確認する。
2. 追加/廃止したワークフローがある場合、入口の「推奨フロー」「よくある使い分け」を最小差分で更新する。

**出力**
- 推奨導線（確定）
- 変更点（差分要約）

### Step 4: コミット（任意 / Action）
1. 変更が妥当ならコミットする（可能なら `chore:` で統一）。
2. 自動生成部分のみの更新か、導線（本文）も更新したかをコミットメッセージに明記する。

**出力**
- コミットハッシュ（任意）
- 変更ファイル一覧

## ✅ Checklist
- [ ] AUTO-GENERATED 範囲が手編集されておらず、生成スクリプト由来の更新になっている
- [ ] Workflows テーブルの `trigger` が `manual/model_decision` に揃い、列崩れが無い
- [ ] SoT（上位契約/生成先/資産所在）が本文から一意に辿れる
- [ ] 推奨導線の入口が `/create-convoy-project-complete` で固定され、リンク切れが無い

---

## Rules

<!-- BEGIN: AUTO-GENERATED RULES -->
| slug | description | file |
| --- | --- | --- |
| agent-frontmatter | Agent 資産の Frontmatter 仕様（必須キー、slug 形式、description のクオート）を定義・検証する。 | .agent/rules/agent-frontmatter.md |
| repo-creation | Convoy（Mission Control）における新規リポジトリ作成・既存フォルダのリポジトリ化を、統一手順で強制・自動実行する。 | .agent/rules/repo-creation.md |
<!-- END: AUTO-GENERATED RULES -->

---

## Templates

| name                         | description                                                                  | file                                          |
| ---------------------------- | ---------------------------------------------------------------------------- | --------------------------------------------- |
| release_notes_template.md    | GitHub Release 用のリリースノートテンプレート（変数埋め込み式）              | .agent/templates/release_notes_template.md    |
| release_notes_template_ja.md | GitHub Release 用のリリースノートテンプレート（変数埋め込み式）              | .agent/templates/release_notes_template_ja.md |
| flutter-quality-gates.yml    | Flutter用CI（Ubuntu）: pub get → analyze → test を実行する品質ゲートテンプレ | .agent/templates/ci/flutter-quality-gates.yml |
| ios-build.yml                | iOSビルド（macOS）: 手動/タグ等でのみ実行するビルドテンプレ（no-codesign）   | .agent/templates/ci/ios-build.yml             |

> Templates は frontmatter を持たず、本文コメント（変数契約）で運用する。

---

## Workflows

<!-- BEGIN: AUTO-GENERATED WORKFLOWS -->
| slug | description | trigger | file |
| --- | --- | --- | --- |
| branding-intake | 製作者への対話的ヒアリングを通じてアプリ別のブランド要件（brief.md / header_prompt.txt）を定義・生成する。 | manual | .agent/workflows/branding-intake.md |
| build-app-flutter | Flutter プロジェクトを標準構成（Riverpod/go_router）で生成し、ブランド正本に基づき品質最小ラインを確保する。 | manual | .agent/workflows/build-app-flutter.md |
| build-app-simple | シンプルな Web アプリを迅速に構築するための技術選定基準と実装手順を定義する。 | model_decision | .agent/workflows/build-app-simple.md |
| create-convoy-project-complete | リポジトリ作成から品質レビュー、リリースまでを Convoy 標準の一気通貫導線で実行する統合 SOP。 | model_decision | .agent/workflows/create-convoy-project-complete.md |
| create-prompt-repo | プロンプト資産を別リポジトリとして管理するため、既存フォルダをGitHubリポジトリへ変換・同期する。 | model_decision | .agent/workflows/create-prompt-repo.md |
| create-release | Semantic Versioning に基づくリリース作成と、バージョン入りヘッダー画像の生成を自動化する。 | model_decision | .agent/workflows/create-release.md |
| create-repo-from-folder | 既存フォルダをConvoy規格のGitHubリポジトリへ整流化し、Private作成・origin検証・main標準化までを完了する。 | model_decision | .agent/workflows/create-repo-from-folder.md |
| generate-header-image | READMEおよびリリース向けのヘッダー画像を生成し、1600x420の規格へクロップして成果物を固定する。 | model_decision | .agent/workflows/generate-header-image.md |
| git-auto-commit | git statusとdiffを根拠に、Convoy標準の作業ブランチ作成・粒度の細かいコミット・マージまでを安全に自動化する。 | model_decision | .agent/workflows/git-auto-commit.md |
| projects-sync | Convoy母艦の manifest を正として、CONVOY_PROJECT 配下の独立プロダクト群を clone/pull で同期する。新規プロダクト追加はGitHub ActionsでPR自動生成する。 | manual | .agent/workflows/projects-sync.md |
| review-repo-quality | リポジトリのREADME・設定・構造・実行ゲートを点検し、Pass/Risk/Actionで出荷可否と改善手順を提示する。 | model_decision | .agent/workflows/review-repo-quality.md |
| update-convoy-identity | READMEとヘッダー画像、Alertsと導線をConvoy標準へ整流化し、初見理解と運用到達性を確立する。 | model_decision | .agent/workflows/update-convoy-identity.md |
| visualize-architecture | リポジトリの論理構成を解析し、Draw.io XMLでアーキテクチャ図を生成してdocs/へ保存する。 | model_decision | .agent/workflows/visualize-architecture.md |
<!-- END: AUTO-GENERATED WORKFLOWS -->

---

## 推奨フロー（Project Complete）
入口は **`/create-convoy-project-complete`** で固定する。

- 必須: `create-repo-from-folder` →（必要なら）`build-app-simple` / `build-app-flutter` →（必要なら）`branding-intake` → `update-convoy-identity` → `review-repo-quality`
- 任意: `visualize-architecture` / `git-auto-commit` / `create-release` / `create-prompt-repo`

---

## よくある使い分け
- **素早くUIを作る（単体Web）**: `build-app-simple`（Vanilla基本、React+Tailwind可）
- **モバイル（Flutter）を作る**: `build-app-flutter`（Riverpod + go_router）
- **ヘッダー画像だけ作る**: `generate-header-image`
- **既存フォルダをConvoy管理にする**: `create-repo-from-folder` → `update-convoy-identity` → `review-repo-quality`

---

## 運用ルール（最低限）
- **モバイルは Flutter 推奨。スタックとビルド環境（iOSはmacOS）は `assets/branding/<productId>/brief.md` を正とする。**
- Workflows は必ず frontmatter（`slug/description/trigger`）を持つ。
- `description` は原則二重引用符でクオートする（YAMLパース事故防止）。
- 結果報告（walkthrough.md 等）は日本語を正とし、「完了内容 / 生成・更新ファイル / 次のアクション」を含める。
