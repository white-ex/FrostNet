import socket
import json
from concurrent.futures import ThreadPoolExecutor

def get_service(port):
    services = {
        21: "FTP",
        22: "SSH",
        80: "HTTP",
        443: "HTTPS",
        135: "RPC",
        3306: "MySQL",
    }
    return services.get(port, "Unknown")

print("scanner tool")
target = input("Target IP: ")

mode = input("Mode (fast/full): ")

if mode == "fast":
    ports = range(1, 500)
else:
    ports = range(1, 1025)

open_ports = []

def scan_port(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.2)

    if s.connect_ex((target, port)) == 0:
        service = get_service(port)
        print(f"[+] {port} ({service})")
        open_ports.append({
            "port": port,
            "service": service
        })

    s.close()

with ThreadPoolExecutor(max_workers=100) as executor:
    executor.map(scan_port, ports)

with open("report.txt", "w") as f:
    for p in open_ports:
        f.write(f"{p['port']} - {p['service']}\n")

with open("report.json", "w") as f:
    json.dump(open_ports, f, indent=4)

print("\nScan complete. Reports saved (txt + json).")