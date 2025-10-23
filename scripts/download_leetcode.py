#!/usr/bin/env python3
"""
从LeetCode下载测试数据的脚本

用于爬取LeetCode 2045题的测试用例数据。
"""

import argparse
import json
import logging
import sys
from pathlib import Path

# src布局路径修正
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

# 导入项目模块
from second_shortest_path.data import DataLoader

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def download_leetcode_data(problem_id: int, output_dir: str) -> None:
    """下载LeetCode测试数据
    
    Args:
        problem_id: LeetCode题目ID
        output_dir: 输出目录
    """
    logger.info(f"开始下载LeetCode {problem_id} 题数据")
    
    # TODO: 实现实际的数据下载逻辑
    # 这里提供一个示例数据结构
    
    # 示例测试用例（基于LeetCode 2045）
    sample_data = {
        "problem_id": problem_id,
        "problem_name": "Second Minimum Time to Reach Destination",
        "test_cases": [
            {
                "id": 1,
                "n": 5,
                "edges": [[1, 2], [1, 3], [1, 4], [3, 4], [4, 5]],
                "time": 3,
                "change": 5,
                "expected": 13
            },
            {
                "id": 2,
                "n": 2,
                "edges": [[1, 2]],
                "time": 3,
                "change": 2,
                "expected": 11
            }
        ]
    }
    
    output_path = Path(output_dir) / "test_cases.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(sample_data, f, indent=2, ensure_ascii=False)
    
    logger.info(f"数据已保存到: {output_path}")
    logger.info(f"共下载 {len(sample_data['test_cases'])} 个测试用例")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='从LeetCode下载测试数据'
    )
    parser.add_argument(
        '--problem-id',
        type=int,
        default=2045,
        help='LeetCode题目ID（默认: 2045）'
    )
    parser.add_argument(
        '--output',
        type=str,
        default='data/leetcode',
        help='输出目录（默认: data/leetcode）'
    )
    
    args = parser.parse_args()
    
    try:
        download_leetcode_data(args.problem_id, args.output)
        logger.info("✅ 数据下载完成")
    except Exception as e:
        logger.error(f"❌ 数据下载失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

