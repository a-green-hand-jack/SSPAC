"""
Two-Distance Dijkstra算法实现

维护每个节点的最短和次短距离，使用优先队列进行高效的路径搜索。
理论时间复杂度: O(M log N)
"""

import heapq
import logging
from typing import Optional

logger = logging.getLogger(__name__)


class TwoDistanceDijkstra:
    """Two-Distance Dijkstra算法实现
    
    为每个节点维护两个距离值：
    - d1[v]: 从源点到节点v的最短距离
    - d2[v]: 从源点到节点v的次短距离
    
    使用最小堆优先队列进行高效的节点选择。
    
    理论复杂度: O(M log N)，其中M是边数，N是节点数
    
    Args:
        graph: 图的邻接表表示，格式为 {node: [(neighbor, weight), ...]}
    
    Examples:
        >>> graph = {0: [(1, 1), (2, 2)], 1: [(2, 1)], 2: []}
        >>> algo = TwoDistanceDijkstra(graph)
        >>> shortest, second_shortest = algo.find_second_shortest(0, 2)
        >>> print(f"最短路径: {shortest}, 次短路径: {second_shortest}")
    """
    
    def __init__(self, graph: dict[int, list[tuple[int, int]]]):
        """初始化算法
        
        Args:
            graph: 图的邻接表表示，格式为 {node: [(neighbor, weight), ...]}
        """
        self.graph = graph
        self.n = len(graph)
        
        # 统计计数器
        self._pq_operations = 0  # 优先队列操作次数（push + pop）
        self._edge_relaxations = 0  # 边松弛次数
        self._iterations = 0  # 主循环迭代次数
        
        logger.debug(f"初始化 TwoDistanceDijkstra，图规模: {self.n} 节点")
    
    def find_second_shortest(
        self, 
        source: int, 
        target: int
    ) -> tuple[Optional[int], Optional[int]]:
        """查找从源点到目标点的最短和次短路径长度
        
        Args:
            source: 源节点
            target: 目标节点
        
        Returns:
            (shortest_distance, second_shortest_distance) 元组
            如果不存在路径，对应值为 None
        
        Raises:
            ValueError: 如果源点或目标点不在图中
        """
        if source not in self.graph:
            raise ValueError(f"源节点 {source} 不在图中")
        if target not in self.graph:
            raise ValueError(f"目标节点 {target} 不在图中")
        
        # 重置统计计数器
        self._pq_operations = 0
        self._edge_relaxations = 0
        self._iterations = 0
        
        # 初始化距离数组
        INF = float('inf')
        d1 = [INF] * self.n  # 最短距离
        d2 = [INF] * self.n  # 次短距离
        
        # 优先队列: (distance, node, is_second)
        # is_second: False表示这是最短路径，True表示这是次短路径
        pq = [(0, source, False)]
        d1[source] = 0
        self._pq_operations += 1  # push
        
        logger.debug(f"开始搜索从 {source} 到 {target} 的第二短路径")
        
        while pq:
            self._iterations += 1
            dist, u, is_second = heapq.heappop(pq)
            self._pq_operations += 1  # pop
            
            # 如果已经找到目标的次短路径，可以提前终止
            if u == target and is_second:
                logger.debug(
                    f"找到目标节点的次短路径，"
                    f"最短: {d1[target]}, 次短: {d2[target]}"
                )
                break
            
            # 跳过过时的状态
            if is_second and dist > d2[u]:
                continue
            if not is_second and dist > d1[u]:
                continue
            
            # 松弛所有出边
            if u in self.graph:
                for v, weight in self.graph[u]:
                    self._relax_edge(u, v, weight, dist, d1, d2, pq)
        
        # 返回结果
        shortest = d1[target] if d1[target] != INF else None
        second_shortest = d2[target] if d2[target] != INF else None
        
        logger.info(
            f"搜索完成: 最短={shortest}, 次短={second_shortest}, "
            f"迭代次数={self._iterations}"
        )
        
        return shortest, second_shortest
    
    def _relax_edge(
        self,
        u: int,
        v: int,
        weight: int,
        current_dist: float,
        d1: list[float],
        d2: list[float],
        pq: list
    ) -> None:
        """执行边松弛操作
        
        尝试通过边(u, v)更新节点v的最短和次短距离。
        
        Args:
            u: 当前节点
            v: 邻居节点
            weight: 边权重
            current_dist: 当前到达u的距离
            d1: 最短距离数组
            d2: 次短距离数组
            pq: 优先队列
        """
        self._edge_relaxations += 1
        new_dist = current_dist + weight
        
        # 如果找到更短的路径
        if new_dist < d1[v]:
            # 原来的最短路径变成次短路径
            d2[v] = d1[v]
            d1[v] = new_dist
            
            heapq.heappush(pq, (d1[v], v, False))
            self._pq_operations += 1
            
            if d2[v] != float('inf'):
                heapq.heappush(pq, (d2[v], v, True))
                self._pq_operations += 1
        
        # 如果找到次短路径
        elif d1[v] < new_dist < d2[v]:
            d2[v] = new_dist
            heapq.heappush(pq, (d2[v], v, True))
            self._pq_operations += 1
    
    def get_statistics(self) -> dict[str, int]:
        """获取算法运行的统计信息
        
        Returns:
            包含统计信息的字典：
            - pq_operations: 优先队列操作次数
            - edge_relaxations: 边松弛次数
            - iterations: 主循环迭代次数
        """
        return {
            'pq_operations': self._pq_operations,
            'edge_relaxations': self._edge_relaxations,
            'iterations': self._iterations,
        }

