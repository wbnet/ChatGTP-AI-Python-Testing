from netmiko import ConnectHandler
import re

# Define the list of Cisco switch DNS names (replace with actual DNS names if needed)
switches = ["SW1", "SW2", "SW3", "SW4"]

# Credentials and connection settings
device_credentials = {
    'username': 'admin',        # Replace with your actual username
    'password': 'yourpassword', # Replace with your actual password
    'device_type': 'cisco_ios', # Change this if using a different device
}

# Function to get loopback IPs from a switch
def get_loopback_ips(switch):
    # Add the DNS name or IP address for the switch dynamically
    device = device_credentials.copy()
    device['ip'] = switch

    try:
        # Connect to the device using SSH
        connection = ConnectHandler(**device)

        # Send the 'show ip interface brief' command
        output = connection.send_command('show ip interface brief')

        loopback_ips = []

        # Parse the output to find loopback interfaces
        for line in output.splitlines():
            if line.lower().startswith('loopback'):
                # Example line: Loopback0     192.168.10.1     YES manual up up
                match = re.search(r'(Loopback\d+)\s+(\d+\.\d+\.\d+\.\d+)', line)
                if match:
                    interface, ip = match.groups()
                    loopback_ips.append((interface, ip))

        # Disconnect after retrieving the info
        connection.disconnect()

        return loopback_ips

    except Exception as e:
        print(f"Error connecting to {switch}: {e}")
        return []

# Main function to get loopback IPs from all switches
def get_all_switch_loopbacks():
    all_ips = {}

    for switch in switches:
        print(f"Connecting to {switch}...")
        ips = get_loopback_ips(switch)
        if ips:
            all_ips[switch] = ips
        else:
            print(f"No loopback interfaces found on {switch} or unable to retrieve info.")

    return all_ips

if __name__ == '__main__':
    # Get loopback IPs from all switches
    loopback_ips = get_all_switch_loopbacks()

    # Display the results
    if loopback_ips:
        print("\nLoopback IP addresses on the switches:")
        for switch, ips in loopback_ips.items():
            print(f"\n{switch}:")
            for interface, ip in ips:
                print(f"  {interface}: {ip}")
    else:
        print("No loopback IPs found on any of the switches.")
