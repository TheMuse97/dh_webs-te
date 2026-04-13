import os
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Create images folder if it does not exist
os.makedirs("images", exist_ok=True)

# Read CSV files with semicolon separator
actors = pd.read_csv("data/lic_actors.csv", sep=";")
places = pd.read_csv("data/lic_places.csv", sep=";")
links = pd.read_csv("data/lic_actor_place_links.csv", sep=";")

# Clean whitespace from names
actors["name"] = actors["name"].astype(str).str.strip()
places["name"] = places["name"].astype(str).str.strip()
links["actor_name"] = links["actor_name"].astype(str).str.strip()
links["place_name"] = links["place_name"].astype(str).str.strip()

# Create graph
G = nx.Graph()

# Add actor nodes
for _, row in actors.iterrows():
    actor_name = row["name"]
    actor_type = row["actor_type"] if pd.notna(row["actor_type"]) else "actor"
    G.add_node(actor_name, node_type="actor", label=actor_name, category=actor_type)

# Add place nodes
for _, row in places.iterrows():
    place_name = row["name"]
    region = row["region"] if pd.notna(row["region"]) else ""
    G.add_node(place_name, node_type="place", label=place_name, category=region)

# Add edges from actor-place links
for _, row in links.iterrows():
    actor_name = row["actor_name"]
    place_name = row["place_name"]
    activity_type = row["activity_type"] if pd.notna(row["activity_type"]) else ""

    if actor_name in G.nodes and place_name in G.nodes:
        G.add_edge(actor_name, place_name, activity=activity_type)

# Separate nodes by type for layout
actor_nodes = [n for n, d in G.nodes(data=True) if d["node_type"] == "actor"]
place_nodes = [n for n, d in G.nodes(data=True) if d["node_type"] == "place"]

# Manual bipartite layout
pos = {}

for i, node in enumerate(actor_nodes):
    pos[node] = (0, -i)

for i, node in enumerate(place_nodes):
    pos[node] = (1.8, -i)

# Labels
labels = {n: d["label"] for n, d in G.nodes(data=True)}

# Draw
plt.figure(figsize=(16, 10))

nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.6)
nx.draw_networkx_nodes(G, pos, nodelist=actor_nodes, node_size=1800)
nx.draw_networkx_nodes(G, pos, nodelist=place_nodes, node_size=1800)
nx.draw_networkx_labels(G, pos, labels=labels, font_size=9)

plt.title("Licorice Trade Network: Actors and Places", fontsize=14)
plt.axis("off")
plt.tight_layout()

# Save image
plt.savefig("images/network.png", dpi=300, bbox_inches="tight")
plt.close()

print("Network image saved to images/network.png")