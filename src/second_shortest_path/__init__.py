"""
Second Shortest Path Algorithms

本包提供两种第二短路径算法的实现和性能评估工具。
"""

__version__ = "0.1.0"

from second_shortest_path.algorithms.dijkstra_two_dist import TwoDistanceDijkstra
from second_shortest_path.algorithms.spfa_extended import StateExtendedSPFA

__all__ = [
    "TwoDistanceDijkstra",
    "StateExtendedSPFA",
]

