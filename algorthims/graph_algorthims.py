# BFS, DFS, Dijkstra's , Prim's
# Author: Dhuha Abdulhussein

import heapq 
import time
from collections import deque


# Campus Graph to use for our algo demos
CAMPUS_GRAPH = {
    "Library" :   [("Gym", 5) , ("Dorms", 3) , ("ECS", 7)],
    "Gym":        [("Library", 5),("Cafeteria", 2), ("Quad", 4)],
    "Dorms":      [("Library", 3),("Cafeteria", 6), ("ECS", 2)],
    "ECS":        [("Library", 7),("Dorms", 2),     ("Science", 3)],
    "Cafeteria":  [("Gym", 2),    ("Dorms", 6),     ("Quad", 1)],
    "Quad":       [("Gym", 4),    ("Cafeteria", 1), ("Science", 5)],
    "Science":    [("ECS", 3),    ("Quad", 5)]
}                   


# ---------- BFS ------------#
# find the path with the fewest edges between nodes"
# TIME COMPLEXITY:  O(V + E)  — V = nodes, E = edges
# SPACE COMPLEXITY: O(V)

def bfs(graph, start, end):
    
    if start == end:
        return [start], 0, [start]
    
    queue = deque([start])
    visited = {start}
    parent = {start: None}
    visited_order = [start]
    
    while queue:
        current = queue.popleft() # from the front
        
        for neighbor, weight in graph[current]:
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                visited_order.append(neighbor)
                
                if neighbor == end:
                    
                    path = []
                    node = end
                    
                    while node is not None:
                        path.append(node)
                        node = parent[node]
                        
                    path.reverse()
                    return path, len(path) -1, visited_order
                
    return [], -1, visited_order


# ----------- DFS ------------
# explore as deep as possible before backtracking 
# TIME COMPLEXITY:  O(V + E)
# SPACE COMPLEXITY: O(V)  [due to recursion stack or explicit stack]

def dfs(graph, start, end=None):
    
    visited = set()
    visited_order = []
    parent = {start: None}
    
    def _dfs_recursive(node):
        # recursive helper function
        visited.add(node)
        visited_order.append(node)
        
        for neighbor, weight in graph[node]:
            if neighbor not in visited:
                parent[neighbor] = node
                _dfs_recursive(neighbor)
                
    _dfs_recursive(start)
    
    is_connected = (len(visited) == len(graph))
    
    path = [] 
    if end and end in visited:
        node = end 
        while node is not None:
            path.append(node)
            node = parent.get(node)
        path.reverse()
        
    return path, visited_order, is_connected


# ---------Dijkstra-----------
# find the path with the minimum total weight (shortest distance)
# TIME COMPLEXITY:  O((V + E) log V)  with a binary heap
# SPACE COMPLEXITY: O(V)

def dijkstra(graph, start, end):
    
    dist = {node: float('inf') for node in graph}
    dist[start] = 0
    
    parent = {start: None}
    
    heap = [(0, start)]
    
    finalized = set()
    
    while heap:
        current_dist, current = heapq.heappop(heap) 
        
        if current in finalized:
            continue
        finalized.add(current)
        
        if current == end:
            break 
        
        for neighbor, weight in graph[current]:
            if neighbor in finalized:
                continue
            
            new_dist = current_dist + weight
            
            if new_dist < dist[neighbor]:
                dist[neighbor] = new_dist
                parent[neighbor] = current
                heapq.heappush(heap, (new_dist, neighbor))
                
    # reconstruct the new path 
    if dist[end] == float('inf'):
        return [], -1
    
    path = []
    node = end 
    
    while node is not None:
        path.append(node)
        node = parent.get(node)
    path.reverse()
    
    return path, dist[end]


# -------- Prim's minimum spanning tree ----------
# connect all nodes in a graph with No cycles and use smallest possible total weight
# TIME COMPLEXITY: O((V+E) log V)
# SPACE COMPLEXITY: O(V+E)

def prims_mst(graph, start):
    
    in_mst = set()
    in_mst.add(start)
    
    heap = [] 
    for neighbor, weight in graph[start]:
        heapq.heappush(heap, (weight, start, neighbor))
        
    mst_edges = []
    total_weight = 0
    
    while heap and len(in_mst) < len(graph):
        weight, from_node, to_node = heapq.heappop(heap)
        
        if to_node in in_mst:
            continue # skip if it's in MST to not create a cycle
        
        in_mst.add(to_node)
        mst_edges.append((from_node, to_node, weight))
        total_weight += weight
        
        for neighbor, w in graph[to_node]:
            if neighbor not in in_mst:
                heapq.heappush(heap, (w, to_node, neighbor))
                
    return mst_edges, total_weight



