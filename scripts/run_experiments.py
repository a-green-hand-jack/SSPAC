#!/usr/bin/env python3
"""
运行完整实验流程的脚本

执行算法基准测试，生成性能指标和可视化图表。
"""

import argparse
import logging
import sys
from pathlib import Path

# src布局路径修正
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

# 导入项目模块
from second_shortest_path.algorithms import StateExtendedSPFA, TwoDistanceDijkstra
from second_shortest_path.data import GraphGenerator
from second_shortest_path.evaluation import PerformanceMetrics, Visualizer

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def run_experiments(
    graph_sizes: list[int],
    density: float,
    output_dir: str
) -> None:
    """运行完整实验
    
    Args:
        graph_sizes: 测试的图规模列表
        density: 图的密度
        output_dir: 结果输出目录
    """
    output_path = Path(output_dir)
    metrics_dir = output_path / "metrics"
    viz_dir = output_path / "visualizations"
    
    metrics_dir.mkdir(parents=True, exist_ok=True)
    viz_dir.mkdir(parents=True, exist_ok=True)
    
    logger.info("=" * 60)
    logger.info("开始运行实验")
    logger.info("=" * 60)
    
    # 1. 生成测试数据
    logger.info(f"📊 生成测试数据: 规模={graph_sizes}, 密度={density}")
    test_suite = GraphGenerator.generate_test_suite(graph_sizes, density)
    
    # 添加特殊测试用例
    special_cases = GraphGenerator.generate_special_cases()
    test_suite.extend(special_cases)
    
    logger.info(f"✅ 生成 {len(test_suite)} 个测试图")
    
    # 2. 初始化算法（注意：需要为每个测试单独创建实例）
    logger.info("🔧 初始化算法")
    algorithm_classes = [TwoDistanceDijkstra, StateExtendedSPFA]
    
    # 3. 运行基准测试
    logger.info("🚀 开始基准测试")
    metrics = PerformanceMetrics()
    
    # 为每个测试用例创建新的算法实例
    results_list = []
    for graph_data in test_suite:
        graph = graph_data['graph']
        source = graph_data.get('source', 0)
        target = graph_data.get('target', graph_data['n'] - 1)
        
        for AlgoClass in algorithm_classes:
            algo = AlgoClass(graph)
            result = metrics.run_single_test(algo, graph, source, target)
            result['test_name'] = graph_data.get('test_name', 'unknown')
            result['graph_type'] = graph_data.get('graph_type', 'random')
            results_list.append(result)
    
    # 转换为DataFrame
    import pandas as pd
    results_df = pd.DataFrame(results_list)
    
    logger.info("✅ 基准测试完成")
    
    # 4. 计算统计数据
    logger.info("📈 计算统计数据")
    stats = metrics.calculate_statistics(results_df)
    
    for algo, algo_stats in stats.items():
        logger.info(f"\n{algo}:")
        logger.info(f"  平均时间: {algo_stats['time_mean']:.6f}s")
        logger.info(f"  中位数: {algo_stats['time_median']:.6f}s")
        logger.info(f"  P95: {algo_stats['time_p95']:.6f}s")
    
    # 5. 导出结果
    logger.info("💾 导出结果数据")
    metrics.export_results(metrics_dir / "benchmark_results.csv")
    
    # 6. 生成可视化
    logger.info("🎨 生成可视化图表")
    
    Visualizer.plot_runtime_comparison(
        results_df,
        viz_dir / "runtime_comparison.png"
    )
    logger.info("  ✅ 运行时间对比图")
    
    Visualizer.plot_scalability(
        results_df,
        viz_dir / "scalability.png"
    )
    logger.info("  ✅ 可扩展性分析图")
    
    Visualizer.plot_complexity_verification(
        results_df,
        viz_dir / "complexity_verification.png"
    )
    logger.info("  ✅ 复杂度验证图")
    
    Visualizer.plot_operations_comparison(
        results_df,
        viz_dir / "operations_comparison.png"
    )
    logger.info("  ✅ 操作次数对比图")
    
    Visualizer.plot_percentile_comparison(
        results_df,
        viz_dir / "percentile_comparison.png"
    )
    logger.info("  ✅ 百分位数对比图")
    
    Visualizer.plot_heatmap(
        results_df,
        viz_dir / "performance_heatmap.png"
    )
    logger.info("  ✅ 性能热力图")
    
    logger.info("=" * 60)
    logger.info("✅ 实验完成！")
    logger.info(f"📁 结果保存在: {output_path}")
    logger.info("=" * 60)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='运行第二短路径算法对比实验'
    )
    parser.add_argument(
        '--sizes',
        type=int,
        nargs='+',
        default=[10, 50, 100, 500],
        help='测试的图规模列表（默认: 10 50 100 500）'
    )
    parser.add_argument(
        '--density',
        type=float,
        default=0.3,
        help='图的密度（默认: 0.3）'
    )
    parser.add_argument(
        '--output',
        type=str,
        default='results',
        help='结果输出目录（默认: results）'
    )
    parser.add_argument(
        '--all',
        action='store_true',
        help='运行所有预设实验'
    )
    
    args = parser.parse_args()
    
    if args.all:
        # 运行完整的实验套件
        graph_sizes = [10, 50, 100, 500, 1000]
    else:
        graph_sizes = args.sizes
    
    try:
        run_experiments(graph_sizes, arg s.density, args.output)
    except Exception as e:
        logger.error(f"❌ 实验运行失败: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()

