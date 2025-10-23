"""
Pytest配置文件

定义测试fixtures和全局配置。
"""

import pytest


@pytest.fixture
def simple_graph():
    """简单测试图fixture
    
    返回一个包含5个节点的简单图。
    """
    graph = {
        0: [(1, 1), (2, 2)],
        1: [(0, 1), (2, 1), (3, 3)],
        2: [(0, 2), (1, 1), (3, 1), (4, 5)],
        3: [(1, 3), (2, 1), (4, 2)],
        4: [(2, 5), (3, 2)],
    }
    return graph


@pytest.fixture
def chain_graph():
    """链式图fixture
    
    返回一个包含10个节点的链式图。
    """
    n = 10
    graph = {i: [] for i in range(n)}
    for i in range(n - 1):
        graph[i].append((i + 1, 1))
        graph[i + 1].append((i, 1))
    return graph


@pytest.fixture
def complete_graph():
    """完全图fixture
    
    返回一个包含5个节点的完全图。
    """
    n = 5
    graph = {i: [] for i in range(n)}
    for i in range(n):
        for j in range(i + 1, n):
            graph[i].append((j, 1))
            graph[j].append((i, 1))
    return graph


@pytest.fixture
def disconnected_graph():
    """非连通图fixture
    
    返回一个包含两个连通分量的图。
    """
    graph = {
        0: [(1, 1)],
        1: [(0, 1), (2, 1)],
        2: [(1, 1)],
        3: [(4, 1)],
        4: [(3, 1)],
    }
    return graph

