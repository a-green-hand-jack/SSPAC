import json
import matplotlib.pyplot as plt
import networkx as nx
import os
import math

def visualize_samples():
    data_path = 'data/leetcode/leetcode_second_shortest_path.json'
    if not os.path.exists(data_path):
        print(f"Error: {data_path} not found.")
        return

    with open(data_path, 'r') as f:
        data = json.load(f)
    
    # Select representative cases
    # 1. Official: ID 1 (Medium graph)
    # 2. Random: Pick one with moderate size (e.g., first one with 10 <= n <= 20)
    # 3. Special: ID 203 (Grid graph) or 201 (Star)
    
    selected_cases = []
    
    # Official
    selected_cases.append(next(c for c in data['test_cases'] if c['id'] == 1))
    
    # Random (try to find one around ID 105 or similar, or just the first random one)
    random_candidates = [c for c in data['test_cases'] if 100 <= c['id'] < 200]
    if random_candidates:
        # Pick one that isn't too huge for visualization
        medium_random = next((c for c in random_candidates if 10 <= c['n'] <= 20), random_candidates[0])
        selected_cases.append(medium_random)
        
    # Special (Grid 4x4 is nice to look at)
    special_candidates = [c for c in data['test_cases'] if c['id'] == 203] 
    if not special_candidates:
         special_candidates = [c for c in data['test_cases'] if c['id'] >= 200]
    if special_candidates:
        selected_cases.append(special_candidates[0])

    num_cases = len(selected_cases)
    fig, axes = plt.subplots(1, num_cases, figsize=(5 * num_cases, 5))
    if num_cases == 1:
        axes = [axes]
    
    print(f"Visualizing {num_cases} graphs...")

    for i, case in enumerate(selected_cases):
        ax = axes[i]
        n = case['n']
        edges = case['edges']
        source = case['source']
        target = case['target']
        title = f"{case['name']} (N={n}, M={len(edges)})"
        
        G = nx.Graph()
        G.add_nodes_from(range(1, n + 1))
        G.add_edges_from(edges)
        
        # Determine layout
        if "Grid" in case['name']:
            # Manual grid layout for 4x4
            pos = {}
            rows = int(math.sqrt(n))
            cols = n // rows
            for node in range(1, n + 1):
                r = (node - 1) // cols
                c = (node - 1) % cols
                pos[node] = (c, -r) # -r to draw top-down
        elif "Star" in case['name']:
            pos = nx.spring_layout(G, k=0.5, seed=42) # standard
        else:
            pos = nx.kamada_kawai_layout(G) # usually good for general graphs

        # Draw nodes
        node_colors = []
        for node in G.nodes():
            if node == source:
                node_colors.append('#32CD32') # Lime Green for Source
            elif node == target:
                node_colors.append('#FF4500') # Orange Red for Target
            else:
                node_colors.append('#ADD8E6') # Light Blue

        nx.draw_networkx_nodes(G, pos, ax=ax, node_color=node_colors, node_size=500, edgecolors='black')
        nx.draw_networkx_labels(G, pos, ax=ax, font_size=10, font_weight='bold')
        nx.draw_networkx_edges(G, pos, ax=ax, edge_color='gray', width=1.5, alpha=0.7)
        
        ax.set_title(title, fontsize=12)
        ax.axis('off')

    plt.tight_layout()
    
    output_dir = 'docs/data'
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'sample_graphs_visualization.png')
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"Visualization saved to: {output_path}")

if __name__ == "__main__":
    visualize_samples()
