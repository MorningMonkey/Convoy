---
slug: "type-check"
description: "TypeScript の型チェック（tsc 等）をSoT（brief.md）に従って実行し、PASS/FAIL と根拠（主要エラー）を報告する原子ワークフロー。"
trigger: "manual"
---
# 🧷 type-check — 型チェック

このワークフローは **型チェックの実行と報告のみ** を行います。  
修正（tsconfig変更・実装修正・依存更新等）は別ワークフローに切り出し、必要ならユーザー承認を取ります。

---

## 定義（このワークフローの狙い）
- TypeScript の型チェックを実行し、結果を **PASS / FAIL** で機械的に報告する
- 失敗時に「次に直すべき箇所」が分かるよう、主要エラーを要約する
- 実行コマンドは **SoT（brief.md）** を優先し、ない場合のみフォールバックする

---

## SoT（Source of Truth）
- スタック/品質ゲート: `assets/branding/<productId>/brief.md`
- 利用可能コマンド一覧: `.agent/INDEX.md`
- 関連（任意）: `.agent/rules/*type*.md`（例: `type-safety`）

---

## 入力（Inputs）
- 対象ブランチ/コミット（任意）
- 実行範囲（任意）：全体 / 特定パッケージ / 特定ディレクトリ
- モノレポ構成（任意）：workspaces/複数tsconfig など

---

## 成果物（Outputs）
- 判定: `PASS` / `FAIL`
- 実行したコマンド（Evidence）
- エラー数（分かる範囲で）
- 主要エラー（最大5件：file:line + メッセージ要約）
- 推奨次アクション（例: bug-fix / type-safety ルール参照）

---

## 安全ガード（Convoy標準）
- `// turbo` 可（検証のみ）
- 自動修正はしない
- 設定変更（tsconfig）・依存追加・push は行わない

---

# 手順

## Step 1: 前提確認（軽量） // turbo
```bash
pwd
ls -la
test -f tsconfig.json || echo "⚠️ tsconfig.json が見つからない（複数構成の可能性）"
```

---

## Step 2: 実行コマンドの決定（SoT優先） // turbo
優先順位：

1. `assets/branding/<productId>/brief.md` に記載の typecheck コマンド
2. `package.json` scripts の `typecheck` / `type-check` / `tsc`
3. フォールバック

---

## Step 3: 型チェック実行 // turbo
### 3.1 package.json の script を優先（推奨）
```bash
pnpm -s typecheck || pnpm -s type-check || npm run -s typecheck || yarn -s typecheck
```

### 3.2 フォールバック（tsc直接）
```bash
npx -y tsc --noEmit || yarn -s tsc --noEmit
```

> 複数候補を試した場合、実行した順序を Evidence に残す。

---

## Step 4: 結果判定
- **成功**: 型エラーなし → `PASS`
- **失敗**: 型エラーあり → `FAIL`

> 退出コードで判定できない場合（出力が不明瞭）は、ログに基づき `FAIL` 寄りで扱い、理由を併記する。

---

## Step 5: 失敗時の要約（最大5件） // turbo
`FAIL` の場合は以下を報告する：

- エラー数（分かる範囲で）
- 代表エラー（最大5件）
  - `file:line`（可能なら `TSxxxx` も）
  - メッセージ（短く要約）
- 影響範囲（ビルド不可、特定パッケージのみ、など）
- 推奨次アクション（最小修正ルート）

---

# 完了報告テンプレ

```markdown
## 🧷 type-check 結果

- 判定: PASS / FAIL
- コマンド（Evidence）: <実行したコマンド（試した順）>
- 対象: <ブランチ/コミット（任意）>

### サマリー
- エラー数: <N>（不明なら“不明”）
- 影響: <例: build阻害 / 一部のみ>

### 主要エラー（最大5件）
1. <file:line> <TSxxxx?> — <message summary>
2. ...
3. ...

### 次のアクション（推奨）
- <例: bug-fix に移行して原因特定→最小修正→再実行>
- 参照: @type-safety（存在する場合）
```


