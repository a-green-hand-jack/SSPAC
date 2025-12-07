# LeetCode 2045 第二短路径数据集说明

本文档详细说明了 `scripts/download_leetcode_data.py` 脚本生成的数据集分布情况。该数据集旨在全面评估第二短路径算法（如 State-Extended SPFA 和 Two-Distance Dijkstra）的性能和正确性。

## 1. 数据集概览

数据集由 **29 个测试用例**组成，涵盖了从简单的手动构造图到大规模随机图以及特殊拓扑结构的图。所有数据均以 JSON 格式存储。

### 数据来源
- **官方示例**: 源自 LeetCode 2045 题目描述。
- **随机生成**: 使用 `networkx` 生成不同规模和密度的连通图。
- **特殊构造**: 针对算法边界情况设计的特殊图结构。

## 2. 数据分布详情

### 2.1 官方测试用例 (Official Test Cases)
共 **5 个**基础用例，用于验证算法的基本正确性。

| ID | 名称 | 节点数 (N) | 描述 |
|----|------|------------|------|
| 1 | Medium graph | 5 | 中等规模图，存在多条路径 |
| 2 | Simple path | 2 | 只有一条边的简单路径，需要往返 |
| 3 | Triangle graph | 3 | 三角形图 |
| 4 | Square graph | 4 | 正方形图 |
| 5 | Linear chain | 5 | 线性链结构 |

### 2.2 随机生成图 (Random Graphs)
共 **20 个**用例，旨在测试算法在不同规模和稀疏度下的性能与鲁棒性。这些图保证是连通的。

| 数量 | 节点范围 (N) | 密度 | 描述 |
|------|--------------|------|------|
| 5 | 5 - 10 | 稀疏 (Sparse) | 小规模稀疏图 |
| 5 | 10 - 20 | 中等 (Medium) | 中小规模一般图 |
| 5 | 20 - 50 | 中等 (Medium) | 中等规模一般图 |
| 5 | 50 - 100 | 稀疏 (Sparse) | 大规模稀疏图 |

*注：源节点固定为 1，目标节点在 [2, N] 中随机选择。*

### 2.3 特殊构造图 (Special Cases)
共 **4 个**特殊用例，用于测试特定拓扑结构下的算法表现。

| ID | 名称 | 规模 | 描述 |
|----|------|------|------|
| 200 | Complete graph K6 | N=6 | 完全图，边数多，路径极其丰富 |
| 201 | Star graph | N=10 | 星形图，中心节点压力大 |
| 202 | Bipartite K4,4 | N=8 | 完全二分图 |
| 203 | Grid graph 4x4 | N=16 | 网格图，模拟曼哈顿距离场景 |

## 3. 图的生成机制 (Graph Generation Mechanism)

### 3.1 边的生成
- **连通性**: 对于随机生成的图，脚本首先会构建一棵随机生成树，以确保图是连通的。
- **随机性**: 在保证连通性的基础上，根据配置的密度（稀疏、中等）随机添加额外的边，直到达到所需的边数 `M`。
- **边列表**: 生成的 `edges` 列表只包含 `[u, v]` 对，表示节点 `u` 和 `v` 之间存在一条无向边。

### 3.2 权重特性
- **无权图**: 本数据集中的图均为**无权图**。所有边都隐含地被视为具有相同的“权重”（例如，穿越时间为 1 单位）。
- **问题对应**: 这与 LeetCode 2045 问题的设定一致，该问题中所有边遍历所需时间相同，因此“最短/第二短路径”主要取决于路径中的边数。本项目的算法实现也基于这一特性。

## 4. 数据格式 (Data Format)

生成的 `leetcode_dataset.json` 文件遵循以下结构：

```json
{
  "metadata": {
    "source": "LeetCode 2045 + Generated",
    "total_cases": 29,
    ...
  },
  "test_cases": [
    {
      "id": 1,
      "name": "Example 1",
      "n": 5,                 // 节点数量
      "edges": [[1, 2], ...], // 边列表 (无向边)
      "source": 1,            // 起点
      "target": 5,            // 终点
      "expected_shortest": 2, // 预期最短路径长度 (边数)
      "expected_second_shortest": 3, // 预期第二短路径长度
      "description": "..."
    },
    ...
  ]
}
```

## 4. 使用方法

### 生成数据
运行以下命令生成数据集：
```bash
python scripts/download_leetcode_data.py --output data/leetcode
```

### 加载数据 (Python 示例)
```python
import json

with open('data/leetcode/leetcode_second_shortest_path.json', 'r') as f:
    dataset = json.load(f)

for case in dataset['test_cases']:
    print(f"Running case {case['id']}: {case['name']}")
    # 在此调用算法...
```
