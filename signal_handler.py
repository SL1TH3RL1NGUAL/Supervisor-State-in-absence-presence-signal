#!/usr/bin/env python3
import sys
import json
import uuid
import hashlib
from datetime import datetime
import os

def get_last_hash():
    if not os.path.exists("witness_log.jsonl"):
        return "0" * 64
    try:
        with open("witness_log.jsonl", "rb") as f:
            f.seek(0, 2)
            if f.tell() == 0: return "0" * 64
            f.seek(max(0, f.tell() - 1024))
            lines = f.readlines()
            if not lines: return "0" * 64
            return hashlib.sha256(lines[-1].strip()).hexdigest()
    except Exception:
        return "0" * 64

def log_witness_event(signal_type, raw_url):
    prev_hash = get_last_hash()
    log_entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "event_id": str(uuid.uuid4()),
        "signal": signal_type,
        "source_uri": raw_url,
        "previous_hash": prev_hash
    }
    with open("witness_log.jsonl", "a") as f:
        f.write(json.dumps(log_entry) + "\n")
    print(f"[+] Event chained. Previous Hash: {prev_hash[:10]}...")

def handle_signal(url):
    try:
        signal_type = url.split("://")[1].split("?")[0]
        print(f"[*] Signal received: {signal_type}")
        log_witness_event(signal_type, url)
        
        if signal_type == "report":
            stix_report = {
                "type": "bundle",
                "id": f"bundle--{uuid.uuid4()}",
                "objects": [{
                    "type": "indicator",
                    "spec_version": "2.1",
                    "id": f"indicator--{uuid.uuid4()}",
                    "created": datetime.utcnow().isoformat() + "Z",
                    "name": "Presence Signal",
                    "pattern": f"[url:value = '{url}']",
                    "pattern_type": "stix"
                }]
            }
            print("[!] Routing STIX 2.1 bundle...")
            print(json.dumps(stix_report, indent=2))
    except Exception as e:
        print(f"[!] Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        handle_signal(sys.argv[1])
    else:
        print("Usage: ./signal_handler.py presence://[type]")
