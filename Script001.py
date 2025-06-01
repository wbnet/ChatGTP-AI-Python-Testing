import psutil
import socket

def get_loopback_ips():
    loopback_ips = []

    # Get all network interfaces and their addresses
    interfaces = psutil.net_if_addrs()

    for interface_name, interface_addresses in interfaces.items():
        for addr in interface_addresses:
            # AF_INET is for IPv4, AF_INET6 for IPv6
            if addr.family in (socket.AF_INET, socket.AF_INET6):
                ip = addr.address
                if ip.startswith("127.") or ip == "::1":
                    loopback_ips.append((interface_name, ip))

    return loopback_ips

if __name__ == "__main__":
    loopbacks = get_loopback_ips()
    if loopbacks:
        print("Loopback interface IP addresses found:")
        for iface, ip in loopbacks:
            print(f"Interface: {iface}, IP: {ip}")
    else:
        print("No loopback IP addresses found.")
