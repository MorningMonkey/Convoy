# UX Scorecard (Standard) — 100 points

## 明確性 (Clarity) — 10 pts
- ラベルは曖昧さがなく明確である
- 情報階層が整理されている
- ユーザーは常に「自分がどこにいるか」を理解できる

## 効率性 (Efficiency) — 10 pts
- 主要な操作パスは最小限のステップで完結する
- 操作要素が届きやすい位置にある（親指フレンドリー）
- デフォルト設定によりユーザーの労力が軽減されている

## エラー防止 (Error prevention) — 10 pts
- 破壊的な操作にはガード（確認など）が存在する
- バリデーションメッセージは具体的で修正可能である
- 無効な状態では操作自体ができないようになっている

## アクセシビリティ (Accessibility) — 10 pts
- タップターゲットが 44px 以上ある
- コントラスト比が適切である
- フォーカス状態が存在する

## 視覚的階層 (Visual hierarchy) — 10 pts
- プライマリとセカンダリの視覚的な区別がある
- スペースと整列が一貫している
- 文字組みはスキャン（流し読み）しやすい

## 一貫性 (Consistency) — 10 pts
- 同じパターンは同じ挙動をする
- アイコンとラベルの使い方が統一されている
- トークン/変数の使用が一貫している

## パフォーマンス (Objective) — 20 pts

### P-LCP-01: LCP (Largest Contentful Paint)
**計測条件 (レビュー時に明記)**
- 計測対象: 対象ページ（spec範囲の代表画面）
- 計測手段: Lighthouse（推奨）または Web Vitals 計測
- モード: Mobile (simulated) を推奨
- 1回ではなく 3回測定し、中央値を採用

**採点基準 (Scoring)**
- 20 pts: LCP <= 1.2s
- 15 pts: LCP <= 1.8s
- 10 pts: LCP <= 2.5s
- 5 pts : LCP <= 3.0s
- 0 pts : > 3.0s または未計測（未計測は “未計測” と明記）

**備考 (Notes)**
- 画像/動画などが主因の場合は、最適化案（圧縮・遅延読み込み・サイズ指定）を “Concrete fixes” に必ず書く


## 視覚的再現度 (Objective) — 20 pts

### V-COLOR-01: Figma Variables との色差 (ΔE)
**定義 (Definition)**
- ΔE は CIEDE2000 を推奨
- 比較対象:
  1) 実装側で最終的にレンダリングされる主要色（text/bg/border/actionの代表）
  2) Figma Variables の対応トークン色

**合格/採点基準 (Pass/Score conditions)**
- 20 pts: 主要色すべて ΔE <= 3
- 15 pts: 主要色の 90% が ΔE <= 3、残りも ΔE <= 5
- 10 pts: 主要色の 80% が ΔE <= 3、残りも ΔE <= 8
- 0 pts : 乖離が大きい、または未検証（未検証は “未検証” と明記）

**運用上のショートカット (推奨)**
- 実装側で “生hex” を使わず、トークン（Tailwind theme / CSS variables mapping）経由に統一できている場合、
  ΔE 検証は “一致（ΔE=0相当）” とみなし、対象色を列挙して証跡を残せば満点扱い可
  （ただし、そのトークンが Figma token と一致していることが前提）

**証跡要件 (Evidence requirements)**
- 対象色リスト（最低: text primary, bg surface, primary action default/hover, border）を review.md に列挙
- 計測方法（スクリプト/ツール/サンプル点）を 1 行で明記
