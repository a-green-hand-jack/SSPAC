由于您提供的洛谷链接（https://www.google.com/url?sa=E\&source=gmail\&q=luogu.com.cn）当前无法直接抓取内容（受限于网站的安全策略），我已通过搜索引擎查阅了该题目（**洛谷 P2865 [USACO06NOV] Roadblocks G**）在其他技术博客（CSDN、博客园）上的题解。

这道题是经典的 **“严格次短路”** 问题。目标是求从起点 $1$ 到终点 $N$ 的路径长度，该长度必须严格大于最短路长度，且是所有满足该条件的路径中最小的。

以下是从网络资源中提取并整理的基于 **SPFA** 和 **Dijkstra** 两种算法的 C++ 实现代码及说明。

### 1\. 基于 SPFA 算法的实现

SPFA 算法通常用于求单源最短路，但在求次短路时，我们需要同时维护 **最短路数组 (`dist1`)** 和 **次短路数组 (`dist2`)**。在松弛操作时，不仅更新最短路，还要根据情况更新次短路。

**核心逻辑：**
对于每一条边 $(u, v)$ 及其权值 $w$：

1.  如果 $dist1[u] + w < dist1[v]$：更新 $dist1[v]$，并将**旧的** $dist1[v]$ 赋值给 $dist2[v]$（因为旧的最短路变成了次短路）。
2.  如果 $dist1[u] + w > dist1[v]$ 且 $dist1[u] + w < dist2[v]$：直接更新 $dist2[v]$（发现了介于最短和次短之间的新路径）。
3.  如果 $dist2[u] + w < dist2[v]$：尝试用 $u$ 的次短路来更新 $v$ 的次短路。

**代码实现：**

```cpp
#include <iostream>
#include <vector>
#include <queue>
#include <cstring>

using namespace std;

const int MAXN = 5005;
const int INF = 0x3f3f3f3f;

struct Edge {
    int v, w;
};

vector<Edge> adj[MAXN];
int dist1[MAXN]; // 最短路
int dist2[MAXN]; // 次短路
bool in_queue[MAXN];
int n, m;

void spfa() {
    memset(dist1, 0x3f, sizeof(dist1));
    memset(dist2, 0x3f, sizeof(dist2));
    memset(in_queue, 0, sizeof(in_queue));

    queue<int> q;
    q.push(1);
    dist1[1] = 0;
    in_queue[1] = true;

    while (!q.empty()) {
        int u = q.front();
        q.pop();
        in_queue[u] = false;

        for (auto& edge : adj[u]) {
            int v = edge.v;
            int w = edge.w;

            // 情况1：发现更短的最短路
            if (dist1[u] + w < dist1[v]) {
                dist2[v] = dist1[v]; // 原最短路变为次短路
                dist1[v] = dist1[u] + w;
                if (!in_queue[v]) {
                    q.push(v);
                    in_queue[v] = true;
                }
            }
            // 情况2：发现严格次短路（大于最短路但小于当前次短路）
            if (dist1[u] + w > dist1[v] && dist1[u] + w < dist2[v]) {
                dist2[v] = dist1[u] + w;
                if (!in_queue[v]) {
                    q.push(v);
                    in_queue[v] = true;
                }
            }
            // 情况3：利用u的次短路更新v的次短路
            if (dist2[u] + w < dist2[v]) {
                dist2[v] = dist2[u] + w;
                if (!in_queue[v]) {
                    q.push(v);
                    in_queue[v] = true;
                }
            }
        }
    }
}

int main() {
    cin >> n >> m;
    for (int i = 0; i < m; i++) {
        int u, v, w;
        cin >> u >> v >> w;
        adj[u].push_back({v, w});
        adj[v].push_back({u, w}); // 双向边
    }

    spfa();

    cout << dist2[n] << endl;
    return 0;
}
```

-----

### 2\. 基于 Dijkstra 算法的实现

Dijkstra 算法通常效率更高且更稳定。同样的，我们需要维护两个距离数组。使用优先队列（最小堆）存储状态，状态中包含当前距离 `d` 和节点 `u`。

**核心逻辑：**
从优先队列取出 $(d, u)$：

1.  如果 $d > dist2[u]$，直接跳过（剪枝）。
2.  遍历邻居 $v$，计算新距离 $new\_dist = d + w$。
3.  如果 $new\_dist < dist1[v]$：
      - 将原 $dist1[v]$ 交换给 $new\_dist$（原最短路“退化”为次短路候选）。
      - 更新 $dist1[v]$，并将新状态入队。
      - 此时 $new\_dist$ 持有的是旧的最短路值，继续判断是否能更新 $dist2[v]$。
4.  如果 $new\_dist < dist2[v]$ 且 $new\_dist > dist1[v]$：
      - 更新 $dist2[v]$ 并入队。

**代码实现：**

```cpp
#include <iostream>
#include <vector>
#include <queue>
#include <cstring>

using namespace std;

const int MAXN = 5005;
const int INF = 0x3f3f3f3f;

struct Edge {
    int v, w;
};

struct Node {
    int id, dist;
    // 优先队列为小根堆，需要重载 > 运算符
    bool operator>(const Node& other) const {
        return dist > other.dist;
    }
};

vector<Edge> adj[MAXN];
int dist1[MAXN]; // 最短路
int dist2[MAXN]; // 次短路
int n, m;

void dijkstra() {
    memset(dist1, 0x3f, sizeof(dist1));
    memset(dist2, 0x3f, sizeof(dist2));
    
    priority_queue<Node, vector<Node>, greater<Node>> pq;
    
    dist1[1] = 0;
    pq.push({1, 0});

    while (!pq.empty()) {
        Node t = pq.top();
        pq.pop();
        
        int u = t.id;
        int d = t.dist;

        // 如果当前取出的距离比次短路还大，则无更新意义
        if (d > dist2[u]) continue;

        for (auto& edge : adj[u]) {
            int v = edge.v;
            int w = edge.w;
            int new_dist = d + w;

            // 如果比最短路还短
            if (new_dist < dist1[v]) {
                // 原最短路变成次短路
                swap(new_dist, dist1[v]); 
                pq.push({v, dist1[v]}); // 将新的最短路入队
                // 此时 new_dist 变成了原来的 dist1[v]的值，继续向下判断是否更新次短路
            }

            // 如果比次短路短，且比最短路长（严格次短）
            if (new_dist < dist2[v] && new_dist > dist1[v]) {
                dist2[v] = new_dist;
                pq.push({v, dist2[v]});
            }
        }
    }
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(0);
    
    cin >> n >> m;
    for (int i = 0; i < m; i++) {
        int u, v, w;
        cin >> u >> v >> w;
        adj[u].push_back({v, w});
        adj[v].push_back({u, w});
    }

    dijkstra();

    cout << dist2[n] << endl;
    return 0;
}
```

### 说明与对比

1.  **SPFA 方法**：
      * **优点**：代码逻辑直观，容易实现。
      * **缺点**：在网格图或特殊构造的图中，时间复杂度可能退化，但在本题（边权非负，数据规模 $N \le 5000$）一般可以通过。
2.  **Dijkstra 方法**：
      * **优点**：利用优先队列，效率非常稳定，是解决此类问题的推荐算法，特别是当数据范围较大或没有负权边时。
      * **实现细节**：使用了 `swap` 技巧，当发现更优的最短路时，原来的最短路值并没有丢弃，而是顺延去尝试更新次短路，这保证了逻辑的简洁和严密。

您可以根据实际需求选择其中一种实现。如果是练习算法模板，建议掌握 Dijkstra 的写法。