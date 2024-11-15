import os
import socket

def add_rule(ip=None, port=None, action="DROP"):
    """
    Adds a rule to block or allow a specific IP or port using iptables.
    :param ip: IP address to block/allow (default is None).
    :param port: Port number to block/allow (default is None).
    :param action: Action for the rule ('DROP' or 'ACCEPT').
    """
    if ip and port:
        cmd = f"sudo iptables -A INPUT -s {ip} -p tcp --dport {port} -j {action}"
    elif ip:
        cmd = f"sudo iptables -A INPUT -s {ip} -j {action}"
    elif port:
        cmd = f"sudo iptables -A INPUT -p tcp --dport {port} -j {action}"
    else:
        print("No IP or port specified.")
        return

    os.system(cmd)
    print(f"Rule added: {cmd}")

def remove_rule(ip=None, port=None):
    """
    Removes a rule for a specific IP or port using iptables.
    :param ip: IP address to remove rule for (default is None).
    :param port: Port number to remove rule for (default is None).
    """
    if ip and port:
        cmd = f"sudo iptables -D INPUT -s {ip} -p tcp --dport {port} -j DROP"
    elif ip:
        cmd = f"sudo iptables -D INPUT -s {ip} -j DROP"
    elif port:
        cmd = f"sudo iptables -D INPUT -p tcp --dport {port} -j DROP"
    else:
        print("No IP or port specified.")
        return

    os.system(cmd)
    print(f"Rule removed: {cmd}")

def list_rules():
    """
    Lists the current iptables rules.
    """
    os.system("sudo iptables -L -n --line-numbers")

def is_ip_blocked(ip):
    """
    Checks if an IP is blocked by attempting to connect.
    :param ip: The IP address to check.
    """
    try:
        with socket.create_connection((ip, 80), timeout=2):
            print(f"{ip} is accessible (not blocked).")
    except socket.timeout:
        print(f"{ip} is blocked or unreachable.")

def main():
    print("=== Simple Python Firewall ===")
    while True:
        print("\nOptions:")
        print("1. Add Rule")
        print("2. Remove Rule")
        print("3. List Rules")
        print("4. Check if IP is Blocked")
        print("5. Exit")

        choice = input("Enter your choice: ")
        if choice == "1":
            ip = input("Enter IP address to block/allow (leave blank for all): ")
            port = input("Enter port to block/allow (leave blank for all): ")
            action = input("Enter action ('DROP' or 'ACCEPT'): ").upper()
            add_rule(ip if ip else None, int(port) if port else None, action)
        elif choice == "2":
            ip = input("Enter IP address to remove rule for (leave blank for all): ")
            port = input("Enter port to remove rule for (leave blank for all): ")
            remove_rule(ip if ip else None, int(port) if port else None)
        elif choice == "3":
            list_rules()
        elif choice == "4":
            ip = input("Enter IP address to check: ")
            is_ip_blocked(ip)
        elif choice == "5":
            print("Exiting... Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
