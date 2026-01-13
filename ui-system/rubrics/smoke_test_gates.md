# Smoke Test Gates (Standard)

These gates are hard requirements. If any gate fails, the run is FAIL.

- G1: Tap targets (buttons/rows/icon buttons) are >= 44px in at least one dimension (prefer both).
- G2: Long text (e.g., long names/IDs) does not break layout; wrapping or truncation is intentional.
- G3: Primary action is visually prominent; secondary actions do not compete.
- G4: Semantic structure is representable (Header / Content / Footer) without relying on absolute positioning.
- G5: Focus styles exist for keyboard navigation (where applicable) and do not shift layout.
