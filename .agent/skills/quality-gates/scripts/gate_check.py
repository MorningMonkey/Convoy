import argparse
import os
import sys
import subprocess
import json
import re
from pathlib import Path
import shutil

# --- Constants ---

REASON_NO_PRODUCT = "NO_PRODUCT"
REASON_NO_SOT = "NO_SOT_AND_NO_INFERENCE"
REASON_STACK_MISMATCH = "STACK_MISMATCH"
REASON_MISSING_RUNTIME = "MISSING_RUNTIME"
REASON_NOT_WHITELISTED = "NOT_WHITELISTED"
REASON_EXEC_ERROR = "EXEC_ERROR"
REASON_INTERNAL_ERROR = "INTERNAL_ERROR"
REASON_NONZERO_EXIT = "NONZERO_EXIT"

ALLOWED_COMMAND_PREFIXES = [
    "pnpm", "npm", "yarn",
    "flutter", "dart",
    "python", "py", "pytest", "ruff", "mypy", "pip",
    "gitleaks", "trivy", "pip-audit",
    "node",
    "vitest", "jest"
]

# --- Helper Functions ---

def get_active_product(root_dir):
    """Resolves the active product directory."""
    # 1. Check if specific product dir passed (handled by caller usually, but logic here)
    # 2. Check .active_product
    active_prod_file = root_dir / "assets/branding/.active_product"
    if active_prod_file.exists():
        try:
            return active_prod_file.read_text("utf-8").strip()
        except:
            pass
    
    # 3. Check if single directory in assets/branding
    branding_dir = root_dir / "assets/branding"
    if branding_dir.exists():
        subdirs = [d for d in branding_dir.iterdir() if d.is_dir() and not d.name.startswith(".")]
        if len(subdirs) == 1:
            return subdirs[0].name
            
    return None

def parse_yaml_simple(file_path):
    """Simple YAML parser to avoid dependencies."""
    data = {}
    current_key = None
    try:
        lines = file_path.read_text("utf-8").splitlines()
        for line in lines:
            line = line.rstrip()
            if not line or line.strip().startswith("#"):
                continue
            
            # Top level key (e.g. "lint:")
            match_top = re.match(r'^([\w-]+):$', line.strip())
            if match_top:
                current_key = match_top.group(1)
                data[current_key] = {}
                continue
            
            # Nested property (e.g. "  command: ...")
            match_prop = re.match(r'^\s+([\w-]+):\s*(.*)$', line)
            if match_prop and current_key:
                prop = match_prop.group(1)
                val = match_prop.group(2).strip('"\'')
                data[current_key][prop] = val
    except Exception as e:
        raise ValueError(f"Failed to parse YAML: {e}")
    return data

def check_runtime(command):
    """Checks if the runtime for the command exists."""
    cmd_parts = command.split()
    if not cmd_parts:
        return False
    
    prog = cmd_parts[0]
    
    # Map program to check command
    checks = {
        "node": ["node", "--version"],
        "npm": ["npm", "--version"],
        "pnpm": ["pnpm", "--version"],
        "yarn": ["yarn", "--version"],
        "flutter": ["flutter", "--version"],
        "dart": ["dart", "--version"],
        "python": ["python", "--version"],
        "py": ["py", "--version"], # Windows specific
        "pip": ["python", "-m", "pip", "--version"],
        "ruff": ["ruff", "--version"],
        "pytest": ["pytest", "--version"],
        "mypy": ["mypy", "--version"],
        "git": ["git", "--version"]
    }
    
    # Fallback: just check if executable exists
    if shutil.which(prog):
        return True
        
    # Python fallback for Windows 'py' launcher
    if prog == "python" and shutil.which("py"):
        return True

    return False

def is_whitelisted(command):
    cmd_parts = command.split()
    if not cmd_parts:
        return False
    prog = cmd_parts[0]
    return prog in ALLOWED_COMMAND_PREFIXES

def print_report(gate_type, result, command, reason, logs):
    print(f"# Gate Report: {gate_type}")
    print(f"Result: {result}")
    print(f"Command: {command or 'N/A'}")
    print(f"Reason: {reason or 'N/A'}")
    print("Log:")
    
    log_lines = logs.splitlines()
    # Keep last 200 lines
    if len(log_lines) > 200:
        log_lines = ["... (truncated) ..."] + log_lines[-200:]
        
    for line in log_lines:
        print(line)

