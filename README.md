# 🍯 Cowrie SSH Honeypot Lab

**Author:** Lillian Jones | [GitHub: LJones910109](https://github.com/LJones910109)  
**Environment:** Kali Linux 2026.1 (VMware Fusion) | MacBook Air  
**Category:** Defensive Security / Threat Detection / Blue Team  
**Difficulty:** Intermediate  

---

## 📌 Objective

Deploy a Cowrie SSH honeypot to simulate a vulnerable service, capture attacker behavior, analyze session logs, and map findings to the MITRE ATT&CK framework. This lab demonstrates real-world deception-based defense techniques used in SOC environments.

---

## 🛠️ Tools & Technologies

| Tool | Purpose |
|------|---------|
| Cowrie 3.0.4 | SSH/Telnet honeypot |
| Python 3.13 | Log parsing and analysis |
| Kali Linux 2026.1 | Attack simulation host |
| VMware Fusion | Virtualization platform |
| JSON | Log format for SIEM ingestion |

---

## 🧪 Lab Environment

```
┌─────────────────────────────────┐
│   MacBook Air (Host)            │
│                                 │
│  ┌──────────────────────────┐   │
│  │  Kali Linux VM           │   │
│  │  IP: 172.16.148.132      │   │
│  │                          │   │
│  │  Cowrie Honeypot         │   │
│  │  Port: 2222 (fake SSH)   │   │
│  │  Logs: cowrie.json       │   │
│  └──────────────────────────┘   │
└─────────────────────────────────┘
```

---

## 📋 Methodology

### Phase 1 — Install & Configure Cowrie

Installed Cowrie from source using Python virtualenv and configured a fake hostname to deceive attackers:

```bash
git clone https://github.com/cowrie/cowrie
cd cowrie
virtualenv cowrie-env
source cowrie-env/bin/activate
pip install -r requirements.txt
pip install -e .
cp src/cowrie/data/etc/cowrie.cfg.dist etc/cowrie.cfg
# Set hostname = webserver01 in etc/cowrie.cfg
cowrie start
```

Verified honeypot was listening:
```bash
ss -tlnp | grep 2222
# LISTEN 0.0.0.0:2222 — confirmed active
```

---

### Phase 2 — Simulate Attack

Simulated an SSH brute-force and post-exploitation session from localhost:

```bash
ssh -p 2222 root@localhost
# Password attempts: 123456, password, admin
# Successful login achieved
```

Post-exploitation commands executed inside the honeypot shell:

```bash
whoami
ls
cat /etc/passwd
uname -a
exit
```

All commands were silently logged by Cowrie. The attacker was served a **fake shell with fabricated system responses** — they never touched the real host.

---

### Phase 3 — Log Analysis

Parsed `cowrie.json` with a custom Python script to extract session data:

```
=======================================================
       COWRIE HONEYPOT - SESSION SUMMARY
=======================================================

[*] Total Events Logged: 16
[*] Failed Logins:       1
[*] Successful Logins:   1

[*] Commands Executed (5 total):
    -> whoami
    -> ls
    -> cat /etc/passwd
    -> uname -a
    -> exit

[*] Source IPs:
    127.0.0.1 — 16 events

=======================================================
  MITRE ATT&CK MAPPING
=======================================================
  T1110 — Brute Force
  T1059 — Command & Scripting Interpreter
  T1087 — Account Discovery (whoami)
  T1083 — File & Directory Discovery (ls)
  T1003 — Credential Dumping (cat /etc/passwd)
=======================================================
```

---

## 📊 Findings

| Event | Count | Details |
|-------|-------|---------|
| Total Events | 16 | Full session lifecycle captured |
| Failed Logins | 1 | Brute-force attempt detected |
| Successful Logins | 1 | Weak credential accepted by honeypot |
| Commands Executed | 5 | Post-exploitation activity logged |
| Session Duration | 90.7s | Full TTY session recorded |
| Source IP | 127.0.0.1 | Simulated internal attacker |

---

## 🎯 MITRE ATT&CK Mapping

| Technique ID | Technique Name | Observed Behavior |
|---|---|---|
| T1110 | Brute Force | Multiple password attempts before success |
| T1059 | Command & Scripting Interpreter | Bash commands executed post-login |
| T1087 | Account Discovery | `whoami` — attacker enumerated current user |
| T1083 | File & Directory Discovery | `ls` — attacker listed directory contents |
| T1003 | OS Credential Dumping | `cat /etc/passwd` — attacker read password file |

---

## 💡 Key Takeaways

- **Cowrie serves fake responses** — attackers believe they have a real shell while every command is silently logged
- **JSON log format** is natively compatible with Splunk, Elastic SIEM, and other ingestion pipelines
- **Honeypots detect threats that firewalls miss** — any connection to a honeypot is inherently suspicious
- **TTY session recording** captures full attacker keystrokes for forensic playback
- **Deception-based defense** is a core blue team skill used in enterprise SOC environments

---

## 📁 Repository Files

```
cowrie-honeypot-lab/
├── README.md               # This file
├── cowrie_analysis.py      # Custom Python log parser
├── cowrie.json             # Sample Cowrie session log
└── screenshots/
    ├── cowrie-running.png  # Honeypot status confirmation
    ├── attack-session.png  # SSH attack simulation
    └── analysis-output.png # Python script output
```

---

## 🔗 References

- [Cowrie GitHub Repository](https://github.com/cowrie/cowrie)
- [MITRE ATT&CK — T1110 Brute Force](https://attack.mitre.org/techniques/T1110/)
- [MITRE ATT&CK — T1059 Command & Scripting Interpreter](https://attack.mitre.org/techniques/T1059/)
- [MITRE ATT&CK — T1003 OS Credential Dumping](https://attack.mitre.org/techniques/T1003/)

---

*This lab was conducted in an isolated virtual environment for educational purposes only.*
