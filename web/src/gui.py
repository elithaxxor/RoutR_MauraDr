import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk
import threading
import asyncio
import uuid
from routR.tools.runner import run_jobs
from .logging import setup_logger
from .config import config
from . import net_services

logger = setup_logger(config["database"])


class ScanGUI(tk.Tk):
    """Simple Tkinter GUI for SMB-Scor3."""

    def __init__(self):
        super().__init__()
        self.title("SMB-Scor3 GUI")
        self.geometry("600x400")
        self.nc_proc = None
        self.ngrok_tcp_proc = None
        self.ngrok_http_proc = None
        self.last_hosts = []
        self.tool_vars = {}
        self.progress = {}
        self.create_widgets()

    def create_widgets(self):
        frame = tk.Frame(self)
        frame.pack(pady=10)

        tk.Label(frame, text="Network CIDR:").grid(row=0, column=0, sticky=tk.W)
        self.cidr_entry = tk.Entry(frame, width=20)
        self.cidr_entry.grid(row=0, column=1)
        self.cidr_entry.insert(0, "192.168.1.0/24")

        tk.Button(frame, text="Start Scan", command=self.start_scan).grid(
            row=0, column=2, padx=5
        )
        self.map_btn = tk.Button(
            frame, text="Show Map", command=self.show_map, state=tk.DISABLED
        )
        self.map_btn.grid(row=0, column=3, padx=5)

        self.netcat_btn = tk.Button(
            frame, text="Start Netcat", command=self.toggle_netcat
        )
        self.netcat_btn.grid(row=1, column=0, pady=5)
        self.ngrok_btn = tk.Button(frame, text="Start Ngrok", command=self.toggle_ngrok)
        self.ngrok_btn.grid(row=1, column=1, pady=5)

        row = 2
        for tool in [
            "masscan",
            "arp_scan",
            "hydra",
            "gvm_cli",
            "miniupnpc",
            "nikto",
            "sqlmap",
            "pgrok",
        ]:
            var = tk.BooleanVar(value=True)
            chk = tk.Checkbutton(frame, text=tool, variable=var)
            chk.grid(row=row, column=0, sticky=tk.W)
            bar = ttk.Progressbar(frame, length=120, mode="determinate")
            bar.grid(row=row, column=1, columnspan=3, sticky=tk.EW, pady=2)
            self.tool_vars[tool] = var
            self.progress[tool] = bar
            row += 1

        self.log_box = scrolledtext.ScrolledText(self, state="disabled", height=15)
        self.log_box.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def start_scan(self):
        cidr = self.cidr_entry.get().strip()
        threading.Thread(target=self.run_scan, args=(cidr,), daemon=True).start()

    def run_scan(self, cidr):
        self.append_log(f"Scanning {cidr}...\n")
        jobs = []
        for tool, var in self.tool_vars.items():
            if var.get():
                if tool == "masscan":
                    jobs.append({"tool": "masscan", "args": [cidr]})
                elif tool == "arp_scan":
                    jobs.append({"tool": "arp_scan"})
                elif tool == "hydra":
                    jobs.append(
                        {
                            "tool": "hydra",
                            "args": [cidr, "ssh", "users.txt", "pass.txt"],
                        }
                    )
                elif tool == "gvm_cli":
                    jobs.append({"tool": "gvm_cli", "args": ["<get_reports>"]})
                elif tool == "miniupnpc":
                    jobs.append({"tool": "miniupnpc"})
                elif tool == "nikto":
                    jobs.append(
                        {"tool": "nikto", "args": ["http://" + cidr.split("/")[0]]}
                    )
                elif tool == "sqlmap":
                    jobs.append(
                        {"tool": "sqlmap", "args": ["http://" + cidr.split("/")[0]]}
                    )
                elif tool == "pgrok":
                    jobs.append({"tool": "pgrok", "args": [80]})
        report = asyncio.run(run_jobs(jobs, str(uuid.uuid4())))
        for result in report["results"]:
            for tool, res in result.items():
                self.progress[tool].configure(value=100)
                self.append_log(f"{tool}: {res.get('error','done')}\n")
        self.append_log("Scan complete.\n")

    def append_log(self, text):
        self.log_box.configure(state="normal")
        self.log_box.insert(tk.END, text)
        self.log_box.configure(state="disabled")
        self.log_box.yview(tk.END)

    def toggle_netcat(self):
        if net_services.is_running(self.nc_proc):
            net_services.stop_process(self.nc_proc)
            self.nc_proc = None
            self.netcat_btn.configure(text="Start Netcat")
            self.append_log("Netcat stopped\n")
        else:
            self.nc_proc = net_services.start_netcat_listener()
            if self.nc_proc:
                self.netcat_btn.configure(text="Stop Netcat")
                self.append_log("Netcat started\n")

    def toggle_ngrok(self):
        if net_services.is_running(self.ngrok_tcp_proc):
            net_services.stop_process(self.ngrok_tcp_proc)
            net_services.stop_process(self.ngrok_http_proc)
            self.ngrok_tcp_proc = None
            self.ngrok_http_proc = None
            self.ngrok_btn.configure(text="Start Ngrok")
            self.append_log("Ngrok tunnels stopped\n")
        else:
            self.ngrok_tcp_proc = net_services.start_ngrok_tcp()
            self.ngrok_http_proc = net_services.start_ngrok_http()
            if self.ngrok_tcp_proc or self.ngrok_http_proc:
                self.ngrok_btn.configure(text="Stop Ngrok")
                self.append_log("Ngrok tunnels started\n")

    def show_map(self):
        if not self.last_hosts:
            messagebox.showinfo("Topology", "Run a scan first")
            return
        from . import network_map

        win = tk.Toplevel(self)
        win.title("Network Topology")
        network_map.show_topology(self.last_hosts, win)


def launch_gui():
    gui = ScanGUI()
    gui.mainloop()


if __name__ == "__main__":
    launch_gui()
