"""
数据加载器测试
"""

import json
import tempfile
from pathlib import Path

import pytest

from second_shortest_path.data import DataLoader


class TestDataLoader:
    """测试DataLoader类"""
    
    def test_convert_to_graph(self):
        """测试测试用例转换为图"""
        test_case = {
            'n': 5,
            'edges': [[0, 1], [1, 2], [2, 3], [3, 4], [0, 4]],
            'time': 2,
            'expected': 10,
        }
        
        graph_data = DataLoader.convert_to_graph(test_case)
        
        assert graph_data['n'] == 5
        assert len(graph_data['edges']) == 5
        assert 'graph' in graph_data
        assert graph_data['source'] == 0
        assert graph_data['target'] == 4
        assert graph_data['expected'] == 10
        
        # 验证图是无向的
        graph = graph_data['graph']
        assert (1, 2) in graph[0]  # 0 -> 1
        assert (0, 2) in graph[1]  # 1 -> 0
    
    def test_load_leetcode_data(self):
        """测试加载LeetCode数据"""
        # 创建临时JSON文件
        test_data = {
            'problem_id': 2045,
            'problem_name': 'Test Problem',
            'test_cases': [
                {
                    'id': 1,
                    'n': 3,
                    'edges': [[0, 1], [1, 2]],
                    'time': 1,
                    'expected': 2,
                }
            ]
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(test_data, f)
            temp_path = f.name
        
        try:
            # 加载数据
            data = DataLoader.load_leetcode_data(temp_path)
            
            assert data['problem_id'] == 2045
            assert len(data['test_cases']) == 1
            assert data['test_cases'][0]['n'] == 3
        finally:
            # 清理临时文件
            Path(temp_path).unlink()
    
    def test_load_nonexistent_file(self):
        """测试加载不存在的文件"""
        with pytest.raises(FileNotFoundError):
            DataLoader.load_leetcode_data('nonexistent_file.json')
    
    def test_save_graph_data(self):
        """测试保存图数据"""
        graph_data = {
            'n': 3,
            'edges': [[0, 1], [1, 2]],
            'source': 0,
            'target': 2,
            'expected': 2,
        }
        
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / 'test_graph.json'
            DataLoader.save_graph_data(graph_data, filepath)
            
            # 验证文件已创建
            assert filepath.exists()
            
            # 验证内容
            with open(filepath, 'r') as f:
                loaded_data = json.load(f)
            
            assert loaded_data['n'] == 3
            assert loaded_data['source'] == 0
            assert loaded_data['target'] == 2
            assert loaded_data['expected'] == 2

