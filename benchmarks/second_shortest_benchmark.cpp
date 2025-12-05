/**
 * 次短路径算法 Benchmark 框架
 *
 * 比较 Two-Distance Dijkstra 和 State-Extended SPFA 在以下场景的性能：
 * 1. 稠密图 (Dense Graph): M ≈ N²/5
 * 2. 稀疏图 (Sparse Graph): M ≈ 5N
 * 3. 网格图 (Grid Graph): 专门用于卡 SPFA 的对抗性测试
 *
 * 编译命令: g++ -std=c++17 -O2 second_shortest_benchmark.cpp -o benchmark
 * 运行命令: ./benchmark
 */

#include <iostream>
#include <vector>
#include <queue>
#include <deque>
#include <random>
#include <chrono>
#include <cstring>
#include <iomanip>
#include <functional>

using namespace std;

// ================= 配置区域 =================
const int INF = 0x3f3f3f3f;
// ===========================================

// 边结构
struct Edge {
    int v, w;
};

// 算法统计信息
struct AlgorithmStats {
    long long push_count = 0;      // 入队/入堆次数
    long long pop_count = 0;       // 出队/出堆次数
    long long edge_relaxations = 0; // 边松弛次数
    long long d1_updates = 0;      // 最短路更新次数
    long long d2_updates = 0;      // 次短路更新次数
    double time_ms = 0;            // 运行时间 (ms)
};

// ============================================================================
// Two-Distance Dijkstra 算法 (次短路径版本)
// ============================================================================
AlgorithmStats dijkstra_second_shortest(
    const vector<vector<Edge>>& adj,
    int n,
    int source,
    int target,
    int& result_d1,
    int& result_d2
) {
    AlgorithmStats stats;
    vector<int> d1(n + 1, INF);  // 最短路
    vector<int> d2(n + 1, INF);  // 次短路

    // 优先队列: (距离, 节点)
    priority_queue<pair<int, int>, vector<pair<int, int>>, greater<pair<int, int>>> pq;

    auto start_time = chrono::high_resolution_clock::now();

    d1[source] = 0;
    pq.push({0, source});
    stats.push_count++;

    while (!pq.empty()) {
        auto [dist, u] = pq.top();
        pq.pop();
        stats.pop_count++;

        // 跳过过时的状态
        if (dist > d2[u]) continue;

        for (const auto& edge : adj[u]) {
            int v = edge.v;
            int w = edge.w;
            int new_dist = dist + w;
            stats.edge_relaxations++;

            // 情况1：找到更短的最短路
            if (new_dist < d1[v]) {
                d2[v] = d1[v];  // 原最短路变为次短路
                d1[v] = new_dist;
                stats.d1_updates++;
                pq.push({d1[v], v});
                stats.push_count++;
            }
            // 情况2：找到严格次短路
            else if (new_dist > d1[v] && new_dist < d2[v]) {
                d2[v] = new_dist;
                stats.d2_updates++;
                pq.push({d2[v], v});
                stats.push_count++;
            }
        }
    }

    auto end_time = chrono::high_resolution_clock::now();
    stats.time_ms = chrono::duration<double, milli>(end_time - start_time).count();

    result_d1 = d1[target];
    result_d2 = d2[target];
    return stats;
}

