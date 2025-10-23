<!-- f6f624f9-7c25-4665-9021-432eb1629736 9fa97f68-695e-4541-82f2-efc8f180c966 -->
# SSPAC 项目初始化计划

## 1. 项目配置文件创建

### 1.1 创建 pyproject.toml

- 位置: `/ibex/user/wuj0c/Courses/CS260/SSPAC/pyproject.toml`
- 内容要点:
  - 项目名: `second-shortest-path`
  - 包名: `second_shortest_path`
  - 版本: `0.1.0`
  - 构建后端: `hatchling`
  - 依赖包: numpy, matplotlib, pandas, networkx, pytest, jupyter, requests, beautifulsoup4, tqdm
  - Python版本要求: `>=3.10`

### 1.2 创建 .gitignore

- 位置: `/ibex/user/wuj0c/Courses/CS260/SSPAC/.gitignore`
- 包含内容:
  - Python标准忽略: `__pycache__/`, `*.pyc`, `*.pyo`, `*.egg-info/`, `dist/`, `build/`
  - 环境: `.env`, `venv/`, `.venv/`
  - IDE: `.idea/`, `.vscode/`, `.DS_Store`
  - 测试: `htmlcov/`, `.pytest_cache/`, `.coverage`
  - 数据: `data/generated/`, `results/`

### 1.3 创建 README.md

- 位置: `/ibex/user/wuj0c/Courses/CS260/SSPAC/README.md`
- 包含内容:
  - 项目简介（第二短路径算法对比）
  - 算法说明（Two-Distance Dijkstra vs State-Extended SPFA）
  - 安装指南（使用uv）
  - 快速开始（运行实验的命令）
  - 项目结构说明
  - 依赖说明

## 2. 源代码目录结构创建

### 2.1 创建核心包目录

创建以下目录及 `__init__.py` 文件:

- `src/second_shortest_path/__init__.py`
- `src/second_shortest_path/algorithms/__init__.py`
- `src/second_shortest_path/data/__init__.py`
- `src/second_shortest_path/evaluation/__init__.py`
- `src/second_shortest_path/utils/__init__.py`

### 2.2 算法模块框架（algorithms/）

#### dijkstra_two_dist.py

```python
class TwoDistanceDijkstra:
    """Two-Distance Dijkstra算法实现
    
    维护每个节点的最短和次短距离，使用优先队列。
    理论复杂度: O(M log N)
    """
    
    def __init__(self, graph: dict):
        """初始化图结构和统计计数器"""
        
    def find_second_shortest(self, source: int, target: int) -> tuple[int, int]:
        """查找最短和次短路径长度"""
        
    def _relax_edge(self, u: int, v: int, weight: int) -> None:
        """边松弛操作"""
        
    def get_statistics(self) -> dict:
        """返回PQ操作次数、边松弛次数等统计信息"""
```

#### spfa_extended.py

```python
class StateExtendedSPFA:
    """State-Extended SPFA算法实现
    
    扩展状态空间，使用队列进行Bellman-Ford式的松弛。
    理论复杂度: O(MN) worst case, O(M) average case
    """
    
    def __init__(self, graph: dict):
        """初始化图结构和统计计数器"""
        
    def find_second_shortest(self, source: int, target: int) -> tuple[int, int]:
        """查找最短和次短路径长度"""
        
    def _relax_edge(self, u: int, v: int, weight: int) -> None:
        """边松弛操作"""
        
    def get_statistics(self) -> dict:
        """返回入队次数、边松弛次数等统计信息"""
```

### 2.3 数据处理模块框架（data/）

#### loader.py

```python
class DataLoader:
    """数据加载器，处理LeetCode数据和其他格式"""
    
    @staticmethod
    def load_leetcode_data(filepath: str) -> dict:
        """从JSON文件加载LeetCode测试数据"""
        
    @staticmethod
    def convert_to_graph(test_case: dict) -> dict:
        """将测试用例转换为邻接表格式"""
        
    @staticmethod
    def load_all_datasets() -> list[dict]:
        """加载所有可用数据集"""
```

#### generator.py

```python
class GraphGenerator:
    """测试图数据生成器"""
    
    @staticmethod
    def generate_random_graph(n: int, m: int, weight_range: tuple[int, int] = (1, 10)) -> dict:
        """生成随机图"""
        
    @staticmethod
    def generate_test_suite(sizes: list[int] = [10, 50, 100, 500, 1000]) -> list[dict]:
        """生成不同规模的测试集"""
        
    @staticmethod
    def generate_special_cases() -> list[dict]:
        """生成特殊测试用例：完全图、稀疏图、链式图等"""
```

### 2.4 评估模块框架（evaluation/）

#### metrics.py

```python
class PerformanceMetrics:
    """性能指标计算与统计"""
    
    def __init__(self):
        """初始化结果存储"""
        
    def run_single_test(self, algorithm, graph: dict, source: int, target: int) -> dict:
        """运行单个测试，返回时间、内存、操作次数等指标"""
        
    def run_benchmark(self, algorithms: list, test_suite: list[dict]) -> pd.DataFrame:
        """运行完整基准测试"""
        
    def calculate_statistics(self) -> dict:
        """计算均值、中位数、P95、P99等统计数据"""
        
    def export_results(self, filepath: str) -> None:
        """导出结果到CSV"""

class ComplexityAnalyzer:
    """时间复杂度验证"""
    
    def empirical_complexity(self, algorithm, graph_sizes: list[int]) -> dict:
        """经验复杂度分析，拟合O(M log N)或O(MN)"""
        
    def compare_theoretical_vs_empirical(self) -> pd.DataFrame:
        """对比理论与实际复杂度"""
```

