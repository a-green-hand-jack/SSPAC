/**
 * C++ 版本的 LeetCode 实验运行脚本
 * 
 * 加载 LeetCode 测试数据，使用 C++ 算法实现运行性能测试
 * 保存详细的性能数据和统计信息到 JSON 和 CSV 文件
 * 不需要外部 JSON 库，仅使用 C++17 标准库
 * 
 * 编译命令：
 *   g++ -std=c++17 -O2 run_leetcode_experiments.cpp -o run_leetcode_experiments
 * 
 * 运行命令：
 *   ./run_leetcode_experiments --data data/leetcode/leetcode_second_shortest_path.json \
 *                              --output results/leetcode_experiments
 */

#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <unordered_map>
#include <string>
#include <chrono>
#include <optional>
#include <iomanip>
#include <filesystem>
#include <algorithm>
#include <cmath>
#include <deque>
#include <queue>
#include <limits>

namespace fs = std::filesystem;

// ============================================================================
// 简单的 JSON 解析和生成
// ============================================================================

class SimpleJson {
public:
    std::string str;
    
    static std::string escape(const std::string& s) {
        std::string result;
        for (char c : s) {
            if (c == '"') result += "\\\"";
            else if (c == '\\') result += "\\\\";
            else if (c == '\n') result += "\\n";
            else if (c == '\r') result += "\\r";
            else result += c;
        }
        return result;
    }
    
    static std::string toString(const std::string& value) {
        return "\"" + escape(value) + "\"";
    }
    
    static std::string toString(double value) {
        std::ostringstream oss;
        oss << std::fixed << std::setprecision(9) << value;
        std::string result = oss.str();
        while (result.back() == '0') result.pop_back();
        if (result.back() == '.') result.pop_back();
        return result;
    }
    
    static std::string toString(int value) {
        return std::to_string(value);
    }
    
    static std::string toString(long long value) {
        return std::to_string(value);
    }
    
    static std::string toString(bool value) {
        return value ? "true" : "false";
    }
};

// ============================================================================
// C++ 算法实现（从 second_shortest_path_algorithms.cpp 中复制）
// ============================================================================

class StateExtendedSPFA {
public:
    explicit StateExtendedSPFA(
        const std::unordered_map<int, std::vector<std::pair<int, int>>>& graph
    ) : graph_(graph), n_(graph.size()) {
        int index = 0;
        for (const auto& [node, _] : graph_) {
            nodeToIndex_[node] = index++;
        }
    }

    std::pair<std::optional<long long>, std::optional<long long>> findSecondShortest(
        int source,
        int target
    ) {
        if (graph_.find(source) == graph_.end()) {
            throw std::invalid_argument("Source node " + std::to_string(source) + " not in graph");
        }
        if (graph_.find(target) == graph_.end()) {
            throw std::invalid_argument("Target node " + std::to_string(target) + " not in graph");
        }

        enqueueOperations_ = 0;
        dequeueOperations_ = 0;
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

        std::deque<std::tuple<int, long long, bool>> queue;
        queue.push_back({sourceIdx, 0, false});
        d1[sourceIdx] = 0;

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

            if (isSecond) {
                inQueue[u][1] = false;
            } else {
                inQueue[u][0] = false;
            }

            if (isSecond && dist > d2[u]) {
                continue;
            }
            if (!isSecond && dist > d1[u]) {
                continue;
            }

            int uNode = source;
            for (const auto& [node, idx] : nodeToIndex_) {
                if (idx == u) {
                    uNode = node;
                    break;
                }
            }

            if (graph_.find(uNode) != graph_.end()) {
                for (const auto& [v, weight] : graph_.at(uNode)) {
                    int vIdx = nodeToIndex_.at(v);
                    relaxEdge(u, vIdx, weight, dist, d1, d2, queue, inQueue);
                }
            }
        }

        std::optional<long long> shortest = (d1[targetIdx] < INF) ? 
            std::optional<long long>(d1[targetIdx]) : std::nullopt;
        std::optional<long long> secondShortest = (d2[targetIdx] < INF) ? 
            std::optional<long long>(d2[targetIdx]) : std::nullopt;

