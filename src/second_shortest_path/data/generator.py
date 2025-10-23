"""
测试图数据生成器

生成各种规模和类型的图用于算法性能测试。
"""

import logging
import random
from typing import Any

import networkx as nx

logger = logging.getLogger(__name__)


class GraphGenerator:
    """测试图数据生成器
    
    生成不同类型和规模的图，用于算法性能测试和评估。
    
    Examples:
        >>> generator = GraphGenerator()
        >>> graph_data = generator.generate_random_graph(n=100, m=500)
        >>> test_suite = generator.generate_test_suite([10, 50, 100])
    """
    
    @staticmethod
    def generate_random_graph(
        n: int, 
        m: int, 
        weight_range: tuple[int, int] = (1, 10),
        seed: int | None = None
    ) -> dict[str, Any]:
        """生成随机图
        
        Args:
            n: 节点数
            m: 边数
            weight_range: 边权重范围 (min, max)
            seed: 随机种子（用于可重复性）
        
        Returns:
            图数据字典，包含节点数、边列表和邻接表
        
        Raises:
            ValueError: 如果边数超过最大可能边数
        """
        if seed is not None:
            random.seed(seed)
        
        max_edges = n * (n - 1) // 2  # 无向图的最大边数
        if m > max_edges:
            raise ValueError(
                f"边数 {m} 超过了 {n} 个节点无向图的最大边数 {max_edges}"
            )
        
        logger.debug(f"生成随机图: {n} 节点, {m} 条边")
        
        # 使用networkx生成随机连通图
        # 先生成一棵生成树确保连通性
        edges_set = set()
        
        # 生成生成树（确保连通）
        nodes = list(range(n))
        random.shuffle(nodes)
        for i in range(1, n):
            u = nodes[i]
            v = random.choice(nodes[:i])
            if u > v:
                u, v = v, u
            edges_set.add((u, v))
        
        # 添加剩余的随机边
        while len(edges_set) < m:
            u = random.randint(0, n - 1)
            v = random.randint(0, n - 1)
            if u != v:
                if u > v:
                    u, v = v, u
                edges_set.add((u, v))
        
        # 为每条边分配随机权重
        edges = []
        for u, v in edges_set:
            weight = random.randint(weight_range[0], weight_range[1])
            edges.append([u, v, weight])
        
        # 构建邻接表
        graph = {i: [] for i in range(n)}
        for u, v, weight in edges:
            graph[u].append((v, weight))
            graph[v].append((u, weight))
        
        return {
            'n': n,
            'edges': [[u, v] for u, v, _ in edges],
            'graph': graph,
            'source': 0,
            'target': n - 1,
            'graph_type': 'random',
        }
    
    @staticmethod
    def generate_test_suite(
        sizes: list[int] = [10, 50, 100, 500, 1000],
        density: float = 0.3
    ) -> list[dict[str, Any]]:
        """生成不同规模的测试集
        
        Args:
            sizes: 节点数列表
            density: 图的密度（边数/最大边数的比例）
        
        Returns:
            测试图数据列表
        """
        test_suite = []
        
        for n in sizes:
            max_edges = n * (n - 1) // 2
            m = int(max_edges * density)
            m = max(m, n - 1)  # 至少要有n-1条边保证连通
            
            logger.info(f"生成测试图: n={n}, m={m}")
            
            graph_data = GraphGenerator.generate_random_graph(n, m)
            graph_data['test_name'] = f"random_n{n}_m{m}"
            test_suite.append(graph_data)
        
        logger.info(f"生成测试套件完成，共 {len(test_suite)} 个测试图")
        
        return test_suite
    
    @staticmethod
    def generate_special_cases() -> list[dict[str, Any]]:
        """生成特殊测试用例
        
        包括：
        - 完全图
        - 稀疏图
        - 链式图
        - 星型图
        - 网格图
        
        Returns:
            特殊测试图数据列表
        """
        special_cases = []
        
        # 1. 完全图
        n = 20
        complete_graph = {i: [] for i in range(n)}
        edges = []
        for i in range(n):
            for j in range(i + 1, n):
                weight = 1
                complete_graph[i].append((j, weight))
                complete_graph[j].append((i, weight))
                edges.append([i, j])
        
        special_cases.append({
            'n': n,
            'edges': edges,
            'graph': complete_graph,
            'source': 0,
            'target': n - 1,
            'graph_type': 'complete',
            'test_name': f'complete_n{n}',
        })
        
        # 2. 链式图
        n = 100
        chain_graph = {i: [] for i in range(n)}
        edges = []
        for i in range(n - 1):
            weight = 1
            chain_graph[i].append((i + 1, weight))
            chain_graph[i + 1].append((i, weight))
            edges.append([i, i + 1])
        
        special_cases.append({
            'n': n,
            'edges': edges,
            'graph': chain_graph,
            'source': 0,
            'target': n - 1,
            'graph_type': 'chain',
            'test_name': f'chain_n{n}',
        })
        
        # 3. 星型图
        n = 50
        star_graph = {i: [] for i in range(n)}
        edges = []
        center = 0
        for i in range(1, n):
            weight = 1
            star_graph[center].append((i, weight))
            star_graph[i].append((center, weight))
            edges.append([center, i])
        
        special_cases.append({
            'n': n,
            'edges': edges,
            'graph': star_graph,
            'source': 1,
            'target': n - 1,
            'graph_type': 'star',
            'test_name': f'star_n{n}',
        })
        
        # 4. 网格图
        rows, cols = 10, 10
        n = rows * cols
        grid_graph = {i: [] for i in range(n)}
        edges = []
        
        def node_id(r: int, c: int) -> int:
            return r * cols + c
        
        for r in range(rows):
            for c in range(cols):
                u = node_id(r, c)
                # 右边
                if c + 1 < cols:
                    v = node_id(r, c + 1)
                    weight = 1
                    grid_graph[u].append((v, weight))
                    grid_graph[v].append((u, weight))
                    edges.append([u, v])
                # 下边
                if r + 1 < rows:
                    v = node_id(r + 1, c)
                    weight = 1
                    grid_graph[u].append((v, weight))
                    grid_graph[v].append((u, weight))
                    edges.append([u, v])
        
        special_cases.append({
            'n': n,
            'edges': edges,
            'graph': grid_graph,
            'source': 0,
            'target': n - 1,
            'graph_type': 'grid',
            'test_name': f'grid_{rows}x{cols}',
        })
        
        logger.info(f"生成 {len(special_cases)} 个特殊测试用例")
        
        return special_cases

