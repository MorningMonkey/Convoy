# .agent Index (Convoy)

このドキュメントは、Convoy（Mission Control）配下の `.agent/` 資産を一覧化し、**実行導線（推奨フロー）**を確定するための「入口」です。

---

## 目的

- Rules（憲法）と Workflows（SOP）により、生成される全リポジトリを **統一品質**で管理する
- AIエージェントが迷わないよう、**参照点（Single Source of Truth）**を固定する
- 人間が運用しやすいよう、**実行順序**と**成果物**を明確化する

---

## Source of Truth

- リポジトリ生成先: `workspace.config.json` の `paths.projectFactoryDir`（推奨: `CONVOY_PROJECT`）
- ルール/手順の格納場所: `.agent/`

---

## Rules

| slug | description | file |
| --- | --- | --- |
| repo-creation | Project Factory配下でのリポジトリ作成規約を強制する | .agent/rules/repo-creation.md |

---

## Templates

| name | description | file |
| --- | --- | --- |
| release_notes_template.md | GitHub Release 用のリリースノートテンプレート（変数埋め込み式） | release_notes_template.md |
| release_notes_template_ja.md | GitHub Release 用のリリースノートテンプレート（変数埋め込み式） | release_notes_template_ja.md |

> Templates は frontmatter を持たず、本文コメント（変数契約）で運用します。

---

## Workflows

| slug | description | trigger | file |
| --- | --- | --- | --- |

---

## 推奨フロー（Project Complete）

以下が Convoy 標準の一気通貫導線です。

- **1) リポジトリ作成（新規/既存）**: `[repo-creation]`（Rule）を遵守し、[create-repo-from-folder](.agent/workflows/create-repo-from-folder.md) または [create-prompt-repo](.agent/workflows/create-prompt-repo.md) を実行
- **2) Identity 注入（ブランド/README）**: [update-convoy-identity](.agent/workflows/update-convoy-identity.md)（ヘッダー/README/Alerts/導線）
- **3) 品質レビュー（出荷前点検）**: [review-repo-quality](.agent/workflows/review-repo-quality.md)（Pass/Risk/Action）
- **4) アーキテクチャ可視化（任意）**: [visualize-architecture](.agent/workflows/visualize-architecture.md)（Draw.io XML）
- **5) リリース作成**: [create-release](.agent/workflows/create-release.md)（テンプレ: `.agent/templates/release_notes_template.md`）
- **6) コミット自動化（任意）**: [git-auto-commit](.agent/workflows/git-auto-commit.md)（変更量が多い場合の分割コミット）

---

## よくある使い分け

- **素早くUIを作る（単体アプリ）**: [build-app-simple](.agent/workflows/build-app-simple.md)
  - 既定: Vanilla（HTML/CSS/JS）
  - 条件に応じて: React + Tailwind（任意でTypeScript）

- **ヘッダー画像だけ作りたい**: [generate-header-image](.agent/workflows/generate-header-image.md)
  - 画像生成が難しい場合は、後から `gh release upload` で追加

- **既存フォルダをConvoy管理にしたい**: [create-repo-from-folder](.agent/workflows/create-repo-from-folder.md) → [update-convoy-identity](.agent/workflows/update-convoy-identity.md) → [review-repo-quality](.agent/workflows/review-repo-quality.md)

---

## 運用ルール（最低限）

- Workflows は必ず frontmatter（`slug/description/trigger`）を持つ
- 禁則ワード（例: `YOROZU`, `Miyabi`）はリポジトリ内に残さない（再発防止はCIで）
- 生成物のコミット方針は、各workflowの「生成物の扱い（ポリシー）」に従う

---
