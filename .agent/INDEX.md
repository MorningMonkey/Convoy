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

---

## 🧩 開発ライフサイクル（企画→実装→リリースの標準順序）
Convoy におけるプロダクト開発は、原則として以下の順序で進行する（“順序”がSoT。実行可否は Workflows の存在に従う）。

### Phase 1: Inception & Discovery（企画・設計）
目的: **何を作るか**（価値・範囲・体験・データ）を確定し、実装の迷いを潰す。

- `/branding-intake`（コンセプト／ブランド要件の確定。成果物: `assets/branding/<productId>/brief.md` 等）
- `/setup-product-discovery`（設計成果物の置き場を標準化：`docs/products/<productId>/{Docs,Decisions}`）
- `/parallel-discovery-antigravity`（UI / Data / CI の 3 エージェントで並列棚卸し）
- `/integrate-discovery-artifacts`（矛盾解消→Convoy標準ドキュメントへ統合）

### Phase 2: Project Setup（プロジェクト立ち上げ）
目的: **開発対象（リポジトリ／工場／資産分離）** を用意する。

- `/projects-sync`（manifest 正の同期・準備）
- `/create-repo-from-folder`（既存フォルダのリポジトリ化・標準化）
- `/create-prompt-repo`（必要時のみ：プロンプト資産の分離）

### Phase 3: Implementation（実装）
目的: **仕様（Phase 1 成果物）に基づき、骨格を作って動かす**。

- `/build-app-flutter`（Flutter 標準骨格：Riverpod / go_router）
- `/build-app-simple`（Web で素早く構築するパス）

### Phase 4: Development & Quality（開発・品質維持）
目的: **日々の変更を安全に積み上げ、品質を落とさない**。

- `/git-auto-commit`（差分根拠で適切な粒度のコミット）
- `/visualize-architecture`（現状可視化：図の自動生成）
- `/review-repo-quality`（README/CI/構造の健康診断）
- `/update-convoy-identity`（README/画像/導線の整流化）

### Phase 5: Release（リリース）
目的: **公開可能な形に整えて出荷**。

- `/generate-header-image`（ストア／SNS／README 用のヘッダー画像生成）
- `/create-release`（SemVer 付与→Release 作成）

### Special: Integrated Flow（統合）
- `/create-convoy-project-complete`（上記のプロセス（作成〜リリース）を一気通貫で実行する統合ワークフロー。慣れてきたらこれ一本で管理可能）

---

## ⚖️ Rules / Constraints
- **SoT（上位契約）**: 管制仕様は `ANTIGRAVITY_AGENT_CONTROL_SPEC.md` を正本とする。
- **SoT（生成先）**: リポジトリ生成先は `workspace.config.json` の `paths.projectFactoryDir` を正本とする（推奨: `CONVOY_PROJECT`）。
- **SoT（資産の所在）**: Rules/Workflows/Templates は `.agent/` 配下に置く。
- **自動生成領域の不変**: `BEGIN: AUTO-GENERATED` 〜 `END: AUTO-GENERATED` の範囲は手編集しない（生成スクリプトで更新する）。
- **Frontmatter 規律**: Workflows/Rules の frontmatter は `slug` を kebab-case、`description` は必ず二重引用符、`trigger` は `model_decision` または `manual`。
- **テーブル整合性**: Workflows テーブルは必ず 4 列（`slug/description/trigger/file`）、Rules テーブルは 3 列（`slug/description/file`）を維持する。
- **参照の一貫性**: README 等から運用導線へ到達できるよう、リンク切れを許容しない。

---

## Rules

