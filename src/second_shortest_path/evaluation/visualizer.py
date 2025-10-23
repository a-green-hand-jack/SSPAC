"""
可视化工具

生成各种性能对比图表，用于分析和展示算法性能。
完全符合 docs/01_visual.md 的要求。
"""

import logging
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy.optimize import curve_fit
from scipy import stats

logger = logging.getLogger(__name__)

# 设置绘图风格
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['font.size'] = 12


class Visualizer:
    """可视化工具类，生成性能对比图表
    
    提供多种可视化方法，用于展示算法性能对比结果。
    所有图表文字使用英文以确保跨平台兼容性。
    
    Examples:
        >>> Visualizer.plot_runtime_comparison(df, "results/runtime.png")
        >>> Visualizer.plot_scalability(df, "results/scalability.png")
    """
    
    @staticmethod
    def plot_runtime_comparison(
        results: pd.DataFrame,
        output_path: str | Path
    ) -> None:
        """运行时间对比箱线图
        
        展示P50/P95/P99百分位数和均值。
        
        Args:
            results: 测试结果DataFrame，需包含 'algorithm' 和 'time' 列
            output_path: 输出图片路径
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"生成运行时间对比图: {output_path}")
        
        plt.figure(figsize=(12, 7))
        
        # 绘制箱线图
        ax = sns.boxplot(
            x='algorithm', 
            y='time', 
            data=results, 
            palette=['#3498db', '#e74c3c'],
            showmeans=True,
            meanprops={'marker': 'D', 'markerfacecolor': 'gold', 'markersize': 10, 'markeredgecolor': 'black', 'markeredgewidth': 1.5}
        )
        
        ax.set_xlabel('Algorithm', fontsize=14, fontweight='bold')
        ax.set_ylabel('Runtime (seconds)', fontsize=14, fontweight='bold')
        ax.set_title('Algorithm Runtime Comparison (Box Plot)', fontsize=16, fontweight='bold')
        ax.tick_params(axis='x', rotation=0)
        
        # 添加图例说明
        from matplotlib.patches import Patch
        from matplotlib.lines import Line2D
        
        legend_elements = [
            Line2D([0], [0], marker='_', color='w', label='Median (P50)',
                   markerfacecolor='black', markersize=12, markeredgecolor='black', linewidth=2),
            Line2D([0], [0], marker='D', color='w', label='Mean',
                   markerfacecolor='gold', markersize=8, markeredgecolor='black', markeredgewidth=1.5),
            Patch(facecolor='#3498db', label='Dijkstra', alpha=0.7),
            Patch(facecolor='#e74c3c', label='SPFA', alpha=0.7),
        ]
        
        ax.legend(handles=legend_elements, loc='upper left', fontsize=11, framealpha=0.95, edgecolor='black')
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        
        logger.info(f"运行时间对比图已保存")
    
    @staticmethod
    def plot_scalability(
        results: pd.DataFrame,
        output_path: str | Path
    ) -> None:
        """可扩展性分析折线图
        
        展示算法性能随图规模的变化。
        
        Args:
            results: 测试结果DataFrame，需包含 'algorithm', 'n', 'time' 列
            output_path: 输出图片路径
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"生成可扩展性分析图: {output_path}")
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
        
        # 左图：按节点数n分组
        for algo in results['algorithm'].unique():
            algo_df = results[results['algorithm'] == algo]
            grouped = algo_df.groupby('n')['time'].mean()
            
            color = '#3498db' if 'Dijkstra' in algo else '#e74c3c'
            ax1.plot(
                grouped.index, grouped.values, 
                marker='o', label=algo, linewidth=2, 
                markersize=6, color=color
            )
        
        ax1.set_xlabel('Number of Nodes (n)', fontsize=14, fontweight='bold')
        ax1.set_ylabel('Average Runtime (seconds)', fontsize=14, fontweight='bold')
        ax1.set_title('Scalability: Runtime vs Nodes', fontsize=14, fontweight='bold')
        ax1.legend(fontsize=12)
        ax1.grid(True, alpha=0.3)
        
        # 右图：按边数m分组
        for algo in results['algorithm'].unique():
            algo_df = results[results['algorithm'] == algo]
            grouped = algo_df.groupby('m')['time'].mean()
            
            color = '#3498db' if 'Dijkstra' in algo else '#e74c3c'
            ax2.plot(
                grouped.index, grouped.values, 
                marker='s', label=algo, linewidth=2, 
                markersize=6, color=color
            )
        
        ax2.set_xlabel('Number of Edges (m)', fontsize=14, fontweight='bold')
        ax2.set_ylabel('Average Runtime (seconds)', fontsize=14, fontweight='bold')
        ax2.set_title('Scalability: Runtime vs Edges', fontsize=14, fontweight='bold')
        ax2.legend(fontsize=12)
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        
        logger.info(f"可扩展性分析图已保存")
    
    @staticmethod
    def plot_complexity_verification(
        results: pd.DataFrame,
        output_path: str | Path
    ) -> None:
        """复杂度验证散点图+拟合曲线
        
        使用scipy进行完整的曲线拟合：
        - Dijkstra: 拟合 T = c * M * log(N)
        - SPFA: 同时拟合 O(M log N) 和 O(MN)，选择R²更高的
        
        Args:
            results: 测试结果DataFrame
            output_path: 输出图片路径
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"生成复杂度验证图: {output_path}")
        
        fig, axes = plt.subplots(1, 2, figsize=(18, 7))
        
        algorithms = results['algorithm'].unique()
        
        for idx, algo in enumerate(algorithms):
            algo_df = results[results['algorithm'] == algo].copy()
            
            ax = axes[idx]
            
            # 计算理论复杂度值
            algo_df['m_log_n'] = algo_df['m'] * np.log(algo_df['n'])
            algo_df['m_n'] = algo_df['m'] * algo_df['n']
            
            # 定义拟合函数
            def linear_func(x, a, b):
                """线性函数: y = ax + b"""
                return a * x + b
            
            # 拟合 O(M log N)
            try:
                x_data_log = algo_df['m_log_n'].values
                y_data = algo_df['time'].values
                
                # 过滤掉无效值
                valid_mask = np.isfinite(x_data_log) & np.isfinite(y_data) & (x_data_log > 0)
                x_data_log_valid = x_data_log[valid_mask]
                y_data_valid = y_data[valid_mask]
                
                popt_log, _ = curve_fit(linear_func, x_data_log_valid, y_data_valid)
                slope_log, intercept_log = popt_log
                
                # 计算R²
                y_pred_log = linear_func(x_data_log_valid, *popt_log)
                ss_res_log = np.sum((y_data_valid - y_pred_log) ** 2)
                ss_tot_log = np.sum((y_data_valid - np.mean(y_data_valid)) ** 2)
                r2_log = 1 - (ss_res_log / ss_tot_log) if ss_tot_log > 0 else 0
                
                logger.info(f"{algo} - O(M log N) 拟合: R² = {r2_log:.4f}")
            except Exception as e:
                logger.warning(f"{algo} - O(M log N) 拟合失败: {e}")
                r2_log = 0
                slope_log = 0
                intercept_log = 0
            
            # 拟合 O(MN)
            try:
                x_data_mn = algo_df['m_n'].values
                
                valid_mask_mn = np.isfinite(x_data_mn) & np.isfinite(y_data) & (x_data_mn > 0)
                x_data_mn_valid = x_data_mn[valid_mask_mn]
                y_data_mn_valid = y_data[valid_mask_mn]
                
                popt_mn, _ = curve_fit(linear_func, x_data_mn_valid, y_data_mn_valid)
                slope_mn, intercept_mn = popt_mn
                
                # 计算R²
                y_pred_mn = linear_func(x_data_mn_valid, *popt_mn)
                ss_res_mn = np.sum((y_data_mn_valid - y_pred_mn) ** 2)
                ss_tot_mn = np.sum((y_data_mn_valid - np.mean(y_data_mn_valid)) ** 2)
                r2_mn = 1 - (ss_res_mn / ss_tot_mn) if ss_tot_mn > 0 else 0
                
                logger.info(f"{algo} - O(MN) 拟合: R² = {r2_mn:.4f}")
            except Exception as e:
                logger.warning(f"{algo} - O(MN) 拟合失败: {e}")
                r2_mn = 0
                slope_mn = 0
                intercept_mn = 0
            
            # 选择最佳拟合
            if r2_log >= r2_mn:
                best_complexity = 'O(M log N)'
                best_r2 = r2_log
                x_plot = algo_df['m_log_n']
                x_label = 'M log N'
                
                # 绘制散点图
                ax.scatter(x_plot, algo_df['time'], alpha=0.6, s=50, label='Actual Data')
                
                # 绘制拟合曲线
                x_line = np.linspace(x_plot.min(), x_plot.max(), 100)
                y_line = linear_func(x_line, slope_log, intercept_log)
                ax.plot(x_line, y_line, 'r--', linewidth=2, 
                       label=f'Fit: T = {slope_log:.2e} * x + {intercept_log:.2e}')
            else:
                best_complexity = 'O(MN)'
                best_r2 = r2_mn
                x_plot = algo_df['m_n']
                x_label = 'M * N'
                
                # 绘制散点图
                ax.scatter(x_plot, algo_df['time'], alpha=0.6, s=50, label='Actual Data')
                
                # 绘制拟合曲线
                x_line = np.linspace(x_plot.min(), x_plot.max(), 100)
                y_line = linear_func(x_line, slope_mn, intercept_mn)
                ax.plot(x_line, y_line, 'r--', linewidth=2, 
                       label=f'Fit: T = {slope_mn:.2e} * x + {intercept_mn:.2e}')
            
            ax.set_xlabel(x_label, fontsize=12, fontweight='bold')
            ax.set_ylabel('Runtime (seconds)', fontsize=12, fontweight='bold')
            ax.set_title(
                f'{algo} Complexity Verification\n'
                f'Best Fit: {best_complexity} (R² = {best_r2:.4f})',
                fontsize=14, fontweight='bold'
            )
            ax.legend(fontsize=10)
            ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        
        logger.info(f"复杂度验证图已保存")
    
    @staticmethod
    def plot_operations_comparison(
        results: pd.DataFrame,
        output_path: str | Path
    ) -> None:
        """操作次数对比分组柱状图
        
        展示：Push次数、Pop次数、边松弛次数。
        
        Args:
            results: 测试结果DataFrame
            output_path: 输出图片路径
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"生成操作次数对比图: {output_path}")
        
        fig, axes = plt.subplots(1, 3, figsize=(18, 6))
        
        # 准备数据
        operation_types = [
            ('operations', 'Queue/PQ Operations'),
            ('edge_relaxations', 'Edge Relaxations'),
            ('push_count', 'Push Operations')
        ]
        
        # 检查数据列是否存在
        available_ops = []
        if 'operations' in results.columns:
            available_ops.append(('operations', 'Queue/PQ Operations'))
        if 'edge_relaxations' in results.columns:
            available_ops.append(('edge_relaxations', 'Edge Relaxations'))
        if 'push_count' in results.columns:
            available_ops.append(('push_count', 'Push Operations'))
        
        if not available_ops:
            logger.warning("没有操作次数数据可供绘图")
            return
        
        for idx, (op_col, op_name) in enumerate(available_ops[:3]):
            ax = axes[idx] if len(available_ops) >= 3 else axes[idx % len(axes)]
            
            # 按算法分组计算平均值
            data_for_plot = []
            for algo in results['algorithm'].unique():
                algo_df = results[results['algorithm'] == algo]
                if op_col in algo_df.columns:
                    avg_ops = algo_df[op_col].mean()
                    data_for_plot.append({
                        'Algorithm': algo,
                        'Operations': avg_ops
                    })
            
            if data_for_plot:
                df_plot = pd.DataFrame(data_for_plot)
                
                colors = ['#3498db' if 'Dijkstra' in algo else '#e74c3c' 
                         for algo in df_plot['Algorithm']]
                
                bars = ax.bar(df_plot['Algorithm'], df_plot['Operations'], color=colors, alpha=0.7)
                
                # 添加数值标签
                for bar in bars:
                    height = bar.get_height()
                    ax.text(
                        bar.get_x() + bar.get_width() / 2., height,
                        f'{int(height):,}',
                        ha='center', va='bottom', fontsize=10
                    )
                
                ax.set_xlabel('Algorithm', fontsize=12, fontweight='bold')
                ax.set_ylabel('Average Count', fontsize=12, fontweight='bold')
                ax.set_title(f'{op_name}', fontsize=14, fontweight='bold')
                ax.tick_params(axis='x', rotation=0)
                ax.grid(True, alpha=0.3, axis='y')
        
        # 隐藏未使用的子图
        for idx in range(len(available_ops), 3):
            axes[idx].set_visible(False)
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        
        logger.info(f"操作次数对比图已保存")
    
    @staticmethod
    def plot_percentile_comparison(
        results: pd.DataFrame,
        output_path: str | Path
    ) -> None:
        """百分位数箱线图
        
        增强版箱线图，添加P50/P95/P99标注和均值点。
        
        Args:
            results: 测试结果DataFrame
            output_path: 输出图片路径
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"生成百分位数对比图: {output_path}")
        
        plt.figure(figsize=(12, 7))
        
        # 箱线图
        ax = sns.boxplot(
            x='algorithm', 
            y='time', 
            data=results, 
            palette=['#3498db', '#e74c3c'],
            showmeans=True,
            meanprops={'marker': 'D', 'markerfacecolor': 'yellow', 'markersize': 10, 'label': 'Mean'}
        )
        
        ax.set_xlabel('Algorithm', fontsize=14, fontweight='bold')
        ax.set_ylabel('Runtime (seconds)', fontsize=14, fontweight='bold')
        ax.set_title('Algorithm Runtime Distribution (Percentile Comparison)', fontsize=16, fontweight='bold')
        ax.tick_params(axis='x', rotation=0)
        
        # 添加百分位数标注
        algorithms = results['algorithm'].unique()
        for i, algo in enumerate(algorithms):
            algo_df = results[results['algorithm'] == algo]
            
            p50 = algo_df['time'].quantile(0.50)
            p95 = algo_df['time'].quantile(0.95)
            p99 = algo_df['time'].quantile(0.99)
            
            # P50 标注（中位数）
            ax.plot(i, p50, 'go', markersize=8, label='P50' if i == 0 else '')
            
            # P95 标注
            ax.plot(i, p95, 'ro', markersize=8, label='P95' if i == 0 else '')
            ax.text(
                i + 0.15, p95, f'P95: {p95:.6f}s',
                ha='left', va='center', fontsize=9, color='red',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.7)
            )
            
            # P99 标注
            ax.plot(i, p99, 'mo', markersize=8, label='P99' if i == 0 else '')
            ax.text(
                i + 0.15, p99, f'P99: {p99:.6f}s',
                ha='left', va='center', fontsize=9, color='purple',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.7)
            )
        
        ax.legend(loc='upper right', fontsize=10)
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        
        logger.info(f"百分位数对比图已保存")
    
    @staticmethod
    def plot_distance_updates_comparison(
        results: pd.DataFrame,
        output_path: str | Path
    ) -> None:
        """距离标签更新次数对比图
        
        对比d1和d2的更新次数，验证理论上限。
        
        Args:
            results: 测试结果DataFrame，需包含 'd1_updates' 和 'd2_updates' 列
            output_path: 输出图片路径
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"生成距离更新对比图: {output_path}")
        
        # 检查必需的列是否存在
        if 'd1_updates' not in results.columns or 'd2_updates' not in results.columns:
            logger.warning("缺少 'd1_updates' 或 'd2_updates' 列，跳过距离更新对比图")
            return
        
        fig, axes = plt.subplots(1, 2, figsize=(16, 6))
        
        algorithms = results['algorithm'].unique()
        
        for idx, algo in enumerate(algorithms):
            algo_df = results[results['algorithm'] == algo]
            
            ax = axes[idx]
            
            # 计算平均更新次数
            avg_d1 = algo_df['d1_updates'].mean()
            avg_d2 = algo_df['d2_updates'].mean()
            
            # 绘制柱状图
            categories = ['d1 Updates', 'd2 Updates']
            values = [avg_d1, avg_d2]
            colors = ['#3498db', '#e74c3c']
            
            bars = ax.bar(categories, values, color=colors, alpha=0.7)
            
            # 添加数值标签
            for bar, val in zip(bars, values):
                height = bar.get_height()
                ax.text(
                    bar.get_x() + bar.get_width() / 2., height,
                    f'{int(val):,}',
                    ha='center', va='bottom', fontsize=11, fontweight='bold'
                )
            
            ax.set_ylabel('Average Update Count', fontsize=12, fontweight='bold')
            ax.set_title(f'{algo} - Distance Label Updates', fontsize=14, fontweight='bold')
            ax.grid(True, alpha=0.3, axis='y')
            
            # 添加理论上限参考线（如果有足够的数据）
            if len(algo_df) > 0:
                avg_n = algo_df['n'].mean()
                theoretical_limit = avg_n * np.log(avg_n)  # O(N log N) 理论上限
                ax.axhline(
                    y=theoretical_limit, 
                    color='green', 
                    linestyle='--', 
                    linewidth=2,
                    label=f'Theoretical O(N log N): {int(theoretical_limit):,}'
                )
                ax.legend(fontsize=10)
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        
        logger.info(f"距离更新对比图已保存")
    
    @staticmethod
    def plot_heatmap(
        results: pd.DataFrame,
        output_path: str | Path
    ) -> None:
        """性能热力图（图密度 x 规模）
        
        Args:
            results: 测试结果DataFrame
            output_path: 输出图片路径
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"生成性能热力图: {output_path}")
        
        # 计算图密度
        results = results.copy()
        results['density'] = results['m'] / (results['n'] * (results['n'] - 1) / 2)
        
        # 离散化密度和规模
        results['density_bin'] = pd.cut(
            results['density'], 
            bins=5, 
            labels=['Very Sparse', 'Sparse', 'Medium', 'Dense', 'Very Dense']
        )
        results['size_bin'] = pd.cut(
            results['n'], 
            bins=5, 
            labels=['XS', 'S', 'M', 'L', 'XL']
        )
        
        fig, axes = plt.subplots(1, 2, figsize=(16, 6))
        
        for idx, algo in enumerate(results['algorithm'].unique()):
            algo_df = results[results['algorithm'] == algo]
            
            # 创建透视表
            pivot_table = algo_df.pivot_table(
                values='time',
                index='density_bin',
                columns='size_bin',
                aggfunc='mean'
            )
            
            # 热力图
            ax = axes[idx]
            sns.heatmap(
                pivot_table,
                annot=True,
                fmt='.6f',
                cmap='YlOrRd',
                ax=ax,
                cbar_kws={'label': 'Runtime (s)'}
            )
            ax.set_title(f'{algo} Performance Heatmap', fontsize=14, fontweight='bold')
            ax.set_xlabel('Graph Size', fontsize=12, fontweight='bold')
            ax.set_ylabel('Graph Density', fontsize=12, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        
        logger.info(f"性能热力图已保存")
