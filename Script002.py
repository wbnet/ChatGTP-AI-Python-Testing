from netmiko import ConnectHandler
import re

# Define the Cisco device
device = {
    'device_type': 'cisco_ios',
    'ip': '192.168.1.1',         # Replace with your switch IP
    'username': 'admin',         # Replace with your username
    'password': 'yourpassword',  # Replace with your password
}

def get_loopback_ips():
    try:
        connection = ConnectHandler(**device)
        output = connection.send_command('show ip interface brief')

        loopback_ips = []

        for line in output.splitlines():
            if line.lower().startswith('loopback'):
                # Example line: Loopback0     192.168.10.1     YES manual up up
                match = re.search(r'(Loopback\d+)\s+(\d+\.\d+\.\d+\.\d+)', line)
                if match:
                    interface, ip = match.groups()
                    loopback_ips.append((interface, ip))

        connection.disconnect()

        return loopback_ips
    except Exception as e:
        print(f"Error: {e}")
        return []

if __name__ == '__main__':
    ips = get_loopback_ips()
    if ips:
        print("Loopback IP addresses found:")
        for intf, ip in ips:
            print(f"{intf}: {ip}")
    else:
        print("No loopback IPs found or unable to connect.")
