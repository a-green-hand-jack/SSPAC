# Second Shortest Path Algorithms Comparison

第二短路径算法性能对比实验项目

## 📖 项目简介

本项目实现并对比了两种求解第二短路径问题的算法：

1. **Two-Distance Dijkstra**: 基于Dijkstra算法的改进版本，维护每个节点的最短和次短距离
2. **State-Extended SPFA**: 基于SPFA的状态扩展版本，使用队列进行Bellman-Ford式的松弛

通过在多种图结构和规模上的基准测试，我们评估和对比了两种算法的：
- 运行时间
- 内存使用
- 操作次数（优先队列操作 vs 队列操作）
- 时间复杂度验证（理论 vs 实际）

## 🎯 算法说明

### Two-Distance Dijkstra
- **核心思想**: 为每个节点维护最短距离（d1）和次短距离（d2）
- **数据结构**: 最小堆优先队列
- **理论复杂度**: O(M log N)，其中M是边数，N是节点数
- **适用场景**: 稠密图、需要确定性性能保证的场景

### State-Extended SPFA
- **核心思想**: 扩展状态空间，使用队列进行Bellman-Ford式的边松弛
- **数据结构**: FIFO队列
- **理论复杂度**: 平均O(M)，最坏O(MN)
- **适用场景**: 稀疏图、随机图结构

## 🚀 快速开始

### 环境要求
- Python >= 3.10
- uv (推荐的包管理器)

### 安装

```bash
# 克隆项目
cd /path/to/SSPAC

# 使用 uv 创建虚拟环境
uv venv

# 激活虚拟环境
source .venv/bin/activate  # Linux/Mac
# 或
.venv\Scripts\activate  # Windows

# 安装依赖
uv pip install -e .

# 安装开发依赖（可选）
uv pip install -e ".[dev]"
```

### 运行实验

```bash
# 1. 下载 LeetCode 测试数据
python scripts/download_leetcode.py --output data/leetcode

# 2. 运行完整实验
python scripts/run_experiments.py --all

# 3. 生成实验报告
python scripts/generate_report.py --output results/report.pdf
```

### 使用 Jupyter Notebook 分析结果

```bash
jupyter notebook notebooks/analysis.ipynb
```

## 📁 项目结构

```
SSPAC/
├── src/second_shortest_path/    # 核心源代码
│   ├── algorithms/               # 算法实现
│   │   ├── dijkstra_two_dist.py # Two-Distance Dijkstra
│   │   └── spfa_extended.py     # State-Extended SPFA
│   ├── data/                     # 数据加载和生成
│   │   ├── loader.py            # 数据加载器
│   │   └── generator.py         # 测试数据生成器
│   ├── evaluation/               # 评估系统
│   │   ├── metrics.py           # 性能指标计算
│   │   └── visualizer.py        # 可视化工具
│   └── utils/                    # 工具函数
│       └── graph.py             # 图相关工具
├── tests/                        # 测试代码
├── data/                         # 数据目录
│   ├── leetcode/                # LeetCode测试数据
│   └── generated/               # 生成的测试数据
├── results/                      # 实验结果
│   ├── metrics/                 # 指标数据（CSV）
│   └── visualizations/          # 可视化图表
├── scripts/                      # 实验脚本
├── notebooks/                    # Jupyter笔记本
└── docs/                         # 文档
```

## 📊 性能指标

项目评估以下性能指标：

1. **运行时间**: Wall-clock time（秒）
2. **内存使用**: Peak memory（MB）
3. **PQ/Queue操作次数**: Push + Pop操作总数
4. **边松弛次数**: 实际执行的松弛操作
5. **迭代次数**: 主循环执行次数

## 📈 可视化输出

实验自动生成以下可视化图表：

1. **运行时间对比** - 柱状图
2. **可扩展性分析** - 折线图（不同图规模）
3. **复杂度验证** - 散点图 + 拟合曲线
4. **操作次数对比** - 分组柱状图
5. **百分位数分析** - 箱线图（P50, P95, P99）
6. **性能热力图** - 图密度 × 图规模

## 🧪 测试

```bash
# 运行所有测试
pytest

# 运行测试并生成覆盖率报告
pytest --cov=src/second_shortest_path --cov-report=html

# 查看覆盖率报告
open htmlcov/index.html
```

## 📦 依赖说明

### 核心依赖
- `numpy`: 数值计算
- `pandas`: 数据处理和分析
- `matplotlib`: 数据可视化
- `networkx`: 图论算法（用于验证）
- `tqdm`: 进度条显示

### 数据获取
- `requests`: HTTP请求
- `beautifulsoup4`: HTML解析

### 开发工具
- `pytest`: 测试框架
- `pytest-cov`: 测试覆盖率
- `black`: 代码格式化
- `isort`: 导入排序

## 📝 使用示例

```python
from second_shortest_path.algorithms import TwoDistanceDijkstra, StateExtendedSPFA
from second_shortest_path.data import GraphGenerator

# 生成测试图
graph = GraphGenerator.generate_random_graph(n=100, m=500)

# 初始化算法
dijkstra = TwoDistanceDijkstra(graph)
spfa = StateExtendedSPFA(graph)

# 查找第二短路径
source, target = 0, 99
d1, d2 = dijkstra.find_second_shortest(source, target)
print(f"最短路径: {d1}, 次短路径: {d2}")

# 获取统计信息
stats = dijkstra.get_statistics()
print(f"PQ操作次数: {stats['pq_operations']}")
print(f"边松弛次数: {stats['edge_relaxations']}")
```

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

## 👥 作者

CS260 课程项目

## 🔗 相关资源

- [LeetCode 2045: Second Minimum Time to Reach Destination](https://leetcode.com/problems/second-minimum-time-to-reach-destination/)
- [Dijkstra算法](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm)
- [SPFA算法](https://en.wikipedia.org/wiki/Shortest_Path_Faster_Algorithm)

