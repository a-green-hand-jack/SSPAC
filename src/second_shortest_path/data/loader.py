"""
数据加载器

提供从各种数据源加载测试数据的功能，包括LeetCode测试用例。
"""

import json
import logging
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


class DataLoader:
    """数据加载器，处理LeetCode数据和其他格式
    
    支持加载和转换多种数据格式，特别是LeetCode测试用例格式。
    
    Examples:
        >>> loader = DataLoader()
        >>> data = loader.load_leetcode_data("data/leetcode/test_cases.json")
        >>> graph = loader.convert_to_graph(data['test_cases'][0])
    """
    
    @staticmethod
    def load_leetcode_data(filepath: str | Path) -> dict[str, Any]:
        """从JSON文件加载LeetCode测试数据
        
        Args:
            filepath: JSON文件路径
        
        Returns:
            包含测试用例的字典，格式为：
            {
                "problem_id": int,
                "problem_name": str,
                "test_cases": [
                    {
                        "id": int,
                        "n": int,
                        "edges": [[int, int], ...],
                        "time": int,
                        "change": int,
                        "expected": int
                    },
                    ...
                ]
            }
        
        Raises:
            FileNotFoundError: 如果文件不存在
            json.JSONDecodeError: 如果JSON格式无效
        """
        filepath = Path(filepath)
        
        if not filepath.exists():
            logger.error(f"数据文件不存在: {filepath}")
            raise FileNotFoundError(f"数据文件不存在: {filepath}")
        
        logger.info(f"加载LeetCode数据: {filepath}")
        
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        num_cases = len(data.get('test_cases', []))
        logger.info(f"成功加载 {num_cases} 个测试用例")
        
        return data
    
    @staticmethod
    def convert_to_graph(test_case: dict[str, Any]) -> dict[str, Any]:
        """将测试用例转换为图数据结构
        
        将LeetCode格式的测试用例转换为算法可以使用的邻接表格式。
        
        Args:
            test_case: LeetCode测试用例，包含 'n' 和 'edges' 字段
        
        Returns:
            包含图数据的字典：
            {
                'n': 节点数,
                'edges': 边列表,
                'graph': 邻接表表示 {node: [(neighbor, weight), ...]},
                'source': 源节点（默认为0）,
                'target': 目标节点（默认为n-1）,
                'expected': 期望结果（如果有）
            }
        
        Examples:
            >>> test_case = {'n': 3, 'edges': [[0, 1], [1, 2]], 'time': 1, 'expected': 2}
            >>> graph_data = DataLoader.convert_to_graph(test_case)
            >>> print(graph_data['graph'])
            {0: [(1, 1)], 1: [(0, 1), (2, 1)], 2: [(1, 1)]}
        """
        n = test_case['n']
        edges = test_case['edges']
        weight = test_case.get('time', 1)  # 默认边权重为1
        
        # 构建邻接表（无向图）
        graph = {i: [] for i in range(n)}
        for u, v in edges:
            graph[u].append((v, weight))
            graph[v].append((u, weight))
        
        result = {
            'n': n,
            'edges': edges,
            'graph': graph,
            'source': 0,  # 默认源点
            'target': n - 1,  # 默认目标点
        }
        
        # 添加期望结果（如果有）
        if 'expected' in test_case:
            result['expected'] = test_case['expected']
        
        logger.debug(f"转换图: {n} 节点, {len(edges)} 条边")
        
        return result
    
    @staticmethod
    def load_all_datasets(data_dir: str | Path = "data") -> list[dict[str, Any]]:
        """加载所有可用数据集
        
        Args:
            data_dir: 数据目录路径
        
        Returns:
            所有数据集的列表，每个元素是一个包含图数据的字典
        """
        data_dir = Path(data_dir)
        datasets = []
        
        # 加载LeetCode数据
        leetcode_dir = data_dir / "leetcode"
        if leetcode_dir.exists():
            for json_file in leetcode_dir.glob("*.json"):
                try:
                    data = DataLoader.load_leetcode_data(json_file)
                    for test_case in data.get('test_cases', []):
                        graph_data = DataLoader.convert_to_graph(test_case)
                        graph_data['source_file'] = str(json_file)
                        datasets.append(graph_data)
                except Exception as e:
                    logger.warning(f"加载文件 {json_file} 时出错: {e}")
        
        # 加载生成的数据
        generated_dir = data_dir / "generated"
        if generated_dir.exists():
            for json_file in generated_dir.glob("*.json"):
                try:
                    with open(json_file, 'r', encoding='utf-8') as f:
                        graph_data = json.load(f)
                        graph_data['source_file'] = str(json_file)
                        datasets.append(graph_data)
                except Exception as e:
                    logger.warning(f"加载文件 {json_file} 时出错: {e}")
        
        logger.info(f"总共加载 {len(datasets)} 个数据集")
        
        return datasets
    
    @staticmethod
    def save_graph_data(graph_data: dict[str, Any], filepath: str | Path) -> None:
        """保存图数据到JSON文件
        
        Args:
            graph_data: 图数据字典
            filepath: 输出文件路径
        """
        filepath = Path(filepath)
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        # 将图数据转换为JSON可序列化的格式
        serializable_data = {
            'n': graph_data['n'],
            'edges': graph_data['edges'],
            'source': graph_data.get('source', 0),
            'target': graph_data.get('target', graph_data['n'] - 1),
        }
        
        if 'expected' in graph_data:
            serializable_data['expected'] = graph_data['expected']
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(serializable_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"图数据已保存到: {filepath}")

