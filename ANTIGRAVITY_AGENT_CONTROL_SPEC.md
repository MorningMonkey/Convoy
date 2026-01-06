# ANTIGRAVITY_AGENT_CONTROL_SPEC

Google Antigravity エージェントが Convoy（Mission Control）を **安全かつ一貫した品質**で運用するための「管制仕様書」です。  
Workspace 内の Rules / Workflows を **どう解釈・実行**すべきかを定義し、人間とエージェントの期待値を揃えます。

---

## 1. 目的とスコープ

- **対象**: Convoy プロダクト（本リポジトリ）配下で動作する Google Antigravity エージェント
- **目的**: 「エージェント主導開発（ADE）」のワークスペースとして、リポジトリ生成・実装・リリースまでを標準化された導線で実行する
- **範囲**:
  - `.agent/` 配下の `rules/*` と `workflows/*`
  - `workspace.config.json` に定義されたパス/デフォルト値
  - `assets/`（ヘッダー画像・ブランド素材）
  - `docs/` および `README.md`（外部共有ドキュメント）

---

## 2. Source of Truth（SoT）

- **運用ルールの正本**: `.agent/`（Rules / Workflows / Templates / INDEX）
- **Workspace 設定の正本**: `workspace.config.json`
- **アーキテクチャ図の正本**: `docs/architecture.drawio`
  - **任意**: README 表示用に `docs/architecture.svg` を併置してよい（drawio からエクスポートした成果物）

> 注意: SoT のファイル名は **大小文字を含めて厳密**です（GitHub は大文字小文字を区別するため、参照切れの原因になります）。

---

## 3. 管制オブジェクト

| 領域 | 役割 | 代表ファイル |
| --- | --- | --- |
| **Rules（憲法）** | 生成物の制約・規約（例: frontmatter 必須キー、命名、禁則） | `.agent/rules/*` |
| **Workflows（SOP）** | Slash コマンドの実行手順（手順/成果物/結果フォーマット） | `.agent/workflows/*` |
| **Templates** | リリースノート等の定型フォーマット | `.agent/templates/*` |
| **Config（設定）** | プロジェクト工場・デフォルト言語・ライセンス等 | `workspace.config.json` |
| **Branding（意匠）** | アプリ別のブランド正本と派生プロンプト | `assets/branding/<productId>/brief.md`, `assets/branding/<productId>/header_prompt.txt` |
| **Header（表示資産）** | README 用ヘッダー画像（最終成果物） | `assets/header_cropped_text.png` |
| **Docs（外部共有）** | README / アーキテクチャ図 | `README.md`, `docs/architecture.drawio`（正本）, `docs/architecture.svg`（任意） |

---

## 4. インターフェース

### 4.1 Slash コマンド（Workflow）

- Slash コマンドは `.agent/workflows/*.md` の **frontmatter `slug`** をトリガーに実行される
- `description` は YAML 事故防止のため **原則クオート**する（日本語・括弧・記号混在に強くする）
- Workflows の最終応答は、**Workflows に定義されたフォーマット**を優先し、逸脱しない

### 4.2 生成物の配置

- プロジェクト工場のルートは `workspace.config.json` の `paths.projectFactoryDir` を唯一の基準（例: `CONVOY_PROJECT`）
- ブランディング資産は `assets/branding/<productId>/` を基準に置く
- ヘッダー画像の最終成果物は **`assets/header_cropped_text.png`**（README が参照する前提）

### 4.3 ブランディング（アプリ別）

- アプリ別のブランド正本は `assets/branding/<productId>/brief.md`
- brief から `assets/branding/<productId>/header_prompt.txt` を派生生成して良い
- 既存リポジトリ改装時は `update-convoy-identity` を経由し、README/ヘッダーを整流化する

> ブランド指針（共通）: 「Mission Control」らしい **工業的・高可読**を優先する  
> - ベース: dark charcoal / metallic neutrals  
> - アクセント: controlled red + blue（過剰にしない）  
> ※ 具体配色はアプリ別 brief を正とする

---

## 5. 安全・品質ガード（必須）

- **Safety First**: 破壊的操作（削除・上書き・強制 push・履歴改変など）は **ユーザー確認を必須**とする
- **Secrets 禁止**: 機密情報（APIキー/トークン/秘密鍵/認証情報）は **一切コミットしない**
- **コミットポリシー**: 意味単位で小さくコミットし、変更理由が追えるメッセージを付ける
- **言語**: デフォルトは日本語。`walkthrough.md` / 最終応答も **日本語を正**とする  
  - 禁止: 英語定型文のみでの結果通知（例: “Result is in walkthrough.md …”）
- **参照切れ防止**: README / docs / workflows のリンクは、コミット前に存在確認する（大小文字含む）
- **特定作品・固有IPの回避**: ヘッダー画像や図版は、特定フランチャイズ/固有キャラクターを想起させる表現を禁止（例: Transformers 等）

---

## 6. 推奨実行フロー（例）

1. `/create-convoy-project-complete` を起点にリポジトリを生成
2. 実装が必要なら `/build-app-simple` を適用
3. アプリ別のブランディング確定が必要なら `/branding-intake` を実行し brief を正本化
4. ブランド適用は `/update-convoy-identity`
5. 品質チェックは `/review-repo-quality`
6. 必要に応じて `/visualize-architecture`（`docs/architecture.drawio` を更新/追加）
7. リリースは `/create-release`

---

## 7. エージェント動作の期待

- Rules / Workflows を単一の **Source of Truth** として扱い、外部テンプレートに依存しない
- 生成した成果物は README / docs / templates にリンクし、**参照切れを作らない**
- 変更点はコミットメッセージ・PR（運用する場合）に明確に記述し、レビュー導線を確保する
- 不確実な操作（削除・置換・リリース等）は、手順に従い確認を挟む

---

*Crafted for mission-ready operations with Google Antigravity.*
