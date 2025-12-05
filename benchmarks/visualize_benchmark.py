"""
Benchmark 可视化脚本

生成三张图：
1. 最短路径：Dijkstra vs Queue-Optimized Bellman-Ford
2. 次短路径：Two-Distance Dijkstra vs State-Extended Bellman-Ford
3. 综合对比
"""

import matplotlib.pyplot as plt
import numpy as np

# 设置样式
plt.rcParams['font.family'] = ['DejaVu Sans', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False
plt.style.use('seaborn-v0_8-whitegrid')

# 数据：网格大小
grid_sizes = [100, 150, 200, 250, 300, 350, 400]
nodes = [s * s for s in grid_sizes]

# 最短路径数据 (ms) - 完整数据
shortest_dijkstra = [1.13, 2.91, 5.33, 8.60, 12.12, 17.30, 24.78]
shortest_bellman_ford = [1.29, 3.04, 7.67, 15.89, 24.76, 45.40, 69.62]

# 次短路径数据 (ms) - 完整数据
second_dijkstra = [2.49, 5.96, 10.93, 17.90, 25.85, 38.75, 50.03]
second_bellman_ford = [1.61, 4.31, 8.83, 21.61, 36.08, 57.39, 86.68]

# 算法名称
BELLMAN_FORD_SHORT = "Queue-Optimized\nBellman-Ford"
BELLMAN_FORD_LABEL = "Queue-Optimized Bellman-Ford"
BELLMAN_FORD_SECOND = "State-Extended\nBellman-Ford"
BELLMAN_FORD_SECOND_LABEL = "State-Extended Bellman-Ford"


def plot_shortest_path():
    """绘制最短路径对比图"""
    fig, ax = plt.subplots(figsize=(12, 7))

    x = np.arange(len(grid_sizes))
    width = 0.35

    bars1 = ax.bar(x - width/2, shortest_dijkstra, width,
                   label='Dijkstra', color='#2ecc71', edgecolor='black')
    bars2 = ax.bar(x + width/2, shortest_bellman_ford, width,
                   label=BELLMAN_FORD_LABEL, color='#e74c3c', edgecolor='black')

    ax.set_xlabel('Grid Size', fontsize=12)
    ax.set_ylabel('Time (ms)', fontsize=12)
    ax.set_title('Shortest Path: Dijkstra vs Queue-Optimized Bellman-Ford on Grid Graphs',
                 fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels([f'{s}×{s}\n({n:,})' for s, n in zip(grid_sizes, nodes)])
    ax.legend(loc='upper left', fontsize=10)

    # 添加数值标签
    for bar in bars1:
        height = bar.get_height()
        ax.annotate(f'{height:.1f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3), textcoords="offset points",
                    ha='center', va='bottom', fontsize=8)
    for bar in bars2:
        height = bar.get_height()
        ax.annotate(f'{height:.1f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3), textcoords="offset points",
                    ha='center', va='bottom', fontsize=8)

    # Dijkstra 始终更快的区域着色
    ax.fill_between([-0.5, 6.5], 0, max(shortest_bellman_ford) * 1.15,
                    alpha=0.08, color='#2ecc71')
    ax.text(3, max(shortest_bellman_ford) * 0.95, 'Dijkstra consistently faster',
            ha='center', fontsize=11, color='#27ae60', fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

    ax.set_xlim(-0.5, 6.5)
    ax.set_ylim(0, max(shortest_bellman_ford) * 1.15)

    plt.tight_layout()
    plt.savefig('shortest_path_benchmark.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Saved: shortest_path_benchmark.png")


def plot_second_shortest_path():
    """绘制次短路径对比图"""
    fig, ax = plt.subplots(figsize=(12, 7))

    x = np.arange(len(grid_sizes))
    width = 0.35

    bars1 = ax.bar(x - width/2, second_dijkstra, width,
                   label='Two-Distance Dijkstra', color='#3498db', edgecolor='black')
    bars2 = ax.bar(x + width/2, second_bellman_ford, width,
                   label=BELLMAN_FORD_SECOND_LABEL, color='#e67e22', edgecolor='black')

    ax.set_xlabel('Grid Size', fontsize=12)
    ax.set_ylabel('Time (ms)', fontsize=12)
    ax.set_title('Second Shortest Path: Two-Distance Dijkstra vs State-Extended Bellman-Ford',
                 fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels([f'{s}×{s}\n({n:,})' for s, n in zip(grid_sizes, nodes)])
    ax.legend(loc='upper left', fontsize=10)

    # 添加数值标签
    for bar in bars1:
        height = bar.get_height()
        ax.annotate(f'{height:.1f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3), textcoords="offset points",
                    ha='center', va='bottom', fontsize=8)
    for bar in bars2:
        height = bar.get_height()
        ax.annotate(f'{height:.1f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3), textcoords="offset points",
                    ha='center', va='bottom', fontsize=8)

    # 标注转折点 (在 200x200 和 250x250 之间)
    crossover_x = 2.5
    ax.axvline(x=crossover_x, color='red', linestyle='--', alpha=0.7, linewidth=2)
    ax.annotate('Crossover Point\n(~62,500 nodes)',
                xy=(crossover_x, max(second_bellman_ford) * 0.7),
                ha='center', fontsize=10, color='red', fontweight='bold',
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.9))

    # 添加区域着色
    ax.fill_between([-0.5, crossover_x], 0, max(second_bellman_ford) * 1.15,
                    alpha=0.08, color='#e67e22')
    ax.fill_between([crossover_x, 6.5], 0, max(second_bellman_ford) * 1.15,
                    alpha=0.08, color='#3498db')

    # 区域标签
    ax.text(1, max(second_bellman_ford) * 0.45, 'Bellman-Ford\nfaster',
            ha='center', fontsize=10, color='#d35400', fontweight='bold')
    ax.text(4.5, max(second_bellman_ford) * 0.45, 'Dijkstra\nfaster',
            ha='center', fontsize=10, color='#2980b9', fontweight='bold')

    ax.set_xlim(-0.5, 6.5)
    ax.set_ylim(0, max(second_bellman_ford) * 1.15)

    plt.tight_layout()
    plt.savefig('second_shortest_path_benchmark.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Saved: second_shortest_path_benchmark.png")


def plot_combined():
    """绘制综合对比图 - 折线图"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    # 左图：最短路径
    ax1.plot(nodes, shortest_dijkstra, 'o-',
             color='#2ecc71', linewidth=2.5, markersize=8, label='Dijkstra')
    ax1.plot(nodes, shortest_bellman_ford, 's-',
             color='#e74c3c', linewidth=2.5, markersize=8, label=BELLMAN_FORD_LABEL)

    ax1.set_xlabel('Number of Nodes', fontsize=11)
    ax1.set_ylabel('Time (ms)', fontsize=11)
    ax1.set_title('Shortest Path\n(Grid Graph)', fontsize=13, fontweight='bold')
    ax1.legend(loc='upper left', fontsize=9)
    ax1.set_xlim(0, max(nodes) * 1.05)
    ax1.set_ylim(0, max(shortest_bellman_ford) * 1.1)

    # 左图着色
    ax1.fill_between(nodes, 0, [max(shortest_bellman_ford) * 1.1] * len(nodes),
                     alpha=0.08, color='#2ecc71')
    ax1.text(max(nodes) * 0.5, max(shortest_bellman_ford) * 0.85,
             'Dijkstra always faster\non grid graphs',
             ha='center', fontsize=10, color='#27ae60', fontweight='bold',
             bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

    # 右图：次短路径
    ax2.plot(nodes, second_dijkstra, 'o-',
             color='#3498db', linewidth=2.5, markersize=8, label='Two-Distance Dijkstra')
    ax2.plot(nodes, second_bellman_ford, 's-',
             color='#e67e22', linewidth=2.5, markersize=8, label=BELLMAN_FORD_SECOND_LABEL)

    # 标注转折点
    crossover_nodes = 62500
    ax2.axvline(x=crossover_nodes, color='red', linestyle='--', alpha=0.7, linewidth=2)
    ax2.annotate('Crossover',
                 xy=(crossover_nodes, 25),
                 xytext=(crossover_nodes + 25000, 35),
                 fontsize=10, color='red', fontweight='bold',
                 arrowprops=dict(arrowstyle='->', color='red', alpha=0.7))

    ax2.set_xlabel('Number of Nodes', fontsize=11)
    ax2.set_ylabel('Time (ms)', fontsize=11)
    ax2.set_title('Second Shortest Path\n(Grid Graph)', fontsize=13, fontweight='bold')
    ax2.legend(loc='upper left', fontsize=9)

    # 右图区域着色
    ax2.fill_between([0, crossover_nodes], 0, max(second_bellman_ford) * 1.1,
                     alpha=0.08, color='#e67e22')
    ax2.fill_between([crossover_nodes, max(nodes) * 1.05], 0, max(second_bellman_ford) * 1.1,
                     alpha=0.08, color='#3498db')

    ax2.set_xlim(0, max(nodes) * 1.05)
    ax2.set_ylim(0, max(second_bellman_ford) * 1.1)

    plt.suptitle('Algorithm Performance Comparison on Grid Graphs',
                 fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig('combined_benchmark.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Saved: combined_benchmark.png")


def plot_speedup_line():
    """绘制加速比折线图 - 更清晰地展示趋势"""
    fig, ax = plt.subplots(figsize=(12, 6))

    # 计算加速比：Bellman-Ford 时间 / Dijkstra 时间
    # > 1 表示 Dijkstra 更快，< 1 表示 Bellman-Ford 更快
    shortest_ratio = [s / d for d, s in zip(shortest_dijkstra, shortest_bellman_ford)]
    second_ratio = [s / d for d, s in zip(second_dijkstra, second_bellman_ford)]

    ax.plot(nodes, shortest_ratio, 'o-',
            color='#27ae60', linewidth=2.5, markersize=10,
            label='Shortest Path (Bellman-Ford / Dijkstra)')
    ax.plot(nodes, second_ratio, 's-',
            color='#e67e22', linewidth=2.5, markersize=10,
            label='Second Shortest Path (Bellman-Ford / Dijkstra)')

    # 基准线
    ax.axhline(y=1, color='black', linestyle='-', linewidth=1.5, alpha=0.7)
    ax.text(max(nodes) * 0.95, 1.08, 'Equal Performance', ha='right', fontsize=9,
            fontstyle='italic')

    # 区域着色
    ax.fill_between([0, max(nodes) * 1.05], 1, max(max(shortest_ratio), max(second_ratio)) * 1.1,
                    alpha=0.1, color='#3498db', label='_Dijkstra faster region')
    ax.fill_between([0, max(nodes) * 1.05], 0, 1,
                    alpha=0.1, color='#e74c3c', label='_Bellman-Ford faster region')

    ax.text(max(nodes) * 0.7, 0.75, 'Bellman-Ford faster', ha='center', fontsize=11,
            color='#c0392b', fontweight='bold')
    ax.text(max(nodes) * 0.7, 2.2, 'Dijkstra faster', ha='center', fontsize=11,
            color='#2980b9', fontweight='bold')

    ax.set_xlabel('Number of Nodes', fontsize=12)
    ax.set_ylabel('Time Ratio (Bellman-Ford / Dijkstra)', fontsize=12)
    ax.set_title('Performance Ratio: Queue-Optimized Bellman-Ford vs Dijkstra on Grid Graphs\n'
                 '(Ratio > 1 means Dijkstra is faster)',
                 fontsize=13, fontweight='bold')
    ax.legend(loc='upper left', fontsize=10)

    ax.set_xlim(0, max(nodes) * 1.05)
    ax.set_ylim(0, max(max(shortest_ratio), max(second_ratio)) * 1.15)

    # 添加数据点标签
    for i, (n, r1, r2) in enumerate(zip(nodes, shortest_ratio, second_ratio)):
        ax.annotate(f'{r1:.2f}x', (n, r1), textcoords="offset points",
                    xytext=(0, 10), ha='center', fontsize=8, color='#27ae60')
        offset = -15 if r2 < r1 else 10
        ax.annotate(f'{r2:.2f}x', (n, r2), textcoords="offset points",
                    xytext=(0, offset), ha='center', fontsize=8, color='#e67e22')

    plt.tight_layout()
    plt.savefig('speedup_ratio.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Saved: speedup_ratio.png")


if __name__ == '__main__':
    print("Generating benchmark visualizations...")
    print()

    plot_shortest_path()
    plot_second_shortest_path()
    plot_combined()
    plot_speedup_line()

    print()
    print("All images generated successfully!")
    print()
    print("Files created:")
    print("  1. shortest_path_benchmark.png      - Shortest path comparison")
    print("  2. second_shortest_path_benchmark.png - Second shortest path comparison")
    print("  3. combined_benchmark.png           - Side-by-side comparison")
    print("  4. speedup_ratio.png                - Performance ratio trends")