#### visualizer.py

```python
class Visualizer:
    """可视化工具类，生成性能对比图表"""
    
    @staticmethod
    def plot_runtime_comparison(results: pd.DataFrame, output_path: str) -> None:
        """运行时间对比柱状图"""
        
    @staticmethod
    def plot_scalability(results: pd.DataFrame, output_path: str) -> None:
        """可扩展性分析折线图"""
        
    @staticmethod
    def plot_complexity_verification(results: pd.DataFrame, output_path: str) -> None:
        """复杂度验证散点图+拟合曲线"""
        
    @staticmethod
    def plot_operations_comparison(results: pd.DataFrame, output_path: str) -> None:
        """PQ操作vs队列操作对比"""
        
    @staticmethod
    def plot_percentile_comparison(results: pd.DataFrame, output_path: str) -> None:
        """百分位数箱线图"""
        
    @staticmethod
    def plot_heatmap(results: pd.DataFrame, output_path: str) -> None:
        """性能热力图（图密度 x 规模）"""
```

### 2.5 工具模块框架（utils/）

#### graph.py

```python
def build_adjacency_list(edges: list[list[int]], n: int) -> dict:
    """构建邻接表表示"""
    
def validate_graph(graph: dict, n: int) -> bool:
    """验证图的合法性"""
    
def graph_statistics(graph: dict) -> dict:
    """计算图的统计信息：节点数、边数、密度等"""
```

## 3. 测试目录创建

### 3.1 测试框架

创建以下测试文件:

- `tests/__init__.py`
- `tests/conftest.py` - pytest fixtures
- `tests/test_dijkstra.py`
- `tests/test_spfa.py`
- `tests/test_data_loader.py`
- `tests/test_graph_generator.py`

每个测试文件包含:

- 正确性测试（与LeetCode期望结果对比）
- 边界情况测试
- 特殊图结构测试

## 4. 数据目录创建

创建数据存储目录:

- `data/leetcode/` - 存放LeetCode测试数据
- `data/leetcode/.gitkeep` - 保持目录在git中
- `data/generated/` - 生成的测试数据（gitignore）

创建占位文件:

- `data/leetcode/test_cases.json` - 空JSON数组模板

## 5. 结果输出目录创建

创建结果存储目录:

- `results/metrics/` - CSV格式指标数据
- `results/visualizations/` - 图表输出
- `results/.gitkeep` - 保持目录结构

## 6. 脚本目录创建

### 6.1 download_leetcode.py

```python
#!/usr/bin/env python3
"""从LeetCode下载测试数据的脚本"""

import sys
from pathlib import Path

# src布局路径修正
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

def main():
    """主函数：爬取LeetCode 2045题数据"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="data/leetcode")
    args = parser.parse_args()
    
    # 实现数据下载逻辑
```

### 6.2 run_experiments.py

```python
#!/usr/bin/env python3
"""运行完整实验流程的脚本"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

def main():
    """主函数：
  1. 加载数据
  2. 初始化算法
  3. 运行基准测试
  4. 收集指标
  5. 生成可视化
  6. 导出报告
    """
```

### 6.3 generate_report.py

```python
#!/usr/bin/env python3
"""生成实验报告的脚本"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

def main():
    """生成PDF格式的实验报告"""
```

## 7. Notebooks创建

创建 `notebooks/analysis.ipynb` - Jupyter笔记本模板，包含:

- 数据加载示例
- 算法运行示例
- 结果分析示例
- 可视化展示

## 8. AI协作文档归档

将现有的 `docs/00_init.md` 保留在 `docs/` 目录中，符合ai_collaboration目录的规范。

## 9. Git初始化

按照Git工作流规范：

1. 初始化git仓库: `git init`
2. 添加所有文件: `git add .`
3. 创建初始提交: `git commit -m "chore: initial commit"`
4. 不添加远程仓库（按用户要求）

## 文件清单总结

总共需要创建约40个文件/目录：

- 3个配置文件（pyproject.toml, .gitignore, README.md）
- 18个Python源文件（含__init__.py）
- 6个测试文件
- 3个脚本文件
- 1个Jupyter笔记本
- 多个目录和.gitkeep文件

### To-dos

- [ ] 创建项目配置文件（pyproject.toml, .gitignore, README.md）
- [ ] 创建src/second_shortest_path目录结构及所有__init__.py文件
- [ ] 实现算法模块框架（dijkstra_two_dist.py, spfa_extended.py）
- [ ] 实现数据处理模块框架（loader.py, generator.py）
- [ ] 实现评估模块框架（metrics.py, visualizer.py）
- [ ] 实现工具模块（graph.py）
- [ ] 创建测试目录结构和测试文件框架
- [ ] 创建数据目录（data/leetcode, data/generated）
- [ ] 创建结果输出目录（results/metrics, results/visualizations）
- [ ] 创建实验脚本（download_leetcode.py, run_experiments.py, generate_report.py）
- [ ] 创建Jupyter笔记本模板（notebooks/analysis.ipynb）
- [ ] 初始化Git仓库并创建初始提交