// ============================================================================
// State-Extended SPFA 算法 (次短路径版本)
// ============================================================================
AlgorithmStats spfa_second_shortest(
    const vector<vector<Edge>>& adj,
    int n,
    int source,
    int target,
    int& result_d1,
    int& result_d2
) {
    AlgorithmStats stats;
    vector<int> d1(n + 1, INF);  // 最短路
    vector<int> d2(n + 1, INF);  // 次短路
    vector<bool> in_queue(n + 1, false);

    queue<int> q;

    auto start_time = chrono::high_resolution_clock::now();

    d1[source] = 0;
    q.push(source);
    in_queue[source] = true;
    stats.push_count++;

    while (!q.empty()) {
        int u = q.front();
        q.pop();
        stats.pop_count++;
        in_queue[u] = false;

        for (const auto& edge : adj[u]) {
            int v = edge.v;
            int w = edge.w;
            stats.edge_relaxations++;

            bool need_enqueue = false;

            // 情况1：发现更短的最短路
            if (d1[u] + w < d1[v]) {
                d2[v] = d1[v];  // 原最短路变为次短路
                d1[v] = d1[u] + w;
                stats.d1_updates++;
                need_enqueue = true;
            }

            // 情况2：发现严格次短路（大于最短路但小于当前次短路）
            if (d1[u] + w > d1[v] && d1[u] + w < d2[v]) {
                d2[v] = d1[u] + w;
                stats.d2_updates++;
                need_enqueue = true;
            }

            // 情况3：利用 u 的次短路更新 v 的次短路
            if (d2[u] != INF && d2[u] + w < d2[v] && d2[u] + w > d1[v]) {
                d2[v] = d2[u] + w;
                stats.d2_updates++;
                need_enqueue = true;
            }

            if (need_enqueue && !in_queue[v]) {
                q.push(v);
                in_queue[v] = true;
                stats.push_count++;
            }
        }
    }

    auto end_time = chrono::high_resolution_clock::now();
    stats.time_ms = chrono::duration<double, milli>(end_time - start_time).count();

    result_d1 = d1[target];
    result_d2 = d2[target];
    return stats;
}

// ============================================================================
// 图生成器
// ============================================================================

// 随机数生成器
mt19937 rng(chrono::steady_clock::now().time_since_epoch().count());

/**
 * 生成稠密图
 * 边数 M ≈ N²/5
 */
void generate_dense_graph(vector<vector<Edge>>& adj, int n) {
    for (int i = 0; i <= n; i++) adj[i].clear();

    long long target_edges = (long long)n * n / 5;
    int actual_edges = 0;

    // 先确保图连通：生成一条从 1 到 n 的链
    for (int i = 1; i < n; i++) {
        int w = uniform_int_distribution<int>(1, 100)(rng);
        adj[i].push_back({i + 1, w});
        adj[i + 1].push_back({i, w});
        actual_edges++;
    }

    // 随机添加剩余边
    for (long long i = 0; i < target_edges - (n - 1); i++) {
        int u = uniform_int_distribution<int>(1, n)(rng);
        int v = uniform_int_distribution<int>(1, n)(rng);
        if (u == v) continue;
        int w = uniform_int_distribution<int>(1, 100)(rng);
        adj[u].push_back({v, w});
        adj[v].push_back({u, w});
        actual_edges++;
    }

    cout << "  节点数: " << n << ", 边数: ~" << actual_edges << endl;
}

/**
 * 生成稀疏图
 * 边数 M ≈ 5N
 */
void generate_sparse_graph(vector<vector<Edge>>& adj, int n) {
    for (int i = 0; i <= n; i++) adj[i].clear();

    int target_edges = n * 5;
    int actual_edges = 0;

    // 先确保图连通：生成一条从 1 到 n 的链
    for (int i = 1; i < n; i++) {
        int w = uniform_int_distribution<int>(1, 100)(rng);
        adj[i].push_back({i + 1, w});
        adj[i + 1].push_back({i, w});
        actual_edges++;
    }

    // 随机添加剩余边
    for (int i = 0; i < target_edges - (n - 1); i++) {
        int u = uniform_int_distribution<int>(1, n)(rng);
        int v = uniform_int_distribution<int>(1, n)(rng);
        if (u == v) continue;
        int w = uniform_int_distribution<int>(1, 100)(rng);
        adj[u].push_back({v, w});
        adj[v].push_back({u, w});
        actual_edges++;
    }

    cout << "  节点数: " << n << ", 边数: ~" << actual_edges << endl;
}

/**
 * 生成网格图 (Grid Graph)
 * 专门用于卡 SPFA 的对抗性测试
 *
 * 网格图的特点：
 * - 直径大 (H + W 步)
 * - 存在大量从起点到终点的路径
 * - 随机权值导致 SPFA 反复松弛同一节点
 */
