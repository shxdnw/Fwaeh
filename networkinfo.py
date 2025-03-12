#
import os
import platform
import socket
import subprocess
import sys
from typing import List, Tuple

# Check if the terminal supports ANSI color codes
def supports_color() -> bool:
    """Check if the terminal supports ANSI color codes."""
    # Check for Windows
    if sys.platform == "win32":
        return False  # Disable colors by default on Windows (unless using Windows Terminal)
    # Check for non-Windows terminals
    return sys.stdout.isatty()  # True if connected to a terminal

# Define colors based on terminal support
SUPPORTS_COLOR = supports_color()

class Colors:
    HEADER = '\033[95m' if SUPPORTS_COLOR else ''
    OKBLUE = '\033[94m' if SUPPORTS_COLOR else ''
    OKGREEN = '\033[92m' if SUPPORTS_COLOR else ''
    WARNING = '\033[93m' if SUPPORTS_COLOR else ''
    FAIL = '\033[91m' if SUPPORTS_COLOR else ''
    ENDC = '\033[0m' if SUPPORTS_COLOR else ''

# Check if netifaces is installed
try:
    import netifaces
    from netifaces import AF_INET, AF_INET6, AF_LINK
    NETIFACES_AVAILABLE = True
except ImportError:
    NETIFACES_AVAILABLE = False
    print(f"{Colors.WARNING}Warning: netifaces module is not installed. Some features will be limited.{Colors.ENDC}")
    print(f"{Colors.WARNING}Install it with: pip install netifaces{Colors.ENDC}")

# Helper functions
def print_section(title: str) -> None:
    """Print a section header with a border"""
    border = "═" * (len(title) + 4)
    print(f"\n{Colors.HEADER}╔{border}╗{Colors.ENDC}")
    print(f"{Colors.HEADER}║  {title}  ║{Colors.ENDC}")
    print(f"{Colors.HEADER}╚{border}╝{Colors.ENDC}")

def print_subsection(title: str) -> None:
    """Print a subsection header"""
    print(f"\n{Colors.OKBLUE}• {title}:{Colors.ENDC}")

def run_cmd(cmd: List[str], privileged: bool = False) -> str:
    """Run a system command and return its output"""
    try:
        if privileged and os.name != 'nt' and os.geteuid() != 0:
            cmd = ["sudo"] + cmd
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except Exception as e:
        return f"{Colors.FAIL}Error: {str(e)}{Colors.ENDC}"

# ------------------ SCAN LEVELS ------------------ #
def basic_scan():
    print_section("Basic Network Scan")
    
    # Host information
    print_subsection("System Information")
    print(f"  Hostname: {Colors.OKGREEN}{socket.gethostname()}{Colors.ENDC}")
    print(f"  OS: {Colors.OKGREEN}{platform.system()} {platform.release()}{Colors.ENDC}")
    
    # Public IP
    print_subsection("Public IP Address")
    try:
        public_ip = run_cmd(['curl', '-s', 'ifconfig.me'])
        print(f"  {Colors.OKGREEN}{public_ip}{Colors.ENDC}")
    except:
        print(f"  {Colors.FAIL}Could not determine public IP{Colors.ENDC}")
    
    # Network interfaces
    if NETIFACES_AVAILABLE:
        print_subsection("Network Interfaces")
        for iface in netifaces.interfaces():
            addrs = netifaces.ifaddresses(iface)
            if AF_INET in addrs:
                print(f"  {Colors.OKBLUE}{iface}:{Colors.ENDC}")
                print(f"    IPv4: {Colors.OKGREEN}{addrs[AF_INET][0]['addr']}{Colors.ENDC}")
                if AF_LINK in addrs:
                    print(f"    MAC: {Colors.OKGREEN}{addrs[AF_LINK][0]['addr']}{Colors.ENDC}")
    else:
        print(f"  {Colors.WARNING}Network interface details unavailable (netifaces not installed).{Colors.ENDC}")

def medium_scan():
    basic_scan()  # Include basic scan details
    print_section("Medium Network Scan")
    
    # Gateways
    if NETIFACES_AVAILABLE:
        print_subsection("Gateways")
        gateways = netifaces.gateways()
        for family, gateway in gateways['default'].items():
            print(f"  Family: {Colors.OKBLUE}AF_INET{family if family != 2 else ''}{Colors.ENDC}")
            print(f"  Gateway: {Colors.OKGREEN}{gateway[0]}{Colors.ENDC}")
            print(f"  Interface: {Colors.OKGREEN}{gateway[1]}{Colors.ENDC}")
    
    # Routing table
    print_subsection("Routing Table")
    system = platform.system()
    if system == "Windows":
        print(run_cmd(['route', 'print']))
    else:
        print(run_cmd(['ip', 'route'] if system == "Linux" else ['netstat', '-nr']))

def verbose_scan():
    medium_scan()  # Include medium scan details
    print_section("Verbose Network Scan")
    
    # Firewall status
    print_subsection("Firewall Configuration")
    system = platform.system()
    if system == "Windows":
        print(run_cmd(['netsh', 'advfirewall', 'show', 'allprofiles']))
        print(run_cmd(['netsh', 'advfirewall', 'firewall', 'show', 'rule', 'name=all']))
    elif system == "Linux":
        print(run_cmd(['ufw', 'status', 'verbose'], privileged=True))
        print(run_cmd(['iptables', '-L', '-n', '-v'], privileged=True))
    elif system == "Darwin":
        print(run_cmd(['pfctl', '-s', 'rules'], privileged=True))
    
    # Active connections
    print_subsection("Active Connections")
    print(run_cmd(['netstat', '-ano'] if system == "Windows" else ['ss', '-tunlp']))

# ------------------ MENU AND MAIN EXECUTION ------------------ #
def show_menu():
    print(f"\n{Colors.HEADER}=== NETWORK SCANNER ==={Colors.ENDC}")
    print(f"{Colors.OKGREEN}1. Basic Scan{Colors.ENDC}       (Quick overview)")
    print(f"{Colors.OKGREEN}2. Medium Scan{Colors.ENDC}      (Detailed network info)")
    print(f"{Colors.OKGREEN}3. Verbose Scan{Colors.ENDC}     (Everything + firewall)")
    print(f"{Colors.FAIL}4. Exit{Colors.ENDC}")
    choice = input(f"{Colors.WARNING}Choose an option (1-4): {Colors.ENDC}")
    return choice

def main():
    while True:
        choice = show_menu()
        
        if choice == '1':
            basic_scan()
        elif choice == '2':
            medium_scan()
        elif choice == '3':
            if os.name != 'nt' and os.geteuid() != 0:
                print(f"\n{Colors.WARNING}⚠️  Some commands might require sudo privileges!{Colors.ENDC}")
            verbose_scan()
        elif choice == '4':
            print(f"\n{Colors.OKGREEN}Exiting...{Colors.ENDC}")
            break
        else:
            print(f"\n{Colors.FAIL}Invalid choice! Please select 1-4.{Colors.ENDC}")
        
        input(f"\n{Colors.OKGREEN}Press Enter to continue...{Colors.ENDC}")

# Ensure the script runs when executed
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.FAIL}Operation cancelled by user.{Colors.ENDC}")
        sys.exit(1)
