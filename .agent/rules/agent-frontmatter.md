---
slug: "agent-frontmatter"
description: "Agent 資産の Frontmatter 仕様（必須キー、slug 形式、description のクオート）を定義・検証する。"
trigger: "model_decision"
---
# 📜 Agent Frontmatter Policy

## 🌌 Overview
本ファイルは、Convoy ワークスペース内のすべての .agent 資産が備えるべき「身分証（Frontmatter）」の規格を定義します。

エージェントが本規格を厳格に遵守することで、スラッシュコマンドの正確なトリガーが保証され、プロジェクト全体における一貫した品質管理と自動化が実現されます。

## ⚖️ Rules / Constraints
エージェントは、以下の制約を「憲法」として遵守しなければなりません。

- **必須配置**: .agent/rules/*.md および .agent/workflows/*.md には、例外なく Frontmatter を付与すること。
- **必須キー**: slug, description, 	rigger の 3 項目を必ず含めること。
- **並び順**: 可読性と統一感のため、以下の順序を厳守すること。
  1. slug
  2. description
  3. 	rigger
- **命名規則**: slug の値は、システム整合性のために必ず **kebab-case** で記述すること。
- **構文安全**: description の値は、YAML 解析エラーを物理的に排除するため、**必ず二重引用符（" "）でクオート** すること。
  - ✅ **OK**: description: "Example: Logic"
  - ❌ **NG**: description: Example: Logic

## 🚀 Workflow / SOP
エージェントが新しい資産を作成、または既存の資産を更新する際は、以下のステップを実行します。

### Step 1: Frontmatter の生成
資産の目的に応じた一意の slug を決定します。description は日本語で簡潔に記述し、記号による誤動作を防ぐため必ずクオートで囲みます。

### Step 2: 構文のバリデーション
保存前に、コロン（:）や特殊記号が YAML 構文を破壊していないか、エージェント自身で自己検閲を行います。

### Step 3: ファイルへの適用
ファイルの先頭（1行目）から Frontmatter を配置します。末尾の --- の後に、一行の空行を挟んで Markdown 本文を開始します。

## ✅ Checklist
エージェントは最終出力の前に、以下の項目が満たされているか確認してください。

- [ ] slug は kebab-case（小文字とハイフンのみ）で記述されているか？
- [ ] description の前後は二重引用符（"）で正しくクオートされているか？
- [ ] slug, description, 	rigger の 3 つの必須キーがすべて含まれており、**slug が先頭** になっているか？
- [ ] ファイルの冒頭が --- で始まり、構文エラーがないか？


