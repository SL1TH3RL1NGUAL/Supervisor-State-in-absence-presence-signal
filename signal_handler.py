#!/usr/bin/env python3
import sys

def handle_signal(url):
    try:
        signal_type = url.split("://")[1].split("?")[0]
        print(f"[*] State-in-absence signal received: {signal_type}")
        if signal_type == "witness":
            print("[+] Initiating Witness-Log retention...")
        elif signal_type == "report":
            print("[!] Routing STIX 2.1 threat report to federal gateways...")
    except IndexError:
        print("[!] Error: Invalid signal format.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        handle_signal(sys.argv[1])
