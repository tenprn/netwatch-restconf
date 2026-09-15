import os
from dotenv import load_dotenv

load_dotenv()

HOST = os.getenv("HOST")

HEADERS = {
    "Accept": "application/yang-data+json"
}

# -------- FOR supported_yang.py --------
YANG_LIBRARY_MODULE = "ietf-yang-library:yang-library"
YANG_LIBRARY_URL = f"https://{HOST}/restconf/data/{YANG_LIBRARY_MODULE}"


# -------- FOR main.py --------
YANG_INT_MODULE = "Cisco-IOS-XE-interfaces-oper:interfaces"
INT_URL = f"https://{HOST}/restconf/data/{YANG_INT_MODULE}"

YANG_CPU_MODULE = "Cisco-IOS-XE-process-cpu-oper:cpu-usage"
CPU_URL = f"https://{HOST}/restconf/data/{YANG_CPU_MODULE}"

YANG_MEMORY_MODULE = "Cisco-IOS-XE-process-memory-oper:memory-usage-processes"
MEMORY_URL = f"https://{HOST}/restconf/data/{YANG_MEMORY_MODULE}"


# -------- FOR dump_data.py --------
# YANG_DUMP_MODULE = "Cisco-IOS-XE-process-memory-oper:memory-usage-processes"
# YANG_DUMP_MODULE = "Cisco-IOS-XE-process-cpu-oper:cpu-usage"
YANG_DUMP_MODULE = "Cisco-IOS-XE-interfaces-oper:interfaces"
DUMP_URL = f"https://{HOST}/restconf/data/{YANG_DUMP_MODULE}"



