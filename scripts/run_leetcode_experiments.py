#!/usr/bin/env python3
"""
在LeetCode数据上运行算法实验

验证算法的正确性，测试性能，并生成详细的实验报告和可视化。
"""

import argparse
import json
import logging
import sys
import time
from pathlib import Path

import pandas as pd

# src布局路径修正
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from second_shortest_path.algorithms import StateExtendedSPFA, TwoDistanceDijkstra
from second_shortest_path.evaluation import Visualizer

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def convert_leetcode_case_to_graph(test_case: dict) -> tuple:
    """将LeetCode测试用例转换为图表示
    
    Args:
        test_case: LeetCode测试用例
    
    Returns:
        (graph, source, target) 三元组
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


def run_leetcode_experiments(
    data_file: str,
    output_dir: str = 'results/leetcode_experiments'
) -> None:
    """在LeetCode数据上运行完整实验
    
    Args:
        data_file: LeetCode数据文件路径
        output_dir: 输出目录
    """
    output_path = Path(output_dir)
    metrics_dir = output_path / "metrics"
    viz_dir = output_path / "visualizations"
    
    metrics_dir.mkdir(parents=True, exist_ok=True)
    viz_dir.mkdir(parents=True, exist_ok=True)
    
    logger.info("=" * 70)
    logger.info("LeetCode 算法性能实验")
    logger.info("=" * 70)
    
    # 加载数据
    logger.info(f"📥 加载数据: {data_file}")
    with open(data_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    test_cases = data['test_cases']
    total_cases = len(test_cases)
    
    logger.info(f"✅ 加载了 {total_cases} 个测试用例\n")
    
    # 初始化统计
    results = []
    official_cases = []  # 有预期结果的用例
    generated_cases = []  # 无预期结果的用例
    
    # 运行实验
    logger.info("🚀 开始运行实验...\n")
    
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
        
        # 记录用例类型
        has_expected = expected_shortest is not None and expected_second is not None
        
        # 测试 Two-Distance Dijkstra
        dijkstra = TwoDistanceDijkstra(graph)
        start_time = time.perf_counter()
        d_shortest, d_second = dijkstra.find_second_shortest(source, target)
        d_time = time.perf_counter() - start_time
        d_stats = dijkstra.get_statistics()
        
        # 测试 State-Extended SPFA
        spfa = StateExtendedSPFA(graph)
        start_time = time.perf_counter()
        s_shortest, s_second = spfa.find_second_shortest(source, target)
        s_time = time.perf_counter() - start_time
        s_stats = spfa.get_statistics()
        
        # 验证结果（如果有预期）
        dijkstra_correct = None
        spfa_correct = None
        
        if has_expected:
            dijkstra_correct = (d_shortest == expected_shortest and 
                               d_second == expected_second)
            spfa_correct = (s_shortest == expected_shortest and 
                           s_second == expected_second)
            
            d_status = "✅" if dijkstra_correct else "❌"
            s_status = "✅" if spfa_correct else "❌"
            
            logger.info(f"  Dijkstra: {d_status} 最短={d_shortest}, 次短={d_second} "
                       f"(耗时: {d_time*1000:.2f}ms)")
            logger.info(f"  SPFA:     {s_status} 最短={s_shortest}, 次短={s_second} "
                       f"(耗时: {s_time*1000:.2f}ms)")
            
            official_cases.append({
                'case_id': case_id,
                'name': name,
                'dijkstra_correct': dijkstra_correct,
                'spfa_correct': spfa_correct,
            })
        else:
            logger.info(f"  Dijkstra: 最短={d_shortest}, 次短={d_second} "
                       f"(耗时: {d_time*1000:.2f}ms)")
            logger.info(f"  SPFA:     最短={s_shortest}, 次短={s_second} "
                       f"(耗时: {s_time*1000:.2f}ms)")
            
            generated_cases.append({
                'case_id': case_id,
                'name': name,
            })
        
        # 记录结果
        results.append({
            'case_id': case_id,
            'name': name,
            'n': n,
            'm': len(edges),
            'has_expected': has_expected,
            'dijkstra_time': d_time,
            'dijkstra_shortest': d_shortest,
            'dijkstra_second': d_second,
            'dijkstra_correct': dijkstra_correct,
            'dijkstra_pq_ops': d_stats.get('pq_operations', 0),
            'dijkstra_edge_relax': d_stats.get('edge_relaxations', 0),
            'spfa_time': s_time,
            'spfa_shortest': s_shortest,
            'spfa_second': s_second,
            'spfa_correct': spfa_correct,
            'spfa_queue_ops': s_stats.get('enqueue_operations', 0),
            'spfa_edge_relax': s_stats.get('edge_relaxations', 0),
        })
        
        logger.info("")
    
    # 生成总结
    logger.info("=" * 70)
    logger.info("实验总结")
    logger.info("=" * 70)
    
    df = pd.DataFrame(results)
    
    # 转换为长格式（长表格式）以兼容可视化函数
    # 创建两个算法的结果列表
    viz_results = []
    
    for _, row in df.iterrows():
        # Dijkstra 结果
        viz_results.append({
            'case_id': row['case_id'],
            'name': row['name'],
            'n': row['n'],
            'm': row['m'],
            'algorithm': 'Dijkstra',
            'time': row['dijkstra_time'],
            'shortest': row['dijkstra_shortest'],
            'second': row['dijkstra_second'],
            'correct': row['dijkstra_correct'],
            'operations': row['dijkstra_pq_ops'],
        })
        
        # SPFA 结果
        viz_results.append({
            'case_id': row['case_id'],
            'name': row['name'],
            'n': row['n'],
            'm': row['m'],
            'algorithm': 'SPFA',
            'time': row['spfa_time'],
            'shortest': row['spfa_shortest'],
            'second': row['spfa_second'],
            'correct': row['spfa_correct'],
            'operations': row['spfa_queue_ops'],
        })
    
    viz_df = pd.DataFrame(viz_results)
    
    # 官方用例统计
    official_correct = [r for r in results if r['has_expected'] and r['dijkstra_correct']]
    official_total = len([r for r in results if r['has_expected']])
    
    logger.info(f"\n📊 官方测试用例:")
    logger.info(f"  总数: {official_total}")
    logger.info(f"  Dijkstra 通过: {sum(1 for r in results if r['has_expected'] and r['dijkstra_correct'])}/{official_total}")
    logger.info(f"  SPFA 通过: {sum(1 for r in results if r['has_expected'] and r['spfa_correct'])}/{official_total}")
    
    if official_total > 0:
        logger.info(f"  Dijkstra 正确率: {sum(1 for r in results if r['has_expected'] and r['dijkstra_correct'])/official_total*100:.1f}%")
        logger.info(f"  SPFA 正确率: {sum(1 for r in results if r['has_expected'] and r['spfa_correct'])/official_total*100:.1f}%")
    
    # 性能统计
    logger.info(f"\n⚡ 性能对比:")
    dijkstra_avg_time = df['dijkstra_time'].mean()
    spfa_avg_time = df['spfa_time'].mean()
    
    logger.info(f"  Dijkstra 平均耗时: {dijkstra_avg_time*1000:.2f}ms")
    logger.info(f"  SPFA 平均耗时: {spfa_avg_time*1000:.2f}ms")
    
    if dijkstra_avg_time > 0 and spfa_avg_time > 0:
        speedup = dijkstra_avg_time / spfa_avg_time
        faster = "Dijkstra" if speedup > 1 else "SPFA"
        logger.info(f"  {faster} 快 {abs(speedup - 1)*100:.1f}%")
    
    # 操作统计
    dijkstra_avg_ops = df['dijkstra_pq_ops'].mean()
    spfa_avg_ops = df['spfa_queue_ops'].mean()
    
    logger.info(f"\n📈 操作统计:")
    logger.info(f"  Dijkstra 平均PQ操作数: {dijkstra_avg_ops:.0f}")
    logger.info(f"  SPFA 平均队列操作数: {spfa_avg_ops:.0f}")
    
    logger.info("=" * 70)
    
    # 保存详细报告
    logger.info("\n💾 保存报告...\n")
    
    # JSON 报告
    report = {
        'metadata': {
            'total_cases': total_cases,
            'official_cases': official_total,
            'generated_cases': len(generated_cases),
        },
        'summary': {
            'dijkstra': {
                'avg_time': float(dijkstra_avg_time),
                'correct_count': sum(1 for r in results if r['has_expected'] and r['dijkstra_correct']),
                'total': official_total,
                'accuracy': sum(1 for r in results if r['has_expected'] and r['dijkstra_correct']) / official_total if official_total > 0 else 0,
                'avg_pq_ops': float(dijkstra_avg_ops),
                'avg_edge_relax': float(df['dijkstra_edge_relax'].mean()),
            },
            'spfa': {
                'avg_time': float(spfa_avg_time),
                'correct_count': sum(1 for r in results if r['has_expected'] and r['spfa_correct']),
                'total': official_total,
                'accuracy': sum(1 for r in results if r['has_expected'] and r['spfa_correct']) / official_total if official_total > 0 else 0,
                'avg_queue_ops': float(spfa_avg_ops),
                'avg_edge_relax': float(df['spfa_edge_relax'].mean()),
            },
        },
        'details': results,
    }
    
    report_path = metrics_dir / "leetcode_report.json"
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    logger.info(f"✅ JSON 报告: {report_path}")
    
    # CSV 报告
    csv_path = metrics_dir / "leetcode_results.csv"
    df.to_csv(csv_path, index=False)
    logger.info(f"✅ CSV 报告: {csv_path}")
    
    # 生成可视化
    logger.info("\n🎨 生成可视化图表...\n")
    
    try:
        Visualizer.plot_runtime_comparison(viz_df, viz_dir / "runtime_comparison.png")
        logger.info("✅ 运行时间对比图")
    except Exception as e:
        logger.warning(f"⚠️  运行时间对比图生成失败: {e}")
    
    try:
        Visualizer.plot_scalability(viz_df, viz_dir / "scalability.png")
        logger.info("✅ 可扩展性分析图")
    except Exception as e:
        logger.warning(f"⚠️  可扩展性分析图生成失败: {e}")
    
    try:
        Visualizer.plot_percentile_comparison(viz_df, viz_dir / "percentile_comparison.png")
        logger.info("✅ 百分位数对比图")
    except Exception as e:
        logger.warning(f"⚠️  百分位数对比图生成失败: {e}")
    
    logger.info("\n" + "=" * 70)
    logger.info("✅ 实验完成！")
    logger.info(f"📁 结果保存在: {output_path}")
    logger.info("=" * 70)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='在LeetCode数据上运行算法实验'
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
        default='results/leetcode_experiments',
        help='输出目录'
    )
    
    args = parser.parse_args()
    
    data_path = Path(args.data)
    if not data_path.exists():
        logger.error(f"❌ 数据文件不存在: {data_path}")
        sys.exit(1)
    
    try:
        run_leetcode_experiments(str(data_path), args.output)
    except Exception as e:
        logger.error(f"❌ 实验运行失败: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
