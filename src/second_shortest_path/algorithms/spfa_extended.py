"""
State-Extended SPFA算法实现

扩展状态空间，使用队列进行Bellman-Ford式的松弛操作。
理论时间复杂度: 平均 O(M)，最坏 O(MN)
"""

import logging
from collections import deque
from typing import Optional

logger = logging.getLogger(__name__)


class StateExtendedSPFA:
    """State-Extended SPFA算法实现
    
    通过扩展状态空间来维护每个节点的最短和次短距离。
    使用FIFO队列进行Bellman-Ford式的边松弛操作。
    
    理论复杂度:
    - 平均情况: O(M)
    - 最坏情况: O(MN)
    其中M是边数，N是节点数
    
    Args:
        graph: 图的邻接表表示，格式为 {node: [(neighbor, weight), ...]}
    
    Examples:
        >>> graph = {0: [(1, 1), (2, 2)], 1: [(2, 1)], 2: []}
        >>> algo = StateExtendedSPFA(graph)
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
        self._enqueue_operations = 0  # 入队次数（向后兼容）
        self._dequeue_operations = 0  # 出队次数（向后兼容）
        self._push_count = 0  # Push操作次数（入队）
        self._pop_count = 0  # Pop操作次数（出队）
        self._edge_relaxations = 0  # 边松弛次数
        self._d1_updates = 0  # d1距离标签更新次数
        self._d2_updates = 0  # d2距离标签更新次数
        self._iterations = 0  # 主循环迭代次数
        
        logger.debug(f"初始化 StateExtendedSPFA，图规模: {self.n} 节点")
    
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
        self._enqueue_operations = 0
        self._dequeue_operations = 0
        self._push_count = 0
        self._pop_count = 0
        self._edge_relaxations = 0
        self._d1_updates = 0
        self._d2_updates = 0
        self._iterations = 0
        
        # 初始化距离数组
        INF = float('inf')
        d1 = [INF] * self.n  # 最短距离
        d2 = [INF] * self.n  # 次短距离
        
        # FIFO队列: (node, distance, is_second)
        # is_second: False表示这是最短路径，True表示这是次短路径
        queue = deque([(source, 0, False)])
        d1[source] = 0
        
        # 记录节点是否在队列中（避免重复入队）
        in_queue = [[False, False] for _ in range(self.n)]  # [in_queue_d1, in_queue_d2]
        in_queue[source][0] = True
        
        self._enqueue_operations += 1
        self._push_count += 1
        
        logger.debug(f"开始搜索从 {source} 到 {target} 的第二短路径")
        
        while queue:
            self._iterations += 1
            u, dist, is_second = queue.popleft()
            self._dequeue_operations += 1
            self._pop_count += 1
            
            # 标记节点已出队
            if is_second:
                in_queue[u][1] = False
            else:
                in_queue[u][0] = False
            
            # 跳过过时的状态
            if is_second and dist > d2[u]:
                continue
            if not is_second and dist > d1[u]:
                continue
            
            # 松弛所有出边
            if u in self.graph:
                for v, weight in self.graph[u]:
                    self._relax_edge(u, v, weight, dist, d1, d2, queue, in_queue)
        
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
        queue: deque,
        in_queue: list[list[bool]]
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
            queue: FIFO队列
            in_queue: 记录节点是否在队列中
        """
        self._edge_relaxations += 1
        new_dist = current_dist + weight
        
        # 如果找到更短的路径
        if new_dist < d1[v]:
            # 原来的最短路径变成次短路径
            old_d1 = d1[v]
            d2[v] = old_d1
            d1[v] = new_dist
            self._d1_updates += 1
            
            # 将节点加入队列（如果不在队列中）
            if not in_queue[v][0]:
                queue.append((v, d1[v], False))
                in_queue[v][0] = True
                self._enqueue_operations += 1
                self._push_count += 1
            
            if d2[v] != float('inf') and not in_queue[v][1]:
                queue.append((v, d2[v], True))
                in_queue[v][1] = True
                self._enqueue_operations += 1
                self._push_count += 1
                if old_d1 != float('inf'):
                    self._d2_updates += 1
        
        # 如果找到次短路径
        elif d1[v] < new_dist < d2[v]:
            d2[v] = new_dist
            self._d2_updates += 1
            
            if not in_queue[v][1]:
                queue.append((v, d2[v], True))
                in_queue[v][1] = True
                self._enqueue_operations += 1
                self._push_count += 1
    
    def get_statistics(self) -> dict[str, int]:
        """获取算法运行的统计信息
        
        Returns:
            包含统计信息的字典：
            - enqueue_operations: 入队次数（向后兼容）
            - dequeue_operations: 出队次数（向后兼容）
            - push_count: Push操作次数（入队）
            - pop_count: Pop操作次数（出队）
            - edge_relaxations: 边松弛次数
            - d1_updates: d1距离标签更新次数
            - d2_updates: d2距离标签更新次数
            - iterations: 主循环迭代次数
        """
        return {
            'enqueue_operations': self._enqueue_operations,
            'dequeue_operations': self._dequeue_operations,
            'push_count': self._push_count,
            'pop_count': self._pop_count,
            'edge_relaxations': self._edge_relaxations,
            'd1_updates': self._d1_updates,
            'd2_updates': self._d2_updates,
            'iterations': self._iterations,
        }

