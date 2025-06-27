import argparse
import json
from .scanning import discover_smb_hosts
from .enumeration import enumerate_lan_hosts
from .scoring import calculate_vulnerability_score, generate_remediation
from .integrations.shodan import ShodanClient
from .integrations.wigle import WigleClient
from .integrations.censys_client import CensysClient


def cmd_scan(args):
    hosts = discover_smb_hosts(args.cidr)
    host_data = enumerate_lan_hosts(hosts, args.intensity)
    for host, data in host_data.items():
        score, category = calculate_vulnerability_score(data)
        print(f"{host}: score {score} ({category})")
        remediation = generate_remediation(data)
        for step in remediation:
            print(f"  - {step}")


def cmd_shodan_search(args):
    client = ShodanClient()
    results = client.search(args.query)
    print(json.dumps(results, indent=2))


def cmd_shodan_host(args):
    client = ShodanClient()
    info = client.host(args.ip)
    print(json.dumps(info, indent=2))


def cmd_wigle_ssid(args):
    client = WigleClient()
    results = client.search_ssid(args.ssid)
    print(json.dumps(results, indent=2))


def cmd_wigle_bssid(args):
    client = WigleClient()
    results = client.search_bssid(args.bssid)
    print(json.dumps(results, indent=2))


def cmd_censys_search(args):
    client = CensysClient()
    results = client.search_hosts(args.query)
    print(json.dumps(results, indent=2))


def main():
    parser = argparse.ArgumentParser(description="SMB-Scor3 Command Line")
    sub = parser.add_subparsers(dest="cmd")

    scan_p = sub.add_parser("scan", help="Scan network for SMB hosts")
    scan_p.add_argument("cidr", help="Network CIDR, e.g. 192.168.1.0/24")
    scan_p.add_argument("--intensity", default="low", choices=["low", "medium", "high"])
    scan_p.set_defaults(func=cmd_scan)

    shodan_s = sub.add_parser("shodan-search", help="Search Shodan")
    shodan_s.add_argument("query", help="Search query")
    shodan_s.set_defaults(func=cmd_shodan_search)

    shodan_h = sub.add_parser("shodan-host", help="Lookup host on Shodan")
    shodan_h.add_argument("ip", help="Target IP")
    shodan_h.set_defaults(func=cmd_shodan_host)

    wigle_ssid = sub.add_parser("wigle-ssid", help="Search Wigle by SSID")
    wigle_ssid.add_argument("ssid", help="SSID to search")
    wigle_ssid.set_defaults(func=cmd_wigle_ssid)

    wigle_bssid = sub.add_parser("wigle-bssid", help="Search Wigle by BSSID")
    wigle_bssid.add_argument("bssid", help="BSSID/MAC")
    wigle_bssid.set_defaults(func=cmd_wigle_bssid)

    censys_s = sub.add_parser("censys-search", help="Search Censys hosts")
    censys_s.add_argument("query", help="Search query")
    censys_s.set_defaults(func=cmd_censys_search)

    args = parser.parse_args()
    if not args.cmd:
        parser.print_help()
        return
    args.func(args)


if __name__ == "__main__":
    main()
