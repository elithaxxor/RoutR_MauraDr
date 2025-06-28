import json
from typing import List, Optional
from pathlib import Path
import tkinter as tk
from tkinter import messagebox

try:
    import networkx as nx
    from networkx.readwrite import json_graph
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

        def edges(self):
            return list(self._edges)

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

    def _node_link_data(g: _SimpleGraph):
        return {
            'nodes': [{'id': n, **attrs} for n, attrs in g.nodes().items()],
            'links': [{'source': a, 'target': b} for a, b in g.edges()]}

    def _node_link_graph(data):
        g = _SimpleGraph()
        for node in data.get('nodes', []):
            nid = node.pop('id')
            g.add_node(nid, **node)
        for link in data.get('links', []):
            g.add_edge(link['source'], link['target'])
        return g

    json_graph = type('json_graph', (), {
        'node_link_data': staticmethod(_node_link_data),
        'node_link_graph': staticmethod(_node_link_graph),
    })

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


def save_topology(graph: nx.Graph, path: str) -> None:
    """Save a graph to a JSON file for historical view mode."""
    data = json_graph.node_link_data(graph)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)


def load_topology(path: str) -> nx.Graph:
    """Load a graph from a JSON file."""
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return json_graph.node_link_graph(data)


def load_history(directory: str) -> List[nx.Graph]:
    """Load all topology JSON files from a directory."""
    graphs = []
    for p in sorted(Path(directory).glob('topology_*.json')):
        try:
            graphs.append(load_topology(str(p)))
        except Exception:
            continue
    return graphs


def export_png(graph: nx.Graph, path: str) -> None:
    """Export a topology graph as PNG."""
    if not plt:
        raise RuntimeError('matplotlib not available')
    pos = nx.spring_layout(graph)
    nx.draw_networkx(graph, pos)
    plt.savefig(path)
    plt.close()


def export_html(graph: nx.Graph, path: str) -> None:
    """Export topology as a minimal interactive HTML."""
    data = json.dumps(json_graph.node_link_data(graph))
    html = (
        "<html><body><div id='graph'></div>"
        "<script src='https://cdn.jsdelivr.net/npm/vis-network/standalone/umd/vis-network.min.js'></script>"
        "<script>var data = new vis.DataSet(JSON.parse('" + data.replace("'", "\'") + "').nodes);"
        "var edges = new vis.DataSet(JSON.parse('" + data.replace("'", "\'") + "').links);"
        "var container=document.getElementById('graph');"
        "new vis.Network(container,{nodes:data,edges:edges},{})</script></body></html>"
    )
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)


def export_d3_html(graph: nx.Graph, path: str) -> None:
    """Export topology as a D3.js force graph."""
    data_json = json.dumps(json_graph.node_link_data(graph)).replace("'", "\'")
    html = """
    <html>
    <body>
    <svg width='800' height='600'></svg>
    <script src='https://d3js.org/d3.v7.min.js'></script>
    <script>
    var graph = JSON.parse('GRAPH_DATA');
    var svg = d3.select('svg'),
        width = +svg.attr('width'),
        height = +svg.attr('height');

    var simulation = d3.forceSimulation(graph.nodes)
        .force('link', d3.forceLink(graph.links).id(d => d.id).distance(80))
        .force('charge', d3.forceManyBody().strength(-100))
        .force('center', d3.forceCenter(width / 2, height / 2));

    var link = svg.append('g').selectAll('line')
        .data(graph.links)
        .enter().append('line')
        .attr('stroke', '#999');

    var node = svg.append('g').selectAll('circle')
        .data(graph.nodes)
        .enter().append('circle')
        .attr('r', 5)
        .attr('fill', '#69b3a2')
        .call(d3.drag()
            .on('start', dragstarted)
            .on('drag', dragged)
            .on('end', dragended));

    node.append('title').text(d => d.id);

    simulation.on('tick', () => {
        link.attr('x1', d => d.source.x)
            .attr('y1', d => d.source.y)
            .attr('x2', d => d.target.x)
            .attr('y2', d => d.target.y);

        node.attr('cx', d => d.x)
            .attr('cy', d => d.y);
    });

    function dragstarted(event) {
        if (!event.active) simulation.alphaTarget(0.3).restart();
        event.subject.fx = event.subject.x;
        event.subject.fy = event.subject.y;
    }

    function dragged(event) {
        event.subject.fx = event.x;
        event.subject.fy = event.y;
    }

    function dragended(event) {
        if (!event.active) simulation.alphaTarget(0);
        event.subject.fx = null;
        event.subject.fy = null;
    }
    </script>
    </body>
    </html>
    """
    html = html.replace('GRAPH_DATA', data_json)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)

