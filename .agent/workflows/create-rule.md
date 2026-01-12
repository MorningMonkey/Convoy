---
slug: "create-rule"
description: "ユーザーの要求から新しいルール（.agent/rules/*.md）をConvoy標準（SoT参照・trigger方針・整合チェック）で対話的に作成する。"
trigger: "manual"
---

# 🧩 create-rule — ルール作成ワークフロー

Convoy のルールは「縛るため」ではなく、**迷いを減らして品質を守る**ための資産です。  
このワークフローは、要求ヒアリングから **整合性チェック → 生成 → 検証 → 登録（INDEX/README導線）**までを一気通貫で行います。

---

## 定義（このワークフローの狙い）
- ルールの目的と適用条件を明確にし、再利用可能な形で `.agent/rules/` に保存する
- 既存ルールと **重複・矛盾**しないように整流化する
- Convoy 標準の trigger 方針（原則 manual / model_decision）を守る
- 生成後に **INDEX/README の導線**で見失わないようにする（任意）

---

## SoT（Source of Truth）
- プロダクト要件/方針: `assets/branding/<productId>/brief.md`（スタック/品質ゲート/対象プラットフォーム）
- 利用可能コマンド一覧: `.agent/INDEX.md`
- 管制仕様: `ANTIGRAVITY_AGENT_CONTROL_SPEC.md`
- ルール配置: `.agent/rules/*.md`

---

## 重要ルール（Convoy標準）
1. **trigger 方針**
   - 原則: `manual` / `model_decision` のみ
   - `always_on` は原則使わない（暴発しやすく、保守不能になりがち）
   - `glob` も原則使わない（Repo構造変更に弱い）。必要なら model_decision で条件を文章化する

2. **SoT参照**
   - 特定の技術スタック（例: React/Next/Flutter）をルールで固定しない  
     → **brief.md を正本**として参照する

3. **安全ガード**
   - 破壊的操作（削除/上書き/強制push/デプロイ等）や機密情報の扱いは、承認と明文化を必須にする

4. **再利用**
   - 既存ルールがあるなら **@参照**（重複を作らない）

---

# 手順

## Step 1: 要求のヒアリング（4W1H + 禁止/例外）
ユーザーから以下を収集する（不足があれば具体質問で補完する）：

1. **目的（Why）**: 何の品質/リスクを抑えたいか
2. **対象（What）**: どの行動/出力/資産を制御したいか
3. **適用条件（When）**: いつ適用するか（状況、キーワード、作業フェーズ）
4. **禁止事項（Must Not）**: 絶対にやってはいけないこと
5. **例外（Exceptions）**: 適用しないケース
6. **成功条件（Done）**: ルールが効いていると判断できる状態

**出力（必須）**
- ルールの1行サマリー: `<目的 + 適用条件>`
- ルールの境界: `<適用/非適用の線引き>`

---

## Step 2: trigger の決定
Convoy の推奨マッピング：

| ユーザーの意図 | 推奨 trigger | 理由 |
|---|---|---|
| 「明示的に呼び出したときだけ」 | `manual` | 暴発しない。SOP/手順に強い |
| 「〜の場合/〜について言及されたら」 | `model_decision` | 条件適用が可能。拡張しやすい |
| 「常に適用したい」 | まず `model_decision` を検討 | always_on は運用が壊れやすい |
| 「特定ファイルだけ」 | まず `model_decision` を検討 | globはrepo変更で壊れやすい |

**このStepの成果**
- trigger と採用理由を明記する
- model_decision の場合、description に **引っ掛けるキーワード**を入れる

---

## Step 3: ルール構造の設計（Convoyテンプレに落とす）
以下の構造で設計案（ドラフト）を作る。  
**必ず「MUST / MUST NOT / SHOULD」** で分ける。

```markdown
---
trigger: "<manual|model_decision>"
description: "<適用条件が分かる1文（キーワード含む）>"
slug: "<kebab-case>"
---
# <ルール名>

## 目的
- <何を守るルールか>

## 適用条件（When）
- <適用される条件>
- <適用されない条件（あれば）>

## MUST（必須）
- <必ず守る>

## MUST NOT（禁止）
- <絶対にやらない>

## SHOULD（推奨）
- <できれば守る>

## 例外（Exceptions）
- <例外条件>

## 参照（References）
- SoT: `assets/branding/<productId>/brief.md`
- 関連ルール: `@<slug>`（存在する場合）
```

**ユーザー合意ポイント**
- 目的と適用条件が曖昧でないか
- 禁止事項が現実的か（開発が止まらないか）
- 例外の扱いが漏れていないか

---

## Step 4: slug / ファイル名の決定（番号プレフィックスは原則廃止）
Convoy では **ファイル名の順序で運用を固定しない**（並び替えが増え、負債化しやすい）。  
したがって **番号プレフィックスは原則不要** とする。

- 形式: `<category>-<topic>.md`
- kebab-case（小文字、ハイフン区切り）
- 例:
  - `security-secrets.md`
  - `commit-message-format.md`
  - `dangerous-ops-approval.md`

> 分類順序を作りたい場合は、**INDEX.md側で分類**する（ファイル名で序列を作らない）。

---

## Step 5: 既存ルールとの整合性チェック（重複・矛盾・再利用）
`.agent/rules/` を確認し、以下を行う：

1. **重複チェック**: 同様の意図のルールが既にないか
2. **矛盾チェック**: MUST/MUST NOT が既存ルールと衝突しないか
3. **参照再利用**: 既存ルールを `@` 参照で再利用できないか

問題があれば、次の形式で報告する：

- 重複候補: `<rule slug>`
- 矛盾点: `<どこが衝突>`
- 対処案: `統合 / 参照 / 置換 / 新規`

---

## Step 6: ルールファイルの生成
- 保存先: `.agent/rules/<slug>.md`
- frontmatter は必ず以下を満たす:
  - `trigger` は `"manual"` か `"model_decision"`（二重引用符推奨）
  - `description` は二重引用符
  - `slug` はファイル名と一致

---

## Step 7: 検証（品質ゲート）
作成したルールを検証する：

1. **frontmatter 構文**: YAMLとして解釈できるか（キー漏れ/型不一致がないか）
2. **適用条件の明確さ**: いつ発動するかが読み手に伝わるか
3. **Convoy整合**: always_on/glob に逃げていないか、SoT参照になっているか
4. **実務性**: 守れるルールか（遵守コストが高すぎないか）

**出力（必須）**
- ルール全文
- trigger と適用条件の説明
- 関連ルール（参照/統合したもの）

---

## Step 8: 登録（導線の更新：任意だが推奨）
ルールを作っただけでは運用されません。以下を「必要に応じて」更新する。

- `.agent/INDEX.md` にルールを追加（カテゴリ別にリンク）
- README.md に “Rules/Workflows” の導線があるなら追記

> ルールの数が増えたら、**テンプレ集（@rule-templates）**へ逆輸入して標準化する。

---

## 完了報告テンプレ
```markdown
## ✅ create-rule 完了

- 生成ファイル: `.agent/rules/<slug>.md`
- trigger: `<manual|model_decision>`
- 適用条件: <いつ発動するか>
- 目的: <何を守るか>
- 関連/参照: <@slug など>
- 次のアクション（任意）: INDEX/READMEへの登録
```


