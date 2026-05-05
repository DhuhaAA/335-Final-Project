# TCAA Algorithms Module README
# Titan Campus Algorithmic Assistant - Algorithm Layer Documentation
# Author: Dhuha Abdulhussein

## Overview

The algorithms module contains all implementations for the TCAA project:
- **Graph Algorithms**: BFS, DFS, Dijkstra, Prim's MST
- **String Matching**: Naive Search, Rabin-Karp, KMP
- **Scheduling**: Greedy Scheduler, DP Knapsack
- **Analysis**: Complexity information and P vs NP explanation

## Project Structure

```
algorthims/
├── __init__.py                 # Package initialization
├── graph_algorthims.py         # Graph algorithms (BFS, DFS, Dijkstra, Prim's)
├── string_algorithms.py        # String matching (Naive, Rabin-Karp, KMP)
├── dynamic_programming.py      # Scheduling (Greedy, DP Knapsack)
└── algorithm_analysis.py       # Complexity analysis and P vs NP
```

## Quick Start

### Installation
No installation required! All code uses standard Python libraries.

### Basic Usage

```python
from algorthims import (
    bfs, dfs, dijkstra, prims_mst, CAMPUS_GRAPH,
    naive_search, rabin_karp, kmp,
    Task, greedy_scheduler, dp_knapsack_scheduler,
    get_algorithm_info, get_complexity_chart
)

# Graph algorithms
path, hops, order = bfs(CAMPUS_GRAPH, "Library", "Science")
path, distance = dijkstra(CAMPUS_GRAPH, "Library", "Science")
edges, total = prims_mst(CAMPUS_GRAPH, "Library")

# String algorithms
matches = naive_search("ABCCDDAA", "AA")
matches = kmp("ABCCDDAA", "AA")

# Scheduling
tasks = [Task("Study", 2.0, 10), Task("Exercise", 1.0, 5)]
greedy = greedy_scheduler(tasks, 3.0)
optimal = dp_knapsack_scheduler(tasks, 3.0)

# Analysis
info = get_algorithm_info("Dijkstra")
chart = get_complexity_chart()
```

## Module Documentation

### graph_algorthims.py

**CAMPUS_GRAPH**: Predefined campus graph with 7 buildings and weighted edges

**Functions:**
- `bfs(graph, start, end)` → `(path, hops, traversal_order)`
- `dfs(graph, start, end=None)` → `(path, traversal_order, is_connected)`
- `dijkstra(graph, start, end)` → `(path, distance)`
- `prims_mst(graph, start)` → `(edges, total_weight)`

### string_algorithms.py

**Functions:**
- `naive_search(text, pattern)` → `[indices]`
- `rabin_karp(text, pattern, prime=101)` → `[indices]`
- `kmp(text, pattern)` → `[indices]`
- `search_all(text, pattern)` → `{dict with all results}`

### dynamic_programming.py

**Task Class:**
- Constructor: `Task(name, duration, value)`
- Method: `task.ratio()` returns value/duration

**Functions:**
- `greedy_scheduler(tasks, available_time)` → `{dict}`
- `dp_knapsack_scheduler(tasks, available_time)` → `{dict}`
- `compare_schedulers(tasks, available_time)` → `{dict with comparison}`

### algorithm_analysis.py

**Functions:**
- `get_algorithm_info(algorithm_name)` → `{dict}`
- `get_complexity_chart()` → `str`
- `get_p_vs_np_explanation()` → `{dict}`
- `complexity_classes_summary()` → `str`

## Algorithm Complexities

| Algorithm | Time | Space | Category |
|-----------|------|-------|----------|
| BFS | O(V + E) | O(V) | Graph |
| DFS | O(V + E) | O(V) | Graph |
| Dijkstra | O((V+E)logV) | O(V) | Graph |
| Prim's MST | O((V+E)logV) | O(V+E) | Graph |
| Naive Search | O(n*m) | O(1) | String |
| Rabin-Karp | O(n+m) avg | O(1) | String |
| KMP | O(n+m) | O(m) | String |
| Greedy | O(nlogn) | O(n) | Scheduling |
| DP Knapsack | O(n*W) | O(n*W) | Scheduling |

## Data Structures

### CAMPUS_GRAPH Format
```python
{
    "Building": [("Neighbor", weight), ...],
    "Library": [("Gym", 5), ("Dorms", 3), ("ECS", 7)],
    ...
}
```

### Task Object
```python
task = Task("Study Math", 2.0, 10)
print(task.name)      # "Study Math"
print(task.duration)  # 2.0
print(task.value)     # 10
print(task.ratio())   # 5.0 (value per hour)
```

### Scheduler Return Format
```python
{
    'selected_tasks': [Task(...), Task(...), ...],
    'total_time': float,
    'total_value': float,
    'efficiency': float (value/time)
}
```

## Error Handling

All functions handle edge cases gracefully:

**Graph Functions:**
- Empty graph → return empty/neutral values
- No path → return empty path and -1
- Single node → handled correctly

**String Functions:**
- Empty pattern → return empty list
- Pattern longer than text → return empty list
- No matches → return empty list

**Scheduling Functions:**
- Empty tasks → return empty selection
- available_time <= 0 → return empty selection
- Tasks exceed time → return what fits

## GUI Integration

See `INTEGRATION_GUIDE.md` for detailed GUI integration specifications.

### Key Import
```python
from algorthims import *
# or specific imports
from algorthims import bfs, dijkstra, Task, greedy_scheduler
```

### Function Signatures (guaranteed stable)
All function signatures and return types are documented in `INTEGRATION_GUIDE.md`

## Libraries Used

**Allowed & Used:**
- `heapq` - Binary heap for Dijkstra and Prim's
- `collections.deque` - Queue for BFS
- `time` - Optional timing

**No Forbidden Libraries:**
- ✗ NetworkX (not used)
- ✗ Pandas (not used)
- ✗ Pre-made algorithm libraries (not used)

## Testing

Run `test_algorithms.py` at project root to verify all algorithms:
```bash
python test_algorithms.py
```

## Performance Notes

**Fast Algorithms:**
- BFS/DFS: O(V + E) - instant on small graphs
- Naive Search: O(n*m) - good for small texts
- Greedy: O(n log n) - very fast scheduling

**Slower Algorithms:**
- Dijkstra: O((V+E)logV) - still fast with heapq
- KMP: O(n+m) - optimized for large texts
- DP Knapsack: O(n*W) - depends on available time

All algorithms are efficient enough for interactive GUI use.

## About the Author

- Name: Dhuha Abdulhussein
- Course: CPSC 335 - Algorithms
- Instructor: Dr. Shah

## Project Information

- **Project**: Titan Campus Algorithmic Assistant (TCAA)
- **Duration**: 2 weeks
- **Points**: 50 total
- **Algorithms Portion**: 20 points

## License

This project is part of CPSC 335 coursework.
