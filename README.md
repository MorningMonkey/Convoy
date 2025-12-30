<div align="center">

<img src="assets/header_cropped_text.png" alt="Header" width="100%" />

# Convoy
### Your Own Repository Organization Zero-gravity Utility

<p align="center">
  <img src="https://img.shields.io/badge/Agent-Google%20Antigravity-blue?style=for-the-badge&logo=google" alt="Agent">
  <img src="https://img.shields.io/badge/Status-Active-success?style=for-the-badge&logo=activitypub" alt="Status">
  <img src="https://img.shields.io/badge/Platform-Windows-0078D6?style=for-the-badge&logo=windows" alt="Platform">
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License">
</p>

**Google Antigravity エージェントと協働するための「エージェント主導開発（ADE）」ワークスペース（Mission Control）**

[コンセプト](#concept) • [はじめ方](#getting-started) • [ワークフロー一覧](#workflow-catalog) • [仕様](#spec)

</div>

---

## Concept

**Convoy（司令塔 / Mission Control）** は単なるリポジトリ管理ツールではありません。  
これは、**「反復作業の重力」から開発者を解放するための、Google Antigravity 専用の管制塔**です。

従来の開発環境が「コードを書く場所」だったのに対し、Convoy は「エージェントにタスクを委任し、指揮する場所」として設計されています。  
Convoy 管理下で生成・運用されるリポジトリは、ここで定義された **Rules（憲法）** と **Workflows（標準作業手順）** により、統一された品質基準で管理されます。

### Core Philosophy

- **Automate Everything**: 初期化、コミット、リリース、品質チェックまで、あらゆるプロセスを Workflow として定義。
- **Agent First**: 人間だけでなく、AIエージェントが理解・実行しやすい構造と契約（frontmatter/出力物/導線）を徹底。
- **Mission Control Branding**: 機能性（UX）に加えて、プロダクトの共通認識（Branding）を **Workflows により自動注入**。

---

## Getting Started

このワークスペースでは **スラッシュコマンド（/）** を使用してエージェントに指示を出します。  
複雑なプロンプト設計を前提にせず、定義済み Workflow を呼び出すことで、標準化された手順が実行されます。

### Source of Truth（重要）

生成先ディレクトリは **`workspace.config.json` の `paths.projectFactoryDir`** が唯一の基準です。  
推奨既定値: `CONVOY_PROJECT`

### 基本コマンド

| コマンド | 説明 |
| :--- | :--- |
| **`/create-convoy-project-complete`** | リポジトリ作成から Identity 注入、初期コミット、（必要なら）初回リリースまでを一気通貫で実行。 |
| **`/build-app-simple`** | 小〜中規模のWebアプリを最短で実装（Vanilla を基本に、必要に応じて React + Tailwind も可）。 |
| **`/create-release`** | 変更差分を解析し、リリースノートを生成して GitHub Release を作成。 |

---

## Architecture

Convoy は、複数プロジェクトを統括する **メタ・ワークスペース**として機能します。

- 図: `docs/architecture.drawio`（必要に応じて `/visualize-architecture` で生成/更新）

```text
<workspace-root>/                     <-- 🛰️ Mission Control (Current)
├── .agent/                           <-- 🧠 Agent Brain
│   ├── rules/                        <-- 憲法 (Standards / Policies)
│   ├── templates/                    <-- フォーマット規格（Release Notes等）
│   ├── workflows/                    <-- 標準手順書（SOP）
│   └── INDEX.md                      <-- 入口（一覧と推奨導線）
│
├── <paths.projectFactoryDir>/        <-- 🏭 Project Factory（例: CONVOY_PROJECT）
│   ├── my-cool-project/              <-- 📦 Generated Repo 1
│   ├── another-service/              <-- 📦 Generated Repo 2
│   └── prompt-repo/                  <-- 📦 Prompt Management
│
└── docs/                             <-- 📚 Docs（任意）
```

---

## Workflow Catalog

利用可能な Workflows（標準作業手順書）の一覧です。  
詳細は **[.agent/INDEX.md](.agent/INDEX.md)** を参照してください（推奨導線を含む）。

### Project Creation（作成）
- **[Create Convoy Project Complete](.agent/workflows/create-convoy-project-complete.md)**: プロジェクト立ち上げの決定版。
- **[Create Repo from Folder](.agent/workflows/create-repo-from-folder.md)**: 既存フォルダのリポジトリ化。
- **[Create Prompt Repo](.agent/workflows/create-prompt-repo.md)**: プロンプト管理専用リポジトリの作成。

### Development（開発）
- **[Build App Simple](.agent/workflows/build-app-simple.md)**: 高速なプロトタイプ・アプリ開発。
- **[Git Auto Commit](.agent/workflows/git-auto-commit.md)**: 粒度の細かいコミットとブランチ管理の自動化。

### Branding & Assets（意匠）
- **[Update Convoy Identity](.agent/workflows/update-convoy-identity.md)**: README/ヘッダー/Alerts/導線の整流化。
- **[Generate Header Image](.agent/workflows/generate-header-image.md)**: README/記事用のヘッダー画像生成（Mission Control スタイル）。

### Quality & Release（品質・公開）
- **[Review Repo Quality](.agent/workflows/review-repo-quality.md)**: リポジトリの健康診断と改善提案（Pass/Risk/Action）。
- **[Create Release](.agent/workflows/create-release.md)**: バージョニングとリリースノート生成。
- **[Visualize Architecture](.agent/workflows/visualize-architecture.md)**: Draw.io XML で論理構成図を生成。

---

## Rules & Policies

エージェントは `.agent/rules/` の Rules に従って自律的に判断します。

- **Repo Creation Rule**: 生成先は `workspace.config.json`（`paths.projectFactoryDir`）を基準とし、multi-repo 前提で独立 `.git` を維持。
- **Mission Control Style**: ニュートラル基調 + 1〜2アクセント、フラット、可読性重視（過度な装飾は禁止）。
- **Safety First**: 破壊的操作や誤接続（origin など）を避けるため、必要な検証・注意喚起を優先。

---

## Spec

- エージェント仕様書（存在する場合）:
  - `CONVOY_AGENT_CONTROL_SPEC.MD`（推奨）
  - 互換: `ANTIGRAVITY_AGENT_CONTROL_SPEC.MD`（移行中は併存可）

---

<div align="center">

Empowered by Google Antigravity & ADE

</div>