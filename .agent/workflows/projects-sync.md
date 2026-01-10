---
slug: "projects-sync"
description: "Convoy母艦の manifest を正として、CONVOY_PROJECT 配下の独立プロダクト群を clone/pull で同期する。新規プロダクト追加はGitHub ActionsでPR自動生成する。"
trigger: "manual"
---

# 🔁 Convoy Projects Sync（Product Factory / Polyrepo）

## 🎯 Goal
- Convoy（母艦）リポジトリから、`projects/manifest.json` を正として  
  `CONVOY_PROJECT/<RepoName>` に各プロダクトを **clone / update（pull）** する。
- 新規プロダクト追加は **Convoy側のGitHub Actions**（workflow_dispatch）で manifest 追記PRを自動生成し、レビュー→マージで反映する。

---

## ✅ Preconditions（事前条件）
### 1) ローカル構成
- Convoy repo をローカルに clone 済み（例：`C:\Users\<user>\convoy`）
- `.gitignore` に `CONVOY_PROJECT/` があり、母艦では追跡しない

### 2) ツール
- Node >= 20
- pnpm（package.json の packageManager に準拠）
- Git
- PowerShell（`pwsh`）

### 3) SSH（推奨）
- GitHub に SSH 公開鍵を登録済み
- 接続確認: `ssh -T git@github.com` が成功する

---

## 🧭 Daily Operation（普段の運用）

### A. 既存プロダクトを最新にする（最頻出）
> GitHub画面は不要。ローカルで完結。

1) Convoy ルートへ移動
```powershell
cd C:\Users\<user>\convoy
```

2) 母艦側（manifest/スクリプト）の更新を取り込む（必要に応じて）
```powershell
git pull
```

3) manifest 検証（壊れていないことを保証）
```powershell
pnpm projects:validate
```

4) 全プロダクト同期（clone / update）
```powershell
pnpm projects:sync
```

---

### B. パスフレーズ入力を減らしたい（任意）
> セッション開始時に1回だけ鍵をロード（環境により保持されない場合あり）

```powershell
ssh-add $env:USERPROFILE\.ssh\id_ed25519
ssh-add -l
```

---

### C. 既存プロダクトを開発してpushする
> Convoyではなく、各プロダクトRepo内で作業する。

```powershell
cd .\CONVOY_PROJECT\Aqua_Ritual
git status
git add .
git commit -m "feat: ..."
git push
```

---

## ➕ Add New Product（新規プロダクト追加：ActionsでPR自動作成）
> 追加作業は「Convoy Repo（GitHub Web）」側で実行する。  
> ローカルはマージ後に `git pull` + `pnpm projects:sync` で反映。

### 1) GitHub（Web）
- GitHub → Convoy リポジトリ → **Actions**
- Workflow: **Add product to manifest (PR)** を選択
- **Run workflow** で以下を入力：
  - `name`: Repo名＝フォルダ名（例 `Aqua_Ritual`）
  - `repo`: `git@github.com:<Owner>/<Repo>.git`
  - `branch`: `main`
  - `onDirty`: `abort`（基本は安全側）

### 2) PRが作られる
- Convoy repo → Pull requests でPRを確認
- 内容確認 → Merge

### 3) ローカルへ反映
```powershell
cd C:\Users\<user>\convoy
git pull
pnpm projects:validate
pnpm projects:sync
```

---

## 🧯 Guard Rails（事故防止の標準）
### 1) pull は fast-forward only
- `projects-sync.ps1` は `git pull --ff-only` を使う
- ローカルの履歴改変や意図しないマージコミットを防止

### 2) ローカル変更（Dirty）時の扱い（manifestの onDirty）
- `abort`: 変更があれば同期を中断（推奨）
- `stash`: stash→pull→stash pop（便利だが衝突時に作業が必要）
- `skip`: そのプロダクトだけスキップして続行

---

## 🔎 Troubleshooting（よくある障害）

### SSH: Permission denied (publickey)
- `ssh -T git@github.com` が通るか確認
- `~/.ssh/id_ed25519.pub` がGitHubに登録済みか確認

### Passphraseが毎回出る
- 運用上は問題なし（手間のみ）
- 減らしたい場合: `ssh-add ~/.ssh/id_ed25519`（セッション毎）

### Dirty working tree detected で止まる
- 変更をコミット or 破棄（推奨）
- どうしても回すなら `onDirty` を `stash` または `skip` に変更して再同期

---

## ✅ Expected Outputs（成功状態）
- `CONVOY_PROJECT/<RepoName>` 配下に各プロダクトが存在
- `pnpm projects:sync` 実行で "Update" または "Clone" が正常に進む
- 新規追加は Actions → PR → Merge → ローカル sync で反映される