void generate_grid_graph(vector<vector<Edge>>& adj, int height, int width, int& total_nodes) {
    total_nodes = height * width;
    for (int i = 0; i <= total_nodes; i++) adj[i].clear();

    // 节点编号映射: (row, col) -> id (从 1 开始)
    auto get_id = [&](int r, int c) {
        return r * width + c + 1;
    };

    int edge_count = 0;

    for (int r = 0; r < height; r++) {
        for (int c = 0; c < width; c++) {
            int u = get_id(r, c);

            // 向右连边
            if (c + 1 < width) {
                int v = get_id(r, c + 1);
                int w = uniform_int_distribution<int>(1, 10)(rng);
                adj[u].push_back({v, w});
                adj[v].push_back({u, w});
                edge_count++;
            }

            // 向下连边
            if (r + 1 < height) {
                int v = get_id(r + 1, c);
                int w = uniform_int_distribution<int>(1, 10)(rng);
                adj[u].push_back({v, w});
                adj[v].push_back({u, w});
                edge_count++;
            }
        }
    }

    cout << "  网格大小: " << height << " x " << width
         << " (节点数: " << total_nodes << ", 边数: " << edge_count << ")" << endl;
}

// ============================================================================
// 结果输出
// ============================================================================

void print_stats(const string& algo_name, const AlgorithmStats& stats, int d1, int d2) {
    cout << "  " << algo_name << ":" << endl;
    cout << "    时间: " << fixed << setprecision(2) << stats.time_ms << " ms" << endl;
    cout << "    最短路: " << (d1 == INF ? -1 : d1)
         << ", 次短路: " << (d2 == INF ? -1 : d2) << endl;
    cout << "    入队次数: " << stats.push_count
         << ", 出队次数: " << stats.pop_count << endl;
    cout << "    边松弛次数: " << stats.edge_relaxations << endl;
    cout << "    d1更新: " << stats.d1_updates
         << ", d2更新: " << stats.d2_updates << endl;
}

void print_comparison(const AlgorithmStats& dijkstra_stats, const AlgorithmStats& spfa_stats) {
    cout << "\n  >>> 性能对比:" << endl;
    if (spfa_stats.time_ms > dijkstra_stats.time_ms && dijkstra_stats.time_ms > 0) {
        cout << "      Dijkstra 比 SPFA 快 " << fixed << setprecision(2)
             << spfa_stats.time_ms / dijkstra_stats.time_ms << " 倍" << endl;
    } else if (dijkstra_stats.time_ms > spfa_stats.time_ms && spfa_stats.time_ms > 0) {
        cout << "      SPFA 比 Dijkstra 快 " << fixed << setprecision(2)
             << dijkstra_stats.time_ms / spfa_stats.time_ms << " 倍" << endl;
    } else {
        cout << "      两者性能相近" << endl;
    }

    cout << "      入队次数比 (SPFA/Dijkstra): " << fixed << setprecision(2)
         << (dijkstra_stats.push_count > 0 ?
             (double)spfa_stats.push_count / dijkstra_stats.push_count : 0) << endl;
}

// ============================================================================
// 实验执行
// ============================================================================

void run_experiment(
    const string& name,
    function<void(vector<vector<Edge>>&, int&)> generator,
    int n_param
) {
    cout << "\n" << string(60, '=') << endl;
    cout << "实验: " << name << endl;
    cout << string(60, '=') << endl;

    const int MAX_N = 200005;
    static vector<vector<Edge>> adj(MAX_N);

    int n = n_param;

    cout << "\n生成图..." << endl;
    generator(adj, n);

    int source = 1;
    int target = n;

    cout << "\n运行算法 (源点: " << source << ", 目标点: " << target << ")..." << endl;

    // 运行 Dijkstra
    int dijk_d1, dijk_d2;
    auto dijkstra_stats = dijkstra_second_shortest(adj, n, source, target, dijk_d1, dijk_d2);

    // 运行 SPFA
    int spfa_d1, spfa_d2;
    auto spfa_stats = spfa_second_shortest(adj, n, source, target, spfa_d1, spfa_d2);

    // 输出结果
    cout << "\n结果:" << endl;
    print_stats("Two-Distance Dijkstra", dijkstra_stats, dijk_d1, dijk_d2);
    cout << endl;
    print_stats("State-Extended SPFA", spfa_stats, spfa_d1, spfa_d2);

    // 验证正确性
    cout << "\n  >>> 正确性验证: ";
    if (dijk_d1 == spfa_d1 && dijk_d2 == spfa_d2) {
        cout << "✓ 两算法结果一致" << endl;
    } else {
        cout << "✗ 结果不一致！" << endl;
        cout << "      Dijkstra: d1=" << dijk_d1 << ", d2=" << dijk_d2 << endl;
        cout << "      SPFA:     d1=" << spfa_d1 << ", d2=" << spfa_d2 << endl;
    }

    print_comparison(dijkstra_stats, spfa_stats);
}

