/**
 * 第二短路径问题的C++算法实现
 * 
 * 包含两个主要算法：
 * 1. State-Extended SPFA (使用FIFO队列)
 * 2. Two-Distance Dijkstra (使用优先队列)
 * 
 * 编译命令: g++ -std=c++17 -O2 second_shortest_path_algorithms.cpp -o second_shortest_path
 * 运行命令: ./second_shortest_path
 */

#include <iostream>
#include <vector>
#include <unordered_map>
#include <deque>
#include <queue>
#include <optional>
#include <limits>
#include <stdexcept>
#include <iomanip>

// ============================================================================
// State-Extended SPFA算法实现
// ============================================================================

/**
 * State-Extended SPFA算法类
 * 
 * 通过扩展状态空间来维护每个节点的最短和次短距离。
 * 使用FIFO队列进行Bellman-Ford式的边松弛操作。
 * 
 * 理论复杂度:
 * - 平均情况: O(M)，其中M是边数
 * - 最坏情况: O(MN)，其中N是节点数
 */
class StateExtendedSPFA {
public:
    /**
     * 初始化算法
     * 
     * @param graph 图的邻接表表示，格式为 {node: [(neighbor, weight), ...]}
     */
    explicit StateExtendedSPFA(
        const std::unordered_map<int, std::vector<std::pair<int, int>>>& graph
    );

    /**
     * 查找从源点到目标点的最短和次短路径长度
     * 
     * @param source 源节点
     * @param target 目标节点
     * @return (最短距离, 次短距离) 对，如果不存在路径则为 std::nullopt
     * @throws std::invalid_argument 如果源点或目标点不在图中
     */
    std::pair<std::optional<long long>, std::optional<long long>> findSecondShortest(
        int source,
        int target
    );

    /**
     * 获取算法运行的统计信息
     * 
     * @return 包含统计信息的字典
     */
    std::unordered_map<std::string, long long> getStatistics() const;

private:
    /**
     * 执行边松弛操作
     */
    void relaxEdge(
        int u,
        int v,
        int weight,
        long long currentDist,
        std::vector<long long>& d1,
        std::vector<long long>& d2,
        std::deque<std::tuple<int, long long, bool>>& queue,
        std::vector<std::vector<bool>>& inQueue
    );

    // 统计计数器
    long long enqueueOperations_ = 0;
    long long dequeueOperations_ = 0;
    long long pushCount_ = 0;
    long long popCount_ = 0;
    long long edgeRelaxations_ = 0;
    long long d1Updates_ = 0;
    long long d2Updates_ = 0;
    long long iterations_ = 0;

    const std::unordered_map<int, std::vector<std::pair<int, int>>>& graph_;
    int n_;
    std::unordered_map<int, int> nodeToIndex_;
};

// StateExtendedSPFA实现
StateExtendedSPFA::StateExtendedSPFA(
    const std::unordered_map<int, std::vector<std::pair<int, int>>>& graph
) : graph_(graph), n_(graph.size()) {
    int index = 0;
    for (const auto& [node, _] : graph_) {
        nodeToIndex_[node] = index++;
    }
}

