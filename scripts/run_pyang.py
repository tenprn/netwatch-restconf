import os
import sys
import shutil
import subprocess
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
INPUT_DIR = PROJECT_ROOT / "yang_module_schema"
OUTPUT_DIR = PROJECT_ROOT / "yang_module_tree"
OUTPUT_FORMAT = "tree"  # pyang format: 'tree' generates YANG tree structure

# Ensure output directory exists
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Locate pyang executable (looks in current Python environment first, then system PATH)
venv_pyang = os.path.join(os.path.dirname(sys.executable), "pyang")
PYANG_BIN = venv_pyang if os.path.isfile(venv_pyang) else (shutil.which("pyang") or "pyang")

# Find all .yang files in the input directory
yang_files = [path for path in INPUT_DIR.iterdir() if path.suffix == ".yang"]

if not yang_files:
    print(f"No .yang files found in '{INPUT_DIR}/'.")
    sys.exit(1)

for input_path in yang_files:
    module_name = input_path.stem
    output_path = OUTPUT_DIR / f"{module_name}.{OUTPUT_FORMAT}"

    print(f"Running pyang on {input_path.name}...")

    cmd = [
        PYANG_BIN,
        "-f", OUTPUT_FORMAT,
        "-p", str(INPUT_DIR),
        str(input_path),
        "-o", str(output_path)
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode == 0:
        print(f"Saved: {output_path}")
    else:
        print(f"Error processing {input_path.name}:")
        if result.stderr:
            print(result.stderr)
        if result.stdout:
            print(result.stdout)
