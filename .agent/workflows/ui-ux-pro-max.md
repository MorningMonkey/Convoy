---
description: UIの計画と実装
slug: "ui-ux-pro-max"
trigger: "manual"
auto_execution_mode: 3
---

# UI/UX Pro Max - デザインインテリジェンス

UIスタイル、カラーパレット、フォントの組み合わせ、チャートタイプ、製品の推奨事項、UXガイドライン、およびスタック固有のベストプラクティスを検索可能なデータベースです。

## 前提条件

Pythonがインストールされているか確認してください：

```bash
python3 --version || python --version
```

Pythonがインストールされていない場合は、OSに合わせてインストールしてください：

**macOS:**
```bash
brew install python3
```

**Ubuntu/Debian:**
```bash
sudo apt update && sudo apt install python3
```

**Windows:**
```powershell
winget install Python.Python.3.12
```

---

## このワークフローの使い方

ユーザーがUI/UX作業（設計、構築、作成、実装、レビュー、修正、改善）を要求した場合、以下のワークフローに従ってください：

### ステップ 1: ユーザー要件の分析

ユーザーの要求から重要な情報を抽出します：
- **製品タイプ**: SaaS、Eコマース、ポートフォリオ、ダッシュボード、ランディングページなど
- **スタイルキーワード**: ミニマル、遊び心のある、プロフェッショナル、エレガント、ダークモードなど
- **業界**: ヘルスケア、フィンテック、ゲーム、教育など
- **スタック**: React、Vue、Next.js、またはデフォルトの `html-tailwind`

### ステップ 2: 関連ドメインの検索

`search.py` を複数回使用して、包括的な情報を収集します。十分なコンテキストが得られるまで検索してください。

```bash
python3 .shared/ui-ux-pro-max/scripts/search.py "<keyword>" --domain <domain> [-n <max_results>]
```

**推奨される検索順序:**

1. **Product (製品)** - 製品タイプのスタイル推奨事項を取得
2. **Style (スタイル)** - 詳細なスタイルガイド（色、効果、フレームワーク）を取得
3. **Typography (タイポグラフィ)** - Google Fontsのインポートを含むフォントの組み合わせを取得
4. **Color (色)** - カラーパレット（プライマリ、セカンダリ、CTA、背景、テキスト、ボーダー）を取得
5. **Landing (ランディング)** - ページ構成を取得（ランディングページの場合）
6. **Chart (チャート)** - チャートの推奨事項を取得（ダッシュボード/分析の場合）
7. **UX** - ベストプラクティスとアンチパターンを取得
8. **Stack (スタック)** - スタック固有のガイドラインを取得（デフォルト: html-tailwind）

### ステップ 3: スタックガイドライン (デフォルト: html-tailwind)

ユーザーがスタックを指定しない場合、**`html-tailwind` をデフォルトとします**。

```bash
python3 .shared/ui-ux-pro-max/scripts/search.py "<keyword>" --stack html-tailwind
```

利用可能なスタック: `html-tailwind`, `react`, `nextjs`, `vue`, `svelte`, `swiftui`, `react-native`, `flutter`, `shadcn`

---

## 検索リファレンス

### 利用可能なドメイン

| ドメイン | 用途 | キーワード例 |
|--------|---------|------------------|
| `product` | 製品タイプの推奨事項 | SaaS, e-commerce, portfolio, healthcare, beauty, service |
| `style` | UIスタイル、色、効果 | glassmorphism, minimalism, dark mode, brutalism |
| `typography` | フォントの組み合わせ、Google Fonts | elegant, playful, professional, modern |
| `color` | 製品タイプ別のカラーパレット | saas, ecommerce, healthcare, beauty, fintech, service |
| `landing` | ページ構成、CTA戦略 | hero, hero-centric, testimonial, pricing, social-proof |
| `chart` | チャートタイプ、ライブラリ推奨 | trend, comparison, timeline, funnel, pie |
| `ux` | ベストプラクティス、アンチパターン | animation, accessibility, z-index, loading |
| `prompt` | AIプロンプト、CSSキーワード | (style name) |

### 利用可能なスタック

| スタック | 焦点 |
|-------|-------|
| `html-tailwind` | Tailwindユーティリティ、レスポンシブ、アクセシビリティ (デフォルト) |
| `react` | State、フック、パフォーマンス、パターン |
| `nextjs` | SSR、ルーティング、画像、APIルート |
| `vue` | Composition API、Pinia、Vue Router |
| `svelte` | Runes、ストア、SvelteKit |
| `swiftui` | Views、State、ナビゲーション、アニメーション |
| `react-native` | コンポーネント、ナビゲーション、リスト |
| `flutter` | Widgets、State、レイアウト、テーマ |
| `shadcn` | shadcn/uiコンポーネント、テーマ、フォーム、パターン |

---

## ワークフロー例

**ユーザーの要求:** "スキンケアサービスのランディングページを作成したい"

**AIの対応:**

```bash
# 1. 製品タイプを検索
python3 .shared/ui-ux-pro-max/scripts/search.py "beauty spa wellness service" --domain product

# 2. スタイルを検索 (業界に基づく: beauty, elegant)
python3 .shared/ui-ux-pro-max/scripts/search.py "elegant minimal soft" --domain style

# 3. タイポグラフィを検索
python3 .shared/ui-ux-pro-max/scripts/search.py "elegant luxury" --domain typography

# 4. カラーパレットを検索
python3 .shared/ui-ux-pro-max/scripts/search.py "beauty spa wellness" --domain color

# 5. ランディングページの構成を検索
python3 .shared/ui-ux-pro-max/scripts/search.py "hero-centric social-proof" --domain landing

# 6. UXガイドラインを検索
python3 .shared/ui-ux-pro-max/scripts/search.py "animation" --domain ux
python3 .shared/ui-ux-pro-max/scripts/search.py "accessibility" --domain ux

# 7. スタックガイドラインを検索 (デフォルト: html-tailwind)
python3 .shared/ui-ux-pro-max/scripts/search.py "layout responsive" --stack html-tailwind
```

