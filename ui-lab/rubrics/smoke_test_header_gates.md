# Smoke Test Gates: AppHeader (Strong)

These are PASS/FAIL gates. If any **Critical** item fails, the output is rejected.

## Critical Gates (must pass)
- [ ] No absolute positioning for the main header layout (use flex/grid; absolute only for tiny decorative elements if unavoidable).
- [ ] Variables mapping is clean: NO `var(--` usage, NO `bg-[var(...)]`, NO `text-[length:var(...)]`.
- [ ] Semantics: interactive elements are `<button>`, links are `<a>`; header uses semantic `<header>`.
- [ ] Accessibility: `focus-visible` styles exist (ring) and aria-labels are applied as specified.
- [ ] Required states are implemented (default/loading/offline) and state behavior matches Spec (e.g., disable actions on loading).

## Quality Gates (must pass for acceptance)
- [ ] Props are typed via a TypeScript interface; sensible defaults exist.
- [ ] Layout is responsive and stable (no overflow; center truncates workspace with `truncate`).
- [ ] Desktop-only behavior is correct (Command hidden on small screens).
- [ ] Tap target size: interactive height >= 44px.
- [ ] Code is production-ready: no placeholder TODOs, no duplicated logic, clean component boundaries.

## Output Checks (manual quick checks)
- [ ] `npm/pnpm build` or TypeScript check passes (if project has it).
- [ ] Lint passes (if configured).
