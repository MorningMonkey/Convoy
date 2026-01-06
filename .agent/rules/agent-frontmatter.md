---
slug: agent-frontmatter
description: "Agent assets の frontmatter 仕様（必須キー/slug形式/descriptionのクオート）を定義する"
trigger: model_decision
---

## Frontmatter Rules

- `.agent/rules/*.md` と `.agent/workflows/*.md` は frontmatter を必須とする
- 必須キー: `slug`, `description`, `trigger`
- `slug` は kebab-case
- `description` は **必ずクオート**する（YAMLの `: ` 誤解釈を防ぐため）
  - OK: `description: "Vanilla: HTML/CSS/JS"`
  - NG: `description: Vanilla: HTML/CSS/JS`
