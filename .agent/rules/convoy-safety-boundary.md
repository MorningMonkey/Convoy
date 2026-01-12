---
slug: "convoy-safety-boundary"
description: "Convoyにおける作業範囲の境界（Boundary）と情報の正本（SoT）に関する安全規定。"
trigger: "model_decision"
---

# 🛡️ Convoy Safety & Boundary Policy

## 🌌 Overview
本ルールは、Convoy (Mission Control) とその配下で生成されるプロダクト (Factory Products) の間の「安全境界」を定義する。
エージェントおよび開発者は、この境界を越境して不意な破壊を行ってはならない。

## ⚖️ Rules / Constraints

### 1. Nested Git Strategy (入れ子Git安全策)
`CONVOY_PROJECT/` 配下は、Convoy本体のリポジトリ履歴とは**完全に分離**されなければならない。

- **Exclude from Parent**: Convoyリポジトリの `.gitignore` にて `CONVOY_PROJECT/` が除外されていることを維持する。
- **Independent Repos**: 配下の各プロダクトフォルダ（例: `CONVOY_PROJECT/my-app`）は、それぞれ独立して `git init` され、独自のリモートを持つ。
- **No Submodules**: 原則として git submodule は使用しない（複雑化回避のため、Polyrepoとして扱う）。

### 2. Execution Boundary (実行境界)
ワークフロー実行時、エージェントは変更対象を明確に限定しなければならない。

- **Scope Limitation**: 特定のプロダクトに対する変更（機能実装、バグ修正）は、そのプロダクトのルートディレクトリ配下のみで行う。
- **Protect Mission Control**: プロダクト作業中に `projects/`, `.agent/`, `docs/` 等のConvoy管理領域を変更してはならない（`projects-sync` 等の専用ワークフローを除く）。

### 3. Single of Truth (SoT) Definitions
判断に迷った際は、以下のファイルを正本として参照する。

- **Project List SoT**: `projects/manifest.json`
  - リポジトリのURL、ローカルパスの正解はここにしかない。
- **Workspace Path SoT**: `workspace.config.json`
  - ファクトリーディレクトリの場所はここで定義される。
- **Product Spec SoT**: `assets/branding/<productId>/brief.md`
  - そのアプリが「何を作るべきか」「どういうデザインか」の正解。

### 4. Workflow Usage Policy
- ワークフローは原則として「対象Repoのパス」を受け取り、その配下だけで実行する規約とする。
- Convoy本体（`.agent` 等）を変更するワークフローは、その旨を明示した専用のもの（例: `/update-convoy-identity`, `/create-rule`）に限る。
