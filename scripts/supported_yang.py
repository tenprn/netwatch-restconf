import os
from pathlib import Path
from dotenv import load_dotenv
from netwatch.config import HEADERS, YANG_LIBRARY_URL
from netwatch.api import get_restconf_data
import time

PROJECT_ROOT = Path(__file__).resolve().parents[1]

load_dotenv(PROJECT_ROOT / ".env")

username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")
output_path = PROJECT_ROOT / "output_files" / "yang_module_list.txt"

if not username or not password:
    raise RuntimeError("USERNAME and PASSWORD must be set in the .env file")

data = get_restconf_data(YANG_LIBRARY_URL, HEADERS, username, password)

if data is None:
    raise RuntimeError("RESTCONF returned no YANG-library data")

yang_library = data["ietf-yang-library:yang-library"]
module_sets = yang_library["module-set"]

output_path.parent.mkdir(parents=True, exist_ok=True)
with output_path.open("w") as f:
    for module_set in module_sets:
        modules = module_set.get("module", [])
        for module in modules:
            f.write(module['name'] + "\n")
print(f"Saved YANG module list at: {output_path}")
time.sleep(1)
print("Done ...\n")
