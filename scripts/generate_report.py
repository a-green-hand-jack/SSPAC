#!/usr/bin/env python3
"""
生成实验报告的脚本

整合实验结果，生成PDF格式的完整报告。
"""

import argparse
import logging
import sys
from pathlib import Path

# src布局路径修正
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def generate_report(results_dir: str, output_file: str) -> None:
    """生成实验报告
    
    Args:
        results_dir: 实验结果目录
        output_file: 输出PDF文件路径
    """
    results_path = Path(results_dir)
    output_path = Path(output_file)
    
    logger.info("=" * 60)
    logger.info("开始生成实验报告")
    logger.info("=" * 60)
    
    # 检查结果目录
    if not results_path.exists():
        raise FileNotFoundError(f"结果目录不存在: {results_path}")
    
    metrics_dir = results_path / "metrics"
    viz_dir = results_path / "visualizations"
    
    if not metrics_dir.exists():
        raise FileNotFoundError(f"指标目录不存在: {metrics_dir}")
    
    if not viz_dir.exists():
        raise FileNotFoundError(f"可视化目录不存在: {viz_dir}")
    
    # 读取结果数据
    import pandas as pd
    
    results_file = metrics_dir / "benchmark_results.csv"
    if not results_file.exists():
        raise FileNotFoundError(f"基准测试结果文件不存在: {results_file}")
    
    logger.info(f"📊 加载结果数据: {results_file}")
    df = pd.read_csv(results_file)
    
    # TODO: 实现PDF报告生成
    # 这里提供一个简单的文本报告作为示例
    
    logger.info("📝 生成报告内容")
    
    report_lines = [
        "=" * 60,
        "第二短路径算法性能对比实验报告",
        "=" * 60,
        "",
        "## 1. 实验概述",
        "",
        f"- 测试算法数量: {df['algorithm'].nunique()}",
        f"- 测试用例数量: {len(df)}",
        f"- 图规模范围: {df['n'].min()} - {df['n'].max()} 节点",
        "",
        "## 2. 算法列表",
        "",
    ]
    
    for algo in df['algorithm'].unique():
        report_lines.append(f"- {algo}")
    
    report_lines.extend([
        "",
        "## 3. 性能统计",
        "",
    ])
    
    for algo in df['algorithm'].unique():
        algo_df = df[df['algorithm'] == algo]
        report_lines.extend([
            f"### {algo}",
            f"- 平均运行时间: {algo_df['time'].mean():.6f}s",
            f"- 中位数: {algo_df['time'].median():.6f}s",
            f"- 标准差: {algo_df['time'].std():.6f}s",
            f"- 最小值: {algo_df['time'].min():.6f}s",
            f"- 最大值: {algo_df['time'].max():.6f}s",
            "",
        ])
    
    report_lines.extend([
        "## 4. 可视化图表",
        "",
        "可视化图表保存在:",
        f"- {viz_dir}",
        "",
        "## 5. 结论",
        "",
        "（请根据实验结果补充结论）",
        "",
        "=" * 60,
    ])
    
    # 保存文本报告
    output_path.parent.mkdir(parents=True, exist_ok=True)
    text_output = output_path.with_suffix('.txt')
    
    with open(text_output, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report_lines))
    
    logger.info(f"✅ 文本报告已生成: {text_output}")
    
    logger.info("=" * 60)
    logger.info("✅ 报告生成完成！")
    logger.info(f"📁 报告保存在: {text_output}")
    logger.info("=" * 60)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='生成实验报告'
    )
    parser.add_argument(
        '--results',
        type=str,
        default='results',
        help='实验结果目录（默认: results）'
    )
    parser.add_argument(
        '--output',
        type=str,
        default='results/report.pdf',
        help='输出报告文件路径（默认: results/report.pdf）'
    )
    
    args = parser.parse_args()
    
    try:
        generate_report(args.results, args.output)
    except Exception as e:
        logger.error(f"❌ 报告生成失败: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()

