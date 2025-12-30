---
slug: build-app-simple
description: シンプルなWebアプリを素早く構築する（Vanilla: HTML/CSS/JS を基本としつつ、必要に応じて React + Tailwind（任意で TypeScript）も利用可）。
trigger: model_decision
---

---

## スタック選定（最小ガイド）

本ワークフローは「過剰設計しない」を意味します。**フレームワーク禁止ではありません**。  
既定は Vanilla（HTML/CSS/JS）ですが、以下の条件では **React + Tailwind** を使用して構いません。

- 画面状態が複雑（一覧/フィルタ/ダイアログ/複数状態など）
- コンポーネント分割が必要
- Tailwind によるデザイン規格統一が必要
- 将来の拡張（画面追加・テスト導入）を見越す

> React/Tailwind を選ぶ場合でも、まずは「最小の画面・最小の状態」から実装し、肥大化を避けます。
# 🏗️ Simple Web App Build Workflow

このワークフローは、フレームワークを使わずに、標準的なWeb技術（HTML5, CSS3, ES6+ JavaScript）のみを用いて、美しく機能的なWebアプリケーションを迅速に構築します。

## Step 1: 🎨 デザインと構造の設計
1. **要件分析**: ユーザーが求めているアプリの機能と「雰囲気」を理解します。
2. **デザイン方針**:
   - **Modern Aesthetics**: 安っぽいデフォルトのスタイルは禁止です。
   - **Typography**: Google Fonts（Inter, Poppins, Noto Sans JPなど）を使用します。
   - **Color**: 洗練されたカラーパレット（グラデーション、ダークモード対応など）をCSS変数で定義します。
   - **Layout**: Flexbox または CSS Grid を使用したレスポンシブデザインにします。

## Step 2: 💻 コアファイルの実装
以下の3つのファイルをルートディレクトリ（または適切なサブディレクトリ）に作成します。

1. **`index.html`**:
   - セマンティックなHTML構造（header, main, footer）。
   - 必要なメタタグ（viewport, description）。
   - Google Fonts と `style.css`, `script.js` の読み込み。

2. **`style.css`**:
   - CSSリセット。
   - ルート変数（`--primary-color`, etc.）の定義。
   - ホバーエフェクトやトランジションを含めたインタラクティブなスタイル。
   - UIパーツ（ボタン、カード、入力フォーム）のスタイリング。

3. **`script.js`**:
   - アプリケーションのロジック。
   - DOM操作による動的なUI更新。
   - イベントリスナーの適切な設定。

## Step 3: 👀 ブラウザでの動作検証
1. 作成した `index.html` をブラウザサブエージェントで開きます。
2. ページの表示崩れがないか、インタラクションが正しく動作するかを目視で確認します。
3. 問題があれば修正し、再度確認します。

## Step 4: 📝 完了確認
- 実装したアプリの概要をユーザーに報告します。


### React + Tailwind（任意）クイックスタート（例: Vite）

```bash
# TypeScript 推奨（不要なら --template react）
npm create vite@latest my-app -- --template react-ts
cd my-app
npm install

# Tailwind
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

- `tailwind.config.*` の `content` を Vite 構成に合わせる
- `src/index.css` に `@tailwind base; @tailwind components; @tailwind utilities;` を追加
- 起動: `npm run dev`
