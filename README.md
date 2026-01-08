<div align="center">

<img src="assets/header_cropped_text.png" alt="Header" />

# Convoy
### ～ Your Own Repository Organization Zero-gravity Utility ～


> Note: ヘッダー画像は `pnpm header:build` により README用バナー規格（1600×420）へ自動で固定されます。

<p align="center">
  <img src="https://img.shields.io/badge/Agent-Google%20Antigravity-blue?style=for-the-badge&logo=google" alt="Agent">
  <img src="https://img.shields.io/badge/Status-Active-success?style=for-the-badge&logo=activitypub" alt="Status">
  <img src="https://img.shields.io/badge/Platform-Windows-0078D6?style=for-the-badge&logo=windows" alt="Platform">
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License">
</p>

**Google Antigravity エージェントと協働するための、究極の「エージェント主導開発（ADE）」ワークスペース**

[コンセプトを読む](#concept) • [使い方](#getting-started) • [ワークフロー一覧](#workflow-catalog) • [管制仕様](ANTIGRAVITY_AGENT_CONTROL_SPEC.md)

</div>

---

## 🌌 Concept

**Convoy（司令塔）** は、単なるリポジトリ管理ツールではありません。
これは、**「反復作業の重力」から開発者を解放するための、Google Antigravity専用の管制塔（Mission Control）** です。

従来の開発環境が「コードを書く場所」であったのに対し、Convoyは「エージェントにタスクを委任し、指揮する場所」として設計されています。
`CONVOY_PROJECT` 配下に生成される全てのリポジトリは、ここで定義された **Rules（憲法）** と **Workflows（標準作業手順）** によって、統一された高品質な基準で管理されます。

### Core Philosophy
- **Automate Everything**: 初期化、コミット、リリース、品質チェックまで、あらゆるプロセスをWorkflowとして定義。
- **Agent First**: 人間が読みやすいだけでなく、AIエージェントが理解・実行しやすい構造を徹底。
- **Convoy Identity**: 機能性だけでなく、Mission Controlとしての統一感（Branding）を自動的に注入。

---

## 🚀 Getting Started

このワークスペースでは、**スラッシュコマンド（/）** を使用してエージェントに指示を出します。
複雑なプロンプトを考える必要はありません。定義済みのWorkflowを呼び出すだけで、熟練のエンジニアのような作業をエージェントが実行します。

### 基本的なコマンド

| コマンド                              | 説明                                                                                                       |
| :------------------------------------ | :--------------------------------------------------------------------------------------------------------- |
| **`/create-convoy-project-complete`** | 🆕 **最強のスターター**<br>リポジトリ作成からブランド化、初期コミット、リリースまでを一撃で完了します。     |
| **`/build-app-simple`**               | 🏗️ **アプリ実装**<br>要件を伝えるだけで、モダンで美しいWebアプリケーションを実装します。                    |
| **`/build-app-flutter`**              | 📱 **Flutter アプリ雛形**<br>Flutterプロジェクト生成、Riverpod / go_router 導入、README反映まで標準化します。 |
| **`/create-release`**                 | 📦 **リリース自動化**<br>変更差分を解析し、美しいリリースノートとヘッダー画像を生成してGitHubへ公開します。 |

---

## 📂 Architecture

Convoyは、複数のプロジェクトを統括する「メタ・ワークスペース」として機能します。

- 図（正本）: [docs/architecture.drawio](docs/architecture.drawio)
- （任意）表示用: `docs/architecture.svg`（drawio からエクスポートして併置可）

```text
d:/Prj/Convoy/            <-- 🛰️ Mission Control (Current)
├── .agent/                      <-- 🧠 Agent Brain
│   ├── rules/                   <-- 憲法 (Coding Standards, Branding Rules)
│   └── workflows/               <-- 手順書 (Deployment, Refactoring SOPs)
│
├── CONVOY_PROJECT/                 <-- 🏭 Project Factory
│   ├── my-cool-project/         <-- 📦 Generated Repo 1
│   ├── another-service/         <-- 📦 Generated Repo 2
│   └── prompt-repo/             <-- 📦 Prompt Management
│
└── ANTIGRAVITY_AGENT_CONTROL_SPEC.md <-- 📜 管制仕様（Control Spec）
```

- **Mission Control**: あなたはここで指令を出します。
- **Project Factory**: エージェントは `CONVOY_PROJECT` ディレクトリ内に成果物を生成します。
- **Agent Brain**: エージェントの行動指針は全て `.agent` 内に集約されており、ここを修正するだけで全プロジェクトの挙動を調整できます。

---

## 📚 Workflow Catalog

利用可能な全ワークフロー（標準作業手順書）の一覧です。

### 🏗️ Project Creation (作成)
- **[🚀 Create Convoy Project Complete](.agent/workflows/create-convoy-project-complete.md)**: プロジェクト立ち上げの決定版。
- **[📂 Create Repo from Folder](.agent/workflows/create-repo-from-folder.md)**: 既存フォルダのリポジトリ化。
- **[🧠 Create Prompt Repo](.agent/workflows/create-prompt-repo.md)**: プロンプト管理専用リポジトリの作成。

### 💻 Development (開発)
- **[🏗️ Build App Simple](.agent/workflows/build-app-simple.md)**: 高速なプロトタイプ・アプリ開発。
- **[📱 Build App Flutter](.agent/workflows/build-app-flutter.md)**: Flutterアプリ雛形の生成と初期品質の標準化。
- **[💾 Git Auto Commit](.agent/workflows/git-auto-commit.md)**: 粒度の細かいコミットとブランチ管理の自動化。

### 🎨 Branding & Assets (意匠)
- **[🌸 Update Convoy Identity](.agent/workflows/update-convoy-identity.md)**: 既存リポジトリを「Convoy」ブランドへ改装。
- **[🎛 Branding Intake](.agent/workflows/branding-intake.md)**: 製作者への問いかけからアプリ別ブランディング（brief.md）を確定。
- **[🎨 Generate Header Image](.agent/workflows/generate-header-image.md)**: 記事やREADME用のヘッダー画像生成。

### ✅ Quality & Release (品質・公開)
- **[🚀 Create Release](.agent/workflows/create-release.md)**: バージョニングとリリースノート生成。
- **[✅ Review Repo Quality](.agent/workflows/review-repo-quality.md)**: リポジトリの健康診断と改善提案。

---


## 🧱 Stack Policy（方針の正本）

本プロジェクトのスタック判断は、**/branding-intake で確定する `assets/branding/<productId>/brief.md` を唯一の正本（SoT）**とします。

- **スマホアプリ（iOS/Android）**: Flutter 推奨（状態管理: Riverpod / ルーティング: go_router を統一）
- **Webアプリ**: React 標準（例外可）
- **iOS運用**: ビルド/署名は macOS（Xcode）で実施（CIは必要時のみ macOS）


## ⚖️ Rules & Policies

エージェントは管制仕様（[ANTIGRAVITY_AGENT_CONTROL_SPEC.md](ANTIGRAVITY_AGENT_CONTROL_SPEC.md)）と、以下のルール（[`.agent/rules`](.agent/rules/)）に従って自律的に判断を行います。

- **Repo Creation Rule**: 新規リポジトリ作成時は、自動的にConvoy標準の `.gitignore` とディレクトリ構成を適用。
- **Branding Rule**: 「Mission Control」らしい工業的・高可読なデザインと言葉遣いを優先（アプリ別の詳細は `assets/branding/<productId>/brief.md` を正とする）。
- **Safety First**: 破壊的なコマンド実行前には必ず確認を求め、安全性を担保。

---

<div align="center">

*Empowered by Google Antigravity & Gemini*
<br>
*Crafted with ❤️ in the Zero-gravity Zone*

</div>
