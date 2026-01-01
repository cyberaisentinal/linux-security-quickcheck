# Linux Security QuickCheck

A quick, **read-only** Linux security visibility script that prints a small report:

- System info (user / host / kernel)
- Logged-in users
- Listening network ports (top 20)
- Key SSH daemon settings (from `/etc/ssh/sshd_config`)
- Firewall status (UFW if installed)

## Why this exists
I built this as a simple portfolio project to demonstrate:
- Linux and security fundamentals
- Python scripting and automation
- Practical reporting for troubleshooting, IT, and entry-level cybersecurity roles

## Requirements
- Linux
- Python 3.9+ (works on most Python 3 versions)

## Run
```bash
python3 quickcheck.py

⚠️ This tool is read-only and intended for educational and defensive security use only.

⚠️ Note: Output shown below was captured on macOS (Darwin).
On Linux systems, firewall (UFW) and SSH config results may differ.

## Example Output

Below is a sample run of the script on a local system:

![Linux Security QuickCheck Output](output_screenshot.png)

⚠️ This tool is read-only and intended for educational and defensive security use only.
