#!/usr/bin/env python3
"""
Linux Security QuickCheck
Author: Levi Davis

Description:
A quick, read-only Linux security visibility script.
Checks basic system info, logged-in users, listening ports, SSH daemon config,
and firewall status (UFW if available).
"""

from __future__ import annotations

import os
import shutil
import subprocess
from datetime import datetime
from typing import List


def run(cmd: List[str]) -> str:
    """Run a command safely (no shell). Returns output or 'Unavailable'."""
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return (result.stdout or result.stderr).strip() or "Unavailable"
    except Exception:
        return "Unavailable"


def header(title: str) -> None:
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


def read_sshd_settings(path: str = "/etc/ssh/sshd_config") -> str:
    """Read key SSHD settings from sshd_config without using grep."""
    if not os.path.exists(path):
        return "SSH config not found."

    keys = {"port", "permitrootlogin", "passwordauthentication"}
    found = {}

    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                parts = line.split()
                if len(parts) < 2:
                    continue
                k = parts[0].lower()
                if k in keys and k not in found:
                    found[k] = " ".join(parts[1:])
    except Exception:
        return "Unable to read SSH config."

    if not found:
        return "No key SSH settings found (or file is non-standard)."

    # Pretty output
    order = ["port", "permitrootlogin", "passwordauthentication"]
    lines = []
    for k in order:
        if k in found:
            lines.append(f"{k}: {found[k]}")
    return "\n".join(lines)


def main() -> None:
    print("Linux Security QuickCheck")
    print(f"Run time: {datetime.now()}")
    print(f"User: {run(['whoami'])}")
    print(f"Hostname: {run(['hostname'])}")
    print(f"OS: {run(['uname', '-a'])}")

    header("Logged-in Users")
    print(run(["who"]))

    header("Listening Network Ports (top 20)")
    if shutil.which("ss"):
        print(run(["bash", "-lc", "ss -tuln | head -n 20"]))
    elif shutil.which("netstat"):
        print(run(["bash", "-lc", "netstat -tuln | head -n 20"]))
    else:
        print("ss/netstat not available on this system.")

    header("SSH Configuration (Key Settings)")
    print(read_sshd_settings())

    header("Firewall Status (UFW)")
    if shutil.which("ufw"):
        print(run(["ufw", "status"]))
    else:
        print("UFW not installed (or not in PATH).")

    print("\nQuickCheck complete.")


if __name__ == "__main__":
    main()
