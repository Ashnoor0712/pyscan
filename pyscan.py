import socket

import json
import csv

from concurrent.futures import ThreadPoolExecutor

import argparse

def get_args():
    parser = argparse.ArgumentParser(description="PyScan - a multithreaded TCP port scanner")
    parser.add_argument("-t", "--target", required=True, help="Target IP or hostname")
    parser.add_argument("-p", "--ports", default="1-1024", help="Port range, e.g. 1-1024")
    parser.add_argument("--threads", type=int, default=100, help="Number of threads to use")
    parser.add_argument("-o", "--output", help="Save results to a file (e.g. results.json or results.csv)")
    return parser.parse_args()
    
def parse_port_range(port_str):
    start, end = port_str.split("-")
    return range(int(start), int(end) + 1)



def scan_port(target, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    result = sock.connect_ex((target, port))
    

    if result == 0:
        try:
            #banner = sock.recv(1024).decode().strip()
            sock.send(b"HEAD / HTTP/1.1\r\nHost: " + target.encode() + b"\r\n\r\n")
            banner = sock.recv(1024).decode(errors="ignore").strip()
        except:
            banner = "No banner"
        first_line = banner.splitlines()[0] if banner else banner
        print(f"Port {port} is OPEN - {first_line}")
        #print(f"Port {port} is OPEN - {banner.splitlines()[0] if banner else banner}")
        #print(f"Port {port} is OPEN")
        sock.close()
        return {"port": port, "status": "open", "banner": first_line}
    
    sock.close()
    return None

import json
import csv

def save_results(results, filename):
    if filename.endswith(".json"):
        with open(filename, "w") as f:
            json.dump(results, f, indent=4)
    elif filename.endswith(".csv"):
        with open(filename, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["port", "status", "banner"])
            writer.writeheader()
            writer.writerows(results)
    else:
        print("Unsupported file type. Use .json or .csv")
        return

    print(f"Results saved to {filename}")

def main():
    args = get_args()
    target = args.target
    ports = parse_port_range(args.ports)
    threads = args.threads

    print(f"Scanning {target} ...")
    with ThreadPoolExecutor(max_workers=threads) as executor:
        #executor.map(lambda port: scan_port(target, port), ports)
        results = list(executor.map(lambda port: scan_port(target,port), ports))
    print("Scan finished.")
    
    open_ports = [r for r in results if r is not None]
    
    if args.output:
        save_results(open_ports, args.output)
    
if __name__ == "__main__":
    main()

