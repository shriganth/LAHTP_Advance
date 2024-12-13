import socket
from concurrent.futures import ThreadPoolExecutor

def scan_port(target_ip, port):
    """
    Scans a single port on the target IP address.
    """
    # ports = []
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)  # Timeout for socket connection
            if s.connect_ex((target_ip, port)) == 0:
                print(f"[+] Port {port} is open.")
                # ports.append(port)
                return port
    except Exception:
        pass
    return None

def main():
    print("Simple Port Scanner")
    target_ip = input("Enter the target IP address: ")
    port_range = input("Enter the port range (e.g., 20-100): ")

    # Parse port range
    start_port, end_port = map(int, port_range.split('-'))
    print(f"Scanning {target_ip} for open ports from {start_port} to {end_port}...\n")

    open_ports = []
    with ThreadPoolExecutor(max_workers=50) as executor:
        results = executor.map(lambda port: scan_port(target_ip, port), range(start_port, end_port + 1))
        open_ports = [port for port in results if port]

    if open_ports:
        # print(f"Open ports found on {target_ip}: {', '.join(map(str, open_ports))}")
        print(f"Open ports found on {target_ip}")
    else:
        print(f"No open ports found on {target_ip}.")

if __name__ == "__main__":
    main()