**その後:** すべての検索結果を統合し、デザインを実装します。

---

## より良い結果を得るためのヒント

1. **キーワードを具体的にする** - "app" よりも "healthcare SaaS dashboard"
2. **複数回検索する** - 異なるキーワードで異なる洞察が得られます
3. **ドメインを組み合わせる** - Style + Typography + Color = 完全なデザインシステム
4. **常にUXを確認する** - "animation", "z-index", "accessibility" で一般的な問題を検索
5. **スタックフラグを使用する** - 実装固有のベストプラクティスを取得
6. **反復する** - 最初の検索が一致しない場合は、別のキーワードを試してください
7. **複数のファイルに分割する** - 保守性を高めるため：
   - コンポーネントを個別のファイルに分割 (`Header.tsx`, `Footer.tsx` など)
   - 再利用可能なスタイルを専用ファイルに抽出
   - 各ファイルを200-300行以内に抑え、焦点を絞る

---

## プロフェッショナルなUIのための共通ルール

これらは、UIを非プロフェッショナルに見せてしまう、見落とされがちな問題です：

### アイコンと視覚要素

| ルール | Do (推奨) | Don't (非推奨) |
|------|----|----- |
| **絵文字アイコン禁止** | SVGアイコン (Heroicons, Lucide, Simple Icons) を使用 | 🎨 🚀 ⚙️ のような絵文字をUIアイコンとして使用 |
| **安定したホバー状態** | ホバー時に色/不透明度のトランジションを使用 | レイアウトがずれるような拡大縮小を使用 |
| **正しいブランドロゴ** | Simple Iconsから公式SVGを調査して使用 | 不正確なロゴパスを推測や使用 |
| **一貫したアイコンサイズ** | `w-6 h-6` で固定されたviewBox (24x24) を使用 | 異なるアイコンサイズをランダムに混在 |

### インタラクションとカーソル

| ルール | Do (推奨) | Don't (非推奨) |
|------|----|----- |
| **カーソルポインター** | クリック可能/ホバー可能なカードに `cursor-pointer` を追加 | インタラクティブ要素にデフォルトカーソルのまま |
| **ホバーフィードバック** | 視覚的なフィードバック (色, 影, 枠線) を提供 | インタラクティブであることを示す表示がない |
| **スムーズなトランジション** | `transition-colors duration-200` を使用 | 状態変化が即時、または遅すぎる (>500ms) |

### ライト/ダークモードのコントラスト

| ルール | Do (推奨) | Don't (非推奨) |
|------|----|----- |
| **ライトモードのガラスカード** | `bg-white/80` またはそれ以上の不透明度を使用 | `bg-white/10` (透明すぎる) を使用 |
| **ライトモードのテキスト** | テキストに `#0F172A` (slate-900) を使用 | 本文に `#94A3B8` (slate-400) を使用 |
| **ライトモードのミュートテキスト** | 最低でも `#475569` (slate-600) を使用 | gray-400 またはそれより明るい色を使用 |
| **ボーダーの視認性** | ライトモードでは `border-gray-200` を使用 | `border-white/10` (不可視) を使用 |

### レイアウトとスペーシング

| ルール | Do (推奨) | Don't (非推奨) |
|------|----|----- |
| **フローティングナビバー** | `top-4 left-4 right-4` のスペーシングを追加 | ナビバーを `top-0 left-0 right-0` に密着させる |
| **コンテンツのパディング** | 固定ナビバーの高さを考慮する | 固定要素の後ろにコンテンツを隠れさせる |
| **一貫した最大幅** | 同じ `max-w-6xl` または `max-w-7xl` を使用 | 異なるコンテナ幅を混在させる |

---

## 納品前チェックリスト

UIコードを納品する前に、以下の項目を確認してください：

### 視覚的品質
- [ ] 絵文字をアイコンとして使用していない (代わりにSVGを使用)
- [ ] すべてのアイコンが一貫したアイコンセット (Heroicons/Lucide) から来ている
- [ ] ブランドロゴが正しい (Simple Iconsで確認済み)
- [ ] ホバー状態がレイアウトシフトを引き起こさない

### インタラクション
- [ ] すべてのクリック可能要素に `cursor-pointer` がある
- [ ] ホバー状態が明確な視覚的フィードバックを提供する
- [ ] トランジションがスムーズである (150-300ms)
- [ ] キーボード操作時にフォーカス状態が可視化されている

### ライト/ダークモード
- [ ] ライトモードのテキストが十分なコントラストを持っている (最低 4.5:1)
- [ ] ガラス/透明要素がライトモードで視認可能である
- [ ] ボーダーが両方のモードで視認可能である
- [ ] 納品前に両方のモードをテストする

### レイアウト
- [ ] フローティング要素が端から適切なスペーシングを持っている
- [ ] 固定ナビバーの後ろにコンテンツが隠れていない
- [ ] 320px, 768px, 1024px, 1440px でレスポンシブである
- [ ] モバイルで横スクロールが発生しない

### アクセシビリティ
- [ ] すべての画像にaltテキストがある
- [ ] フォーム入力にラベルがある
- [ ] 色だけを識別子としていない
- [ ] `prefers-reduced-motion` が尊重されている