<!-- BEGIN: AUTO-GENERATED RULES -->
| slug | description | file |
| --- | --- | --- |
| agent-frontmatter | Agent 資産の Frontmatter 仕様（必須キー、slug 形式、description のクオート）を定義・検証する。 | .agent/rules/agent-frontmatter.md |
| code-review | コードレビュー、PRレビュー、コードの品質チェックを求められた場合に適用する。 | .agent/rules/code-review.md |
| command-rules | コマンドの連結実行（&&, ;）を禁止し、1ステップごとの確実な実行と結果確認を義務付けるルール。 | .agent/rules/command-rules.md |
| documentation | ドキュメント作成、README更新、API仕様書、技術文書について言及された場合に適用する。 | .agent/rules/documentation.md |
| japanese-rule | エージェントの思考・計画・応答・コミットメッセージなど、全ての出力を日本語に統一するルール。 | .agent/rules/japanese-rule.md |
| meta-rule-creation | 新しいルールの作成、ルールファイルの設計、エージェント制約の定義について言及された場合に適用する。 | .agent/rules/meta-rule-creation.md |
| meta-workflow-creation | 新しいワークフローの作成、タスク自動化の設計、作業手順書の定義について言及された場合に適用する。 | .agent/rules/meta-workflow-creation.md |
| ops | ビルド、テスト、デプロイ、運用に関する質問や作業を行う場合に適用する。 | .agent/rules/ops.md |
| repo-creation | Convoy（Mission Control）における新規リポジトリ作成・既存フォルダのリポジトリ化を、統一手順で強制・自動実行する。 | .agent/rules/repo-creation.md |
| security-mandates | シークレット管理、危険な関数の禁止、入力検証、出力エンコーディングなど、コード実装における必須セキュリティ基準を定義する。 | .agent/rules/security-mandates.md |
| testing-standards | テストの作成、テスト戦略、テストカバレッジについて言及された場合に適用する。 | .agent/rules/testing-standards.md |
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
| define-state-machines | アプリのコアロジックを解析し、Mermaidステートマシン図とUIマッピング図を生成して整合性を担保する。 | manual | .agent/workflows/define-state-machines.md |
| generate-header-image | READMEおよびリリース向けのヘッダー画像を生成し、1600x420の規格へクロップして成果物を固定する。 | model_decision | .agent/workflows/generate-header-image.md |
| git-auto-commit | git statusとdiffを根拠に、Convoy標準の作業ブランチ作成・粒度の細かいコミット・マージまでを安全に自動化する。 | model_decision | .agent/workflows/git-auto-commit.md |
| integrate-discovery-artifacts | AntigravityのUI/Data/CI Artifactsをレビューし、衝突解消→Convoy docsへ収束→ADRで決定ログ化する統合SOP。 | manual | .agent/workflows/integrate-discovery-artifacts.md |
| parallel-discovery-antigravity | Antigravity Managerで UI/データ/CI の3エージェントを並列稼働し、ArtifactsをConvoyの正本ドキュメント（docs/products/<productId>/）へ収束させる。 | manual | .agent/workflows/parallel-discovery-antigravity.md |
| projects-sync | Convoy母艦の manifest を正として、CONVOY_PROJECT 配下の独立プロダクト群を clone/pull で同期する。新規プロダクト追加はGitHub ActionsでPR自動生成する。 | manual | .agent/workflows/projects-sync.md |
| review-repo-quality | リポジトリのREADME・設定・構造・実行ゲートを点検し、Pass/Risk/Actionで出荷可否と改善手順を提示する。 | model_decision | .agent/workflows/review-repo-quality.md |
| setup-product-discovery | Convoy内でプロダクトの棚卸し→MVP決定→設計を回すための成果物置き場（SoT/Docs/Decisions）を標準生成する。 | manual | .agent/workflows/setup-product-discovery.md |
| update-convoy-identity | READMEとヘッダー画像、Alertsと導線をConvoy標準へ整流化し、初見理解と運用到達性を確立する。 | model_decision | .agent/workflows/update-convoy-identity.md |
| visualize-architecture | リポジトリの論理構成を解析し、Draw.io XMLでアーキテクチャ図を生成してdocs/へ保存する。 | model_decision | .agent/workflows/visualize-architecture.md |
<!-- END: AUTO-GENERATED WORKFLOWS -->

---

## 推奨フロー（導入：Discovery起点）
初期導入は **`/branding-intake`** を先頭とする。

- 標準（推奨）: `branding-intake` → `setup-product-discovery` → `parallel-discovery-antigravity` → `integrate-discovery-artifacts` → `build-app-flutter / build-app-simple`
- 既存フォルダから開始: `create-repo-from-folder` →（必要なら）`update-convoy-identity` → `review-repo-quality` → `create-release`
- 慣れてきたら（統合版）: `create-convoy-project-complete`（作成〜リリースまで一気通貫）

---

## よくある使い分け
- **企画・設計を詰める**: `branding-intake` → `setup-product-discovery` → `parallel-discovery-antigravity` → `integrate-discovery-artifacts`
- **素早くUIを作る（単体Web）**: `build-app-simple`（Vanilla基本、React+Tailwind可）
- **モバイル（Flutter）**: `build-app-flutter`（Riverpod + go_router）
- **ヘッダー画像だけ作る**: `generate-header-image`
- **既存フォルダをConvoy管理にする**: `create-repo-from-folder` → `update-convoy-identity` → `review-repo-quality`

---

## 運用ルール（最低限）
- **モバイルは Flutter 推奨。スタックとビルド環境（iOSはmacOS）は `assets/branding/<productId>/brief.md` を正とする。**
- Workflows は必ず frontmatter（`slug/description/trigger`）を持つ。
- `description` は原則二重引用符でクオートする（YAMLパース事故防止）。
- 結果報告（walkthrough.md 等）は日本語を正とし、「完了内容 / 生成・更新ファイル / 次のアクション」を含める。
