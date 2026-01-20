
import json
import networkx as nx

def load_graph(path):
    try:
        with open(path, 'r') as f:
            data = json.load(f)
    except Exception as e:
        print(f"❌ Error loading graph: {e}")
        return None

    G = nx.DiGraph()
    G.add_nodes_from(data.get("nodes", []))
    for e in data.get("edges", []):
        if e.get("source") and e.get("target"):
            G.add_edge(e["source"], e["target"], weight=e["weight"])
    print(f"✅ Graph loaded: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")
    return G

def find_shortest_path(G, source, target):
    if source not in G or target not in G:
        return {"error": "Invalid source or destination"}, 0
    try:
        path = nx.dijkstra_path(G, source, target, weight="weight")
        cost = nx.dijkstra_path_length(G, source, target, weight="weight")
        return path, cost
    except nx.NetworkXNoPath:
        return {"error": f"No path from {source} to {target}"}, 0
