from netmiko import ConnectHandler
from getpass import getpass

# Prompt for credentials
username = input("Username: ")
password = getpass("Password: ")

# Define switch DNS names
switches = ["SW1", "SW2", "SW3", "SW4"]

# Function to parse interface errors
def parse_errors(output):
    errors = {}
    interfaces = output.splitlines()
    current_interface = None
    for line in interfaces:
        if "line protocol" in line:
            current_interface = line.split(" ")[0]
        if current_interface:
            if any(err in line for err in ["input error", "CRC", "output error"]):
                errors.setdefault(current_interface, []).append(line.strip())
    return errors

# Loop through each switch
for switch in switches:
    print(f"\nConnecting to {switch}...")
    device = {
        "device_type": "cisco_ios",
        "host": switch,
        "username": username,
        "password": password,
    }

    try:
        connection = ConnectHandler(**device)
        output = connection.send_command("show interfaces")
        connection.disconnect()

        error_data = parse_errors(output)
        if error_data:
            print(f"\n⚠️ Errors found on {switch}:")
            for intf, msgs in error_data.items():
                print(f"  {intf}:")
                for msg in msgs:
                    print(f"    {msg}")
        else:
            print(f"✅ No errors found on {switch}.")
    except Exception as e:
        print(f"❌ Failed to connect to {switch}: {e}")
