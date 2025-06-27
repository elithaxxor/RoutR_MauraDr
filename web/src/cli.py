import argparse
import json
from .scanning import discover_smb_hosts
from .enumeration import enumerate_lan_hosts
from .scoring import calculate_vulnerability_score, generate_remediation
from .integrations.shodan import ShodanClient
from .integrations.wigle import WigleClient
from .integrations.censys_client import CensysClient
from .plugin_manager import list_plugins as pm_list, enable_plugin, disable_plugin, install_plugin
from .query_library import list_queries, save_query, get_query
from pathlib import Path
from .batch_api import run_batch, save_report
from .ipv6_support import discover_ipv6_hosts
from .result_dashboard import ResultDashboard
from .mobile_companion import send_summary as send_mobile_summary
from .correlation import correlate_hosts
from .export_scheduler import ExportScheduler
from .update_db import update_database
from .plugin_harness import run_tests as run_plugin_tests
from .scan_profiles import (
    add_profile,
    remove_profile,
    list_profiles,
    run_scheduled,
)


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


def cmd_plugin_list(args):
    for name, enabled in pm_list():
        status = 'enabled' if enabled else 'disabled'
        print(f"{name}: {status}")


def cmd_plugin_enable(args):
    if enable_plugin(args.name):
        print(f"Enabled {args.name}")
    else:
        print(f"Plugin {args.name} not found")


def cmd_plugin_disable(args):
    if disable_plugin(args.name):
        print(f"Disabled {args.name}")
    else:
        print(f"Plugin {args.name} was not enabled")


def cmd_plugin_install(args):
    if install_plugin(args.url):
        print("Plugin installed")
    else:
        print("Failed to install plugin")


def cmd_query_list(args):
    queries = list_queries(args.service)
    for name, q in queries.items():
        print(f"{name}: {q}")


def cmd_query_save(args):
    save_query(args.service, args.name, args.query)
    print("Query saved")


def cmd_query_run(args):
    query = get_query(args.service, args.name)
    if not query:
        print("Query not found")
        return
    if args.service == 'shodan':
        cmd_shodan_search(argparse.Namespace(query=query))
    elif args.service == 'censys':
        cmd_censys_search(argparse.Namespace(query=query))
    else:
        cmd_wigle_ssid(argparse.Namespace(ssid=query))


def cmd_batch(args):
    data = run_batch(args.file)
    if args.output:
        save_report(data, args.output)
    print(json.dumps(data, indent=2))


def cmd_ipv6_scan(args):
    hosts = discover_ipv6_hosts(args.cidr)
    for h in hosts:
        print(h)


def cmd_dashboard_ports(args):
    dash = ResultDashboard(Path(args.dir))
    summary = dash.summarize_ports()
    print(json.dumps(summary, indent=2))


def cmd_mobile_send(args):
    msg = args.message
    if args.file:
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
                msg = f.read()
        except Exception:
            pass
    if not send_mobile_summary(args.title, msg):
        print('Failed to send notification')


