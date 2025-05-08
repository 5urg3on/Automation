# **zone-transfer-attack**

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

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

## **Acknowledgments**

* Inspired by common DNS auditing tools.
* Uses `dig` for querying DNS servers.

---

### Let me know if you'd like any additional details, changes, or customizations!