std::pair<std::optional<long long>, std::optional<long long>> StateExtendedSPFA::findSecondShortest(
    int source,
    int target
) {
    if (graph_.find(source) == graph_.end()) {
        throw std::invalid_argument("源节点 " + std::to_string(source) + " 不在图中");
    }
    if (graph_.find(target) == graph_.end()) {
        throw std::invalid_argument("目标节点 " + std::to_string(target) + " 不在图中");
    }

    // 重置统计计数器
    enqueueOperations_ = 0;
    dequeueOperations_ = 0;
    pushCount_ = 0;
    popCount_ = 0;
    edgeRelaxations_ = 0;
    d1Updates_ = 0;
    d2Updates_ = 0;
    iterations_ = 0;

    // 初始化距离数组
    const long long INF = std::numeric_limits<long long>::max() / 2;
    std::vector<long long> d1(n_, INF);  // 最短距离
    std::vector<long long> d2(n_, INF);  // 次短距离

    int sourceIdx = nodeToIndex_.at(source);
    int targetIdx = nodeToIndex_.at(target);

    // FIFO队列: (node_index, distance, is_second)
    std::deque<std::tuple<int, long long, bool>> queue;
    queue.push_back({sourceIdx, 0, false});
    d1[sourceIdx] = 0;

    // 记录节点是否在队列中 [in_queue_d1, in_queue_d2]
    std::vector<std::vector<bool>> inQueue(n_, std::vector<bool>(2, false));
    inQueue[sourceIdx][0] = true;

    enqueueOperations_++;
    pushCount_++;

    while (!queue.empty()) {
        iterations_++;
        auto [u, dist, isSecond] = queue.front();
        queue.pop_front();
        dequeueOperations_++;
        popCount_++;

        // 标记节点已出队
        if (isSecond) {
            inQueue[u][1] = false;
        } else {
            inQueue[u][0] = false;
        }

        // 跳过过时的状态
        if (isSecond && dist > d2[u]) {
            continue;
        }
        if (!isSecond && dist > d1[u]) {
            continue;
        }

        // 获取原始节点ID
        int uNode = source;
        for (const auto& [node, idx] : nodeToIndex_) {
            if (idx == u) {
                uNode = node;
                break;
            }
        }

        // 松弛所有出边
        if (graph_.find(uNode) != graph_.end()) {
            for (const auto& [v, weight] : graph_.at(uNode)) {
                int vIdx = nodeToIndex_.at(v);
                relaxEdge(u, vIdx, weight, dist, d1, d2, queue, inQueue);
            }
        }
    }

    // 返回结果
    std::optional<long long> shortest = (d1[targetIdx] < INF) ? 
        std::optional<long long>(d1[targetIdx]) : std::nullopt;
    std::optional<long long> secondShortest = (d2[targetIdx] < INF) ? 
        std::optional<long long>(d2[targetIdx]) : std::nullopt;

    return {shortest, secondShortest};
}

void StateExtendedSPFA::relaxEdge(
    int u,
    int v,
    int weight,
    long long currentDist,
    std::vector<long long>& d1,
    std::vector<long long>& d2,
    std::deque<std::tuple<int, long long, bool>>& queue,
    std::vector<std::vector<bool>>& inQueue
) {
    edgeRelaxations_++;
    long long newDist = currentDist + weight;
    const long long INF = std::numeric_limits<long long>::max() / 2;

    // 如果找到更短的路径
    if (newDist < d1[v]) {
        long long oldD1 = d1[v];
        d2[v] = oldD1;
        d1[v] = newDist;
        d1Updates_++;

        // 将节点加入队列（如果不在队列中）
        if (!inQueue[v][0]) {
            queue.push_back({v, d1[v], false});
            inQueue[v][0] = true;
            enqueueOperations_++;
            pushCount_++;
        }

        if (d2[v] != INF && !inQueue[v][1]) {
            queue.push_back({v, d2[v], true});
            inQueue[v][1] = true;
            enqueueOperations_++;
            pushCount_++;
            if (oldD1 != INF) {
                d2Updates_++;
            }
        }
    }
    // 如果找到次短路径
    else if (d1[v] < newDist && newDist < d2[v]) {
        d2[v] = newDist;
        d2Updates_++;

        if (!inQueue[v][1]) {
            queue.push_back({v, d2[v], true});
            inQueue[v][1] = true;
            enqueueOperations_++;
            pushCount_++;
        }
    }
}

std::unordered_map<std::string, long long> StateExtendedSPFA::getStatistics() const {
    return {
        {"enqueue_operations", enqueueOperations_},
        {"dequeue_operations", dequeueOperations_},
        {"push_count", pushCount_},
        {"pop_count", popCount_},
        {"edge_relaxations", edgeRelaxations_},
        {"d1_updates", d1Updates_},
        {"d2_updates", d2Updates_},
        {"iterations", iterations_}
    };
}

// ============================================================================
// Two-Distance Dijkstra算法实现
// ============================================================================

/**
 * Two-Distance Dijkstra算法类
 * 
 * 为每个节点维护两个距离值：
 * - d1[v]: 从源点到节点v的最短距离
 * - d2[v]: 从源点到节点v的次短距离
 * 
 * 使用最小堆优先队列进行高效的节点选择。
 * 
 * 理论复杂度: O(M log N)，其中M是边数，N是节点数
 */
class TwoDistanceDijkstra {
private:
    /**
     * 优先队列中的元素结构
     */
    struct PQElement {
        long long distance;
        int node;
        bool isSecond;

        bool operator>(const PQElement& other) const {
            return distance > other.distance;
        }
    };

public:
    /**
     * 初始化算法
     */
    explicit TwoDistanceDijkstra(
        const std::unordered_map<int, std::vector<std::pair<int, int>>>& graph
    );

