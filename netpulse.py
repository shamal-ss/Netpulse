#!/usr/bin/env python3
import socket
import sys
import subprocess
import time

def banner():
    print(r"""
    _   _      _   ______       _             
   | \ | |    | |  | ___ \     | |            
   |  \| | ___| |_ | |_/ /_   _| |___  ___    
   | . ` |/ _ \ __||  __/| | | | / __|/ _ \   
   | |\  |  __/ |_ | |   | |_| | \__ \  __/   
   \_| \_/\___|\__|\_|    \__,_|_|___/\___| by shamal-⌨  
    """)

def check_host(target):
    try:
        ip = socket.gethostbyname(target)
        print(f"[*] Resolving target {target} -> {ip}")
        command = ["ping", "-c", "1", ip]
        response = subprocess.call(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if response == 0:
            print(f"[*] Host {ip} is online and reachable.")
        else:
            print(f"[-] Host {ip} did not respond to ping, proceeding with port scan...")
        return ip
    except socket.gaierror:
        print(f"[-] Error: Could not resolve hostname {target}")
        sys.exit(1)

def scan_ports(ip, ports):
    print(f"[*] Scanning ports on {ip}...")
    open_ports = []
    start_time = time.time()
    
    for port in ports:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.5)
            result = s.connect_ex((ip, port))
            if result == 0:
                open_ports.append(port)
            s.close()
        except KeyboardInterrupt:
            print("\n[-] Scan aborted by user.")
            sys.exit()
        except socket.error:
            pass
            
    end_time = time.time()
    print(f"[*] Scan completed in {end_time - start_time:.2f} seconds.")
    return open_ports

def main():
    banner()
    if len(sys.argv) < 2:
        print("Usage: python3 netpulse.py <website_or_ip>")
        sys.exit(1)
        
    target = sys.argv[1]
    ip = check_host(target)
    
    common_ports = [21, 22, 23, 25, 53, 80, 110, 135, 139, 443, 445, 993, 995, 3306, 3389, 8080]
    
    open_ports = scan_ports(ip, common_ports)
    
    print("\n" + "=" * 45)
    print("                  NETPULSE REPORT")
    print("=" * 45)
    print(f" Target : {target}")
    print(f" IP     : {ip}")
    print("-" * 45)
    print(" Open Ports:")
    if open_ports:
        for p in open_ports:
            print(f"   [+] Port {p} is OPEN")
    else:
        print("   [-] No open ports found among checked targets.")
    print("=" * 45)

if __name__ == "__main__":
    main()

