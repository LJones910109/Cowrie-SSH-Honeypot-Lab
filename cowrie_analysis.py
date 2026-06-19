#!/usr/bin/env python3
import json
from collections import Counter

LOG_FILE = '/home/kali/cowrie/var/log/cowrie/cowrie.json'

events = []
with open(LOG_FILE) as f:
    for line in f:
        events.append(json.loads(line))

print("=" * 55)
print("       COWRIE HONEYPOT - SESSION SUMMARY")
print("=" * 55)

failed = [e for e in events if e.get('eventid') == 'cowrie.login.failed']
success = [e for e in events if e.get('eventid') == 'cowrie.login.success']
print(f"\n[*] Total Events Logged: {len(events)}")
print(f"[*] Failed Logins:       {len(failed)}")
print(f"[*] Successful Logins:   {len(success)}")

commands = [e.get('input') for e in events if e.get('eventid') == 'cowrie.command.input']
print(f"\n[*] Commands Executed ({len(commands)} total):")
for cmd in commands:
    print(f"    -> {cmd}")

ips = [e.get('src_ip') for e in events if e.get('src_ip')]
ip_counts = Counter(ips)
print(f"\n[*] Source IPs:")
for ip, count in ip_counts.most_common():
    print(f"    {ip} — {count} events")

print("\n" + "=" * 55)
print("  MITRE ATT&CK MAPPING")
print("=" * 55)
print("  T1110 — Brute Force")
print("  T1059 — Command & Scripting Interpreter")
print("  T1087 — Account Discovery (whoami)")
print("  T1083 — File & Directory Discovery (ls)")
print("  T1003 — Credential Dumping (cat /etc/passwd)")
print("=" * 55)