    /**
     * 查找从源点到目标点的最短和次短路径长度
     */
    std::pair<std::optional<long long>, std::optional<long long>> findSecondShortest(
        int source,
        int target
    );

    /**
     * 获取算法运行的统计信息
     */
    std::unordered_map<std::string, long long> getStatistics() const;

private:
    /**
     * 执行边松弛操作
     */
    void relaxEdge(
        int u,
        int v,
        int weight,
        long long currentDist,
        std::vector<long long>& d1,
        std::vector<long long>& d2,
        std::priority_queue<PQElement, std::vector<PQElement>, std::greater<PQElement>>& pq
    );

    long long pqOperations_ = 0;
    long long pushCount_ = 0;
    long long popCount_ = 0;
    long long edgeRelaxations_ = 0;
    long long d1Updates_ = 0;
    long long d2Updates_ = 0;
    long long iterations_ = 0;

    const std::unordered_map<int, std::vector<std::pair<int, int>>>& graph_;
    int n_;
    std::unordered_map<int, int> nodeToIndex_;
};

// TwoDistanceDijkstra实现
TwoDistanceDijkstra::TwoDistanceDijkstra(
    const std::unordered_map<int, std::vector<std::pair<int, int>>>& graph
) : graph_(graph), n_(graph.size()) {
    int index = 0;
    for (const auto& [node, _] : graph_) {
        nodeToIndex_[node] = index++;
    }
}

std::pair<std::optional<long long>, std::optional<long long>> TwoDistanceDijkstra::findSecondShortest(
    int source,
    int target
) {
    if (graph_.find(source) == graph_.end()) {
        throw std::invalid_argument("源节点 " + std::to_string(source) + " 不在图中");
    }
    if (graph_.find(target) == graph_.end()) {
        throw std::invalid_argument("目标节点 " + std::to_string(target) + " 不在图中");
    }

    // 重置统计计数器
    pqOperations_ = 0;
    pushCount_ = 0;
    popCount_ = 0;
    edgeRelaxations_ = 0;
    d1Updates_ = 0;
    d2Updates_ = 0;
    iterations_ = 0;

    const long long INF = std::numeric_limits<long long>::max() / 2;
    std::vector<long long> d1(n_, INF);
    std::vector<long long> d2(n_, INF);

    int sourceIdx = nodeToIndex_.at(source);
    int targetIdx = nodeToIndex_.at(target);

    // 优先队列: (distance, node_index, is_second)
    std::priority_queue<PQElement, std::vector<PQElement>, std::greater<PQElement>> pq;
    pq.push({0, sourceIdx, false});
    d1[sourceIdx] = 0;
    pqOperations_++;
    pushCount_++;

    while (!pq.empty()) {
        iterations_++;
        auto [dist, u, isSecond] = pq.top();
        pq.pop();
        pqOperations_++;
        popCount_++;

        // 如果已经找到目标的次短路径，可以提前终止
        if (u == targetIdx && isSecond) {
            break;
        }

        // 跳过过时的状态
        if (isSecond && dist > d2[u]) {
            continue;
        }
        if (!isSecond && dist > d1[u]) {
            continue;
        }

        // 获取原始节点ID
        int uNode = source;
        for (const auto& [node, idx] : nodeToIndex_) {
            if (idx == u) {
                uNode = node;
                break;
            }
        }

        // 松弛所有出边
        if (graph_.find(uNode) != graph_.end()) {
            for (const auto& [v, weight] : graph_.at(uNode)) {
                int vIdx = nodeToIndex_.at(v);
                relaxEdge(u, vIdx, weight, dist, d1, d2, pq);
            }
        }
    }

    std::optional<long long> shortest = (d1[targetIdx] < INF) ? 
        std::optional<long long>(d1[targetIdx]) : std::nullopt;
    std::optional<long long> secondShortest = (d2[targetIdx] < INF) ? 
        std::optional<long long>(d2[targetIdx]) : std::nullopt;

    return {shortest, secondShortest};
}

