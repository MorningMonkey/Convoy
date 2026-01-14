---
name: quality-gates
description: Unified interface for verification gates (lint, type-check, test, security, ui). Use when running quality checks to ensure robustness and consistency across different project stacks.
---

# Quality Gates

This skill provides a unified way to run verification gates for any project stack (Node, Flutter, Python, etc.).

## Usage

Use the `gate_check.py` script to run checks.

```bash
python .agent/skills/quality-gates/scripts/gate_check.py --type <gate_type> [--product <product_name>] [--dry-run]
```

### Supported Gate Types

- `lint`: Format and static analysis (ESLint, Ruff, Flutter Analyze, etc.)
- `type`: Type checking (TSC, MyPy, etc.)
- `test`: Unit and automated tests (Jest, Pytest, Flutter Test, etc.)
- `security`: Security scans (Trivy, Gitleaks, Audit, etc.)
- `ui`: UI verification (Screenshot capture / comparison)

## Logic

1.  **SoT Priority**: Checks `assets/branding/<Product>/quality-gates.yml` first.
2.  **Auto-Inference**: Falls back to determining commands from `package.json`, `pubspec.yaml`, or `pyproject.toml`.
3.  **Safety**:
    - Returns **SKIP** (Exit 0) if the stack doesn't match or tools are missing.
    - Returns **FAIL** (Exit 1) if the check actually fails.
    - Whitelists safe commands to prevent arbitrary execution.

## Configuration

Place a `quality-gates.yml` file in your product's branding directory to override defaults:

```yaml
# assets/branding/<Product>/quality-gates.yml
lint:
  command: "pnpm lint"
type:
  command: "pnpm typecheck"
```
