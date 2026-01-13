# UI Review

## Meta
- productId: {{productId}}
- specId: {{specId}}
- runId: {{runId}}
- figmaPage: {{figmaPage}}
- figmaUrl: {{figmaUrl}}
- gates: {{gatesPath}}
- rubric: {{rubricPath}}
- threshold: {{threshold}}

## Result
- Smoke Gates: PASS / FAIL
- UX Score: __/100
- Verdict: SHIP / FIX / REDESIGN

---

## Smoke Gates (Checklist)
> For each item, mark PASS/FAIL and add 1-line evidence.
> **Required**: G-KEYBOARD-01, G-ROUTING-01, G-SECURITY-01 must be checked.

- [ ] G1: Tap targets >= 44px — PASS/FAIL — Evidence:
- [ ] G2: Long text does not break layout — PASS/FAIL — Evidence:
- [ ] G3: Primary action is visually clear — PASS/FAIL — Evidence:
- [ ] G4: Semantic structure (Header/Content/Footer) is representable — PASS/FAIL — Evidence:
- [ ] G5: No accidental absolute positioning for core layout — PASS/FAIL — Evidence:

### Hard Gates
- [ ] G-KEYBOARD-01: Tab focusable — PASS/FAIL — Evidence:
- [ ] G-ROUTING-01: No 404s — PASS/FAIL — Evidence:
- [ ] G-SECURITY-01: No secrets — PASS/FAIL — Evidence:

---

## UX Scorecard

### Scores (Subjective)
- Clarity: __/10
- Efficiency: __/10
- Error prevention: __/10
- Accessibility: __/10
- Visual hierarchy: __/10
- Consistency: __/10

### Scores (Objective)
> 0 pts if not measured.
- Performance (LCP): __/20
- Visual Fidelity (Color): __/20

**Total:** __/100

### Top issues (Priority)
1. P0 (ship blocker):
2. P1 (should fix before ship):
3. P2 (nice to have):

### Concrete fixes (Spec-level / Figma-level)
- Fix 1:
- Fix 2:
- Fix 3:

---

## Notes for MCP iteration
- Next prompt changes:
- Spec changes:
- Figma changes:
