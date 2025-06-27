import json
from typing import List, Optional
import tkinter as tk
from tkinter import messagebox

try:
    import networkx as nx
except ImportError:  # pragma: no cover - library may be missing in tests
    class _SimpleGraph:
        def __init__(self):
            self._nodes = {}
            self._edges = set()

        def add_node(self, node, **attrs):
            self._nodes[node] = attrs

        def add_edge(self, a, b):
            self._edges.add((a, b))

        def nodes(self):  # mimic networkx API partially
            return self._nodes

        def has_edge(self, a, b):
            return (a, b) in self._edges or (b, a) in self._edges

        def has_node(self, n):
            return n in self._nodes

    class nx:  # type: ignore
        Graph = _SimpleGraph

        @staticmethod
        def spring_layout(graph):
            return {n: (i, 0) for i, n in enumerate(graph.nodes())}

        @staticmethod
        def draw_networkx(*args, **kwargs):
            pass

try:
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    import matplotlib.pyplot as plt
except Exception:  # pragma: no cover - matplotlib may be missing
    FigureCanvasTkAgg = None
    plt = None

from . import network_info
from .integrations import shodan_client
from .config import config


def build_topology(hosts: List[str], router_ip: Optional[str] = None, shodan_api_key: Optional[str] = None) -> nx.Graph:
    """Create a NetworkX graph of the router and discovered hosts.

    Parameters
    ----------
    hosts: list of IP addresses discovered on the network.
    router_ip: optional router IP to use. If not provided, will attempt to detect.
    shodan_api_key: if provided, query Shodan for each host and attach results.
    """
    G = nx.Graph()
    router_ip = router_ip or network_info.get_router_ip()
    if router_ip:
        G.add_node(router_ip, type="router")
    for ip in hosts:
        G.add_node(ip, type="device")
        if router_ip:
            G.add_edge(router_ip, ip)
    api_key = shodan_api_key or config.get("shodan_api_key")
    if api_key:
        for ip in hosts:
            data = shodan_client.shodan_host(ip, api_key)
            if data:
                G.nodes[ip]["shodan"] = data
    return G


def show_topology(hosts: List[str], parent: tk.Toplevel, router_ip: Optional[str] = None) -> None:
    """Display an interactive topology map in a Tk window."""
    G = build_topology(hosts, router_ip)
    fig, ax = plt.subplots(figsize=(6, 4))
    pos = nx.spring_layout(G)
    nx.draw_networkx(G, pos, ax=ax, node_color="skyblue", edge_color="gray")
    canvas = FigureCanvasTkAgg(fig, master=parent)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def on_click(event):
        if not event.inaxes:
            return
        x, y = event.xdata, event.ydata
        closest, dist = None, None
        for node, (nx_pos, ny_pos) in pos.items():
            d = (nx_pos - x) ** 2 + (ny_pos - y) ** 2
            if dist is None or d < dist:
                dist = d
                closest = node
        info = G.nodes[closest].get("shodan")
        if info:
            ports = info.get("ports") or []
            summary = json.dumps({"ip": closest, "ports": ports}, indent=2)
        else:
            summary = closest
        messagebox.showinfo("Host Info", summary)

    fig.canvas.mpl_connect("button_press_event", on_click)

