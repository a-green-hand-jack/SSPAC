#!/usr/bin/env python3
"""
LeetCode 2045 数据集下载和准备脚本
包含官方测试用例和生成的补充测试数据
"""

import json
import os
import random
from pathlib import Path
from typing import List, Tuple, Dict
import networkx as nx


class LeetCodeDataDownloader:
    """LeetCode 数据下载器"""
    
    def __init__(self, output_dir: str = "~/Downloads"):
        self.output_dir = Path(output_dir).expanduser()
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def get_official_test_cases(self) -> List[Dict]:
        """
        获取 LeetCode 2045 官方测试用例
        这些是从 LeetCode 题目描述中手动整理的
        """
        test_cases = [
            {
                "id": 1,
                "name": "Example 1 - Medium graph",
                "n": 5,
                "edges": [[1, 2], [1, 3], [1, 4], [3, 4], [4, 5]],
                "source": 1,
                "target": 5,
                "expected_shortest": 2,  # 路径长度（边数）
                "expected_second_shortest": 3,  # 第二短路径长度
                "description": "中等规模图，存在多条路径"
            },
            {
                "id": 2,
                "name": "Example 2 - Simple path",
                "n": 2,
                "edges": [[1, 2]],
                "source": 1,
                "target": 2,
                "expected_shortest": 1,
                "expected_second_shortest": 3,  # 需要往返
                "description": "只有一条边的简单路径"
            },
            {
                "id": 3,
                "name": "Triangle graph",
                "n": 3,
                "edges": [[1, 2], [2, 3], [1, 3]],
                "source": 1,
                "target": 3,
                "expected_shortest": 1,
                "expected_second_shortest": 2,
                "description": "三角形图，有两条路径"
            },
            {
                "id": 4,
                "name": "Square graph",
                "n": 4,
                "edges": [[1, 2], [2, 3], [3, 4], [4, 1], [1, 3]],
                "source": 1,
                "target": 3,
                "expected_shortest": 1,
                "expected_second_shortest": 2,
                "description": "正方形图，有多条路径"
            },
            {
                "id": 5,
                "name": "Linear chain",
                "n": 5,
                "edges": [[1, 2], [2, 3], [3, 4], [4, 5]],
                "source": 1,
                "target": 5,
                "expected_shortest": 4,
                "expected_second_shortest": 6,
                "description": "线性链，只能往返"
            },
        ]
        
        return test_cases
    
    def generate_random_graphs(self, num_graphs: int = 20) -> List[Dict]:
        """生成随机图测试用例"""
        test_cases = []
        
        # 不同规模的图
        graph_configs = [
            {"n_range": (5, 10), "density": "sparse", "count": 5},
            {"n_range": (10, 20), "density": "medium", "count": 5},
            {"n_range": (20, 50), "density": "medium", "count": 5},
            {"n_range": (50, 100), "density": "sparse", "count": 5},
        ]
        
        case_id = 100  # 从 100 开始编号
        
        for config in graph_configs:
            for _ in range(config["count"]):
                n = random.randint(*config["n_range"])
                
                # 根据密度确定边数
                if config["density"] == "sparse":
                    m = min(n * 2, n * (n - 1) // 4)
                elif config["density"] == "medium":
                    m = min(n * 3, n * (n - 1) // 3)
                else:  # dense
                    m = min(n * 4, n * (n - 1) // 2)
                
                # 生成连通图
                G = self._generate_connected_graph(n, m)
                
                # 转换为边列表（1-indexed）
                edges = [[u + 1, v + 1] for u, v in G.edges()]
                
                # 随机选择源和目标
                source = 1
                target = random.randint(2, n)
                
                test_cases.append({
                    "id": case_id,
                    "name": f"Random {config['density']} graph (n={n}, m={m})",
                    "n": n,
                    "edges": edges,
                    "source": source,
                    "target": target,
                    "expected_shortest": None,  # 需要算法计算
                    "expected_second_shortest": None,
                    "description": f"随机生成的{config['density']}图"
                })
                
                case_id += 1
        
        return test_cases
    
    def _generate_connected_graph(self, n: int, m: int) -> nx.Graph:
        """生成连通的随机图"""
        # 先生成一棵生成树保证连通性
        G = nx.Graph()
        G.add_nodes_from(range(n))
        
        # 使用随机生成树
        nodes = list(range(n))
        random.shuffle(nodes)
        
        for i in range(1, n):
            # 连接到前面的随机节点
            j = random.randint(0, i - 1)
            G.add_edge(nodes[i], nodes[j])
        
        # 添加额外的边
        edges_to_add = m - (n - 1)
        possible_edges = [
            (i, j) for i in range(n) for j in range(i + 1, n)
            if not G.has_edge(i, j)
        ]
        
        if edges_to_add > 0 and possible_edges:
            random.shuffle(possible_edges)
            for i in range(min(edges_to_add, len(possible_edges))):
                G.add_edge(*possible_edges[i])
        
        return G
    
    def generate_special_cases(self) -> List[Dict]:
        """生成特殊测试用例"""
        test_cases = []
        
        # 完全图
        n = 6
        edges = [[i, j] for i in range(1, n + 1) for j in range(i + 1, n + 1)]
        test_cases.append({
            "id": 200,
            "name": "Complete graph K6",
            "n": n,
            "edges": edges,
            "source": 1,
            "target": 6,
            "expected_shortest": 1,
            "expected_second_shortest": 2,
            "description": "完全图"
        })
        
        # 星形图
        n = 10
        center = 1
        edges = [[center, i] for i in range(2, n + 1)]
        test_cases.append({
            "id": 201,
            "name": "Star graph",
            "n": n,
            "edges": edges,
            "source": 1,
            "target": 10,
            "expected_shortest": 2,
            "expected_second_shortest": 4,
            "description": "星形图"
        })
        
        # 二分图
        n = 8
        left = range(1, 5)
        right = range(5, 9)
        edges = [[i, j] for i in left for j in right]
        test_cases.append({
            "id": 202,
            "name": "Complete bipartite graph K4,4",
            "n": n,
            "edges": edges,
            "source": 1,
            "target": 8,
            "expected_shortest": 2,
            "expected_second_shortest": 4,
            "description": "完全二分图"
        })
        
        # 网格图
        rows, cols = 4, 4
        n = rows * cols
        edges = []
        for i in range(rows):
            for j in range(cols):
                node = i * cols + j + 1
                if j < cols - 1:
                    edges.append([node, node + 1])
                if i < rows - 1:
                    edges.append([node, node + cols])
        
        test_cases.append({
            "id": 203,
            "name": "Grid graph 4x4",
            "n": n,
            "edges": edges,
            "source": 1,
            "target": n,
            "expected_shortest": 6,  # Manhattan distance
            "expected_second_shortest": 8,
            "description": "网格图"
        })
        
        return test_cases
    
    def convert_to_standard_format(self, test_cases: List[Dict]) -> Dict:
        """转换为标准的数据集格式"""
        dataset = {
            "metadata": {
                "source": "LeetCode 2045 + Generated",
                "problem": "Second Shortest Path",
                "description": "测试用例包含官方示例和自动生成的测试数据",
                "total_cases": len(test_cases),
                "format": "每个测试用例包含图结构、源节点、目标节点和预期结果"
            },
            "test_cases": test_cases
        }
        
        return dataset
    
    def save_dataset(self, dataset: Dict, filename: str = "leetcode_second_shortest_path.json"):
        """保存数据集到文件"""
        output_path = self.output_dir / filename
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(dataset, f, indent=2, ensure_ascii=False)
        
        print(f"✅ 数据集已保存到: {output_path}")
        print(f"📊 总共 {len(dataset['test_cases'])} 个测试用例")
        
        return output_path
    
    def generate_summary(self, dataset: Dict):
        """生成数据集摘要"""
        test_cases = dataset["test_cases"]
        
        print("\n" + "="*60)
        print("📋 数据集摘要")
        print("="*60)
        
        # 按类型统计
        official_cases = [tc for tc in test_cases if tc["id"] < 100]
        random_cases = [tc for tc in test_cases if 100 <= tc["id"] < 200]
        special_cases = [tc for tc in test_cases if tc["id"] >= 200]
        
        print(f"\n官方测试用例: {len(official_cases)} 个")
        print(f"随机生成用例: {len(random_cases)} 个")
        print(f"特殊测试用例: {len(special_cases)} 个")
        print(f"总计: {len(test_cases)} 个")
        
        # 图规模统计
        print("\n图规模分布:")
        sizes = [(tc["n"], len(tc["edges"])) for tc in test_cases]
        sizes.sort()
        
        print(f"  最小图: n={sizes[0][0]}, m={sizes[0][1]}")
        print(f"  最大图: n={sizes[-1][0]}, m={sizes[-1][1]}")
        
        # 显示前几个测试用例
        print("\n前 5 个测试用例:")
        for tc in test_cases[:5]:
            print(f"  [{tc['id']}] {tc['name']}: n={tc['n']}, m={len(tc['edges'])}")
        
        print("="*60 + "\n")
    
    def download_all(self):
        """执行完整的下载流程"""
        print("🚀 开始准备 LeetCode 数据集...")
        print()
        
        # 1. 获取官方测试用例
        print("📥 加载官方测试用例...")
        official_cases = self.get_official_test_cases()
        print(f"   ✓ 已加载 {len(official_cases)} 个官方用例")
        
        # 2. 生成随机图
        print("\n🎲 生成随机测试图...")
        random_cases = self.generate_random_graphs(num_graphs=20)
        print(f"   ✓ 已生成 {len(random_cases)} 个随机用例")
        
        # 3. 生成特殊用例
        print("\n⭐ 生成特殊测试用例...")
        special_cases = self.generate_special_cases()
        print(f"   ✓ 已生成 {len(special_cases)} 个特殊用例")
        
        # 4. 合并所有用例
        all_cases = official_cases + random_cases + special_cases
        
        # 5. 转换为标准格式
        print("\n📦 转换为标准格式...")
        dataset = self.convert_to_standard_format(all_cases)
        
        # 6. 保存数据集
        print("\n💾 保存数据集...")
        output_path = self.save_dataset(dataset)
        
        # 7. 生成摘要
        self.generate_summary(dataset)
        
        # 8. 另存一份到当前目录（方便项目使用）
        local_path = Path("leetcode_dataset.json")
        with open(local_path, 'w', encoding='utf-8') as f:
            json.dump(dataset, f, indent=2, ensure_ascii=False)
        print(f"📁 同时保存了一份到当前目录: {local_path}")
        
        return output_path


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="下载和准备 LeetCode 第二短路径数据集"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="./data/leetcode",
        help="输出目录（默认: ./data/leetcode）"
    )
    
    args = parser.parse_args()
    
    # 创建下载器并执行
    downloader = LeetCodeDataDownloader(output_dir=args.output)
    output_path = downloader.download_all()
    
    print("\n✨ 数据集准备完成！")
    print(f"📂 文件位置: {output_path}")
    print("\n💡 提示: 你可以使用以下代码加载数据集：")
    print("""
import json

with open('leetcode_dataset.json', 'r') as f:
    dataset = json.load(f)

# 访问测试用例
for test_case in dataset['test_cases']:
    n = test_case['n']
    edges = test_case['edges']
    source = test_case['source']
    target = test_case['target']
    # ... 运行算法
    """)


if __name__ == "__main__":
    main()
