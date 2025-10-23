"""
性能指标计算与分析

提供算法性能测试、统计分析和复杂度验证功能。
"""

import logging
import time
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from tqdm import tqdm

logger = logging.getLogger(__name__)


class PerformanceMetrics:
    """性能指标计算与统计
    
    运行算法基准测试，收集性能指标，并提供统计分析功能。
    
    Examples:
        >>> metrics = PerformanceMetrics()
        >>> result = metrics.run_single_test(algorithm, graph, source, target)
        >>> df = metrics.run_benchmark([algo1, algo2], test_suite)
    """
    
    def __init__(self):
        """初始化性能指标收集器"""
        self.results = []
        logger.debug("初始化 PerformanceMetrics")
    
    def run_single_test(
        self,
        algorithm: Any,
        graph: dict[int, list[tuple[int, int]]],
        source: int,
        target: int
    ) -> dict[str, Any]:
        """运行单个测试
        
        Args:
            algorithm: 算法实例（需要有find_second_shortest和get_statistics方法）
            graph: 图的邻接表表示
            source: 源节点
            target: 目标节点
        
        Returns:
            包含性能指标的字典：
            {
                'algorithm': 算法名称,
                'n': 节点数,
                'm': 边数,
                'time': 运行时间(秒),
                'result': (shortest, second_shortest),
                'statistics': 算法统计信息,
            }
        """
        algo_name = algorithm.__class__.__name__
        n = len(graph)
        m = sum(len(neighbors) for neighbors in graph.values()) // 2
        
        logger.debug(f"运行测试: {algo_name}, n={n}, m={m}")
        
        # 测量运行时间
        start_time = time.perf_counter()
        result = algorithm.find_second_shortest(source, target)
        end_time = time.perf_counter()
        
        elapsed_time = end_time - start_time
        
        # 获取算法统计信息
        stats = algorithm.get_statistics()
        
        test_result = {
            'algorithm': algo_name,
            'n': n,
            'm': m,
            'source': source,
            'target': target,
            'time': elapsed_time,
            'shortest': result[0],
            'second_shortest': result[1],
            **stats,
        }
        
        self.results.append(test_result)
        
        return test_result
    
    def run_benchmark(
        self,
        algorithms: list[Any],
        test_suite: list[dict[str, Any]],
        show_progress: bool = True
    ) -> pd.DataFrame:
        """运行完整基准测试
        
        Args:
            algorithms: 算法实例列表
            test_suite: 测试图数据列表
            show_progress: 是否显示进度条
        
        Returns:
            包含所有测试结果的DataFrame
        """
        logger.info(
            f"开始基准测试: {len(algorithms)} 个算法, "
            f"{len(test_suite)} 个测试用例"
        )
        
        self.results = []
        total_tests = len(algorithms) * len(test_suite)
        
        if show_progress:
            pbar = tqdm(total=total_tests, desc="运行基准测试")
        
        for graph_data in test_suite:
            graph = graph_data['graph']
            source = graph_data.get('source', 0)
            target = graph_data.get('target', graph_data['n'] - 1)
            test_name = graph_data.get('test_name', 'unknown')
            
            for algorithm in algorithms:
                try:
                    result = self.run_single_test(algorithm, graph, source, target)
                    result['test_name'] = test_name
                    result['graph_type'] = graph_data.get('graph_type', 'unknown')
                    
                    # 如果有期望结果，进行验证
                    if 'expected' in graph_data:
                        expected = graph_data['expected']
                        actual = result['second_shortest']
                        result['correct'] = (actual == expected)
                        if actual != expected:
                            logger.warning(
                                f"结果不匹配: {test_name}, "
                                f"期望={expected}, 实际={actual}"
                            )
                    
                except Exception as e:
                    logger.error(
                        f"测试失败: {algorithm.__class__.__name__}, "
                        f"{test_name}, 错误: {e}"
                    )
                
                if show_progress:
                    pbar.update(1)
        
        if show_progress:
            pbar.close()
        
        df = pd.DataFrame(self.results)
        logger.info(f"基准测试完成，共 {len(self.results)} 个结果")
        
        return df
    
    def calculate_statistics(self, df: pd.DataFrame) -> dict[str, Any]:
        """计算统计数据
        
        Args:
            df: 测试结果DataFrame
        
        Returns:
            包含统计信息的字典：
            - mean: 平均值
            - median: 中位数
            - p95: 95百分位数
            - p99: 99百分位数
            - std: 标准差
        """
        stats = {}
        
        for algo in df['algorithm'].unique():
            algo_df = df[df['algorithm'] == algo]
            
            stats[algo] = {
                'time_mean': algo_df['time'].mean(),
                'time_median': algo_df['time'].median(),
                'time_p95': algo_df['time'].quantile(0.95),
                'time_p99': algo_df['time'].quantile(0.99),
                'time_std': algo_df['time'].std(),
            }
            
            # 如果有操作次数统计
            if 'pq_operations' in algo_df.columns:
                stats[algo]['pq_operations_mean'] = algo_df['pq_operations'].mean()
            if 'enqueue_operations' in algo_df.columns:
                stats[algo]['queue_operations_mean'] = (
                    algo_df['enqueue_operations'].mean()
                )
            if 'edge_relaxations' in algo_df.columns:
                stats[algo]['edge_relaxations_mean'] = (
                    algo_df['edge_relaxations'].mean()
                )
        
        logger.info("统计数据计算完成")
        
        return stats
    
    def export_results(self, filepath: str | Path) -> None:
        """导出结果到CSV
        
        Args:
            filepath: 输出CSV文件路径
        """
        filepath = Path(filepath)
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        df = pd.DataFrame(self.results)
        df.to_csv(filepath, index=False)
        
        logger.info(f"结果已导出到: {filepath}")


