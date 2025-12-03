# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a CS260 course project comparing two second shortest path algorithms:
- **Two-Distance Dijkstra**: Maintains shortest (d1) and second-shortest (d2) distances for each node using a min-heap. Complexity: O(M log N)
- **State-Extended SPFA**: Uses FIFO queue with Bellman-Ford style relaxation. Complexity: Average O(M), Worst O(MN)

## Commands

### Environment Setup
```bash
uv venv
source .venv/bin/activate
uv pip install -e .
uv pip install -e ".[dev]"  # with dev dependencies
```

### Running Scripts
Always use `uv run` for Python execution:
```bash
uv run python scripts/download_leetcode.py --output data/leetcode
uv run python scripts/run_experiments.py --all
uv run python scripts/generate_report.py --output results/report.pdf
```

### Testing
```bash
uv run pytest                                    # run all tests
uv run pytest tests/test_dijkstra.py            # run single test file
uv run pytest -k "test_simple"                  # run tests by name pattern
uv run pytest --cov=src/second_shortest_path --cov-report=html  # with coverage
```

### Code Formatting
```bash
uv run black src/ tests/
uv run isort src/ tests/
```

## Architecture

### Core Algorithms (`src/second_shortest_path/algorithms/`)
- `dijkstra_two_dist.py`: `TwoDistanceDijkstra` class - heap-based algorithm
- `spfa_extended.py`: `StateExtendedSPFA` class - queue-based algorithm
- Both classes share the same interface:
  - `find_second_shortest(source, target) -> (shortest, second_shortest)`
  - `get_statistics() -> dict` (returns pq_operations, edge_relaxations, iterations, etc.)

### Graph Representation
Adjacency list format: `{node: [(neighbor, weight), ...]}`

### Data Pipeline
- `data/loader.py`: Load test data from files
- `data/generator.py`: Generate synthetic graphs
- `evaluation/metrics.py`: Performance metrics calculation
- `evaluation/visualizer.py`: Plotting results

### Test Fixtures (`tests/conftest.py`)
Pre-defined graph fixtures: `simple_graph`, `chain_graph`, `complete_graph`, `disconnected_graph`

## Coding Standards

- **Language**: Chinese for comments, docstrings, and logs; English for visualization labels
- **Logging**: Use `logging` module, never `print()`
- **Type hints**: Required for all function parameters and returns
- **Paths**: Use `pathlib.Path` for all file operations
- **Style**: PEP 8, formatted with black (line-length=100) and isort
- **Docstrings**: Google style

## Testing Requirements

- Tests in `tests/` directory, files named `test_*.py`
- Use pytest fixtures for test data
- Mock external dependencies (no network/filesystem in unit tests)
- Target 80%+ coverage for project, 90%+ for new code

## Git Commits

Use Conventional Commits in Chinese:
- `feat(算法): 添加新功能`
- `fix(数据): 修复bug`
- `docs(README): 更新文档`
- `test(单元测试): 添加测试用例`
- `refactor(重构): 代码重构`