        return {shortest, secondShortest};
    }

    std::unordered_map<std::string, long long> getStatistics() const {
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

private:
    void relaxEdge(
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

        if (newDist < d1[v]) {
            long long oldD1 = d1[v];
            d2[v] = oldD1;
            d1[v] = newDist;
            d1Updates_++;

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
        } else if (d1[v] < newDist && newDist < d2[v]) {
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

class TwoDistanceDijkstra {
private:
    struct PQElement {
        long long distance;
        int node;
        bool isSecond;

        bool operator>(const PQElement& other) const {
            return distance > other.distance;
        }
    };

public:
    explicit TwoDistanceDijkstra(
        const std::unordered_map<int, std::vector<std::pair<int, int>>>& graph
    ) : graph_(graph), n_(graph.size()) {
        int index = 0;
        for (const auto& [node, _] : graph_) {
            nodeToIndex_[node] = index++;
        }
    }

    std::pair<std::optional<long long>, std::optional<long long>> findSecondShortest(
        int source,
        int target
    ) {
        if (graph_.find(source) == graph_.end()) {
            throw std::invalid_argument("Source node " + std::to_string(source) + " not in graph");
        }
        if (graph_.find(target) == graph_.end()) {
            throw std::invalid_argument("Target node " + std::to_string(target) + " not in graph");
        }

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

            if (u == targetIdx && isSecond) {
                break;
            }

            if (isSecond && dist > d2[u]) {
                continue;
            }
            if (!isSecond && dist > d1[u]) {
                continue;
            }

            int uNode = source;
            for (const auto& [node, idx] : nodeToIndex_) {
                if (idx == u) {
                    uNode = node;
                    break;
                }
            }

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

    std::unordered_map<std::string, long long> getStatistics() const {
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

private:
    void relaxEdge(
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

// ============================================================================
// 工具函数
// ============================================================================

struct TestResult {
    int caseId;
    std::string name;
    int n;
    int m;
    bool hasExpected;
    
    double dijkstraTime;
    std::optional<long long> dijkstraShortest;
    std::optional<long long> dijkstraSecond;
    std::optional<bool> dijkstraCorrect;
    std::unordered_map<std::string, long long> dijkstraStats;
    
    double spfaTime;
    std::optional<long long> spfaShortest;
    std::optional<long long> spfaSecond;
    std::optional<bool> spfaCorrect;
    std::unordered_map<std::string, long long> spfaStats;
};

/**
 * 简单的 JSON 值解析
 */
std::string getJsonString(const std::string& json, const std::string& key) {
    size_t pos = json.find("\"" + key + "\"");
    if (pos == std::string::npos) return "";
    
    pos = json.find(":", pos);
    if (pos == std::string::npos) return "";
    
    pos = json.find("\"", pos);
    if (pos == std::string::npos) return "";
    
    size_t end = json.find("\"", pos + 1);
    if (end == std::string::npos) return "";
    
    return json.substr(pos + 1, end - pos - 1);
}

int getJsonInt(const std::string& json, const std::string& key) {
    size_t pos = json.find("\"" + key + "\"");
    if (pos == std::string::npos) return 0;
    
    pos = json.find(":", pos);
    if (pos == std::string::npos) return 0;
    
    while (pos < json.size() && (json[pos] == ':' || json[pos] == ' ')) pos++;
    
    size_t end = pos;
    while (end < json.size() && std::isdigit(json[end])) end++;
    
    return std::stoi(json.substr(pos, end - pos));
}

std::vector<std::pair<int, int>> getJsonEdges(const std::string& json) {
    std::vector<std::pair<int, int>> edges;
    
    size_t pos = json.find("\"edges\"");
    if (pos == std::string::npos) return edges;
    
    pos = json.find("[", pos);
    size_t end = json.find("]", pos);
    
    std::string edgesStr = json.substr(pos + 1, end - pos - 1);
    
    size_t start = 0;
    while ((pos = edgesStr.find("[", start)) != std::string::npos) {
        size_t edgeEnd = edgesStr.find("]", pos);
        std::string edgeStr = edgesStr.substr(pos + 1, edgeEnd - pos - 1);
        
        size_t comma = edgeStr.find(",");
        int u = std::stoi(edgeStr.substr(0, comma));
        int v = std::stoi(edgeStr.substr(comma + 1));
        
        edges.push_back({u, v});
        start = edgeEnd + 1;
    }
    
    return edges;
}

/**
 * 将 LeetCode 测试用例转换为图表示
 */
std::tuple<
    std::unordered_map<int, std::vector<std::pair<int, int>>>,
    int,
    int
> convertLeetcodeToGraph(const std::string& testCaseJson) {
    int n = getJsonInt(testCaseJson, "n");
    int source = getJsonInt(testCaseJson, "source");
    int target = getJsonInt(testCaseJson, "target");
    
    std::unordered_map<int, std::vector<std::pair<int, int>>> graph;
    
    for (int i = 1; i <= n; i++) {
        graph[i] = {};
    }
    
    auto edges = getJsonEdges(testCaseJson);
    for (const auto& [u, v] : edges) {
        graph[u].push_back({v, 1});
        graph[v].push_back({u, 1});
    }
    
    return {graph, source, target};
}

/**
 * 格式化时间为可读字符串
 */
std::string formatTime(double seconds) {
    if (seconds >= 1.0) {
        return std::to_string(static_cast<int>(seconds * 1000)) + "ms";
    } else if (seconds >= 0.001) {
        std::ostringstream oss;
        oss << std::fixed << std::setprecision(2) << (seconds * 1000) << "ms";
        return oss.str();
    } else {
        std::ostringstream oss;
        oss << std::fixed << std::setprecision(2) << (seconds * 1000000) << "us";
        return oss.str();
    }
}

/**
 * 读取整个 JSON 文件
 */
std::string readJsonFile(const std::string& filename) {
    std::ifstream file(filename);
    if (!file.is_open()) {
        throw std::runtime_error("Cannot open file: " + filename);
    }
    
    std::stringstream buffer;
    buffer << file.rdbuf();
    return buffer.str();
}

/**
 * 提取测试用例数组
 */
std::vector<std::string> extractTestCases(const std::string& json) {
    std::vector<std::string> testCases;
    
    size_t pos = json.find("\"test_cases\"");
    if (pos == std::string::npos) return testCases;
    
    pos = json.find("[", pos);
    size_t end = json.rfind("]");
    
    std::string casesStr = json.substr(pos + 1, end - pos - 1);
    
    int braceCount = 0;
    size_t start = 0;
    
    for (size_t i = 0; i < casesStr.size(); i++) {
        if (casesStr[i] == '{') {
            if (braceCount == 0) start = i;
            braceCount++;
        } else if (casesStr[i] == '}') {
            braceCount--;
            if (braceCount == 0) {
                testCases.push_back(casesStr.substr(start, i - start + 1));
            }
        }
    }
    
    return testCases;
}

/**
 * 保存 CSV 结果
 */
void saveCsvResults(
    const std::vector<TestResult>& results,
    const fs::path& outputPath
) {
    std::ofstream file(outputPath);
    
    file << "case_id,name,n,m,dijkstra_time_ms,dijkstra_shortest,dijkstra_second,"
         << "dijkstra_correct,dijkstra_pq_ops,dijkstra_push,dijkstra_pop,"
         << "dijkstra_edge_relax,dijkstra_d1_updates,dijkstra_d2_updates,"
         << "spfa_time_ms,spfa_shortest,spfa_second,"
         << "spfa_correct,spfa_queue_ops,spfa_push,spfa_pop,"
         << "spfa_edge_relax,spfa_d1_updates,spfa_d2_updates\n";
    
    for (const auto& row : results) {
        file << row.caseId << ","
             << row.name << ","
             << row.n << ","
             << row.m << ","
             << (row.dijkstraTime * 1000.0) << ","
             << (row.dijkstraShortest ? std::to_string(row.dijkstraShortest.value()) : "-1") << ","
             << (row.dijkstraSecond ? std::to_string(row.dijkstraSecond.value()) : "-1") << ","
             << (row.dijkstraCorrect ? (row.dijkstraCorrect.value() ? "true" : "false") : "N/A") << ","
             << row.dijkstraStats.at("pq_operations") << ","
             << row.dijkstraStats.at("push_count") << ","
             << row.dijkstraStats.at("pop_count") << ","
             << row.dijkstraStats.at("edge_relaxations") << ","
             << row.dijkstraStats.at("d1_updates") << ","
             << row.dijkstraStats.at("d2_updates") << ","
             << (row.spfaTime * 1000.0) << ","
             << (row.spfaShortest ? std::to_string(row.spfaShortest.value()) : "-1") << ","
             << (row.spfaSecond ? std::to_string(row.spfaSecond.value()) : "-1") << ","
             << (row.spfaCorrect ? (row.spfaCorrect.value() ? "true" : "false") : "N/A") << ","
             << row.spfaStats.at("enqueue_operations") << ","
             << row.spfaStats.at("push_count") << ","
             << row.spfaStats.at("pop_count") << ","
             << row.spfaStats.at("edge_relaxations") << ","
             << row.spfaStats.at("d1_updates") << ","
             << row.spfaStats.at("d2_updates") << "\n";
    }
    
    file.close();
}

/**
 * 保存 JSON 结果
 */
void saveJsonResults(
    const std::vector<TestResult>& results,
    int officialCases,
    int dijkstraCorrect,
    int spfaCorrect,
    double avgDijkstraTime,
    double avgSpfaTime,
    const fs::path& outputPath
) {
    std::ofstream file(outputPath);
    
    file << "{\n";
    file << "  \"metadata\": {\n";
    file << "    \"total_cases\": " << results.size() << ",\n";
    file << "    \"official_cases\": " << officialCases << ",\n";
    file << "    \"generated_cases\": " << (results.size() - officialCases) << "\n";
    file << "  },\n";
    
    file << "  \"summary\": {\n";
    file << "    \"dijkstra\": {\n";
    file << "      \"avg_time\": " << avgDijkstraTime << ",\n";
    file << "      \"correct_count\": " << dijkstraCorrect << ",\n";
    file << "      \"total\": " << officialCases << ",\n";
    file << "      \"accuracy\": " << (officialCases > 0 ? (double)dijkstraCorrect / officialCases : 0) << "\n";
    file << "    },\n";
    file << "    \"spfa\": {\n";
    file << "      \"avg_time\": " << avgSpfaTime << ",\n";
    file << "      \"correct_count\": " << spfaCorrect << ",\n";
    file << "      \"total\": " << officialCases << ",\n";
    file << "      \"accuracy\": " << (officialCases > 0 ? (double)spfaCorrect / officialCases : 0) << "\n";
    file << "    }\n";
    file << "  },\n";
    
    file << "  \"details\": [\n";
    for (size_t i = 0; i < results.size(); i++) {
        const auto& row = results[i];
        file << "    {\n";
        file << "      \"case_id\": " << row.caseId << ",\n";
        file << "      \"name\": \"" << row.name << "\",\n";
        file << "      \"n\": " << row.n << ",\n";
        file << "      \"m\": " << row.m << ",\n";
        file << "      \"dijkstra_time\": " << row.dijkstraTime << ",\n";
        file << "      \"dijkstra_shortest\": " << (row.dijkstraShortest ? std::to_string(row.dijkstraShortest.value()) : "null") << ",\n";
        file << "      \"dijkstra_second\": " << (row.dijkstraSecond ? std::to_string(row.dijkstraSecond.value()) : "null") << ",\n";
        file << "      \"spfa_time\": " << row.spfaTime << ",\n";
        file << "      \"spfa_shortest\": " << (row.spfaShortest ? std::to_string(row.spfaShortest.value()) : "null") << ",\n";
        file << "      \"spfa_second\": " << (row.spfaSecond ? std::to_string(row.spfaSecond.value()) : "null") << "\n";
        file << "    }";
        if (i < results.size() - 1) file << ",";
        file << "\n";
    }
    file << "  ]\n";
    file << "}\n";
    
    file.close();
}

// ============================================================================
// 主程序
// ============================================================================

int main(int argc, char* argv[]) {
    std::string dataFile = "data/leetcode/leetcode_second_shortest_path.json";
    std::string outputDir = "results/leetcode_experiments";
    
    for (int i = 1; i < argc; i++) {
        std::string arg = argv[i];
        if (arg == "--data" && i + 1 < argc) {
            dataFile = argv[++i];
        } else if (arg == "--output" && i + 1 < argc) {
            outputDir = argv[++i];
        }
    }
    
    fs::path outputPath(outputDir);
    fs::path metricsDir = outputPath / "metrics";
    fs::create_directories(metricsDir);
    
    std::cout << std::string(70, '=') << "\n";
    std::cout << "C++ LeetCode 算法性能实验\n";
    std::cout << std::string(70, '=') << "\n\n";
    
    std::cout << "📥 加载数据: " << dataFile << "\n";
    
    std::string jsonContent;
    try {
        jsonContent = readJsonFile(dataFile);
    } catch (const std::exception& e) {
        std::cerr << "❌ 错误: " << e.what() << "\n";
        return 1;
    }
    
    auto testCaseJsons = extractTestCases(jsonContent);
    std::cout << "✅ 加载了 " << testCaseJsons.size() << " 个测试用例\n\n";
    
    std::cout << "🚀 开始运行实验...\n\n";
    
    std::vector<TestResult> results;
    int officialCases = 0;
    int dijkstraCorrect = 0;
    int spfaCorrect = 0;
    double totalDijkstraTime = 0;
    double totalSpfaTime = 0;
    
    for (size_t idx = 0; idx < testCaseJsons.size(); idx++) {
        const auto& testCaseJson = testCaseJsons[idx];
        
        int caseId = getJsonInt(testCaseJson, "id");
        if (caseId == 0) caseId = idx + 1;
        
        std::string name = getJsonString(testCaseJson, "name");
        if (name.empty()) name = "Test " + std::to_string(caseId);
        
        int n = getJsonInt(testCaseJson, "n");
        auto edges = getJsonEdges(testCaseJson);
        int m = edges.size();
        
        auto [graph, source, target] = convertLeetcodeToGraph(testCaseJson);
        
        bool hasExpected = testCaseJson.find("\"expected_shortest\"") != std::string::npos;
        
        std::optional<long long> expectedShortest = std::nullopt;
        std::optional<long long> expectedSecond = std::nullopt;
        
        if (hasExpected) {
            expectedShortest = getJsonInt(testCaseJson, "expected_shortest");
            expectedSecond = getJsonInt(testCaseJson, "expected_second_shortest");
            officialCases++;
        }
        
        std::cout << "[" << (idx + 1) << "/" << testCaseJsons.size() << "] " << name 
                 << " (n=" << n << ", m=" << m << ")\n";
        
        TestResult result;
        result.caseId = caseId;
        result.name = name;
        result.n = n;
        result.m = m;
        result.hasExpected = hasExpected;
        
        // 测试 Dijkstra
        try {
            TwoDistanceDijkstra dijkstra(graph);
            auto start = std::chrono::high_resolution_clock::now();
            auto [shortest, second] = dijkstra.findSecondShortest(source, target);
            auto end = std::chrono::high_resolution_clock::now();
            
            result.dijkstraShortest = shortest;
            result.dijkstraSecond = second;
            result.dijkstraTime = std::chrono::duration<double>(end - start).count();
            result.dijkstraStats = dijkstra.getStatistics();
        } catch (const std::exception& e) {
            std::cerr << "  Dijkstra 错误: " << e.what() << "\n";
        }
        
        // 测试 SPFA
        try {
            StateExtendedSPFA spfa(graph);
            auto start = std::chrono::high_resolution_clock::now();
            auto [shortest, second] = spfa.findSecondShortest(source, target);
            auto end = std::chrono::high_resolution_clock::now();
            
            result.spfaShortest = shortest;
            result.spfaSecond = second;
            result.spfaTime = std::chrono::duration<double>(end - start).count();
            result.spfaStats = spfa.getStatistics();
        } catch (const std::exception& e) {
            std::cerr << "  SPFA 错误: " << e.what() << "\n";
        }
        
        totalDijkstraTime += result.dijkstraTime;
        totalSpfaTime += result.spfaTime;
        
        // 验证结果
        if (hasExpected) {
            bool dijkstraOk = (result.dijkstraShortest == expectedShortest && 
                               result.dijkstraSecond == expectedSecond);
            bool spfaOk = (result.spfaShortest == expectedShortest && 
                           result.spfaSecond == expectedSecond);
            
            result.dijkstraCorrect = dijkstraOk;
            result.spfaCorrect = spfaOk;
            
            if (dijkstraOk) dijkstraCorrect++;
            if (spfaOk) spfaCorrect++;
            
            std::cout << "  Dijkstra: " << (dijkstraOk ? "✅" : "❌")
                     << " 最短=" << (result.dijkstraShortest ? std::to_string(result.dijkstraShortest.value()) : "N/A")
                     << ", 次短=" << (result.dijkstraSecond ? std::to_string(result.dijkstraSecond.value()) : "N/A")
                     << " (耗时: " << formatTime(result.dijkstraTime) << ")\n";
            
            std::cout << "  SPFA:     " << (spfaOk ? "✅" : "❌")
                     << " 最短=" << (result.spfaShortest ? std::to_string(result.spfaShortest.value()) : "N/A")
                     << ", 次短=" << (result.spfaSecond ? std::to_string(result.spfaSecond.value()) : "N/A")
                     << " (耗时: " << formatTime(result.spfaTime) << ")\n";
        } else {
            std::cout << "  Dijkstra: 最短=" << (result.dijkstraShortest ? std::to_string(result.dijkstraShortest.value()) : "N/A")
                     << ", 次短=" << (result.dijkstraSecond ? std::to_string(result.dijkstraSecond.value()) : "N/A")
                     << " (耗时: " << formatTime(result.dijkstraTime) << ")\n";
            
            std::cout << "  SPFA:     最短=" << (result.spfaShortest ? std::to_string(result.spfaShortest.value()) : "N/A")
                     << ", 次短=" << (result.spfaSecond ? std::to_string(result.spfaSecond.value()) : "N/A")
                     << " (耗时: " << formatTime(result.spfaTime) << ")\n";
        }
        
        std::cout << "\n";
        
        results.push_back(result);
    }
    
    // 生成总结
    std::cout << std::string(70, '=') << "\n";
    std::cout << "实验总结\n";
    std::cout << std::string(70, '=') << "\n\n";
    
    std::cout << "📊 官方测试用例:\n"
             << "  总数: " << officialCases << "\n"
             << "  Dijkstra 通过: " << dijkstraCorrect << "/" << officialCases << "\n"
             << "  SPFA 通过: " << spfaCorrect << "/" << officialCases << "\n";
    
    if (officialCases > 0) {
        std::cout << "  Dijkstra 正确率: " << (100.0 * dijkstraCorrect / officialCases) << "%\n"
                 << "  SPFA 正确率: " << (100.0 * spfaCorrect / officialCases) << "%\n";
    }
    
    std::cout << "\n⚡ 性能对比:\n";
    
    double avgDijkstraTime = results.size() > 0 ? totalDijkstraTime / results.size() : 0;
    double avgSpfaTime = results.size() > 0 ? totalSpfaTime / results.size() : 0;
    
    std::cout << "  Dijkstra 平均耗时: " << formatTime(avgDijkstraTime) << "\n"
             << "  SPFA 平均耗时: " << formatTime(avgSpfaTime) << "\n";
    
    if (avgDijkstraTime > 0 && avgSpfaTime > 0) {
        double speedup = avgDijkstraTime / avgSpfaTime;
        std::string faster = speedup > 1 ? "SPFA" : "Dijkstra";
        double ratio = speedup > 1 ? (speedup - 1) * 100 : (1.0 / speedup - 1) * 100;
        std::cout << "  " << faster << " 快 " << ratio << "%\n";
    }
    
    std::cout << "\n" << std::string(70, '=') << "\n";
    
    // 保存结果
    std::cout << "\n💾 保存报告...\n\n";
    
    fs::path jsonPath = metricsDir / "leetcode_report.json";
    saveJsonResults(results, officialCases, dijkstraCorrect, spfaCorrect, 
                   avgDijkstraTime, avgSpfaTime, jsonPath);
    std::cout << "✅ JSON 报告: " << jsonPath << "\n";
    
    fs::path csvPath = metricsDir / "leetcode_results.csv";
    saveCsvResults(results, csvPath);
    std::cout << "✅ CSV 报告: " << csvPath << "\n";
    
    std::cout << "\n" << std::string(70, '=') << "\n";
    std::cout << "✅ 实验完成！\n";
    std::cout << "📁 结果保存在: " << outputPath << "\n";
    std::cout << std::string(70, '=') << "\n";
    
    return 0;
}
