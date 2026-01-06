---
slug: update-convoy-identity
description: "リポジトリの見た目と導線（README/ヘッダー/Alerts/運用メタ情報）をConvoy（Mission Control）標準に整流化します"
trigger: model_decision
---

# Convoy Identity Update

このワークフローは、リポジトリの **READMEレイアウト** と **ヘッダー画像** を整備し、Convoy（Mission Control）管理下であることが分かる導線（Docs / .agent / Workflows 等）を注入します。

- 目的: 「初見で何のリポジトリか分かる」「すぐに動かせる」「運用ルールへ辿れる」を最短で実現する
- 前提: Convoyは multi-repo 運用を想定し、各リポジトリは独立して起動・品質チェックできること

---

## Inputs（必須）

- `assets/branding/<productId>/brief.md`（Brand Brief / 正本）
- `assets/branding/<productId>/header_prompt.txt`（ヘッダー生成用プロンプト）
- 既存の `README.md`

## Outputs（期待成果物）

- `assets/header.png`（入力/元画像）
- `assets/header_cropped_text.png`（READMEに貼る最終ヘッダー画像）
- 更新された `README.md`

---

## Preflight: Branding Brief（必須）

- `assets/branding/<productId>/brief.md` の存在を確認します。
- 存在しない場合は、先に `/branding-intake` を実行して brief を作成してください。
- brief が無い状態では本ワークフローを続行しません（ブランディングの一貫性を守るため）。

---

## Step 1: Header（README用バナー）の準備 // turbo

- 目的: README最上部に置く「リポジトリ用ヘッダー画像」を統一する
- 実行（例）:
  - `pnpm header:build`（crop → text付与）
- 制約:
  - **English only / no non-Latin scripts**（日本語・漢字・非ラテン文字を入れない）
  - スタイルは **Mission Control**（neutral + 1–2 accents / flat / readable）
  - 過度な装飾・テクスチャ（箔/模様/強いグラデ）を避け、情報の可読性を優先

### 生成物の扱い（ポリシー）
- 推奨: `assets/header_cropped_text.png` は **コミット可**（README表示の安定目的）
- それ以外の中間生成物は `.gitignore`（差分ノイズ削減）

---

## Step 2: README更新（Convoyレイアウト） // turbo

`README.md` を以下の順で整備します（既存内容がある場合は尊重しつつ整流化）。

1. **ヘッダー画像**: 最上部に配置
2. **One-liner**: 何のプロダクトか1行で説明
3. **Quick Start**: 3〜6行で起動まで到達
4. **Core Features**: 3〜7項目で要点
5. **GitHub Alerts**: 重要注意（Breaking/Experimental 等）がある場合
6. **Convoy Note**: Convoy管理であることと Source of Truth を明記
7. **Links**: Docs / .agent/INDEX / Workflows / Issues / Releases への導線

### READMEヘッダー例（コピペ用）

```md
<div align="center">
  <img src="assets/header_cropped_text.png" alt="<PROJECT_NAME> Header" width="100%" />
</div>

# <PROJECT_NAME>

<ONE_LINE_DESCRIPTION>

[Docs](<DOCS_URL>) · [.agent/INDEX](.agent/INDEX.md) · [Workflows](.agent/workflows) · [Issues](<ISSUES_URL>) · [Releases](<RELEASES_URL>)
```

> 補足:
> - `Issues/Releases` は GitHub リモートが無い段階では未確定になり得ます（必要なら後で差し替え）。
> - `.agent/INDEX` は Convoy 本体repoの導線が正本です。生成物repoで `.agent/` を持たない方針の場合は、このリンクを削除または「Convoy側のINDEXを参照」と注記します。

### GitHub Alerts（例・日本語）

```md
> [!IMPORTANT]
> このリポジトリは Convoy（Mission Control）標準で管理されています。変更は Rules と Workflows に従ってください。
```

### Convoy Note（固定テンプレ・日本語）

```md
> [!NOTE]
> このリポジトリは Convoy（Mission Control workspace）で管理されています。
> Source of Truth: `workspace.config.json`（`paths.projectFactoryDir`）
```

---

## Step 3: 検証（強制） // turbo

- READMEのプレビューでレイアウト崩れがないこと（画像/改行/Alerts/リンク）
- ヘッダー画像に以下が混入していないこと
  - 余計な文字（意図しない透かし/テンプレ文字）
  - 日本語・非ラテン文字（English only）
- 機密情報が含まれていないこと（Tokens/Keys/Secrets 等）
- 運用導線が README から辿れること（Docs / Rules / Workflows / INDEX 等、方針に沿った導線）

---

## Step 4: コミット（任意） // turbo

変更が妥当なら最小粒度でコミットします（README/asset/設定を分けるのが望ましい）。

例:
```bash
git add README.md assets/header_cropped_text.png
git commit -m "style: apply Convoy identity (README/header/alerts)"
```

注意:
- `COMMIT_MSG.txt` 等の一時ファイルはコミットしない（必要なら `.gitignore`）
- 中間生成物は原則コミットしない（ポリシーに従う）

---

## 最終応答（必須・日本語のみ）

- 結果報告は日本語で「完了内容 / 生成・更新ファイル / 次のアクション」を含める
- 「結果は walkthrough.md を参照してください」の一文だけで終えない（本文に要点を要約）
- 英語の定型文（例: "Result is in walkthrough.md ..."）は禁止

### 出力フォーマット（固定）

- 完了:
- 生成・更新ファイル:
- 次のアクション:
