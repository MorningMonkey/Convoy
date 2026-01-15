---
trigger: "manual"
description: ".agent/INDEX.md を自動更新し、現在の Workflows/Rules/Templates 構成と同期させる。"
slug: "update-agent-index"
---
# update-agent-index — INDEX.md の更新

## 目的
- `.agent/INDEX.md` の自動生成パート（Workflows/Rulesテーブル）を、現在のファイルシステムの状態に合わせて最新化する。
- 新しいワークフローやルールの追加後、あるいは `git-auto-commit` の前に実行することで、ドキュメントの整合性を保つ。

## 入力（Inputs）
- なし（ファイルシステムをスキャン）

## 成果物（Outputs）
- 更新された `.agent/INDEX.md`

## 承認ポイント（Approvals）
- なし（安全なローカル更新のみ）

## 手順
### Step 1: INDEX更新スクリプトの実行
// turbo
`scripts/generate_agent_index.py` を実行し、INDEX.md を上書き更新する。

```bash
python scripts/generate_agent_index.py --index .agent/INDEX.md --write
```

## 検証（Evidence）
- `git diff .agent/INDEX.md` で変更を確認する（変更がない場合もある）。

## 完了報告（Report）
- INDEX.md が最新化された旨を報告。
