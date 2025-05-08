# **zone-transfer-attack**

## DNS Zone Transfer Vulnerability

A **DNS Zone Transfer** (AXFR) vulnerability can pose significant risks if not properly secured. Here’s a breakdown of the threats it can introduce:

### 1. Exposure of Sensitive Domain Information
A successful zone transfer can expose a lot of internal details about the target domain, including:

- **All subdomains**: Names of internal subdomains, which can give attackers insight into the internal structure of a network (e.g., `dev.example.com`, `mail.example.com`, `intranet.example.com`).
- **IP addresses**: Internal and external IP addresses of the domain’s servers. This information helps attackers identify entry points for further attacks.
- **Nameservers**: Attackers can get a list of authoritative nameservers that manage the domain, potentially allowing them to target DNS infrastructure vulnerabilities.
- **Other resource records**: This includes mail servers, TXT records, and potentially, sensitive configurations (e.g., SPF, DKIM for email).

### 2. Reconnaissance for Targeted Attacks
With full knowledge of all subdomains and IP addresses, attackers can:

- **Conduct targeted attacks**: Knowing all subdomains allows them to tailor attacks, such as exploiting a vulnerable service running on one of the subdomains.
- **Find hidden services**: Attackers may identify servers that were intended to be private or internal but are inadvertently exposed.
- **Phishing campaigns**: Knowing the exact names of subdomains and mail servers can make phishing campaigns more convincing.

### 3. Brute Force Attacks on Subdomains
Once an attacker has a list of subdomains, they can:

- **Brute-force subdomain names**: With common subdomain names such as `mail`, `dev`, or `intranet`, they can attempt to exploit any weak services running on these subdomains (e.g., HTTP, FTP).
- **Exploit outdated systems**: They can identify subdomains running legacy or vulnerable systems (e.g., old web applications, outdated content management systems like WordPress).

### 4. Exposure of DNS Configuration Data
Sensitive DNS configuration data such as:

- **SPF, DKIM, and DMARC records**: These records help in email authentication and can be exploited for spoofing attacks if not configured properly.
- **MX (Mail Exchange) records**: If the domain relies on external or specific mail servers, attackers can target those mail servers for email-based attacks or DoS attacks.

### 5. Denial of Service (DoS) Attacks
**Amplified Denial of Service (DoS)**: Attackers can also use the information from a zone transfer to amplify their attack. If they identify nameservers or domain resolvers, they can attempt to overwhelm those systems with requests, making them unavailable for legitimate use.

Securing your DNS zone transfers is crucial to protecting the integrity and confidentiality of your domain's infrastructure.


## Zone Transfer Attack Check

`zone-transfer-attack` is a python tool designed to attempt DNS zone transfers (AXFR) on target domains by querying their authoritative DNS servers. It helps security professionals identify misconfigurations or vulnerabilities in DNS servers that might expose sensitive zone data.

### **Features**

* Attempts DNS zone transfer (AXFR) on target domains.
* Probes all authoritative DNS servers associated with the domain.
* Provides output indicating whether zone transfer is allowed or refused.
* Outputs detailed responses when a zone transfer is successful.

---

## **Getting Started**

To get started with `zone-transfer-attack`, follow the steps below.

### **Prerequisites**

* Python 3.x
* `dig` tool (usually part of the `dnsutils` package on Linux)

### **Install Dependencies**

Make sure `dig` is installed. On a Debian-based system (like Kali), you can install it with:

```bash
sudo apt update
sudo apt install dnsutils
```

### **Clone the Repository**

Clone the project to your local machine:

```bash
git clone https://github.com/5urg3on/Automation.git
cd Automation/zone-transfer-attack
```

### **Setup and Usage**

1. **Prepare your `companies.txt` file**: List the domains you want to test, one per line. The file should be placed in the same folder as the Python script.

   Example `companies.txt`:

   ```
   example.com
   targetdomain.com
   anotherdomain.org
   ```

2. **Run the script**:

```bash
python3 zone_transfer_check.py
```

The script will attempt zone transfers for each domain listed in `companies.txt`, trying each authoritative nameserver.

### **Output**

The script will print results in the terminal, indicating whether zone transfer was successful or refused. Successful transfers will display DNS records, while failures will indicate a refusal or error.

Example output:

```bash
[*] Trying AXFR on example.com via ns1.example.com...
[-] Zone transfer refused by ns1.example.com

[*] Trying AXFR on anotherdomain.org via ns1.anotherdomain.org...
[+] Zone transfer SUCCESS for anotherdomain.org via ns1.anotherdomain.org
example.com.    86400 IN  A   93.184.216.34
www.example.com. 86400 IN  CNAME example.com.
...
```

---

## **Contributing**

Contributions are welcome! If you find bugs or would like to enhance the functionality, feel free to open issues or submit pull requests.

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-name`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature-name`).
5. Create a pull request.

---

## **License**

This project is licensed under the MIT License.

---

## **Acknowledgments**

* Inspired by common DNS auditing tools.
* Uses `dig` for querying DNS servers.

---

### Let me know if you'd like any additional details, changes, or customizations!
