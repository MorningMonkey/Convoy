# Smoke Test Gates (Standard)

これらは必須要件 (Hard Requirements) です。一つでも失敗した場合、Run全体が「FAIL」となります。

- **G1**: タップターゲット（ボタン/行/アイコン等）は、少なくとも一辺が **44px以上** である（両辺44px推奨）。
- **G2**: 長いテキスト（名前/ID等）によってレイアウトが崩れない。折り返しまたは省略（truncation）が意図されていること。
- **G3**: プライマリアクションは視覚的に目立ち、セカンダリアクションと競合していない。
- **G4**: セマンティック構造（Header / Content / Footer）が適切であり、絶対配置 (fixed/absolute) に過度に依存していないこと。
- **G5**: キーボード操作時のフォーカススタイルが存在し、フォーカス時にレイアウトがずれないこと。

## 厳格なスモークテスト (Hard Gates)

### G-KEYBOARD-01: すべての操作要素が Tab でフォーカス可能
**合格基準 (Pass criteria)**
- 主要画面（対象Specのスコープ）に存在する以下が **Tab/Shift+Tab** で到達可能
  - `<button>` / `<a>` / input / select / textarea / role="button" 等の「操作要素」
- フォーカス順が論理的（視線順・読み順に概ね一致）で、フォーカストラップがない
- フォーカス可視化がある（focus ring / outline 等が見える）

**失敗例 (Fail examples)**
- クリックできるのに Tab では到達できない要素がある（div onClick 等）
- Tab を押すとフォーカスが消える／ループする
- フォーカスが当たっているのに見えない（可視化ゼロ）

**検証方法 (How to verify)**
- キーボードのみで操作（マウス禁止）
- Tab で全操作要素を一巡できることを確認
- 必要なら “見えないボタン” を DOM から特定（buttonでない場合は要修正）

---

### G-ROUTING-01: 意図しない 404 遷移がない
**合格基準 (Pass criteria)**
- アプリ内導線（ヘッダー/ナビ/主要CTA/内部リンク）を辿って **意図しない 404** に到達しない
- 404ページが存在すること自体は許容（ただし「壊れリンク」で到達しない）
- ルーティング定義（router）とリンク先（href/to）が整合

**失敗例 (Fail examples)**
- 内部リンクが存在しないパスを参照している
- trailing slash / params の不整合で 404 になる
- basePath 設定漏れで 404 になる（特にSPA/静的ホスティング）

**検証方法 (How to verify)**
- 画面内リンクを全クリック（対象Spec範囲）
- Router定義（routes）とリンク先を突合
- 404 が出た場合、どのリンクから来たかを必ず記録（review.md に “入口” を残す）

---

### G-SECURITY-01: 平文の秘密情報（APIキー等）が含まれない
**合格基準 (Pass criteria)**
- リポジトリ追跡対象（tracked files）に以下が含まれない
  - API keys / tokens / private keys / secret strings
- 例外：ダミーキー（`DUMMY_...` 等）であることが明確なものは可（ただし本番実装に混入しない）

**失敗例 (Fail examples)**
- `sk-...` / `AIza...` / `-----BEGIN PRIVATE KEY-----` / `apiKey: "..."` 等がコミット対象に存在
- `.env` 相当が追跡されている

**検証方法 (How to verify)**
- `git grep`（または同等）でパターン検索し、ヒット0であること
- ヒットがある場合、環境変数化 or Secret Manager 前提へ移行して修正