void run_grid_experiment(int height, int width) {
    cout << "\n" << string(60, '=') << endl;
    cout << "实验: 网格图 (Grid Graph) - 对抗性测试" << endl;
    cout << string(60, '=') << endl;

    const int MAX_N = 200005;
    static vector<vector<Edge>> adj(MAX_N);

    int n;

    cout << "\n生成图..." << endl;
    generate_grid_graph(adj, height, width, n);

    int source = 1;
    int target = n;

    cout << "\n运行算法 (源点: " << source << ", 目标点: " << target << ")..." << endl;

    // 运行 Dijkstra
    int dijk_d1, dijk_d2;
    auto dijkstra_stats = dijkstra_second_shortest(adj, n, source, target, dijk_d1, dijk_d2);

    // 运行 SPFA
    int spfa_d1, spfa_d2;
    auto spfa_stats = spfa_second_shortest(adj, n, source, target, spfa_d1, spfa_d2);

    // 输出结果
    cout << "\n结果:" << endl;
    print_stats("Two-Distance Dijkstra", dijkstra_stats, dijk_d1, dijk_d2);
    cout << endl;
    print_stats("State-Extended SPFA", spfa_stats, spfa_d1, spfa_d2);

    // 验证正确性
    cout << "\n  >>> 正确性验证: ";
    if (dijk_d1 == spfa_d1 && dijk_d2 == spfa_d2) {
        cout << "✓ 两算法结果一致" << endl;
    } else {
        cout << "✗ 结果不一致！" << endl;
        cout << "      Dijkstra: d1=" << dijk_d1 << ", d2=" << dijk_d2 << endl;
        cout << "      SPFA:     d1=" << spfa_d1 << ", d2=" << spfa_d2 << endl;
    }

    print_comparison(dijkstra_stats, spfa_stats);
}

// ============================================================================
// 主函数
// ============================================================================

int main() {
    cout << string(60, '=') << endl;
    cout << "次短路径算法 Benchmark" << endl;
    cout << "Two-Distance Dijkstra vs State-Extended SPFA" << endl;
    cout << string(60, '=') << endl;

    // 实验1：稠密图
    // 预期: Dijkstra 应该显著快于 SPFA
    run_experiment(
        "稠密图 (Dense Graph)",
        [](vector<vector<Edge>>& adj, int& n) {
            generate_dense_graph(adj, n);
        },
        3000  // N = 3000, M ≈ 1,800,000
    );

    // 实验2：稀疏图
    // 预期: 两者性能可能相近，SPFA 可能稍快
    run_experiment(
        "稀疏图 (Sparse Graph)",
        [](vector<vector<Edge>>& adj, int& n) {
            generate_sparse_graph(adj, n);
        },
        10000  // N = 10000, M ≈ 50,000
    );

    // 实验3：网格图 (对抗性测试)
    // 预期: Dijkstra 应该比 SPFA 快很多倍
    run_grid_experiment(100, 100);  // 100x100 网格，10000 节点

    // 实验4：更大的网格图
    run_grid_experiment(150, 150);  // 150x150 网格，22500 节点

    // 实验5：更大的网格图 - 与最短路径对比
    run_grid_experiment(200, 200);  // 200x200 网格，40000 节点

    // 实验6-9：继续扩大规模
    run_grid_experiment(250, 250);  // 62500 节点
    run_grid_experiment(300, 300);  // 90000 节点
    run_grid_experiment(350, 350);  // 122500 节点
    run_grid_experiment(400, 400);  // 160000 节点

    cout << "\n" << string(60, '=') << endl;
    cout << "Benchmark 完成" << endl;
    cout << string(60, '=') << endl;

    return 0;
}
