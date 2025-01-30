import sys

if len(sys.argv) < 2:
    print("Usage: python generated_code.py <file_path>")
    sys.exit(1)

file_path = sys.argv[1]

import networkx as nx

# Load the graph from the GML file
G = nx.read_gml(file_path, label='label')

# Calculate PageRank
page_rank = nx.pagerank(G)

# Store the result in a dictionary with node labels as keys
result = {node: rank for node, rank in page_rank.items()}

print(result)