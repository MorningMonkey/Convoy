# UX Scorecard: AppHeader (Psychology-based)

Scoring: 0 = NG / 1 = OK / 2 = Good
Pass guideline: Total >= 16/20 and no critical NG.

## 1) Information hierarchy (Gestalt / Visual hierarchy)
- Title is the most prominent element.
- Workspace/status is secondary and does not compete with title.

## 2) Cognitive load (Hick / Miller)
- Primary actions are limited (right side <= 2 actions, primary CTA <= 1).
- No unnecessary labels/icons.

## 3) Affordance & recognition (Recognition > recall)
- Buttons look and behave like buttons.
- Labels are explicit (“Settings”, “Command”, “Back”).

## 4) Fitts’ Law (target size & reach)
- Tap targets >= 44px height.
- Important actions are easy to hit (not tiny, not cramped).

## 5) Consistency (Jakob’s Law)
- Back is always on the left, settings on the right.
- Spacing and alignment are consistent.

## 6) Feedback & system status (Visibility of system status)
- Loading disables actions and communicates “Loading…”.
- Offline state is clearly visible (chip + optional dot).

## 7) Error prevention & recovery
- In loading/offline, the user is not led into dead ends.
- Disabled states are visually obvious.

## 8) Grouping & scanning (Gestalt proximity/alignment)
- Left/center/right groups are visually separated.
- Workspace chip truncates gracefully rather than wrapping unpredictably.

## 9) Accessibility (A11y)
- focus-visible styles exist.
- aria-labels are set for icon-only or ambiguous buttons.

## 10) Minimalism (Signal > noise)
- No heavy branding imagery in header.
- Background does not reduce readability.

### Notes
Record issues and fixes per run in ui-lab/runs/<date>_<product>_<spec>/review.md