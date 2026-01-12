---
slug: "run-tests"
description: "プロジェクトの単体/自動テストをSoT（brief.md）に従って実行し、PASS/FAIL/PASS_WITH_SKIPPED を根拠（失敗/スキップ要約）つきで報告する原子ワークフロー。"
trigger: "manual"
---
# 🧪 run-tests — テスト実行

このワークフローは **実行と報告のみ** を行います。  
テスト修正や実装修正は別ワークフロー（例: `bug-fix`）へ切り出します。

---

## 定義（このワークフローの狙い）
- テストを実行し、結果を **機械的に分類**（PASS / FAIL / PASS_WITH_SKIPPED）して報告する
- 失敗時に、次の手が打てるだけの **根拠（失敗テスト・理由）** を残す
- 実行コマンドは **SoT（brief.md）** を優先し、ない場合のみフォールバックする

---

## SoT（Source of Truth）
- テスト方針/コマンド: `assets/branding/<productId>/brief.md`
- 利用可能コマンド一覧: `.agent/INDEX.md`
- 関連（任意）: `.agent/rules/*.md`（quality/security 等）

---

## 入力（Inputs）
- 対象ブランチ/コミット（任意）
- 実行範囲（任意）：全テスト / 特定パス / 特定スイート
- 実行環境（任意）：Node/Flutter/Python 等  
  ※ 最終判断は brief.md を正本とする

---

## 成果物（Outputs）
- 判定: `PASS` / `FAIL` / `PASS_WITH_SKIPPED`
- 実行したコマンド（Evidence）
- 実行サマリー（総数、成功/失敗/スキップ、実行時間）
- 失敗テスト（最大5件、理由要約）
- 推奨次アクション（例: bug-fix で収束、テストフレイク対策）

---

## 安全ガード（Convoy標準）
- `// turbo` 可（検証のみ）
- 依存追加・設定変更・ファイル削除・push は行わない
- “落ちたから直す” はこの workflow ではしない（別に切る）

---

# 手順

## Step 1: 前提確認（軽量） // turbo
- リポジトリ直下で実行されているか
- 主要設定（package.json / pubspec / pytest設定 など）が存在するか

```bash
pwd
ls -la
```

---

## Step 2: 実行コマンドの決定（SoT優先） // turbo
優先順位：

1. `assets/branding/<productId>/brief.md` に記載の test コマンド
2. `package.json` scripts の `test`
3. フォールバック（検出順で試す）

---

## Step 3: テスト実行 // turbo
### Node（pnpm/npm/yarn）フォールバック例
```bash
pnpm -s test || npm test --silent || yarn -s test
```

### Python の例
```bash
pytest
```

### Flutter の例
```bash
flutter test
```

> 注意: 複数候補を試した場合、実行順序を Evidence として報告に残す。

---

## Step 4: 結果判定（分類ルール）
- **成功**: 全テスト通過 → `PASS`
- **失敗**: 失敗したテストあり → `FAIL`
- **スキップあり**: スキップされたテストがあるが失敗なし → `PASS_WITH_SKIPPED`

> ツールが “skip” を明示しない場合は、出力から推定し、曖昧なら `PASS` または `FAIL` のどちらかに倒す（理由を記載）。

---

## Step 5: 出力要約（最大5件） // turbo
以下を報告する：

- 総テスト数（分かる範囲で）
- 成功/失敗/スキップの内訳（分かる範囲で）
- 失敗したテスト名と理由（最大5件）
- 実行時間（分かる範囲で）
- 失敗がある場合の推奨次アクション（例: `bug-fix` で再現→原因→修正→回帰証明）

---

# 完了報告テンプレ

```markdown
## 🧪 run-tests 結果

- 判定: PASS / FAIL / PASS_WITH_SKIPPED
- コマンド（Evidence）: <実行したコマンド（試した順）>
- 対象: <ブランチ/コミット（任意）>

### サマリー
- 合計: <N>（不明なら“不明”）
- 成功: <N>
- 失敗: <N>
- スキップ: <N>
- 実行時間: <...>

### 失敗（最大5件）
1. <test name> — <reason>
2. ...
3. ...

### スキップ（最大5件）
1. <test name> — <reason/marker>
2. ...

### 次のアクション（推奨）
- <例: bug-fix に移行して再現テスト→原因→修正→再実行>
```