void TwoDistanceDijkstra::relaxEdge(
    int u,
    int v,
    int weight,
    long long currentDist,
    std::vector<long long>& d1,
    std::vector<long long>& d2,
    std::priority_queue<PQElement, std::vector<PQElement>, std::greater<PQElement>>& pq
) {
    edgeRelaxations_++;
    long long newDist = currentDist + weight;
    const long long INF = std::numeric_limits<long long>::max() / 2;

    if (newDist < d1[v]) {
        long long oldD1 = d1[v];
        d2[v] = oldD1;
        d1[v] = newDist;
        d1Updates_++;

        pq.push({d1[v], v, false});
        pqOperations_++;
        pushCount_++;

        if (d2[v] != INF) {
            pq.push({d2[v], v, true});
            pqOperations_++;
            pushCount_++;
            if (oldD1 != INF) {
                d2Updates_++;
            }
        }
    } else if (d1[v] < newDist && newDist < d2[v]) {
        d2[v] = newDist;
        d2Updates_++;
        pq.push({d2[v], v, true});
        pqOperations_++;
        pushCount_++;
    }
}

std::unordered_map<std::string, long long> TwoDistanceDijkstra::getStatistics() const {
    return {
        {"pq_operations", pqOperations_},
        {"push_count", pushCount_},
        {"pop_count", popCount_},
        {"edge_relaxations", edgeRelaxations_},
        {"d1_updates", d1Updates_},
        {"d2_updates", d2Updates_},
        {"iterations", iterations_}
    };
}

// ============================================================================
// 测试和演示代码
// ============================================================================

void printStatistics(
    const std::string& algorithmName,
    const std::unordered_map<std::string, long long>& stats
) {
    std::cout << "\n" << algorithmName << " 统计信息:\n";
    std::cout << std::string(50, '-') << "\n";
    for (const auto& [key, value] : stats) {
        std::cout << std::left << std::setw(30) << key 
                  << ": " << value << "\n";
    }
}

int main() {
    // 构造测试图
    std::unordered_map<int, std::vector<std::pair<int, int>>> graph = {
        {0, {{1, 1}, {2, 2}}},
        {1, {{2, 1}}},
        {2, {}}
    };

    std::cout << "=" << std::string(48, '=') << "\n";
    std::cout << "第二短路径问题 - C++算法实现演示\n";
    std::cout << "=" << std::string(48, '=') << "\n";

    std::cout << "\n测试图的邻接表表示:\n";
    std::cout << "  0 -> [(1, 1), (2, 2)]\n";
    std::cout << "  1 -> [(2, 1)]\n";
    std::cout << "  2 -> []\n";

    // 测试 StateExtendedSPFA
    std::cout << "\n" << std::string(50, '-') << "\n";
    std::cout << "State-Extended SPFA 算法\n";
    std::cout << std::string(50, '-') << "\n";
    
    StateExtendedSPFA spfa(graph);
    auto [shortest1, second1] = spfa.findSecondShortest(0, 2);
    
    std::cout << "查询: 从节点 0 到节点 2\n";
    std::cout << "最短路径: " << (shortest1 ? std::to_string(shortest1.value()) : "无") << "\n";
    std::cout << "次短路径: " << (second1 ? std::to_string(second1.value()) : "无") << "\n";
    
    printStatistics("State-Extended SPFA", spfa.getStatistics());

    // 测试 TwoDistanceDijkstra
    std::cout << "\n" << std::string(50, '-') << "\n";
    std::cout << "Two-Distance Dijkstra 算法\n";
    std::cout << std::string(50, '-') << "\n";
    
    TwoDistanceDijkstra dijkstra(graph);
    auto [shortest2, second2] = dijkstra.findSecondShortest(0, 2);
    
    std::cout << "查询: 从节点 0 到节点 2\n";
    std::cout << "最短路径: " << (shortest2 ? std::to_string(shortest2.value()) : "无") << "\n";
    std::cout << "次短路径: " << (second2 ? std::to_string(second2.value()) : "无") << "\n";
    
    printStatistics("Two-Distance Dijkstra", dijkstra.getStatistics());

    // 演示异常处理
    std::cout << "\n" << std::string(50, '-') << "\n";
    std::cout << "异常处理演示\n";
    std::cout << std::string(50, '-') << "\n";
    
    try {
        spfa.findSecondShortest(0, 999);  // 节点999不存在
    } catch (const std::invalid_argument& e) {
        std::cout << "捕获异常: " << e.what() << "\n";
    }

    std::cout << "\n" << std::string(50, '=') << "\n";
    std::cout << "演示完成\n";
    std::cout << "=" << std::string(48, '=') << "\n";

    return 0;
}
