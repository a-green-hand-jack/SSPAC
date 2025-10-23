"""
算法实现模块

包含Two-Distance Dijkstra和State-Extended SPFA两种算法的实现。
"""

from second_shortest_path.algorithms.dijkstra_two_dist import TwoDistanceDijkstra
from second_shortest_path.algorithms.spfa_extended import StateExtendedSPFA
# from second_shortest_path.algorithms.second_shortest_path_cpp import StateExtendedSPFA, TwoDistanceDijkstra

__all__ = [
    "TwoDistanceDijkstra",
    "StateExtendedSPFA",
]

