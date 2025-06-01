from netmiko import ConnectHandler
from getpass import getpass
import time

# Prompt for credentials
username = input("Username: ")
password = getpass("Password: ")

# Define switch DNS names
switches = ["SW1", "SW2", "SW3", "SW4"]

# Function to check CPU, Memory, and Interface errors
def get_switch_info(switch):
    device = {
        "device_type": "cisco_ios",
        "host": switch,
        "username": username,
        "password": password,
    }
    
    try:
        # Connect to the device
        connection = ConnectHandler(**device)

        print(f"\nConnected to {switch}...\n")
        
        # Gather CPU and memory info
        cpu_output = connection.send_command("show processes cpu")
        memory_output = connection.send_command("show memory statistics")
        interfaces_output = connection.send_command("show interfaces")
        
        connection.disconnect()

        # Check for CPU overload
        print(f"\n--- CPU Utilization for {switch} ---")
        if "CPU utilization" in cpu_output:
            print(cpu_output.splitlines()[-5:])
        else:
            print("CPU utilization info not found.")
        
        # Check for memory usage
        print(f"\n--- Memory Usage for {switch} ---")
        if "Total" in memory_output:
            print(memory_output.splitlines()[-10:])
        else:
            print("Memory usage info not found.")
        
        # Parse interface errors (input drops, output drops, etc.)
        print(f"\n--- Interface Errors for {switch} ---")
        errors = parse_interface_errors(interfaces_output)
        if errors:
            for intf, msgs in errors.items():
                print(f"{intf}:")
                for msg in msgs:
                    print(f"  - {msg}")
        else:
            print("No interface errors detected.")
        
        # Check for network drops or high traffic
        print(f"\n--- Interface Utilization for {switch} ---")
        parse_traffic_utilization(interfaces_output)

    except Exception as e:
        print(f"❌ Failed to connect to {switch}: {e}")


# Parse interface errors from "show interfaces" output
def parse_interface_errors(output):
    errors = {}
    current_interface = None
    for line in output.splitlines():
        if "line protocol" in line:
            current_interface = line.split(" ")[0]
        if current_interface:
            if any(err in line for err in ["input errors", "CRC", "output drops", "collisions"]):
                errors.setdefault(current_interface, []).append(line.strip())
    return errors

# Parse traffic utilization (looking for "bandwidth" or "utilization")
def parse_traffic_utilization(output):
    for line in output.splitlines():
        if "input rate" in line or "output rate" in line:
            print(line.strip())

# Main loop to check each switch
for switch in switches:
    get_switch_info(switch)
    time.sleep(2)  # Small delay between checks to avoid too much load
