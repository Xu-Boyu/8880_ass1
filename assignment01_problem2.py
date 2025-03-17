import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import os
os.environ["LANG"] = "en_US.UTF-8"
os.environ["LC_ALL"] = "en_US.UTF-8"
os.environ["NO_AT_BRIDGE"] = "1"


# read data
cities_file = 'global-cities.dat'
edges_file = 'global-net.dat'

G = nx.Graph()

# add all the cities
city_map = {}
with open("global-cities.dat", "r", encoding="utf-8") as f:
    for line in f:
        parts = line.strip().split("|")
        if len(parts) == 3 and parts[1].isdigit():
            city_id = int(parts[1])
            city_name = parts[2]
            city_map[city_id] = city_name
            G.add_node(city_id)

with open("global-net.dat", "r", encoding="utf-8") as f:
    for line in f:
        parts = line.strip().split()
        if len(parts) == 2:
            u, v = int(parts[0]), int(parts[1])
            G.add_edge(u, v)

num_nodes = G.number_of_nodes()
num_edges = G.number_of_edges()
print(f"Graph has {num_nodes} nodes and {num_edges} edges.")

components = list(nx.connected_components(G))
num_components = len(components)
largest_component = max(components, key=len)
G_largest = G.subgraph(largest_component).copy()

print(f"Graph has {num_components} connected components.")
print(f"Largest component has {G_largest.number_of_nodes()} nodes and {G_largest.number_of_edges()} edges.")


# 2. Compute the connectivity component
components = list(nx.connected_components(G))
num_components = len(components)
largest_component = max(components, key=len)
G_largest = G.subgraph(largest_component).copy()
print(f"Graph has {num_components} connected components.")
print(f"Largest component has {G_largest.number_of_nodes()} nodes and {G_largest.number_of_edges()} edges.")

# 3. Find the 10 nodes with the highest degree
degree_sorted = sorted(G_largest.degree, key=lambda x: x[1], reverse=True)[:10]
top_degree_cities = [(city_map[node], degree) for node, degree in degree_sorted]
print("Top 10 airports with highest degree:")
for city, degree in top_degree_cities:
    print(f"{city}: {degree}")

# 4. 绘制度分布
degree_sequence = [deg for _, deg in G_largest.degree()]
degree_count = pd.Series(degree_sequence).value_counts(normalize=True).sort_index()
plt.figure()
plt.plot(degree_count.index, degree_count.values, 'bo-', markersize=5)
plt.xlabel("Degree")
plt.ylabel("Fraction of Nodes")
plt.title("Degree Distribution")
plt.xscale("log")
plt.yscale("log")
plt.grid(True)
plt.show()

# 计算图的直径并找到最长路径
try:
    diameter = nx.diameter(G_largest)  # 计算直径
    peripheral_nodes = nx.periphery(G_largest)  # 找到远端点

    if len(peripheral_nodes) >= 2:
        longest_path = nx.shortest_path(G_largest, source=peripheral_nodes[0], target=peripheral_nodes[-1])
        longest_path_str = " -> ".join(city_map.get(node, f'Unknown({node})') for node in longest_path)
        print(f"Longest shortest path: {longest_path_str}")
    else:
        print("Error: Could not find a valid longest shortest path.")

except Exception as e:
    print("Error computing longest path:", e)


# 6. Calculate the shortest path
CBR, CPT = None, None
for node, name in city_map.items():
    if name == "Canberra":  # 确保匹配的是城市名称，而不是机场代码
        CBR = node
    if name == "Cape Town":
        CPT = node

if CBR and CPT:
    if CBR in G_largest and CPT in G_largest:  # 确保它们在最大连通分量中
        shortest_path = nx.shortest_path(G_largest, source=CBR, target=CPT)
        path_cities = [city_map[node] for node in shortest_path]
        print("Shortest path from Canberra to Cape Town:", " -> ".join(path_cities))
    else:
        print("Canberra or Cape Town is not in the largest component.")
else:
    print("Canberra or Cape Town not found in dataset.")

# 7. Calculate mediational centrality and find the top 10
betweenness = nx.betweenness_centrality(G_largest)
top_betweenness = sorted(betweenness.items(), key=lambda x: x[1], reverse=True)[:10]
top_betweenness_cities = [(city_map[node], centrality) for node, centrality in top_betweenness]
print("Top 10 airports by betweenness centrality:")
for city, centrality in top_betweenness_cities:
    print(f"{city}: {centrality}")

