---
slug: update-convoy-identity
description: リポジトリの見た目と導線（README/ヘッダー/Alerts/運用メタ情報）をConvoy（Mission Control）標準に整流化します
trigger: model_decision
---

# Convoy Identity Update

このワークフローは、リポジトリの **READMEレイアウト** と **ヘッダー画像** を整備し、Convoy（Mission Control）管理下であることが分かる導線（Docs/Issues/Workflows 等）を注入します。

- 目的: 「初見で何のリポジトリか分かる」「すぐに動かせる」「運用ルールへ辿れる」を最短で実現する
- 前提: Convoyは multi-repo 運用を想定し、各リポジトリは独立して起動・品質チェックできること

---

## Inputs（推奨）

- `assets/branding/<productId>/brief.md`（Brand Brief）
- `assets/branding/<productId>/header_prompt.txt`（ヘッダー生成用プロンプト）
- 既存の `README.md`
- （任意）ロゴ/アイコン素材

## Outputs（期待成果物）

- `assets/header.png`（入力/元画像）
- `assets/header_cropped_text.png`（READMEに貼る最終ヘッダー画像）
- 更新された `README.md`

---

## Step 1: Header（README用バナー）の準備 // turbo

- 目的: README最上部に置く「リポジトリ用ヘッダー画像」を統一する
- 実行（例）:
  - `pnpm header:build`（crop → text付与）
- 制約:
  - **English only / no non-Latin scripts**（日本語・漢字・非ラテン文字を入れない）
  - スタイルは **Mission Control**（neutral + 1–2 accents / flat / readable）
  - 過度な装飾・テクスチャ（箔/模様/グラデ）を避け、情報の可読性を優先

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
7. **Links**: Docs / Issues / Workflows / Releases への導線

### READMEヘッダー例

```md
<div align="center">
  <img src="assets/header_cropped_text.png" alt="Repository Header" width="100%" />
</div>

# <PROJECT_NAME>

<ONE_LINE_DESCRIPTION>

[Docs](<DOCS_URL>) · [Issues](<ISSUES_URL>) · [Releases](<RELEASES_URL>)
```

### GitHub Alerts（例）

```md
> [!IMPORTANT]
> This project is managed under Convoy standards. Changes must follow the defined Rules and Workflows.
```

### Convoy Note（固定テンプレ）

```md
> [!NOTE]
> This repository is managed with Convoy (Mission Control workspace).
> See: https://github.com/MorningMonkey/Convoy
> Source of Truth: `workspace.config.json` (`paths.projectFactoryDir`)
```

---

## Step 3: 検証（強制） // turbo

- READMEのプレビューでレイアウト崩れがないこと（画像/改行/Alerts/リンク）
- ヘッダー画像に以下が混入していないこと
  - 余計な文字（意図しない透かし/テンプレ文字）
  - 日本語・非ラテン文字（English only）
- 機密情報が含まれていないこと（Tokens/Keys/Secrets 等）
- `.agent/` への導線が README から辿れること（Workflows / Rules / Templates）

---

## Step 4: コミット（任意） // turbo

変更が妥当なら最小粒度でコミットします（README/asset/設定を分けるのが望ましい）。

例:
```bash
git add README.md assets/header_cropped_text.png
git commit -m "✨ style: apply Convoy identity (README/header/alerts)"
```

注意:
- `COMMIT_MSG.txt` 等の一時ファイルはコミットしない（必要なら `.gitignore`）
- 中間生成物は原則コミットしない（ポリシーに従う）
