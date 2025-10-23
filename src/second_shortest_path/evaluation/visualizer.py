"""
可视化工具

生成各种性能对比图表，用于分析和展示算法性能。
"""

import logging
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

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
        """运行时间对比柱状图
        
        Args:
            results: 测试结果DataFrame，需包含 'algorithm' 和 'time' 列
            output_path: 输出图片路径
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"生成运行时间对比图: {output_path}")
        
        plt.figure(figsize=(10, 6))
        
        # 按算法分组计算平均时间
        avg_times = results.groupby('algorithm')['time'].mean().sort_values()
        
        # 绘制柱状图
        ax = avg_times.plot(kind='bar', color=['#3498db', '#e74c3c'])
        ax.set_xlabel('Algorithm', fontsize=14)
        ax.set_ylabel('Average Runtime (seconds)', fontsize=14)
        ax.set_title('Algorithm Runtime Comparison', fontsize=16, fontweight='bold')
        ax.tick_params(axis='x', rotation=45)
        
        # 添加数值标签
        for i, v in enumerate(avg_times.values):
            ax.text(i, v, f'{v:.6f}s', ha='center', va='bottom', fontsize=10)
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
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
        
        plt.figure(figsize=(10, 6))
        
        # 按算法和节点数分组
        for algo in results['algorithm'].unique():
            algo_df = results[results['algorithm'] == algo]
            grouped = algo_df.groupby('n')['time'].mean()
            
            plt.plot(grouped.index, grouped.values, marker='o', label=algo, linewidth=2)
        
        plt.xlabel('Number of Nodes (n)', fontsize=14)
        plt.ylabel('Average Runtime (seconds)', fontsize=14)
        plt.title('Algorithm Scalability Analysis', fontsize=16, fontweight='bold')
        plt.legend(fontsize=12)
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        logger.info(f"可扩展性分析图已保存")
    
    @staticmethod
    def plot_complexity_verification(
        results: pd.DataFrame,
        output_path: str | Path
    ) -> None:
        """复杂度验证散点图+拟合曲线
        
        Args:
            results: 测试结果DataFrame
            output_path: 输出图片路径
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"生成复杂度验证图: {output_path}")
        
        fig, axes = plt.subplots(1, 2, figsize=(16, 6))
        
        for idx, algo in enumerate(results['algorithm'].unique()):
            algo_df = results[results['algorithm'] == algo]
            
            ax = axes[idx]
            
            # 计算 M log N
            algo_df = algo_df.copy()
            algo_df['m_log_n'] = algo_df['m'] * np.log(algo_df['n'])
            
            # 散点图
            ax.scatter(algo_df['m_log_n'], algo_df['time'], alpha=0.6, s=50)
            
            # 拟合直线
            z = np.polyfit(algo_df['m_log_n'], algo_df['time'], 1)
            p = np.poly1d(z)
            x_line = np.linspace(algo_df['m_log_n'].min(), algo_df['m_log_n'].max(), 100)
            ax.plot(x_line, p(x_line), 'r--', linewidth=2, label='Linear Fit')
            
            ax.set_xlabel('M log N', fontsize=12)
            ax.set_ylabel('Runtime (seconds)', fontsize=12)
            ax.set_title(f'{algo} Complexity Verification', fontsize=14, fontweight='bold')
            ax.legend(fontsize=10)
            ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        logger.info(f"复杂度验证图已保存")
    
    @staticmethod
    def plot_operations_comparison(
        results: pd.DataFrame,
        output_path: str | Path
    ) -> None:
        """PQ操作vs队列操作对比
        
        Args:
            results: 测试结果DataFrame
            output_path: 输出图片路径
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"生成操作次数对比图: {output_path}")
        
        plt.figure(figsize=(10, 6))
        
        # 提取操作次数
        data = []
        for algo in results['algorithm'].unique():
            algo_df = results[results['algorithm'] == algo]
            
            if 'pq_operations' in algo_df.columns:
                ops = algo_df['pq_operations'].mean()
                data.append({'Algorithm': algo, 'Operations': ops, 'Type': 'PQ Operations'})
            
            if 'enqueue_operations' in algo_df.columns:
                ops = algo_df['enqueue_operations'].mean()
                data.append({'Algorithm': algo, 'Operations': ops, 'Type': 'Queue Operations'})
            
            if 'edge_relaxations' in algo_df.columns:
                ops = algo_df['edge_relaxations'].mean()
                data.append({'Algorithm': algo, 'Operations': ops, 'Type': 'Edge Relaxations'})
        
        if data:
            df = pd.DataFrame(data)
            
            # 分组柱状图
            pivot_df = df.pivot(index='Algorithm', columns='Type', values='Operations')
            ax = pivot_df.plot(kind='bar', width=0.8)
            
            ax.set_xlabel('Algorithm', fontsize=14)
            ax.set_ylabel('Average Number of Operations', fontsize=14)
            ax.set_title('Algorithm Operations Comparison', fontsize=16, fontweight='bold')
            ax.tick_params(axis='x', rotation=45)
            ax.legend(title='Operation Type', fontsize=10)
            
            plt.tight_layout()
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            plt.close()
            
            logger.info(f"操作次数对比图已保存")
        else:
            logger.warning("没有操作次数数据可供绘图")
    
    @staticmethod
    def plot_percentile_comparison(
        results: pd.DataFrame,
        output_path: str | Path
    ) -> None:
        """百分位数箱线图
        
        Args:
            results: 测试结果DataFrame
            output_path: 输出图片路径
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"生成百分位数对比图: {output_path}")
        
        plt.figure(figsize=(10, 6))
        
        # 箱线图
        ax = sns.boxplot(x='algorithm', y='time', data=results, palette='Set2')
        ax.set_xlabel('Algorithm', fontsize=14)
        ax.set_ylabel('Runtime (seconds)', fontsize=14)
        ax.set_title('Algorithm Runtime Distribution (Box Plot)', fontsize=16, fontweight='bold')
        ax.tick_params(axis='x', rotation=45)
        
        # 添加统计信息
        for i, algo in enumerate(results['algorithm'].unique()):
            algo_df = results[results['algorithm'] == algo]
            median = algo_df['time'].median()
            p95 = algo_df['time'].quantile(0.95)
            ax.text(
                i, p95, f'P95: {p95:.6f}s',
                ha='center', va='bottom', fontsize=9, color='red'
            )
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        logger.info(f"百分位数对比图已保存")
    
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
        results['density_bin'] = pd.cut(results['density'], bins=5, labels=['Very Sparse', 'Sparse', 'Medium', 'Dense', 'Very Dense'])
        results['size_bin'] = pd.cut(results['n'], bins=5, labels=['XS', 'S', 'M', 'L', 'XL'])
        
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
            ax.set_xlabel('Graph Size', fontsize=12)
            ax.set_ylabel('Graph Density', fontsize=12)
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        logger.info(f"性能热力图已保存")

