# Gemini Context: Second Shortest Path Algorithms Comparison (SSPAC)

## Project Overview
This project, **SSPAC**, implements and benchmarks algorithms for finding the second shortest path in graphs. It compares two primary algorithms:
1.  **Two-Distance Dijkstra:** A modified Dijkstra's algorithm maintaining shortest and second-shortest distances.
2.  **State-Extended SPFA:** An extension of the Shortest Path Faster Algorithm (SPFA) using a queue-based relaxation approach.

The project includes a Python implementation for flexibility and analysis, and a C++ implementation for high-performance benchmarking.

## Key Technologies
*   **Language:** Python 3.10+ (Primary), C++17 (Performance comparison)
*   **Package Manager:** `uv`
*   **Libraries:** `numpy`, `pandas`, `matplotlib`, `networkx`, `pytest`
*   **Tools:** Jupyter Notebooks for analysis.

## Directory Structure
*   `src/second_shortest_path/`: Main Python package.
    *   `algorithms/`: Implementation of `TwoDistanceDijkstra` and `StateExtendedSPFA` (Python & C++).
    *   `data/`: Data loaders and graph generators.
    *   `evaluation/`: Metrics calculation and visualization tools.
*   `tests/`: Unit tests using `pytest`.
*   `scripts/`: Utility scripts for downloading data, running experiments, and generating reports.
*   `data/`: Storage for LeetCode datasets and generated graphs.
*   `docs/`: Documentation and analysis reports.
*   `notebooks/`: Jupyter notebooks for interactive analysis.

## Development Workflows

### 1. Environment Setup
The project uses `uv` for dependency management.

```bash
# Create and activate virtual environment
uv venv
source .venv/bin/activate

# Install dependencies
uv pip install -e ".[dev]"
```

### 2. Building & Running (Python)

**Run Experiments:**
```bash
python scripts/run_experiments.py --all
```

**Download Data (LeetCode):**
```bash
python scripts/download_leetcode.py --output data/leetcode
```

**Generate Report:**
```bash
python scripts/generate_report.py --output results/report.pdf
```

### 3. Building & Running (C++)
Located in `src/second_shortest_path/algorithms/`.

**Compile:**
```bash
cd src/second_shortest_path/algorithms/
g++ -std=c++17 -O2 -march=native -Wall -Wextra second_shortest_path_algorithms.cpp -o second_shortest_path
```

**Run:**
```bash
./second_shortest_path
```

### 4. Testing
Run the comprehensive test suite using `pytest`.

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src/second_shortest_path --cov-report=html
```

## Coding Conventions
*   **Style:** Adheres to `black` (line length 100) and `isort` standards.
*   **Type Hinting:** Python code should use type hints.
*   **Documentation:** Classes and functions should have docstrings explaining their purpose and parameters.