class ComplexityAnalyzer:
    """时间复杂度验证
    
    通过拟合实验数据来验证算法的实际时间复杂度。
    
    Examples:
        >>> analyzer = ComplexityAnalyzer()
        >>> complexity = analyzer.empirical_complexity(algorithm, [10, 50, 100, 500])
    """
    
    def empirical_complexity(
        self,
        algorithm: Any,
        graph_sizes: list[int],
        density: float = 0.3,
        num_trials: int = 5
    ) -> dict[str, Any]:
        """经验复杂度分析
        
        通过在不同规模的图上运行算法，拟合时间复杂度。
        
        Args:
            algorithm: 算法实例
            graph_sizes: 测试的图规模列表
            density: 图的密度
            num_trials: 每个规模重复测试的次数
        
        Returns:
            包含拟合结果的字典
        """
        from second_shortest_path.data.generator import GraphGenerator
        
        logger.info(f"开始经验复杂度分析: {graph_sizes}")
        
        data_points = []
        
        for n in tqdm(graph_sizes, desc="经验复杂度分析"):
            max_edges = n * (n - 1) // 2
            m = int(max_edges * density)
            m = max(m, n - 1)
            
            times = []
            for _ in range(num_trials):
                graph_data = GraphGenerator.generate_random_graph(n, m)
                graph = graph_data['graph']
                source = graph_data['source']
                target = graph_data['target']
                
                start_time = time.perf_counter()
                algorithm.find_second_shortest(source, target)
                end_time = time.perf_counter()
                
                times.append(end_time - start_time)
            
            avg_time = np.mean(times)
            data_points.append({
                'n': n,
                'm': m,
                'time': avg_time,
            })
        
        # 尝试拟合 O(M log N) 和 O(MN)
        df = pd.DataFrame(data_points)
        
        # 计算理论值
        df['m_log_n'] = df['m'] * np.log(df['n'])
        df['m_n'] = df['m'] * df['n']
        
        # 线性拟合
        from scipy import stats
        
        # 拟合 O(M log N)
        slope1, intercept1, r_value1, _, _ = stats.linregress(
            df['m_log_n'], df['time']
        )
        
        # 拟合 O(MN)
        slope2, intercept2, r_value2, _, _ = stats.linregress(
            df['m_n'], df['time']
        )
        
        result = {
            'data_points': data_points,
            'o_m_log_n': {
                'slope': slope1,
                'intercept': intercept1,
                'r_squared': r_value1 ** 2,
            },
            'o_m_n': {
                'slope': slope2,
                'intercept': intercept2,
                'r_squared': r_value2 ** 2,
            },
        }
        
        # 判断更符合哪个复杂度
        if r_value1 ** 2 > r_value2 ** 2:
            result['best_fit'] = 'O(M log N)'
        else:
            result['best_fit'] = 'O(MN)'
        
        logger.info(
            f"复杂度分析完成: {result['best_fit']}, "
            f"R²={max(r_value1**2, r_value2**2):.4f}"
        )
        
        return result
    
    def compare_theoretical_vs_empirical(
        self,
        df: pd.DataFrame
    ) -> pd.DataFrame:
        """对比理论与实际复杂度
        
        Args:
            df: 包含测试结果的DataFrame
        
        Returns:
            包含对比结果的DataFrame
        """
        comparison = []
        
        for algo in df['algorithm'].unique():
            algo_df = df[df['algorithm'] == algo]
            
            # 计算理论操作次数
            algo_df = algo_df.copy()
            algo_df['theoretical_m_log_n'] = algo_df['m'] * np.log(algo_df['n'])
            algo_df['theoretical_m_n'] = algo_df['m'] * algo_df['n']
            
            comparison.append(algo_df)
        
        result_df = pd.concat(comparison, ignore_index=True)
        
        return result_df

