from .utils import *


def display_interface_health(interface_data):
    interfaces = extract_interfaces(interface_data)

    print_dash_line(67)
    print(f"INTERFACES            | STATUS                  | IP ADDRESS")    
    print_dash_line(67)
    
    if interface_data is None: 
        print("ERROR - NOT FOUND DATA")
        print_dash_line(67)
        return

    for interface in interfaces:
        if interface.get("name", "Unknown") != "Unknown" and not interface.get("name", "Unknown").startswith("Loopback"):
            name = interface['name']
            ipv4 = interface.get('ipv4', "-")
            mask = interface.get('ipv4-subnet-mask', "-")
            prefix = mask_to_prefix_length(mask)
            status = check_interface_health(interface.get("admin-status", "Unknown"), interface.get("oper-status", "Unknown"))
            
            print(f"{name:<21} | {status:<23} | {ipv4}/{prefix}")
    print_dash_line(67)
    

def check_interface_health(admin_status, oper_status):
    admin = str(admin_status).lower()
    oper = str(oper_status).lower()

    if admin == "unknown" or oper == "unknown":
        return "ERROR - NOT FOUND DATA"
    elif "up" in admin and ("ready" in oper or "up" in oper):
        return "UP - OK"
    elif "up" in admin and ("no-pass" in oper or "down" in oper):
        return "DOWN - CHECK CABLE"
    elif "down" in admin:
        return "DOWN - ENABLE INTERFACE"
    else: 
        return "ERROR"

def display_top_memory(mem_data):
    if mem_data is None: 
        print(f"\nTOP 5 MEMORY-CONSUMING PROCESSES")
        print_dash_line(49)
        print("ERROR - NOT FOUND DATA")
        print_dash_line(49)
        return
    
    top_memories = get_top_memory_processes(mem_data, 5)
    print("\nTOP 5 MEMORY-CONSUMING PROCESSES")
    print("------------------------------------------------")
    print("PROCESS NAME                          | (MB)")
    print("--------------------------------------|---------")
    for process in top_memories:
        name = process['name']
        holding_memory = process['holding-memory']
        print(f"{name:<37} |  {holding_memory:<20}")
    print(f"------------------------------------------------\n")
    

def get_top_memory_processes(data, limit=5):
    processes = extract_memory_processes(data)
    processes = sorted(
        processes,
        key=lambda process: int(process["holding-memory"]),
        reverse=True
    )
    for process in processes:
        process['holding-memory'] = round(bytes_to_mb(process['holding-memory']), 2)
    return processes[:limit]


def display_cpu_health(cpu_data):
    if cpu_data is None:
        print(f"CPU USAGE")
        print(f"------------------------------------------------")
        print("ERROR - NOT FOUND DATA")
        print(f"------------------------------------------------\n")
        return
    
    cpu = extract_cpu_utilization(cpu_data)
    status = check_cpu_health(cpu)
    print(f"CPU USAGE")
    print(f"------------------------------------------------")
    print(f"5 Seconds : {cpu['five-seconds']}%  - {status['five-seconds']}")
    print(f"1 Minute  : {cpu['one-minute']}%  - {status['one-minute']}")
    print(f"5 Minutes : {cpu['five-minutes']}%  - {status['five-minutes']}")
    print(f"------------------------------------------------\n")


def check_cpu_health(cpu):
    status = {}

    if cpu['five-seconds'] > 80:
        status['five-seconds'] = "High CPU"
    elif cpu['five-seconds'] > 60:
        status['five-seconds'] = "Medium CPU"
    else:
        status['five-seconds'] = "Working Normally"
    
    if cpu['one-minute'] > 80:
        status['one-minute'] = "High CPU"
    elif cpu['one-minute'] > 60:
        status['one-minute'] = "Medium CPU"
    else:
        status['one-minute'] = "Working Normally"
    
    if cpu['five-minutes'] > 80:
        status['five-minutes'] = "High CPU"
    elif cpu['five-minutes'] > 60:
        status['five-minutes'] = "Medium CPU"
    else:
        status['five-minutes'] = "Working Normally"

    return status
