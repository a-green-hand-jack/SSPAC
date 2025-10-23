"""
数据处理模块

包含数据加载器和测试数据生成器。
"""

from second_shortest_path.data.generator import GraphGenerator
from second_shortest_path.data.loader import DataLoader

__all__ = [
    "DataLoader",
    "GraphGenerator",
]

