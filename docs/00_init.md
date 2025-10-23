完美！让我给你制定一个详细的项目计划。我会帮你创建一个完整的 Python 项目，使用 uv 作为环境管理工具。

## 📋 项目实施计划

### 项目结构
```
second-shortest-path/
├── pyproject.toml           # uv 项目配置
├── README.md                # 项目说明
├── src/
│   ├── __init__.py
│   ├── algorithms/
│   │   ├── __init__.py
│   │   ├── dijkstra_two_dist.py    # Two-Distance Dijkstra
│   │   └── spfa_extended.py        # State-Extended SPFA
│   ├── data/
│   │   ├── __init__.py
│   │   ├── loader.py               # 数据加载器
│   │   └── generator.py            # 测试数据生成器
│   ├── evaluation/
│   │   ├── __init__.py
│   │   ├── metrics.py              # 性能指标计算
│   │   └── visualizer.py           # 可视化工具
│   └── utils/
│       ├── __init__.py
│       └── graph.py                # 图相关工具函数
├── data/
│   ├── leetcode/                   # LeetCode 测试数据
│   │   └── test_cases.json
│   └── generated/                  # 生成的测试数据
├── tests/
│   ├── __init__.py
│   ├── test_dijkstra.py
│   └── test_spfa.py
├── notebooks/
│   └── analysis.ipynb              # 结果分析笔记本
├── results/
│   ├── metrics/                    # 指标结果
│   └── visualizations/             # 可视化图表
└── scripts/
    ├── download_leetcode.py        # 下载 LeetCode 数据
    ├── run_experiments.py          # 运行实验
    └── generate_report.py          # 生成报告
```

---

## 🎯 详细实施步骤（按时间顺序）

### **Phase 1: 项目初始化 (15分钟)**
```bash
⏱️ 时间: 0:00 - 0:15

任务:
1. 创建项目目录结构
2. 初始化 uv 项目
3. 配置依赖包
4. 创建基本文件框架
```

**依赖包清单:**
```toml
dependencies = [
    "numpy>=1.24.0",
    "matplotlib>=3.7.0",
    "pandas>=2.0.0",
    "networkx>=3.1",
    "pytest>=7.4.0",
    "jupyter>=1.0.0",
    "requests>=2.31.0",
    "beautifulsoup4>=4.12.0",
    "tqdm>=4.66.0",
]
```

---

### **Phase 2: 下载 LeetCode 数据 (20分钟)**
```bash
⏱️ 时间: 0:15 - 0:35

任务:
1. 实现 LeetCode 2045 数据爬取脚本
2. 将数据保存到 ~/Downloads/leetcode_data.json
3. 转换为标准格式
4. 验证数据完整性
```

**数据格式:**
```json
{
  "problem_id": 2045,
  "problem_name": "Second Minimum Time to Reach Destination",
  "test_cases": [
    {
      "id": 1,
      "n": 5,
      "edges": [[1,2],[1,3],[1,4],[3,4],[4,5]],
      "time": 3,
      "change": 5,
      "expected": 13
    }
  ]
}
```

---

### **Phase 3: 实现核心算法 (60分钟)**
```bash
⏱️ 时间: 0:35 - 1:35

任务清单:
```

#### **3.1 Two-Distance Dijkstra (30分钟)**
```python
class TwoDistanceDijkstra:
    def __init__(self, graph):
        """初始化"""
        
    def find_second_shortest(self, source, target):
        """主算法"""
        # 返回: (shortest_length, second_shortest_length)
        
    def _relax_edge(self, ...):
        """边松弛操作"""
        
    def get_statistics(self):
        """获取统计信息: PQ操作次数, 边松弛次数等"""
```

#### **3.2 State-Extended SPFA (30分钟)**
```python
class StateExtendedSPFA:
    def __init__(self, graph):
        """初始化"""
        
    def find_second_shortest(self, source, target):
        """主算法"""
        # 返回: (shortest_length, second_shortest_length)
        
    def _relax_edge(self, ...):
        """边松弛操作"""
        
    def get_statistics(self):
        """获取统计信息: 入队次数, 边松弛次数等"""
```

---

### **Phase 4: 数据加载与生成 (30分钟)**
```bash
⏱️ 时间: 1:35 - 2:05

任务:
```

#### **4.1 数据加载器 (15分钟)**
```python
class DataLoader:
    @staticmethod
    def load_leetcode_data(filepath):
        """加载 LeetCode 数据"""
        
    @staticmethod
    def convert_to_graph(test_case):
        """转换为图数据结构"""
        
    @staticmethod
    def load_all_datasets():
        """加载所有数据集"""
```

#### **4.2 数据生成器 (15分钟)**
```python
class GraphGenerator:
    @staticmethod
    def generate_random_graph(n, m, weight_range=(1, 10)):
        """生成随机图"""
        
    @staticmethod
    def generate_test_suite(sizes=[10, 50, 100, 500, 1000]):
        """生成不同规模的测试集"""
        
    @staticmethod
    def generate_special_cases():
        """生成特殊测试用例: 完全图, 稀疏图, 链式图等"""
```

---

### **Phase 5: 评估指标系统 (40分钟)**
```bash
⏱️ 时间: 2:05 - 2:45

任务:
```

