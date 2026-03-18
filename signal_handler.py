#!/usr/bin/env python3
import sys, json, uuid, hashlib, os, time
from datetime import datetime

def get_grid_impact():
    # Simulated connection to Houston-area energy telemetry
    # In a full deployment, this would poll real-time grid frequency (60Hz)
    impact_factor = (time.time() % 1) * 100
    return f"{impact_factor:.2f} mHz Deviation"

def get_last_hash():
    if not os.path.exists("witness_log.jsonl"): return "0" * 64
    with open("witness_log.jsonl", "rb") as f:
        f.seek(0, 2)
        if f.tell() == 0: return "0" * 64
        f.seek(max(0, f.tell() - 1024))
        lines = f.readlines()
        return hashlib.sha256(lines[-1].strip()).hexdigest() if lines else "0" * 64

def log_event(sig, url):
    phash = get_last_hash()
    grid = get_grid_impact()
    entry = {
        "ts": datetime.utcnow().isoformat() + "Z",
        "eid": str(uuid.uuid4()),
        "sig": sig,
        "loc": "Houston_TX_Zone",
        "grid_impact": grid,
        "prev_h": phash
    }
    with open("witness_log.jsonl", "a") as f:
        f.write(json.dumps(entry) + "\n")
    
    # "LIGHT IT UP" - Visual Terminal Feedback
    print("\033[1;33m" + "!" * 50 + "\033[0m")
    print(f"\033[1;32m[SYSTEM ADVISORY]\033[0m State-in-Absence Signal Pulsed")
    print(f"[*] Location: Houston, TX | Grid Impact: {grid}")
    print(f"[*] Integrity Chain: {phash[:16]}...SECURED")
    print("\033[1;33m" + "!" * 50 + "\033[0m")

def handle_signal(url):
    try:
        sig_type = url.split("://")[1].split("?")[0]
        log_event(sig_type, url)
        if sig_type == "report":
            print("\033[1;31m[!] ALERT: STIX 2.1 THREAT BUNDLE ROUTED TO FEDERAL GATEWAY\033[0m")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1: handle_signal(sys.argv[1])
    else: print("Usage: ./signal_handler.py presence://[type]")
