---
slug: "update-convoy-identity"
description: "READMEとヘッダー画像、Alertsと導線をConvoy標準へ整流化し、初見理解と運用到達性を確立する。"
trigger: "model_decision"
---
# 🧭 update-convoy-identity

## 🌌 Overview
本ワークフローは、リポジトリの「顔」となる README とヘッダー画像を Convoy（Mission Control）標準へ整流化し、
初見で目的が分かり、すぐ起動でき、運用ルールへ到達できる状態を最短で成立させる。
Convoy は multi-repo 運用を前提とし、各リポジトリが独立して起動・品質チェック可能であることを守る。

## ⚖️ Rules / Constraints
- **SoT（Brand Brief）**: `assets/branding/<productId>/brief.md` を正本とする。存在しない場合は続行しない（先に `/branding-intake` を実行）。
- **ヘッダー出力のSoT**: README が参照するヘッダー画像は `assets/header_cropped_text.png` を既定とする。
- **画像内テキストの制約**: ヘッダー画像内の文字は **English only / no non-Latin scripts**（日本語・漢字・非ラテン文字禁止）。
- **スタイル規律**: Mission Control（neutral + 1–2 accents / flat / readable）。過度な装飾・強いテクスチャ・強いグラデは避け、可読性を優先する。
- **Convoy導線の必須**: README から Docs / `.agent/INDEX` / Workflows 等の運用導線へ到達できることを必須とする。
- **中間生成物の扱い**: `assets/header_cropped_text.png` はコミット可（表示安定のため）。それ以外の中間生成物は原則 `.gitignore` で除外する。
- **機密排除**: README / 画像 / 設定に Tokens/Keys/Secrets 等の機密を含めない。
- **最終応答の言語**: 最終報告は日本語のみ。英語の定型文で終えない。

## 🚀 Workflow / SOP

### Step 1: Preflight（Branding Brief の確認）
1. `assets/branding/<productId>/brief.md` の存在を確認する。
2. 存在しない場合は本ワークフローを停止し、`/branding-intake` の実行を指示する。

**出力**
- Preflight 結果（OK / Stop）
- brand brief のパス（SoT）

### Step 2: Header（README用バナー）の準備
1. `pnpm header:build` を実行し、crop → text 付与までを一括生成する。
2. 生成物のうち README 用の最終成果物を `assets/header_cropped_text.png` として確定する。
3. 画像内テキストが English only であること、意図しない透かしやテンプレ文字が無いことを確認する。

**出力**
- `assets/header.png`（入力/元画像）
- `assets/header_cropped_text.png`（README に貼る最終ヘッダー）

### Step 3: README更新（Convoyレイアウトへ整流化）
1. 既存の README 内容を尊重しつつ、以下の順で整流化する。
   - ヘッダー画像（最上部）
   - One-liner（1行説明）
   - Quick Start（3〜6行で起動）
   - Core Features（3〜7項目）
   - GitHub Alerts（必要時）
   - Convoy Note（SoT 明記）
   - Links（Docs / `.agent/INDEX` / Workflows / Issues / Releases への導線）
2. `.agent/` を持たない方針の場合は、`.agent/INDEX` リンクを削除するか「Convoy 側の INDEX を参照」と注記する。

**出力**
- 更新された `README.md`（導線と起動手順を含む）

### Step 4: 検証（強制）
1. README プレビューで崩れがないことを確認する（画像/改行/Alerts/リンク）。
2. ヘッダー画像の禁止要素混入を確認する（日本語・非ラテン文字、意図しない文字）。
3. 機密情報が含まれていないことを確認する。
4. README から運用導線へ到達できることを確認する。

**出力**
- 検証結果（OK / 要修正）
- 要修正の場合の最小修正ポイント（ファイル/行/見出し）

### Step 5: コミット（任意）
1. 変更が妥当なら最小粒度でコミットする（README/asset/設定は分割が望ましい）。
2. `COMMIT_MSG.txt` 等の一時ファイルはコミットしない（必要なら `.gitignore`）。
3. 中間生成物は原則コミットしない（ポリシーに従う）。

**出力**
- コミット一覧（任意）
- コミットに含めたファイル一覧（README / 最終ヘッダー 等）

### Step 6: 最終報告（日本語）
固定フォーマットで、完了内容・更新ファイル・次アクションを日本語で報告する。

**出力（固定）**
- 完了:
- 生成・更新ファイル:
- 次のアクション:

## ✅ Checklist
- [ ] `assets/branding/<productId>/brief.md` が存在し、SoT に基づいて整流化されている
- [ ] `assets/header_cropped_text.png` が生成され、English only を満たしている
- [ ] README が Convoy レイアウトに整い、Docs / Workflows 等の導線が通っている
- [ ] 機密情報や一時ファイル、中間生成物の混入がない