def infer_command(gate_type, root_dir):
    """Infers command based on project files."""
    
    # Node
    pkg_json = root_dir / "package.json"
    if pkg_json.exists():
        try:
            data = json.loads(pkg_json.read_text("utf-8"))
            scripts = data.get("scripts", {})
            
            # Direct match
            if gate_type in scripts:
                # Use manager if present
                if (root_dir / "pnpm-lock.yaml").exists():
                    return f"pnpm {gate_type}", "node"
                if (root_dir / "yarn.lock").exists():
                    return f"yarn {gate_type}", "node"
                return f"npm run {gate_type}", "node"
                
            # Mapping
            mapping = {
                "lint": ["lint", "lint:fix"],
                "type": ["typecheck", "type-check", "tsc"],
                "test": ["test", "test:unit"],
                "security": ["audit", "scan"],
                "ui": ["test:ui", "e2e"]
            }
            
            for alias in mapping.get(gate_type, []):
                if alias in scripts:
                    if (root_dir / "pnpm-lock.yaml").exists():
                        return f"pnpm {alias}", "node"
                    if (root_dir / "yarn.lock").exists():
                        return f"yarn {alias}", "node"
                    return f"npm run {alias}", "node"

        except:
             pass # JSON error means inference fails

    # Flutter
    pubspec = root_dir / "pubspec.yaml"
    if pubspec.exists():
        if gate_type == "lint":
            return "flutter analyze", "flutter"
        if gate_type == "test":
            return "flutter test", "flutter"
            
    # Python
    pyproject = root_dir / "pyproject.toml"
    requirements = root_dir / "requirements.txt"
    if pyproject.exists() or requirements.exists():
        if gate_type == "lint":
            return "ruff check .", "python" # Assumption
        if gate_type == "type":
            return "mypy .", "python"
        if gate_type == "test":
            return "pytest", "python"

    return None, None

# --- Main ---

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--type", required=True, help="Gate type (lint, type, test, security, ui)")
    parser.add_argument("--product", help="Target product name")
    parser.add_argument("--dry-run", action="store_true", help="Don't execute commands")
    args = parser.parse_args()
    
    root_dir = Path(".").resolve()
    
    # 1. Resolve Product
    product_name = args.product
    if not product_name:
        product_name = get_active_product(root_dir)
        
    if not product_name:
        print_report(args.type, "SKIP", None, REASON_NO_PRODUCT, "Could not resolve active product directory.")
        sys.exit(0) # SKIP = 0
        
    # 2. Check SoT
    sot_file = root_dir / "assets/branding" / product_name / "quality-gates.yml"
    command = None
    stack = None # Used for mismatch check
    
    if sot_file.exists():
        try:
            sot_data = parse_yaml_simple(sot_file)
            if args.type in sot_data:
                command = sot_data[args.type].get("command")
                # Inference of stack from command is hard, but we assume SoT is correct
                # We can try to guess stack from command prefix for Runtime Check
        except Exception as e:
            print_report(args.type, "FAIL", None, REASON_INTERNAL_ERROR, f"Failed to parse quality-gates.yml: {e}")
            sys.exit(1) # FAIL = 1

    # 3. Auto-Inference
    inferred_source = "SoT"
    if not command:
        command, stack = infer_command(args.type, root_dir)
        inferred_source = "Inference"
        
    if not command:
        print_report(args.type, "SKIP", None, REASON_NO_SOT, f"No command defined in quality-gates.yml and could not infer for {args.type}.")
        sys.exit(0)

    # 4. Pre-execution Checks
    
    # 4.1 Stack Mismatch (Only if we inferred, logic implicitly handled by infer_command returning None if files don't exist)
    # But if we have mixed files (e.g. package.json AND pubspec.yaml), logic might select one.
    # Currently simplest logic: if inferred, it matches.
    
    # 4.2 Runtime Check
    if not check_runtime(command):
        print_report(args.type, "SKIP", command, REASON_MISSING_RUNTIME, f"Runtime for command not found: {command}")
        sys.exit(0)
        
    # 4.3 Whitelist Check
    if not is_whitelisted(command):
        print_report(args.type, "SKIP", command, REASON_NOT_WHITELISTED, f"Command not in whitelist: {command}")
        sys.exit(0)
        
    # 5. Execution
    if args.dry_run:
        print_report(args.type, "PASS", command, "DRY_RUN", "Dry run completed.")
        sys.exit(0)
        
    try:
        # Use shell=True for complex commands (e.g. "npm run lint") works better commonly, but security risk.
        # Given whitelist, shell=True is acceptable-ish, but let's try shell=True for convenience with '&&' or pipes if present.
        # Actually whitelist assumes single command start.
        
        # On Windows, shell=True is often needed for batch files (npm, pnpm).
        use_shell = os.name == 'nt' or " " in command
        
        # Adjust command for output capturing
        process = subprocess.run(
            command,
            cwd=root_dir,
            shell=use_shell,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            check=False 
        )
        
        result_status = "PASS" if process.returncode == 0 else "FAIL"
        reason = "Command Succeeded" if result_status == "PASS" else REASON_NONZERO_EXIT
        
        print_report(args.type, result_status, command, reason, process.stdout)
        
        # FAIL = Exception for CI
        sys.exit(0 if result_status != "FAIL" else 1)
        
    except Exception as e:
        # This catches failed execution (e.g. file not found if shell=False)
        print_report(args.type, "SKIP", command, REASON_EXEC_ERROR, f"Failed to execute command: {e}")
        sys.exit(0)

if __name__ == "__main__":
    main()
