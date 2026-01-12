---
slug: "git-policy"
description: "Convoyプロジェクトのバージョン管理におけるコミット粒度、Push義務、メッセージ規約、および事故防止のための品質基準を定義する。"
trigger: "model_decision"
---

# 🛡️ Git Policy & Standards

## 🌌 Overview
本ドキュメントは、Convoy（Mission Control）の開発ワークフローにおける Git 運用の行動規範を定義する。
開発者およびエージェントは、本ポリシーに従ってコミット、プッシュ、マージを行う義務がある。
目的は「履歴の可読性担保」「最新状態の共有」「事故防止」である。

## ⚖️ Rules / Constraints

### 1. MUST: Atomic Commit（1目的）
- **One Logical Change**: 1つのコミットには「1つの論理的な変更（目的）」のみを含める。
- **Separation**: 機能追加（feat）とリファクタリング（refactor）、フォーマット修正（style）は混ぜずに分割する。
- **Justification**: 後からのRevertやCherry-pick、履歴解読を容易にするため。

### 2. MUST: Push Timing（Pushタイミング）
- **Task Completion**: 作業単位（画面の実装、チケットの消化、論理ブロックの完了）が終わったら必ずPushする。
- **Interruption**: 離席、端末移動、タスク切り替えの際は、作業途中であってもPushする（"Leave No Trace"）。
- **Before PR**: Pull Request を作成する前に、必ずローカルの変更を全てPushする。
- **Prohibition**: 「動作確認できていないから」「後でまとめて」という理由でローカルにコミットを溜め込まない。必要ならWIPとしてPushする。

### 3. MUST: No Direct Commit to Main（main直コミット禁止）
- **Branch Workflow**: 原則として `main` (または `master`) ブランチへの直接コミットを禁止する。必ず `feature/xxx` や `fix/xxx` ブランチを経由し、PR/Mergeを行う。
- **Exception**:
  - 緊急のHotfix（CI通過済み）
  - 軽微なドキュメント修正（README等）
  - 初期構築フェーズで承認された場合

### 4. MUST: Commit Messages（メッセージ規約）
- **Header Structure**: `<type>: <subject>`
  - `type`: `fix` (バグ修正), `feat` (機能追加), `docs` (ドキュメント), `refactor` (リファクタ), `chore` (雑務), `test` (テスト), `perf` (パフォーマンス), `style` (フォーマット)
  - `subject`: 日本語で記述する。短潔に、命令形で書く（「〜を修正」）。
  - 絵文字の使用は任意だが、視認性向上のため推奨される。
- **Body**:
  - 3行程度の箇条書きで詳細を記述する。
  - 「なぜ変更したか」「何をしたか」に焦点を当てる。
- **Example**:
  ```text
  fix: 🐛 ログイン時のnull参照エラーを修正
  
  - ユーザーオブジェクト未取得時のガード句を追加
  - エラーハンドリングのログ出力を強化
  - 関連ユニットテストを追加
  ```

### 5. SHOULD: Verify Before Merge（検証）
- マージ（またはPR作成）前に、必ずローカルで最小限の検証（Lint, Type Check, Unit Test）を行うこと。
- `verify-code` ワークフローの通過を推奨する。

### 6. MODE: Merge Strategy（Merge方式）
プロジェクトの方針またはリーダーの指示に従い、以下のいずれかを採用する。

- **Mode A (History Focus)**: `--no-ff` (Merge Commit)。履歴を統合せず、機能開発の文脈を残す。チーム開発や複雑な機能向け。
- **Mode B (Log Focus)**: Squash Merge。履歴を一直線にする。個人開発や小規模な修正向け。

### 7. EXCEPTIONS（例外）
- **Offline**: 通信環境がない場合は、ローカルコミットを許容するが、復帰次第即座にPushすること。
- **WIP**: 実験的なコードや一時保存の場合は、メッセージ先頭に `wip:` を付与し、品質担保の対象外であることを明示する。

### 8. SAFETY（事故防止）
- **Secrets**: APIキー、パスワード、トークン等の機密情報をコミットしない。疑わしいファイルは `.gitignore` する。
- **Large Binaries**: 動画、高解像度画像、バイナリファイル等を無制限にリポジトリへ追加しない。Git LFSの使用を検討する。
