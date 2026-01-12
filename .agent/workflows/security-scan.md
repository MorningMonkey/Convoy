---
slug: "security-scan"
description: "依存関係脆弱性・シークレット混入・基本セキュリティ規約違反をSoT（brief.md）と既存ルールに従って検査し、PASS/PASS_WITH_WARNINGS/FAIL を根拠つきで報告する原子ワークフロー。"
trigger: "manual"
---

# 🔐 security-scan — セキュリティスキャン

このワークフローは **検査と報告のみ** を行います。  
修正（依存更新・コード修正・シークレット無効化など）は別ワークフローに切り出し、必要ならユーザー承認を取ります。

---

## 定義（このワークフローの狙い）
- 依存関係の脆弱性（SCA）を検査し、重大度別に要約する
- コード/設定への **シークレット混入** を検出する（可能な範囲で）
- 既存のセキュリティルール（例: security-mandates）に反するパターンを機械的に点検する
- 結果を `PASS / PASS_WITH_WARNINGS / FAIL` で分類し、**次にやるべき修正**を提示する

---

## SoT（Source of Truth）
- スタック/運用方針: `assets/branding/<productId>/brief.md`
- セキュリティルール: `.agent/rules/*security*.md`（例: `security-mandates`）
- 利用可能コマンド一覧: `.agent/INDEX.md`
- 管制仕様: `ANTIGRAVITY_AGENT_CONTROL_SPEC.md`

---

## 入力（Inputs）
- 対象ブランチ/コミット（任意）
- 実行環境（任意）：Node/Flutter/Python 等（最終判断は brief.md を正本とする）
- スキャン対象範囲（任意）：repo全体 / 特定ディレクトリ

---

## 成果物（Outputs）
- 判定: `PASS` / `PASS_WITH_WARNINGS` / `FAIL`
- 実行コマンド（Evidence）
- 脆弱性の内訳（Critical/High/Medium/Low：分かる範囲で）
- 検出事項の要約（最大10件）
- 推奨次アクション（依存更新、secret無効化、修正方針）

---

## 安全ガード（Convoy標準）
- `// turbo` 可（検査のみ）
- 修正（依存更新、設定変更、push、secret rotate）はしない
- 重大な検出があれば、**公開前に止める**（FAIL）

---

# 手順

## Step 1: 前提確認（軽量） // turbo
```bash
pwd
ls -la
```

---

## Step 2: 依存関係の脆弱性チェック（SCA） // turbo
SoT（brief.md）に指定があればそれを最優先。なければ以下をフォールバックとして実行する。

### Node（pnpm/npm/yarn）例
```bash
pnpm audit || npm audit || yarn audit
```

### Python 例
```bash
pip-audit
```

### Flutter/Dart（プロジェクトがFlutterの場合）
> pub の監査はツール環境に依存するため、brief.md の指定を優先する。  
> 指定が無い場合は “実行できない” を報告し、Action を提示する。

---

## Step 3: シークレット検出（簡易） // turbo
目的：コード/設定に **誤って秘密情報が混入**していないかを早期検出する。

### 3.1 既知パターン（簡易 grep）
以下は “誤検知あり” 前提の簡易検出。検出した場合は **内容をそのまま貼らず**、ファイルパスと周辺状況だけを報告する。

```bash
# 例: 秘密鍵/トークンっぽい文字列、AWSキーっぽい形式など（簡易）
grep -RIn --exclude-dir=node_modules --exclude-dir=.git   -E "BEGIN (RSA|OPENSSH|EC) PRIVATE KEY|AKIA[0-9A-Z]{16}|xox[baprs]-|sk-[A-Za-z0-9]{20,}" . || true
```

### 3.2 .env / 認証情報ファイルの追跡
- `.env` / `.env.*` がコミット対象になっていないか
- `*.pem`, `*.key`, `id_rsa` 等が混入していないか

```bash
git ls-files | grep -E "\.env(\.|$)|\.pem$|\.key$|id_rsa$" || true
```

> 本格運用では secret scanner（例: gitleaks 等）を導入するのが望ましい。  
> ただしこの workflow は “導入” までは行わない（別途承認）。

---

## Step 4: セキュリティ規約違反チェック（静的パターン） // turbo
`security-mandates` 等のルールに基づき、代表的な禁止パターンを検出する。

### 例（代表チェック：環境差あり）
- `eval(` の使用
- SQL文字列連結（疑い）
- サニタイズなし入力の直使用（疑い）

```bash
# eval（JS/TS）
grep -RIn --exclude-dir=node_modules --exclude-dir=.git "eval\(" . || true

# SQL連結の疑い（言語横断で雑に拾う）
grep -RIn --exclude-dir=node_modules --exclude-dir=.git -E "SELECT .*\+|INSERT .*\+|UPDATE .*\+" . || true
```

> ここは “疑い検知” が中心。誤検知は許容し、報告で整理する。

---

## Step 5: 結果判定（分類ルール）
- **PASS**: 重大度 High/Critical が 0、secret混入なし、規約違反なし
- **PASS_WITH_WARNINGS**: Low/Medium のみ、または疑い検知のみ（要確認）
- **FAIL**: Critical/High の脆弱性、secret混入の疑い（高確度）、明確な規約違反（危険）がある

> “secret混入” は原則 FAIL 扱い（公開前に止める）。

---

# 完了報告テンプレ

```markdown
## 🔐 security-scan 結果

- 判定: PASS / PASS_WITH_WARNINGS / FAIL
- コマンド（Evidence）: <実行したコマンド（試した順）>
- 対象: <ブランチ/コミット（任意）>

### 依存脆弱性（SCA）
- Critical: <N>
- High: <N>
- Medium: <N>
- Low: <N>
- 主な指摘（最大10件）:
  1. <package> <version> — <severity> — <hint>
  2. ...

### シークレット検出
- 検出: あり/なし
- 対象（ファイル/箇所）: <file:line>（内容は貼らない）
- 推奨: <無効化/削除/履歴対応/ローテーションの要否>

### 規約違反チェック
- eval: <件数>
- SQL連結疑い: <件数>
- その他: <...>

### 次のアクション（推奨）
- <依存更新、secret対応、ルール追加、CI導入 等>
```


