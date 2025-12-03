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