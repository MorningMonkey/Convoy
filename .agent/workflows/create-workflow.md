---
slug: "create-workflow"
description: "ユーザー要求から新しいワークフロー（.agent/workflows/*.md）をConvoy標準（SoT参照・安全ガード・再利用・検証）で対話的に作成する。"
trigger: "manual"
---

# 🧭 create-workflow — ワークフロー作成

Convoy の workflow は「手順書」ではなく、**迷いなく安全に実行できる運用資産**です。  
このワークフローは、要求ヒアリングから **分解 → 安全設計 → 既存資産との整合 → 生成 → 検証 → 導線登録**までを一気通貫で行います。

---

## 定義（このワークフローの狙い）
- ユーザーの目的を、**実行可能で安全なステップ**へ落とし込む
- 危険操作（push/削除/デプロイ等）を確実にガードし、承認ポイントを明示する
- 既存 workflow / rule の再利用を優先し、重複を作らない
- 生成後に運用（INDEX/README）へ繋がる形に整える（任意）

---

## SoT（Source of Truth）
- プロダクト要件/方針: `assets/branding/<productId>/brief.md`
- 利用可能コマンド一覧: `.agent/INDEX.md`
- 管制仕様: `ANTIGRAVITY_AGENT_CONTROL_SPEC.md`
- Workflows: `.agent/workflows/*.md`
- Rules: `.agent/rules/*.md`

---

## Convoy 標準（守るべき前提）
- frontmatter は **必ず** `trigger / description / slug` を持つ（descriptionは二重引用符推奨）
- `slug` は kebab-case（例: `integrate-discovery-artifacts`）
- `trigger` は原則 **`manual`**（常用）  
  `model_decision` は「状況で使い分けたい共通手順」のみ
- `always_on` / `glob` は workflow では基本使わない（運用が壊れやすい）
- 破壊的操作は **承認必須**（turbo を付けない）

---

# 手順

## Step 1: タスクのヒアリング（目的と境界を固定）
ユーザーから以下を収集する。未確定は未確定のままでOKだが、曖昧な場合は具体質問で補完する。

1. **ゴール（Goal）**: 最終的に何を達成したいか
2. **対象（Scope）**: どのプロジェクト/ディレクトリ/リポジトリ/環境が対象か
3. **入力（Inputs）**: 必要な情報（URL、ブランチ、環境名、設定値など）
4. **成果物（Outputs）**: 生成/更新されるファイルや状態
5. **承認ポイント（Approvals）**: ユーザー承認が必要な操作（push/削除/デプロイ等）
6. **使用ツール（Tools）**: ターミナル、ブラウザ、生成ツール、CI 等

**このStepの成果（必須）**
- 1行サマリー: `<Goal + Scope>`
- Done条件: `<成功と判断できる状態>`
- 失敗条件: `<中断/ロールバックが必要な状態>`

---

## Step 2: ステップの分解（1ステップ=1アクション）
分解基準：
- 1ステップ = 1つの明確なアクション
- 依存関係（前の成果物が必要か）を明示
- 独立しているものは並列化検討（ただし運用上は「順次」が無難な場合が多い）

ステップ分類：
| 種類 | 内容 | 例 |
|---|---|---|
| 分析 | 情報収集・現状把握 | ファイル/差分/設定の確認 |
| 計画 | 方針策定・選択肢提示 | 実装方針、代替案 |
| 実行 | 生成/変更/操作 | ファイル作成、設定更新 |
| 検証 | 確認/テスト | lint/test/build/スモーク |
| 報告 | 結果提示 | 変更点、次アクション |

**このStepの成果**
- ステップ一覧（番号付き）
- 依存関係メモ（Step A の出力が Step B に必要、など）

---

## Step 3: Turbo の判定（安全ガード）
`// turbo` は「承認不要で機械的に進めてよい」工程の目印。  
危険操作は turbo 禁止。

### Turbo 適用可（例）
- 読み取り: `git status`, `ls`, `cat`, `grep`
- 静的検証: `lint`, `format check`, `typecheck`
- テスト/ビルド: `test`, `build`（外部課金/外部書き込みが無い場合）

