# RoutR_MauraDr


NetVision is a Bash-based utility that automates network discovery, quick port scanning (with stealthy SYN scans and OS detection), and simple router analysis (including an attempt to detect router firmware). Additionally, it installs and starts **netcat** (on port 6666) and **ngrok** (TCP on port 6667, HTTP on port 80) for easy remote tunneling and local port listening.

---

## TODO: 

**Add auto-search** for firmware bugs and auto ssh with firmware defualt passwords

## **Table of Contents**  
1. [Features](#features)  
2. [Requirements](#requirements)  
3. [Installation](#installation)  
4. [Usage](#usage)  
5. [How It Works (Detailed)](#how-it-works-detailed)  
   - [Firmware Detection](#firmware-detection)  
   - [ARP Table & DNS Table Gathering](#arp-table--dns-table-gathering)  
   - [Stealth Port Scan & OS Detection](#stealth-port-scan--os-detection)  
   - [Ngrok & Netcat Setup](#ngrok--netcat-setup)  
   - [Output Files & Logs](#output-files--logs)  
6. [License](#license)  

---

## **Features** <a id="features"></a>  
- **Local Network Data**  
  - Local IP, Router IP, WAN IP, DNS servers, Subnet mask, Router MAC, etc.  
- **ARP Table Scan**  
  - Resolves device IPs, MAC addresses, and hostnames on the local LAN.  
- **Router DNS Table**  
  - Attempts to discover local DNS entries via SNMP, UPnP, and brute force DNS queries.  
- **Router Make & Model**  
  - Scrapes the router’s login page for common brand keywords.  
- **Router Firmware Detection**  
  - Tries SNMP (`snmpwalk`), HTTP scraping, and UPnP for firmware strings.  
- **Stealthy Quick Port Scan**  
  - Uses **nmap** for a SYN scan on **top 10 ports**, plus **OS detection** (requires `sudo`).  
  - Saves open ports to both `.txt` and `.json` for easy review.  
- **Netcat Listener**  
  - Listens on **port 6666**.  
- **Ngrok Tunnels**  
  - **TCP** tunnel for port **6667**  
  - **HTTP** tunnel for port **80**  

---

## **Requirements** <a id="requirements"></a>  
- **Bash** (most Linux/Unix-based systems have it by default).  
- **curl**, **wget**, or **apt-get/yum** for automatic installation (optional but recommended).  
- **sudo/root** privileges to:
  - Install packages.  
  - Run stealth scans (SYN) and OS detection reliably.  
  - Listen on privileged ports if needed (80).  
- **Internet Connection** for:
  - WAN IP detection.  
  - Downloading `ngrok` if not already installed.  

---

## **Installation** <a id="installation"></a>  
1. **Download** or **Clone** this repository to your local machine.  
2. **Make the script executable**:  
   ```bash
   chmod +x netvision.sh
   ```
3. (Optional) **Place** it in a directory within your `$PATH`, e.g.:  
   ```bash
   sudo mv netvision.sh /usr/local/bin/netvision
   sudo chmod +x /usr/local/bin/netvision
   ```

---

## **Usage** <a id="usage"></a>  
1. **Run** the script (ideally with `sudo` for best results):  
   ```bash
   sudo ./netvision.sh
   ```
   or, if moved into `$PATH`:
   ```bash
   sudo netvision
   ```
2. **Watch** the console output as NetVision:  
   - Installs missing dependencies (SNMP, nmap, netcat, miniupnpc, etc.)  
   - Displays local network info (IP, DNS, router details, etc.)  
   - Performs an **ARP table scan** and a **router DNS table scan**.  
   - Runs a **quick stealth port scan** on the router (top 10 ports), trying to detect the OS.  
   - **Starts** netcat on **port 6666** and spawns **ngrok** tunnels (TCP on 6667, HTTP on 80).  

---

## **How It Works (Detailed)** <a id="how-it-works-detailed"></a>

### **Firmware Detection** <a id="firmware-detection"></a>  
NetVision tries to detect the router’s firmware version in the following order:

1. **SNMP** (if enabled on the router):  
   - It runs `snmpwalk -v2c -c public <router_ip> 1.3.6.1.2.1.1.1.0` to see if a firmware string is exposed in the system description OID.  
2. **HTTP**:  
   - It makes a `curl` request to `http://<router_ip>` and searches for a text pattern like **“Firmware Version”**.  
3. **UPnP**:  
   - If available, it runs `upnpc -l` to see if the router exposes a firmware string in UPnP device descriptions.  
4. **Fallback**:  
   - If none of the above yield a match, NetVision prints `Unknown (Check router web interface manually)`.

> **Note**: Consumer routers are **inconsistent** in how (or if) they expose firmware details. This step often fails on locked-down or custom routers.  

---

### **ARP Table & DNS Table Gathering** <a id="arp-table--dns-table-gathering"></a>  
- **ARP Table**:  
  - Runs `arp -a` to list discovered devices, extracts IP and MAC, attempts to resolve hostnames via `nslookup`, and prints them in a neat table.  
  - Results are **optionally** saved to `discovered_ips.txt` / `.json`.  
- **Router DNS Table**:  
  - Uses SNMP, UPnP, and a **DNS brute force** approach (with `nslookup`) to look for local DNS records the router might know about.  
  - Very dependent on the router’s capabilities and can be **hit or miss**.

---

### **Stealth Port Scan & OS Detection** <a id="stealth-port-scan--os-detection"></a>  
- **Nmap**:  
  - NetVision uses `sudo nmap -sS -n --top-ports 10 -O --osscan-limit --osscan-guess` to scan the router IP (or any target).  
  - **SYN Stealth Scan (`-sS`)** sends SYN packets without completing TCP handshakes, which is often less conspicuous.  
  - **OS Detection (`-O`)** tries to guess the remote operating system.  
    - This step can be **inconclusive** if the router has few open ports or unusual TCP behavior.  
  - Writes raw scan output (including potential OS guess) to `quick_scan.txt`.  
  - Parses open ports to `open_ports.txt` and `open_ports.json`.

---

### **Ngrok & Netcat Setup** <a id="ngrok--netcat-setup"></a>  
1. **Netcat**:  
   - Listens in the background on **TCP port 6666**.  
   - You can manually connect to it (e.g., `nc <ip> 6666`) for testing.  
2. **Ngrok**:  
   - **Downloads** if not found, then runs two separate processes in the background:  
     - **`ngrok tcp 6667`**: Creates a publicly accessible TCP tunnel to your local machine’s **port 6667**.  
     - **`ngrok http 80`**: Creates a publicly accessible HTTP tunnel to your local machine’s **port 80**.  
   - If you have a web server on port 80, you may need to stop it, or change ports to avoid conflicts.  
   - For a stable, authenticated tunnel, add your **ngrok auth token** in the script’s commented section.  

---

### **Output Files & Logs** <a id="output-files--logs"></a>  

1. **`quick_scan.txt`**  
   - Contains the raw output of the Nmap top-ports scan with OS detection, plus any notes about ping success/failure.
2. **`open_ports.txt`** / **`open_ports.json`**  
   - Lists the open TCP ports discovered among the top 10.  
   - The JSON file uses the format:
     ```json
     [
       { "port": "22" },
       { "port": "80" }
     ]
     ```
3. **`discovered_ips.txt`** / **`discovered_ips.json`**  
   - From the ARP table parsing, each IP discovered is stored in both text and JSON.  
4. **`router_dns_table.txt`** / **`router_dns_table.json`**  
   - Attempts to summarize local DNS entries your router may know.  
5. **`router_dns_table.txt`**, **`router_dns_table.json`**  
   - Summarize any found local DNS mappings via SNMP, UPnP, or fallback DNS brute force.

---

## **License** <a id="license"></a>
This script is released under the [MIT License](https://opensource.org/licenses/MIT). You are free to use, modify, and distribute it. Please ensure you have **permission** and **authority** to run port scans or gather device info on your network.

**Disclaimer**: Use responsibly and within the bounds of local laws and organizational policies. The author(s) assume no liability for misuse.  

---

**Enjoy exploring and testing your network with NetVision!** For questions or suggestions, feel free to open an issue or send a pull request.  
