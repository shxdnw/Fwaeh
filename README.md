# Network Scanner 🔍

A Python script to analyze network configurations and firewall settings with an interactive menu system. Works on Windows, Linux, and macOS.

---

## Features ✨
- **Three scan levels**:
  - **Simple**: Quick overview (hostname, IP, interfaces).
  - **Medium**: Detailed network info (gateways, routing tables).
  - **Verbose**: Full audit (firewall rules, active connections).
- **Cross-platform**: Works on Windows, Linux, and macOS.
- **Interactive menu**: Easy-to-use terminal interface.

---

## Installation ⚙️

1. **Install Python 3.6+**:
   - Download from [python.org](https://www.python.org/downloads/).

2. **Install dependencies**:
   ```bash
   pip install netifaces
Download the script:

```bash
git clone https://github.com/shxdnw/Fwaeh.git
cd networkinfo
```
Usage 🚀
Run the script:

```bash
python networkinfo.py
```
Menu Options:
Simple Scan: Quick network overview.

Medium Scan: Detailed network configuration.

Verbose Scan: Full network and firewall audit.

Exit: Quit the program.

Note: Verbose scan may require admin privileges on Unix systems:

```bash
sudo python3 networkinfo.py
```
Dependencies 📦

Python 3.6+

netifaces
