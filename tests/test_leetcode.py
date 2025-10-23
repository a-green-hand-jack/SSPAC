#!/usr/bin/env python3
"""
在LeetCode数据上测试两种算法

验证算法的正确性，并生成详细的测试报告。
"""

import json
import logging
import sys
import time
from pathlib import Path

# src布局路径修正
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from second_shortest_path.algorithms import StateExtendedSPFA, TwoDistanceDijkstra
from second_shortest_path.data import DataLoader

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def convert_leetcode_case_to_graph(test_case: dict) -> dict:
    """将LeetCode测试用例转换为图表示
    
    Args:
        test_case: LeetCode测试用例
    
    Returns:
        图的邻接表表示
    """
    n = test_case['n']
    edges = test_case['edges']
    source = test_case['source']
    target = test_case['target']
    
    # 构建邻接表（无向图，边权重为1）
    graph = {i: [] for i in range(n + 1)}  # LeetCode使用1-indexed
    
    for u, v in edges:
        graph[u].append((v, 1))
        graph[v].append((u, 1))
    
    return graph, source, target


def test_on_leetcode_data(data_file: str, output_file: str = None) -> None:
    """在LeetCode数据上运行测试
    
    Args:
        data_file: LeetCode数据文件路径
        output_file: 输出报告文件路径
    """
    logger.info("=" * 70)
    logger.info("LeetCode数据集测试")
    logger.info("=" * 70)
    
    # 加载数据
    with open(data_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    test_cases = data['test_cases']
    total_cases = len(test_cases)
    
    logger.info(f"📊 加载了 {total_cases} 个测试用例\n")
    
    # 初始化统计
    dijkstra_stats = {
        'total_time': 0,
        'correct': 0,
        'incorrect': 0,
        'errors': 0,
        'details': [],
    }
    
    spfa_stats = {
        'total_time': 0,
        'correct': 0,
        'incorrect': 0,
        'errors': 0,
        'details': [],
    }
    
    # 运行测试
    for idx, test_case in enumerate(test_cases, 1):
        case_id = test_case.get('id', idx)
        name = test_case.get('name', f'Test {case_id}')
        n = test_case['n']
        edges = test_case['edges']
        expected_shortest = test_case.get('expected_shortest')
        expected_second = test_case.get('expected_second_shortest')
        
        logger.info(f"[{idx}/{total_cases}] {name} (n={n}, m={len(edges)})")
        
        # 转换图
        graph, source, target = convert_leetcode_case_to_graph(test_case)
        
        # 如果没有预期结果，跳过验证
        if expected_shortest is None or expected_second is None:
            logger.info(f"  ⚠️  无预期结果，仅记录运行结果")
            
            try:
                dijkstra = TwoDistanceDijkstra(graph)
                start_time = time.perf_counter()
                d_shortest, d_second = dijkstra.find_second_shortest(source, target)
                elapsed_time = time.perf_counter() - start_time
                dijkstra_stats['total_time'] += elapsed_time
                logger.info(f"  Dijkstra: 最短={d_shortest}, 次短={d_second} (耗时: {elapsed_time*1000:.2f}ms)")
            except Exception as e:
                logger.error(f"  Dijkstra: ERROR - {e}")
            
            try:
                spfa = StateExtendedSPFA(graph)
                start_time = time.perf_counter()
                s_shortest, s_second = spfa.find_second_shortest(source, target)
                elapsed_time = time.perf_counter() - start_time
                spfa_stats['total_time'] += elapsed_time
                logger.info(f"  SPFA: 最短={s_shortest}, 次短={s_second} (耗时: {elapsed_time*1000:.2f}ms)")
            except Exception as e:
                logger.error(f"  SPFA: ERROR - {e}")
            
            logger.info("")
            continue
        
        # 测试 Two-Distance Dijkstra
        try:
            dijkstra = TwoDistanceDijkstra(graph)
            start_time = time.perf_counter()
            d_shortest, d_second = dijkstra.find_second_shortest(source, target)
            elapsed_time = time.perf_counter() - start_time
            
            dijkstra_stats['total_time'] += elapsed_time
            
            # 验证结果
            d_correct = (d_shortest == expected_shortest and 
                        d_second == expected_second)
            
            if d_correct:
                dijkstra_stats['correct'] += 1
                status = "✅ PASS"
            else:
                dijkstra_stats['incorrect'] += 1
                status = "❌ FAIL"
            
            dijkstra_stats['details'].append({
                'case_id': case_id,
                'name': name,
                'status': status,
                'expected': (expected_shortest, expected_second),
                'actual': (d_shortest, d_second),
                'time': elapsed_time,
            })
            
            logger.info(f"  Dijkstra: {status} - 最短={d_shortest}, 次短={d_second} "
                       f"(耗时: {elapsed_time*1000:.2f}ms)")
        
        except Exception as e:
            dijkstra_stats['errors'] += 1
            logger.error(f"  Dijkstra: ❌ ERROR - {e}")
        
        # 测试 State-Extended SPFA
        try:
            spfa = StateExtendedSPFA(graph)
            start_time = time.perf_counter()
            s_shortest, s_second = spfa.find_second_shortest(source, target)
            elapsed_time = time.perf_counter() - start_time
            
            spfa_stats['total_time'] += elapsed_time
            
            # 验证结果
            s_correct = (s_shortest == expected_shortest and 
                        s_second == expected_second)
            
            if s_correct:
                spfa_stats['correct'] += 1
                status = "✅ PASS"
            else:
                spfa_stats['incorrect'] += 1
                status = "❌ FAIL"
            
            spfa_stats['details'].append({
                'case_id': case_id,
                'name': name,
                'status': status,
                'expected': (expected_shortest, expected_second),
                'actual': (s_shortest, s_second),
                'time': elapsed_time,
            })
            
            logger.info(f"  SPFA:     {status} - 最短={s_shortest}, 次短={s_second} "
                       f"(耗时: {elapsed_time*1000:.2f}ms)")
        
        except Exception as e:
            spfa_stats['errors'] += 1
            logger.error(f"  SPFA:     ❌ ERROR - {e}")
        
        logger.info("")
    
    # 生成总结
    logger.info("=" * 70)
    logger.info("测试总结")
    logger.info("=" * 70)
    
    logger.info("\n📈 Two-Distance Dijkstra:")
    logger.info(f"  总耗时: {dijkstra_stats['total_time']:.3f}s")
    logger.info(f"  通过: {dijkstra_stats['correct']}/{total_cases}")
    logger.info(f"  失败: {dijkstra_stats['incorrect']}/{total_cases}")
    logger.info(f"  错误: {dijkstra_stats['errors']}/{total_cases}")
    logger.info(f"  正确率: {dijkstra_stats['correct']/total_cases*100:.1f}%")
    logger.info(f"  平均耗时: {dijkstra_stats['total_time']/total_cases*1000:.2f}ms/case")
    
    logger.info("\n📈 State-Extended SPFA:")
    logger.info(f"  总耗时: {spfa_stats['total_time']:.3f}s")
    logger.info(f"  通过: {spfa_stats['correct']}/{total_cases}")
    logger.info(f"  失败: {spfa_stats['incorrect']}/{total_cases}")
    logger.info(f"  错误: {spfa_stats['errors']}/{total_cases}")
    logger.info(f"  正确率: {spfa_stats['correct']/total_cases*100:.1f}%")
    logger.info(f"  平均耗时: {spfa_stats['total_time']/total_cases*1000:.2f}ms/case")
    
    # 性能对比
    if dijkstra_stats['total_time'] > 0 and spfa_stats['total_time'] > 0:
        speedup = dijkstra_stats['total_time'] / spfa_stats['total_time']
        faster = "Dijkstra" if speedup > 1 else "SPFA"
        logger.info(f"\n⚡ 性能对比:")
        logger.info(f"  {faster} 快 {abs(speedup - 1)*100:.1f}%")
    
    logger.info("=" * 70)
    
    # 保存详细报告
    if output_file:
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        report = {
            'summary': {
                'total_cases': total_cases,
                'dijkstra': {
                    'correct': dijkstra_stats['correct'],
                    'incorrect': dijkstra_stats['incorrect'],
                    'errors': dijkstra_stats['errors'],
                    'total_time': dijkstra_stats['total_time'],
                    'accuracy': dijkstra_stats['correct'] / total_cases,
                },
                'spfa': {
                    'correct': spfa_stats['correct'],
                    'incorrect': spfa_stats['incorrect'],
                    'errors': spfa_stats['errors'],
                    'total_time': spfa_stats['total_time'],
                    'accuracy': spfa_stats['correct'] / total_cases,
                },
            },
            'dijkstra_details': dijkstra_stats['details'],
            'spfa_details': spfa_stats['details'],
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        logger.info(f"\n📄 详细报告已保存到: {output_path}")


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='在LeetCode数据上测试两种算法'
    )
    parser.add_argument(
        '--data',
        type=str,
        default='data/leetcode/leetcode_second_shortest_path.json',
        help='LeetCode数据文件路径'
    )
    parser.add_argument(
        '--output',
        type=str,
        default='results/leetcode_test_report.json',
        help='输出报告文件路径'
    )
    
    args = parser.parse_args()
    
    data_path = Path(args.data)
    if not data_path.exists():
        logger.error(f"❌ 数据文件不存在: {data_path}")
        sys.exit(1)
    
    try:
        test_on_leetcode_data(str(data_path), args.output)
        logger.info("\n✅ 测试完成！")
    except Exception as e:
        logger.error(f"❌ 测试失败: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