### Turbo 適用不可（例）
- ファイル削除、リネーム大量、上書き
- `git push`, `merge`, `rebase`, `force push`
- デプロイ/リリース/タグ作成
- 外部APIへの書き込み、課金が発生し得る操作
- DB/本番相当への変更

**このStepの成果**
- 各ステップの turbo 可否と理由
- 承認ポイントの明確化（どこで止めるか）

---

## Step 4: エラーハンドリング設計（止め方を決める）
各ステップについて「想定エラーと対処」を決める。  
原則：**自動で危険なリトライをしない**。

テンプレ：

```text
ステップ: <Step N: ...>
想定エラー:
  - <error1>: <対処（情報収集→ユーザー報告→中断/継続）>
  - <error2>: <対処>
最大リトライ: <0-1（原則少なめ）>
失敗時: <中断して報告 / 代替案提示>
```

---

## Step 5: ワークフロー構造の設計（Convoyテンプレ）
Convoy workflow は以下を含むと運用しやすい：

- 目的（Purpose）
- 入力（Inputs）
- 成果物（Outputs）
- 手順（Steps）
- 承認ポイント（Approvals）
- 検証（Evidence）

テンプレ：

```markdown
---
trigger: "manual"
description: "<ワークフローの目的を1-2文で>"
slug: "<kebab-case>"
---
# <ワークフロー名>

## 目的
- <何を達成するか>

## 入力（Inputs）
- <必要な情報>

## 成果物（Outputs）
- <生成/更新されるファイルや状態>

## 承認ポイント（Approvals）
- <承認が必要な操作を列挙>

## 手順
### Step 1: <...> // turbo
...

### Step N: <...>
...（承認が必要なら明記して停止）

## 検証（Evidence）
- <実行コマンド/確認観点>

## 完了報告（Report）
- <何をどう報告するか>
```

---

## Step 6: slug / ファイル名の決定（呼び出しコマンドと一致）
- 形式: `<verb>-<object>.md`（例: `create-release.md` → `/create-release`）
- kebab-case、小文字
- “何をするか” が一目で分かる動詞を先頭にする（create/setup/integrate/review/generate 等）

---

## Step 7: 既存 workflow / rule との整合性（重複を作らない）
`.agent/workflows/` と `.agent/rules/` を確認し、以下を行う：

1. **重複チェック**: 同等の workflow が既にないか
2. **再利用可能性**: 既存 workflow を呼び出す設計にできないか（統合/オーケストレーション）
3. **命名整合**: 既存の命名規則（動詞・対象）と整合しているか
4. **ルール適合**: 既存ルール（security/type-safety 等）に違反しないか

問題があれば、次の形式で報告：

- 重複候補: `/existing-workflow`
- 差分: `<何が違う>`
- 対処案: `統合 / 置換 / 新規`

---

## Step 8: ワークフローファイルの生成
- 保存先: `.agent/workflows/<slug>.md`
- frontmatter は必ず:
  - `trigger`（通常 `"manual"`）
  - `description`（二重引用符）
  - `slug`（ファイル名と一致）

---

## Step 9: 検証（品質ゲート）
作成した workflow を検証する：

1. **frontmatter 構文**: YAMLとして解釈できるか（キー漏れ/型不一致）
2. **論理性**: 順序・依存関係が正しいか
3. **指示の明確さ**: エージェントが迷わない粒度か（入力/出力が書かれているか）
4. **turbo 安全性**: 危険操作に turbo が付いていないか
5. **承認ポイント**: push/削除/デプロイ前に必ず止まるか
6. **SoT参照**: スタック/品質ゲートが brief.md に寄っているか

---

## Step 10: 完了報告（テンプレ）
```markdown
## ✅ create-workflow 完了

- 生成ファイル: `.agent/workflows/<slug>.md`
- 呼び出しコマンド: `/<slug>`
- 目的: <1行>
- 成果物: <Outputs>
- 承認ポイント: <Approvals>
- 検証: <Evidence>
- 関連: <rules/workflows>
```

---

## 付録: オーケストレーション（他 workflow を呼ぶときの注意）
- “呼び出しだけ” の統合 workflow を作る場合は `model_decision` を検討してよい
- 結果の集約は **チェックリスト形式**で残す（Pass/Risk/Action）
- 危険操作を含む workflow を内包する場合、統合側でも承認ポイントを明示する


