import os
from .config import INT_URL, CPU_URL, MEMORY_URL, HEADERS
from datetime import datetime
from dotenv import load_dotenv
from .api import get_restconf_data
from .display import display_interface_health, display_top_memory, display_cpu_health
import time

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

load_dotenv()
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

def network_health_report(interface_data, cpu_data, memory_data):
    print("\n============= NETWORK HEALTH REPORT ============\n")
    display_interface_health(interface_data)
    display_top_memory(memory_data)
    display_cpu_health(cpu_data)


# MAIN EXECUTION
if not USERNAME or not PASSWORD:
    raise RuntimeError("USERNAME and PASSWORD must be set in the .env file")

print("\nLoading data from device ...")
int_data = get_restconf_data(INT_URL, HEADERS, USERNAME, PASSWORD)
cpu_data = get_restconf_data(CPU_URL, HEADERS, USERNAME, PASSWORD)
mem_data = get_restconf_data(MEMORY_URL, HEADERS, USERNAME, PASSWORD)

if int_data is None or cpu_data is None or mem_data is None:
    if int_data is None:
        print("Failed to get Interface data")
    if cpu_data is None:
        print("Failed to get CPU data")
    if mem_data is None:
        print("Failed to get Memory data")
    exit()

network_health_report(int_data, cpu_data, mem_data)
