import json
import matplotlib.pyplot as plt
import os
import numpy as np

def analyze_distribution():
    data_path = 'data/leetcode/leetcode_second_shortest_path.json'
    if not os.path.exists(data_path):
        print(f"Error: {data_path} not found.")
        return

    with open(data_path, 'r') as f:
        data = json.load(f)

    test_cases = data['test_cases']
    
    categories = {
        'Official': [],
        'Random': [],
        'Special': []
    }

    for tc in test_cases:
        cid = tc['id']
        n = tc['n']
        m = len(tc['edges'])
        
        if cid < 100:
            categories['Official'].append((n, m))
        elif 100 <= cid < 200:
            categories['Random'].append((n, m))
        else:
            categories['Special'].append((n, m))

    print(f"{ 'Category':<15} | { 'Count':<5} | { 'Node Range':<15} | { 'Edge Range':<15}")
    print("-" * 60)
    
    for cat, points in categories.items():
        if not points:
            continue
        count = len(points)
        ns = [p[0] for p in points]
        ms = [p[1] for p in points]
        n_range = f"{min(ns)}-{max(ns)}"
        m_range = f"{min(ms)}-{max(ms)}"
        print(f"{cat:<15} | {count:<5} | {n_range:<15} | {m_range:<15}")

    # Plotting
    plt.figure(figsize=(10, 6))
    
    colors = {'Official': 'blue', 'Random': 'green', 'Special': 'red'}
    markers = {'Official': 'o', 'Random': 'x', 'Special': 's'}
    
    for cat, points in categories.items():
        if not points:
            continue
        ns = [p[0] for p in points]
        ms = [p[1] for p in points]
        plt.scatter(ns, ms, label=cat, c=colors[cat], marker=markers[cat], alpha=0.7, s=100)

    plt.title('Dataset Distribution: Nodes vs Edges')
    plt.xlabel('Number of Nodes (N)')
    plt.ylabel('Number of Edges (M)')
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.legend()
    
    output_dir = 'docs/data'
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'dataset_distribution.png')
    plt.savefig(output_path)
    print(f"\nDistribution plot saved to: {output_path}")

if __name__ == "__main__":
    analyze_distribution()
