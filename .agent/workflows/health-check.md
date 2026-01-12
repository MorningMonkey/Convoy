---
slug: "health-check"
description: "Convoy/GA-Workspace の .agent 構成（rules/workflows/INDEX/README/参照整合・frontmatter・重複・呼び出し依存）を検査し、Pass/Risk/Action の健康診断レポートを出す。"
trigger: "manual"
---

# 🏥 health-check — GA-Workspace 健全性チェック

---

## 定義（このワークフローの狙い）
- `.agent/` 配下が **実行可能な状態**か（構造・frontmatter・参照）
- ルール/ワークフローが **増えても破綻しない**か（重複・命名・導線）
- ワークフローが **安全に止まれる**設計か（承認ポイント・turboの付け方）
- 以上を **Pass / Risk / Action** で報告し、修正手順（処方箋）まで提示する

---

## SoT（Source of Truth）
- `.agent/INDEX.md`（利用可能コマンドの正本）
- `README.md`（オンボーディング導線の正本）
- `.agent/rules/*.md` / `.agent/workflows/*.md`（運用資産）
- `ANTIGRAVITY_AGENT_CONTROL_SPEC.md`（管制仕様）
- `assets/branding/<productId>/brief.md`（プロダクトのスタック/品質ゲート）

---

## 検査範囲
1. 構造（ディレクトリと重要ファイル）
2. frontmatter（YAMLキーと整合）
3. slug 重複（rules/workflows 横断）
4. 参照整合（@参照、リンク、workflow呼び出し）
5. 安全ガード（危険操作に turbo が付いていないか、承認ポイントが明記されているか）
6. 導線（INDEX/README から辿れるか）

---

## 重要ルール（Convoy品質ガード）
- 診断は **破壊的操作をしない**（読み取りのみ）
- 修正提案は **最小変更**を優先する
- “運用上の事故” に直結する項目（参照切れ・slug衝突・危険操作）は Must Fix 扱い

---

# 手順

## Step 1: 構造チェック（存在確認） // turbo
以下を確認する：

- `.agent/` が存在
- `.agent/rules/` が存在
- `.agent/workflows/` が存在
- `.agent/INDEX.md` が存在
- `README.md` が存在（任意だが推奨）
- `ANTIGRAVITY_AGENT_CONTROL_SPEC.md` が存在（運用上推奨）

### コマンド例
```bash
echo "=== .agent structure ==="
ls -la .agent || echo "❌ .agent/ が見つからない"
ls -la .agent/rules 2>/dev/null || echo "❌ .agent/rules/ が見つからない"
ls -la .agent/workflows 2>/dev/null || echo "❌ .agent/workflows/ が見つからない"
test -f .agent/INDEX.md || echo "❌ .agent/INDEX.md が見つからない"
test -f README.md || echo "⚠️ README.md が見つからない（任意）"
test -f ANTIGRAVITY_AGENT_CONTROL_SPEC.md || echo "⚠️ ANTIGRAVITY_AGENT_CONTROL_SPEC.md が見つからない（推奨）"
```

---

## Step 2: frontmatter チェック（最低限の整合） // turbo
rules/workflows の各ファイルで以下を確認：

- frontmatter 区切り `---` が先頭にある
- `trigger` / `description` / `slug` が存在
- `slug` とファイル名（拡張子除く）が一致
- `trigger` が Convoy 方針に反していない  
  - rules: 原則 `manual` / `model_decision`  
  - workflows: 原則 `manual`（必要時のみ `model_decision`）
- `description` が空ではない

### コマンド例（軽量チェック）
```bash
echo "=== frontmatter keys ==="
for f in .agent/rules/*.md .agent/workflows/*.md; do
  [ -f "$f" ] || continue
  echo "--- $f ---"
  head -30 "$f" | sed -n '1,30p' | grep -E '^(trigger|description|slug):' || echo "⚠️ $f: frontmatterキー不足の可能性"
done
```

> 厳密なYAMLパースは環境差が出るため、ここでは “事故りやすい不足” を先に拾う。  
> 必要なら後段の Action でより強い検査を提案する。

---

## Step 3: slug 重複チェック（衝突はMust Fix） // turbo
- `.agent/rules/` と `.agent/workflows/` を横断して `slug` が重複していないか
- 同一カテゴリ内（rules同士/ workflows同士）も重複を禁止

### コマンド例
```bash
echo "=== slug duplicates ==="
grep -R "^slug:" -n .agent/rules .agent/workflows | sed 's/^/FOUND /'
# ここから重複抽出（環境によりawk/sortを利用）
```

---

## Step 4: 参照整合性チェック（@参照 / リンク / workflow呼び出し） // turbo
以下を確認：

### 4.1 `@...` 参照
- `@rule-templates` のような “slug参照” がある場合、実体が存在するか
- `@path/to/file.md` のような “パス参照” がある場合、参照先が存在するか

### 4.2 README / INDEX のリンク
- `README.md` 内の `docs/...` や `.agent/...` へのリンクが存在するか（大小文字含む）
- `.agent/INDEX.md` から workflows/rules が辿れるか

### 4.3 workflow 呼び出し
- 文中に `/some-workflow` がある場合、`.agent/workflows/some-workflow.md` が存在するか
- 統合workflowが “呼び出しだけ” になっていて、結果集約が無い場合は Risk

---

## Step 5: 安全ガードチェック（turbo/承認ポイント）
以下は “運用事故” に直結するため重点的に見る：

- デプロイ、push、削除、依存追加、外部API書き込み などの操作に `// turbo` が付いていないか
- 危険操作の前に **承認ポイント**が明記されているか
- 「勝手に進める」表現（例: “実行せよ” だけで承認要求なし）がないか

---

## Step 6: 導線チェック（迷子防止）
- `.agent/INDEX.md` に主要 workflow が載っているか
- README に onboarding の入口があるか（例: `/branding-intake` から始める、など）
- `ANTIGRAVITY_AGENT_CONTROL_SPEC.md` の入口が統合フロー（`/create-convoy-project-complete`）で固定されているか（運用方針に合うか）

---

# 健康診断レポート（出力テンプレ）

```markdown
## 🏥 GA-Workspace 健康診断結果

### 総合診断
- 判定: ✅ 健康 / ⚠️ 要注意 / ❌ 要治療
- 根拠: <最重要な所見を1-3点>

---

## Pass（問題なし）
- <OK項目>

## Risk（要注意）
- <リスク項目: 影響/確率/重大度>

## Must Fix（要治療）
- <即修正が必要な項目: 参照切れ/slug衝突/危険操作turbo 等>

---

## 構造
- .agent/: ✅/❌
- rules/: ✅/❌
- workflows/: ✅/❌
- INDEX.md: ✅/❌
- README.md: ✅/⚠️/❌

## frontmatter
- キー不足: <N>件
- slug不一致: <N>件
- trigger方針逸脱: <N>件

## 参照整合性
- 未解決 @参照: <N>件
- 未解決リンク: <N>件
- 未解決 workflow 呼び出し: <N>件

## 安全ガード
- 危険操作turbo: <N>件
- 承認ポイント欠落: <N>件

---

## 処方箋（Action）
1. <最小修正手順>
2. <最小修正手順>
3. <必要なら自動化提案: lint/CI>

### 次のアクション（任意）
- `/review-repo-quality` を実行して品質ゲートを追加診断
```

---

## コメント（診断の言い回し）
- 健康: 「元気だね。私もうれしい」
- 要注意: 「ちょっと気になるところがあるけど、動くよ」
- 要治療: 「あれ……直さないと動かないかも。手伝うね」