def cmd_correlate(args):
    with open(args.file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    result = correlate_hosts(data)
    print(json.dumps(result, indent=2))


def cmd_export_schedule(args):
    def load():
        try:
            with open(args.results, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return {}

    sched = ExportScheduler()
    sched.schedule(load, interval=args.interval, csv=args.csv)
    try:
        sched.run()
    except KeyboardInterrupt:
        pass


def cmd_update_db(args):
    if update_database(args.url):
        print("Database updated")
    else:
        print("Update failed")


def cmd_plugin_test(args):
    results = run_plugin_tests([Path(p) for p in args.paths])
    for path, ok in results.items():
        print(f"{path}: {'ok' if ok else 'fail'}")


def cmd_schedule_list(args):
    for prof in list_profiles():
        print(f"{prof['name']} {prof['cidr']} {prof.get('intensity','low')} {prof.get('interval',3600)}")


def cmd_schedule_add(args):
    add_profile(args.name, args.cidr, args.intensity, args.interval)
    print("Profile saved")


def cmd_schedule_remove(args):
    remove_profile(args.name)
    print("Profile removed")


def cmd_schedule_run(args):
    def run_scan(cidr, intensity):
        print(f"Would scan {cidr} ({intensity})")

    run_scheduled(run_scan)


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

    plugin = sub.add_parser("plugin", help="Manage plugins")
    psub = plugin.add_subparsers(dest="p_cmd")
    p_list = psub.add_parser("list", help="List plugins")
    p_list.set_defaults(func=cmd_plugin_list)
    p_en = psub.add_parser("enable", help="Enable plugin")
    p_en.add_argument("name")
    p_en.set_defaults(func=cmd_plugin_enable)
    p_dis = psub.add_parser("disable", help="Disable plugin")
    p_dis.add_argument("name")
    p_dis.set_defaults(func=cmd_plugin_disable)
    p_ins = psub.add_parser("install", help="Install plugin from URL")
    p_ins.add_argument("url")
    p_ins.set_defaults(func=cmd_plugin_install)

    q = sub.add_parser("query", help="Manage saved queries")
    qsub = q.add_subparsers(dest="q_cmd")
    q_list = qsub.add_parser("list", help="List queries")
    q_list.add_argument("service", choices=["shodan", "censys", "wigle"])
    q_list.set_defaults(func=cmd_query_list)
    q_save = qsub.add_parser("save", help="Save a query")
    q_save.add_argument("service", choices=["shodan", "censys", "wigle"])
    q_save.add_argument("name")
    q_save.add_argument("query")
    q_save.set_defaults(func=cmd_query_save)
    q_run = qsub.add_parser("run", help="Run a saved query")
    q_run.add_argument("service", choices=["shodan", "censys", "wigle"])
    q_run.add_argument("name")
    q_run.set_defaults(func=cmd_query_run)

    ipv6_p = sub.add_parser("ipv6-scan", help="Discover IPv6 hosts")
    ipv6_p.add_argument("cidr", help="IPv6 network range")
    ipv6_p.set_defaults(func=cmd_ipv6_scan)

    dash = sub.add_parser("dashboard", help="Summarize past results")
    dash.add_argument("dir", help="Directory of result JSONs")
    dash.set_defaults(func=cmd_dashboard_ports)

    mobile = sub.add_parser("mobile-send", help="Send a message to mobile device")
    mobile.add_argument("title")
    mobile.add_argument("message")
    mobile.add_argument("--file")
    mobile.set_defaults(func=cmd_mobile_send)

    corr = sub.add_parser("correlate", help="Correlate results with Shodan/Censys")
    corr.add_argument("file", help="Results JSON")
    corr.set_defaults(func=cmd_correlate)

    esched = sub.add_parser("export-schedule", help="Schedule periodic exports")
    esched.add_argument("results", help="Results JSON to export")
    esched.add_argument("--interval", type=int, default=3600)
    esched.add_argument("--csv", action="store_true")
    esched.set_defaults(func=cmd_export_schedule)

    batch = sub.add_parser("batch", help="Run batch API lookups")
    batch.add_argument("file", help="File with IPs or queries")
    batch.add_argument("--output", help="Write results to file")
    batch.set_defaults(func=cmd_batch)

    upd = sub.add_parser("update-db", help="Update vulnerability database")
    upd.add_argument("--url", default=None, help="Source URL")
    upd.set_defaults(func=cmd_update_db)

    ptest = psub.add_parser("test", help="Validate plugin files")
    ptest.add_argument("paths", nargs="+", help="Plugin paths")
    ptest.set_defaults(func=cmd_plugin_test)

    sched = sub.add_parser("schedule", help="Manage scan profiles")
    ssub = sched.add_subparsers(dest="s_cmd")
    s_list = ssub.add_parser("list", help="List profiles")
    s_list.set_defaults(func=cmd_schedule_list)
    s_add = ssub.add_parser("add", help="Add profile")
    s_add.add_argument("name")
    s_add.add_argument("cidr")
    s_add.add_argument("--intensity", default="low")
    s_add.add_argument("--interval", type=int, default=3600)
    s_add.set_defaults(func=cmd_schedule_add)
    s_del = ssub.add_parser("remove", help="Remove profile")
    s_del.add_argument("name")
    s_del.set_defaults(func=cmd_schedule_remove)
    s_run = ssub.add_parser("run", help="Run scheduled scans")
    s_run.set_defaults(func=cmd_schedule_run)

    args = parser.parse_args()
    if not args.cmd:
        parser.print_help()
        return
    args.func(args)


if __name__ == "__main__":
    main()
