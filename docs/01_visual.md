好问题！让我给你详细解释适合你项目的性能指标。

## 📊 推荐的评估指标体系

根据你的报告内容，我建议使用以下指标：

---

## 🎯 核心指标（必须测量）

### 1. **运行时间 (Wall-Clock Time)**
**含义**: 算法从开始到结束的实际时间

**为什么重要**:
- 最直观的性能衡量
- 用户实际关心的指标

**如何测量**:
```python
import time

start_time = time.perf_counter()
result = algorithm.run(graph, source, target)
end_time = time.perf_counter()

runtime = end_time - start_time  # 单位：秒
```

**报告形式**:
- 平均值 (Mean)
- 中位数 (Median/P50)
- P95 百分位数
- P99 百分位数

**用途**: 直接对比两种算法的实际性能

---

### 2. **优先队列/队列操作次数**

#### 2a. **Push 操作次数**
**含义**: 向优先队列/FIFO队列中插入元素的次数

**理论值**:
- **Dijkstra**: O(M) - 每条边最多触发 2 次 push
- **SPFA**: O(MN) worst case - 节点可能多次入队

**测量方法**:
```python
class TwoDistanceDijkstra:
    def __init__(self):
        self.push_count = 0
        
    def find_second_shortest(self, ...):
        while pq:
            ...
            pq.push((new_dist, node))
            self.push_count += 1
```

**意义**: 反映算法的工作量

---

#### 2b. **Pop 操作次数**
**含义**: 从队列中取出元素的次数

**理论值**:
- 应该等于或略小于 Push 次数
- Dijkstra: 最多 O(M)
- SPFA: 最多 O(MN)

**意义**: 验证算法执行了多少次主循环迭代

---

### 3. **边松弛次数 (Edge Relaxation Count)**
**含义**: 尝试更新节点距离标签的次数

**详细说明**:
```python
# 每次执行这个逻辑时计数
if cand < d1[u]:
    d1[u] = cand
    edge_relaxation_count += 1
```

**理论值**:
- **Dijkstra**: O(M) - 每条边处理有限次
- **SPFA**: O(MN) - 边可能被重复处理

**意义**: 
- 反映算法实际处理的工作量
- 与理论复杂度直接相关

---

### 4. **距离标签更新次数**

#### 4a. **d1 更新次数** (最短路径标签)
**含义**: d1[v] 被改变的次数

**理论上限**: 每个节点的 d1 最多更新 O(log N) 次（Dijkstra）

#### 4b. **d2 更新次数** (第二短路径标签)
**含义**: d2[v] 被改变的次数

**意义**: 反映找到第二短路径的努力程度

---

## 📈 复杂度验证指标（用于绘图）

### 5. **时间复杂度验证数据**
**含义**: 运行时间与图规模的关系

**如何使用**:
```python
# 收集数据
data_points = []
for test_case in dataset:
    n = test_case['n']
    m = len(test_case['edges'])
    runtime = measure_runtime(algorithm, test_case)
    
    data_points.append({
        'n': n,
        'm': m,
        'runtime': runtime
    })

# 拟合曲线
# Dijkstra: 拟合 runtime ≈ c * m * log(n)
# SPFA: 拟合 runtime ≈ c * m * n (worst) 或 c * m (average)
```

**输出**: 
- 散点图 + 拟合曲线
- 验证理论复杂度

---

### 6. **空间复杂度 (可选)**
**含义**: 算法运行时的内存使用

**测量**:
```python
import tracemalloc

tracemalloc.start()
result = algorithm.run(...)
current, peak = tracemalloc.get_traced_memory()
tracemalloc.stop()

memory_usage = peak / 1024 / 1024  # MB
```

**理论值**:
- 两种算法都是 O(N + M)
- 差异应该不大

---

## 🎨 可视化指标汇总

### 图表 1: 运行时间对比
```
指标: runtime (秒)
图表类型: 柱状图 / 箱线图
X轴: 算法 (Dijkstra vs SPFA)
Y轴: 运行时间
分组: 按图规模分组
```

### 图表 2: 可扩展性分析
```
指标: runtime vs 图规模
图表类型: 折线图
X轴: 节点数 n 或边数 m
Y轴: 运行时间
多条线: Dijkstra vs SPFA
```

### 图表 3: 复杂度验证
```
指标: runtime vs m*log(n) 或 m*n
图表类型: 散点图 + 拟合曲线
目的: 验证 O(M log N) vs O(MN)
```

### 图表 4: 操作次数对比
```
指标: push_count, pop_count, edge_relaxations
图表类型: 分组柱状图
对比: 不同图规模下的操作次数
```

### 图表 5: 百分位数分析
```
指标: P50, P95, P99 运行时间
图表类型: 箱线图
用途: 展示性能稳定性
```

---

## 📋 完整指标表格

| 指标名称 | 符号 | 单位 | 理论值 (Dijkstra) | 理论值 (SPFA) | 用途 |
|---------|------|------|------------------|---------------|------|
| 运行时间 | T | 秒 | - | - | 性能对比 |
| Push次数 | P_push | 次 | O(M) | O(MN) | 工作量 |
| Pop次数 | P_pop | 次 | O(M) | O(MN) | 迭代次数 |
| 边松弛次数 | R_edge | 次 | O(M) | O(MN) | 处理量 |
| d1更新次数 | U_d1 | 次 | O(N log N) | O(N²) | 标签更新 |
| d2更新次数 | U_d2 | 次 | O(N log N) | O(N²) | 标签更新 |
| 内存使用 | Mem | MB | O(N+M) | O(N+M) | 空间开销 |

---

## 🎯 最小必需指标集（如果时间紧）

如果今天要完成，至少要测量：

1. ✅ **运行时间** (T)
2. ✅ **Push 操作次数** (P_push)
3. ✅ **边松弛次数** (R_edge)

这三个指标就足以：
- 对比实际性能
- 验证理论复杂度
- 生成主要图表

---

## 📊 数据收集示例代码

```python
class PerformanceMetrics:
    def __init__(self):
        self.runtime = 0
        self.push_count = 0
        self.pop_count = 0
        self.edge_relaxations = 0
        self.d1_updates = 0
        self.d2_updates = 0
        
    def to_dict(self):
        return {
            'runtime': self.runtime,
            'push_count': self.push_count,
            'pop_count': self.pop_count,
            'edge_relaxations': self.edge_relaxations,
            'd1_updates': self.d1_updates,
            'd2_updates': self.d2_updates,
        }

def measure_algorithm(algorithm, test_case):
    # 重置计数器
    algorithm.reset_metrics()
    
    # 构建图
    graph = build_graph(test_case)
    
    # 测量运行时间
    start = time.perf_counter()
    l1, l2 = algorithm.run(graph, test_case['source'], test_case['target'])
    end = time.perf_counter()
    
    # 收集指标
    metrics = algorithm.get_metrics()
    metrics.runtime = end - start
    
    return metrics, (l1, l2)
```

---

## 💡 我的建议

**优先级排序**:

**第一优先级** (必须):
1. 运行时间
2. Push 操作次数
3. 边松弛次数

**第二优先级** (推荐):
4. Pop 操作次数
5. 距离标签更新次数

**第三优先级** (可选):
6. 内存使用
7. 缓存命中率等细节

对于今天完成的项目，**只需要第一优先级的 3 个指标**就够了！

你觉得这个指标体系怎么样？需要我：
1. 调整指标？
2. 解释某个指标的具体含义？
3. 直接开始实现算法和指标收集系统？