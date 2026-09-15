import os
from pathlib import Path
from netwatch.config import HEADERS, DUMP_URL, YANG_DUMP_MODULE
from netwatch.api import get_restconf_data
from dotenv import load_dotenv
import json
import time

PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = PROJECT_ROOT / "output_files"

load_dotenv(PROJECT_ROOT / ".env")
username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")

if not username or not password:
    raise RuntimeError("USERNAME and PASSWORD must be set in the .env file")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
module_name = YANG_DUMP_MODULE.split(':')[0]

response_data = get_restconf_data(DUMP_URL, HEADERS, username, password)
if response_data is None:
    raise RuntimeError("RESTCONF returned no data; output file was not created")

output_path = OUTPUT_DIR / f"{module_name}.json"
with output_path.open("w") as f:
    json.dump(response_data, f, indent=4)
    print(f"Saved: {output_path}")
    time.sleep(1)
    print("Done ...\n")
