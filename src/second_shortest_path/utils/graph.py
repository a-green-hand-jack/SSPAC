"""
图相关工具函数

提供图的构建、验证和统计功能。
"""

import logging
from typing import Any

logger = logging.getLogger(__name__)


def build_adjacency_list(
    edges: list[list[int]],
    n: int,
    weights: list[int] | None = None,
    directed: bool = False
) -> dict[int, list[tuple[int, int]]]:
    """构建邻接表表示
    
    Args:
        edges: 边列表，格式为 [[u, v], ...]
        n: 节点数
        weights: 边权重列表，如果为None则所有边权重为1
        directed: 是否为有向图
    
    Returns:
        邻接表字典 {node: [(neighbor, weight), ...]}
    
    Examples:
        >>> edges = [[0, 1], [1, 2]]
        >>> graph = build_adjacency_list(edges, 3)
        >>> print(graph)
        {0: [(1, 1)], 1: [(0, 1), (2, 1)], 2: [(1, 1)]}
    """
    graph = {i: [] for i in range(n)}
    
    if weights is None:
        weights = [1] * len(edges)
    
    if len(edges) != len(weights):
        raise ValueError(f"边数({len(edges)})与权重数({len(weights)})不匹配")
    
    for (u, v), weight in zip(edges, weights):
        if u < 0 or u >= n or v < 0 or v >= n:
            raise ValueError(f"节点索引越界: u={u}, v={v}, n={n}")
        
        graph[u].append((v, weight))
        if not directed:
            graph[v].append((u, weight))
    
    logger.debug(f"构建邻接表: {n} 节点, {len(edges)} 条边, 有向={directed}")
    
    return graph


def validate_graph(graph: dict[int, list[tuple[int, int]]], n: int) -> bool:
    """验证图的合法性
    
    检查图是否满足以下条件：
    1. 所有节点都在范围 [0, n) 内
    2. 所有边权重为正数
    3. 没有自环
    
    Args:
        graph: 图的邻接表表示
        n: 节点数
    
    Returns:
        True 如果图合法，否则 False
    """
    if len(graph) != n:
        logger.error(f"图节点数不匹配: 期望 {n}, 实际 {len(graph)}")
        return False
    
    for u in range(n):
        if u not in graph:
            logger.error(f"缺少节点 {u}")
            return False
        
        for v, weight in graph[u]:
            # 检查节点范围
            if v < 0 or v >= n:
                logger.error(f"邻居节点越界: u={u}, v={v}, n={n}")
                return False
            
            # 检查权重
            if weight <= 0:
                logger.error(f"边权重非正: ({u}, {v}) 权重={weight}")
                return False
            
            # 检查自环
            if u == v:
                logger.error(f"存在自环: 节点 {u}")
                return False
    
    logger.debug("图验证通过")
    return True


def graph_statistics(graph: dict[int, list[tuple[int, int]]]) -> dict[str, Any]:
    """计算图的统计信息
    
    Args:
        graph: 图的邻接表表示
    
    Returns:
        包含统计信息的字典：
        - n: 节点数
        - m: 边数（无向图）
        - avg_degree: 平均度数
        - max_degree: 最大度数
        - min_degree: 最小度数
        - density: 图的密度
        - avg_weight: 平均边权重
    """
    n = len(graph)
    
    # 计算度数
    degrees = [len(neighbors) for neighbors in graph.values()]
    avg_degree = sum(degrees) / n if n > 0 else 0
    max_degree = max(degrees) if degrees else 0
    min_degree = min(degrees) if degrees else 0
    
    # 计算边数（假设无向图，每条边被计算两次）
    total_edges = sum(degrees)
    m = total_edges // 2 if total_edges % 2 == 0 else (total_edges + 1) // 2
    
    # 计算密度
    max_edges = n * (n - 1) / 2
    density = m / max_edges if max_edges > 0 else 0
    
    # 计算平均权重
    all_weights = []
    for neighbors in graph.values():
        for _, weight in neighbors:
            all_weights.append(weight)
    avg_weight = sum(all_weights) / len(all_weights) if all_weights else 0
    
    stats = {
        'n': n,
        'm': m,
        'avg_degree': avg_degree,
        'max_degree': max_degree,
        'min_degree': min_degree,
        'density': density,
        'avg_weight': avg_weight,
    }
    
    logger.debug(
        f"图统计: n={n}, m={m}, 密度={density:.4f}, "
        f"平均度数={avg_degree:.2f}"
    )
    
    return stats

