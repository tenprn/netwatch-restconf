import ipaddress

def print_dash_line(length):
    for _ in range(length):
        print("-", end="")
    print("")

def bytes_to_mb(value):
    return int(value) / (1024 * 1024)

def extract_interfaces(interface_data):
    return interface_data[
        "Cisco-IOS-XE-interfaces-oper:interfaces"
    ]["interface"]

def extract_memory_processes(memory_data):
    return memory_data[
        "Cisco-IOS-XE-process-memory-oper:memory-usage-processes"
    ]["memory-usage-process"]

def extract_cpu_utilization(data):
    cpu = data[
        "Cisco-IOS-XE-process-cpu-oper:cpu-usage"
    ]["cpu-utilization"]

    return {
        "five-seconds": cpu["five-seconds"],
        "one-minute": cpu["one-minute"],
        "five-minutes": cpu["five-minutes"]
    }

def mask_to_prefix_length(mask):
    """
    Converts a subnet mask (e.g. '255.255.255.0') to a prefix length (e.g. 24).
    Returns None if the mask is invalid or empty.
    """
    if not isinstance(mask, str) or mask.count('.') != 3:
        return None
    
    octets = mask.split('.')
    if not all(octet.isdigit() and 0 <= int(octet) <= 255 for octet in octets):
        return None

    if not mask:
        return None
    try:
        return ipaddress.IPv4Network(f"0.0.0.0/{mask}").prefixlen
    except (ValueError, AttributeError):
        return None
