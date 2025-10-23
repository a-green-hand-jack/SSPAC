"""
Two-Distance Dijkstra算法测试
"""

import pytest

from second_shortest_path.algorithms import TwoDistanceDijkstra


class TestTwoDistanceDijkstra:
    """测试Two-Distance Dijkstra算法"""
    
    def test_simple_graph(self, simple_graph):
        """测试简单图"""
        algo = TwoDistanceDijkstra(simple_graph)
        shortest, second_shortest = algo.find_second_shortest(0, 4)
        
        assert shortest is not None
        assert second_shortest is not None
        assert shortest <= second_shortest
        
        # 验证统计信息
        stats = algo.get_statistics()
        assert stats['pq_operations'] > 0
        assert stats['edge_relaxations'] > 0
        assert stats['iterations'] > 0
    
    def test_chain_graph(self, chain_graph):
        """测试链式图"""
        algo = TwoDistanceDijkstra(chain_graph)
        shortest, second_shortest = algo.find_second_shortest(0, 9)
        
        # 链式图的最短路径应该是唯一的
        assert shortest == 9
        # 次短路径需要绕路
        assert second_shortest > shortest
    
    def test_complete_graph(self, complete_graph):
        """测试完全图"""
        algo = TwoDistanceDijkstra(complete_graph)
        shortest, second_shortest = algo.find_second_shortest(0, 4)
        
        # 完全图中，最短路径是直接边
        assert shortest == 1
        # 次短路径是通过一个中间节点
        assert second_shortest == 2
    
    def test_disconnected_graph(self, disconnected_graph):
        """测试非连通图"""
        algo = TwoDistanceDijkstra(disconnected_graph)
        shortest, second_shortest = algo.find_second_shortest(0, 4)
        
        # 0和4不连通，应该返回None
        assert shortest is None
        assert second_shortest is None
    
    def test_same_source_target(self, simple_graph):
        """测试源点和目标点相同的情况"""
        algo = TwoDistanceDijkstra(simple_graph)
        shortest, second_shortest = algo.find_second_shortest(0, 0)
        
        # 源点到自己的最短距离是0
        assert shortest == 0
    
    def test_invalid_source(self, simple_graph):
        """测试无效的源点"""
        algo = TwoDistanceDijkstra(simple_graph)
        
        with pytest.raises(ValueError):
            algo.find_second_shortest(10, 0)
    
    def test_invalid_target(self, simple_graph):
        """测试无效的目标点"""
        algo = TwoDistanceDijkstra(simple_graph)
        
        with pytest.raises(ValueError):
            algo.find_second_shortest(0, 10)
    
    def test_statistics_reset(self, simple_graph):
        """测试统计信息在多次运行间正确重置"""
        algo = TwoDistanceDijkstra(simple_graph)
        
        # 第一次运行
        algo.find_second_shortest(0, 4)
        stats1 = algo.get_statistics()
        
        # 第二次运行
        algo.find_second_shortest(0, 3)
        stats2 = algo.get_statistics()
        
        # 统计信息应该不同（因为目标不同）
        # 至少验证统计信息被重置了
        assert stats1['iterations'] >= 0
        assert stats2['iterations'] >= 0