#### **5.1 性能指标 (20分钟)**
```python
class PerformanceMetrics:
    """性能指标计算"""
    
    def __init__(self):
        self.results = []
        
    def run_single_test(self, algorithm, graph, source, target):
        """运行单个测试"""
        # 返回: {
        #   'time': 运行时间,
        #   'result': (l1, l2),
        #   'pq_ops': PQ操作次数,
        #   'edge_relaxations': 边松弛次数,
        #   'memory': 内存使用
        # }
        
    def run_benchmark(self, algorithms, test_suite):
        """运行基准测试"""
        
    def calculate_statistics(self):
        """计算统计数据: 平均值, 中位数, P95, P99等"""
        
    def export_results(self, filepath):
        """导出结果到 CSV"""
```

#### **5.2 复杂度验证 (20分钟)**
```python
class ComplexityAnalyzer:
    """时间复杂度验证"""
    
    def empirical_complexity(self, algorithm, graph_sizes):
        """经验复杂度分析"""
        # 拟合 O(M log N) 或 O(MN)
        
    def compare_theoretical_vs_empirical(self):
        """对比理论与实际复杂度"""
```

---

### **Phase 6: 可视化系统 (40分钟)**
```bash
⏱️ 时间: 2:45 - 3:25

任务:
```

#### **6.1 性能对比图 (20分钟)**
```python
class Visualizer:
    @staticmethod
    def plot_runtime_comparison(results):
        """运行时间对比"""
        # 柱状图: Dijkstra vs SPFA
        
    @staticmethod
    def plot_scalability(results):
        """可扩展性分析"""
        # 折线图: 不同图规模下的性能
        
    @staticmethod
    def plot_complexity_verification(results):
        """复杂度验证图"""
        # 散点图 + 拟合曲线
        
    @staticmethod
    def plot_operations_comparison(results):
        """操作次数对比"""
        # PQ操作 vs Queue操作
```

#### **6.2 统计箱线图 (20分钟)**
```python
    @staticmethod
    def plot_percentile_comparison(results):
        """百分位数对比: P50, P95, P99"""
        
    @staticmethod
    def plot_heatmap(results):
        """性能热力图"""
        # 不同图密度 x 不同规模
        
    @staticmethod
    def generate_comprehensive_report():
        """生成综合报告"""
```

---

### **Phase 7: 实验运行脚本 (30分钟)**
```bash
⏱️ 时间: 3:25 - 3:55

任务:
```

```python
# scripts/run_experiments.py
def main():
    # 1. 加载数据
    # 2. 初始化算法
    # 3. 运行测试
    # 4. 收集指标
    # 5. 生成可视化
    # 6. 导出报告
    
if __name__ == "__main__":
    main()
```

---

### **Phase 8: 测试与验证 (30分钟)**
```bash
⏱️ 时间: 3:55 - 4:25

任务:
1. 单元测试
2. 集成测试
3. 正确性验证
4. 边界情况测试
```

---

### **Phase 9: 文档与报告 (35分钟)**
```bash
⏱️ 时间: 4:25 - 5:00

任务:
1. README.md
2. 代码注释完善
3. 实验报告模板
4. 使用说明
```

---

## 📊 关键指标定义

### **性能指标:**
1. **运行时间**: Wall-clock time (秒)
2. **内存使用**: Peak memory (MB)
3. **PQ/Queue 操作次数**: Push + Pop 次数
4. **边松弛次数**: 实际松弛操作
5. **迭代次数**: 主循环执行次数

### **复杂度验证:**
1. **理论复杂度**:
   - Dijkstra: O(M log N)
   - SPFA: O(MN) worst, O(M) average
   
2. **经验复杂度**:
   - 通过拟合实际数据得出

### **统计数据:**
- Median (P50)
- P95 percentile
- P99 percentile
- Mean
- Standard deviation

---

## 🎨 可视化清单

1. **运行时间对比** (bar chart)
2. **可扩展性分析** (line chart)
3. **复杂度验证** (scatter + fit curve)
4. **操作次数对比** (grouped bar)
5. **百分位数箱线图** (box plot)
6. **性能热力图** (heatmap)

---

## ⚡ 快速启动命令

```bash
# 1. 初始化项目
cd ~/projects
mkdir second-shortest-path && cd second-shortest-path
uv init

# 2. 下载数据
python scripts/download_leetcode.py --output ~/Downloads

# 3. 运行实验
python scripts/run_experiments.py --all

# 4. 生成报告
python scripts/generate_report.py --output results/report.pdf
```

---

## ✅ 验收标准

- [ ] 两种算法正确实现
- [ ] LeetCode 数据下载并加载
- [ ] 所有测试用例通过
- [ ] 生成至少 6 种可视化图表
- [ ] 导出 CSV 格式的指标数据
- [ ] 完整的 README 文档
- [ ] 代码注释覆盖率 > 80%

---

## 🚀 现在开始实施？

我现在可以：

1. **立即开始创建项目** - 我会一步步帮你搭建整个项目
2. **分阶段实施** - 每完成一个 Phase 你确认后再继续
3. **先看示例代码** - 我先展示几个核心模块的实现

你想怎么开始？我建议我们直接开始 **Phase 1: 项目初始化**！