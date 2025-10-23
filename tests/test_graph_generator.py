"""
图生成器测试
"""

import pytest

from second_shortest_path.data import GraphGenerator


class TestGraphGenerator:
    """测试GraphGenerator类"""
    
    def test_generate_random_graph(self):
        """测试生成随机图"""
        n, m = 10, 20
        graph_data = GraphGenerator.generate_random_graph(n, m, seed=42)
        
        assert graph_data['n'] == n
        assert len(graph_data['edges']) == m
        assert 'graph' in graph_data
        assert graph_data['source'] == 0
        assert graph_data['target'] == n - 1
        
        # 验证图是连通的（至少有n-1条边）
        graph = graph_data['graph']
        assert len(graph) == n
    
    def test_generate_random_graph_too_many_edges(self):
        """测试生成边数过多的图"""
        n = 5
        max_edges = n * (n - 1) // 2
        
        with pytest.raises(ValueError):
            GraphGenerator.generate_random_graph(n, max_edges + 1)
    
    def test_generate_random_graph_reproducibility(self):
        """测试随机图的可重复性"""
        n, m = 10, 20
        seed = 42
        
        graph1 = GraphGenerator.generate_random_graph(n, m, seed=seed)
        graph2 = GraphGenerator.generate_random_graph(n, m, seed=seed)
        
        # 使用相同种子应该生成相同的图
        assert graph1['edges'] == graph2['edges']
    
    def test_generate_test_suite(self):
        """测试生成测试套件"""
        sizes = [10, 20, 30]
        test_suite = GraphGenerator.generate_test_suite(sizes)
        
        assert len(test_suite) == len(sizes)
        
        for i, graph_data in enumerate(test_suite):
            assert graph_data['n'] == sizes[i]
            assert 'test_name' in graph_data
    
    def test_generate_special_cases(self):
        """测试生成特殊用例"""
        special_cases = GraphGenerator.generate_special_cases()
        
        assert len(special_cases) > 0
        
        # 验证每个特殊用例都有必要的字段
        for graph_data in special_cases:
            assert 'n' in graph_data
            assert 'edges' in graph_data
            assert 'graph' in graph_data
            assert 'graph_type' in graph_data
            assert 'test_name' in graph_data
        
        # 验证包含不同类型的图
        graph_types = [g['graph_type'] for g in special_cases]
        assert 'complete' in graph_types
        assert 'chain' in graph_types
        assert 'star' in graph_types
        assert 'grid' in graph_types
    
    def test_complete_graph_structure(self):
        """测试完全图的结构"""
        special_cases = GraphGenerator.generate_special_cases()
        complete_graph = next(g for g in special_cases if g['graph_type'] == 'complete')
        
        n = complete_graph['n']
        graph = complete_graph['graph']
        
        # 完全图中，每个节点应该连接到其他所有节点
        for node in range(n):
            assert len(graph[node]) == n - 1
    
    def test_chain_graph_structure(self):
        """测试链式图的结构"""
        special_cases = GraphGenerator.generate_special_cases()
        chain_graph = next(g for g in special_cases if g['graph_type'] == 'chain')
        
        n = chain_graph['n']
        graph = chain_graph['graph']
        
        # 链式图中，除了两端，每个节点应该有2个邻居
        assert len(graph[0]) == 1  # 起点
        assert len(graph[n - 1]) == 1  # 终点
        
        for node in range(1, n - 1):
            assert len(graph[node]) == 2  # 中间节点

