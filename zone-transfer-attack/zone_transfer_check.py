import subprocess
import os

# Function to read domains from the file
def read_domains_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            # Lines starting with '#' will be treated as comments and skipped
            domains = [line.strip() for line in file.readlines() if line.strip() and not line.strip().startswith("#")]
        return domains
    except FileNotFoundError:
        print(f"[!] {file_path} not found!")
        return []

def get_ns_records(domain):
    """Get NS records using dig"""
    try:
        result = subprocess.check_output(["dig", "+short", "NS", domain], text=True)
        return [ns.strip('.') for ns in result.splitlines() if ns]
    except subprocess.CalledProcessError:
        return []

def try_zone_transfer(domain, nameserver):
    """Attempt AXFR zone transfer"""
    try:
        print(f"\n[*] Trying AXFR on {domain} via {nameserver}...")
        output = subprocess.check_output(["dig", "AXFR", f"@{nameserver}", domain], text=True)
        if "Transfer failed" in output or "connection timed out" in output or "REFUSED" in output:
            print(f"[-] Zone transfer refused by {nameserver}")
        elif "ANSWER SECTION" in output or domain in output:
            print(f"[+] Zone transfer SUCCESS for {domain} via {nameserver}")
            print(output)
        else:
            print(f"[-] No data returned by {nameserver}")
    except subprocess.CalledProcessError:
        print(f"[-] Error querying {nameserver}")

def main():
    # Path to companies.txt (same directory as the script)
    file_path = os.path.join(os.getcwd(), "companies.txt")
    
    # Load domains from the file
    domains = read_domains_from_file(file_path)
    if not domains:
        print("[!] No domains to process!")
        return

    for domain in domains:
        print(f"\n[*] Processing {domain}...")
        ns_servers = get_ns_records(domain)
        if not ns_servers:
            print(f"[!] No NS records found for {domain}")
            continue
        for ns in ns_servers:
            try_zone_transfer(domain, ns)

if __name__ == "__main__":
    main()
