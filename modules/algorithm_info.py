import tkinter as tk


def launch():
    window = tk.Toplevel()
    window.title("Algorithm Information")
    window.geometry("700x600")
    window.configure(bg="#f0f4f7")

    # --- Title ---
    title = tk.Label(
        window,
        text="Algorithm Information",
        font=("Arial", 18, "bold"),
        bg="#f0f4f7"
    )
    title.pack(pady=10)

    # --- Output Box ---
    text = tk.Text(
        window,
        wrap="word",
        bg="#1e1e1e",
        fg="#00ffcc",
        insertbackground="white",
        font=("Consolas", 10)
    )
    text.pack(fill="both", expand=True, padx=10, pady=10)

    content = """
================ GRAPH ALGORITHMS ================

BFS (Breadth-First Search)
- Explores nodes level by level
- Finds shortest path in unweighted graphs
- Time Complexity: O(V + E)

DFS (Depth-First Search)
- Explores as deep as possible before backtracking
- Used for traversal and connectivity
- Time Complexity: O(V + E)

Dijkstra’s Algorithm
- Finds shortest path in weighted graphs
- Uses a priority queue (heap)
- Time Complexity: O((V + E) log V)

Prim’s Algorithm (MST)
- Builds a minimum spanning tree
- Connects all nodes with minimum total weight
- Time Complexity: O(E log V)


================ OPTIMIZATION ================

Greedy Algorithm
- Chooses the best option at each step
- Fast but not always optimal
- Time Complexity: O(n log n)

Dynamic Programming (0/1 Knapsack)
- Evaluates all combinations
- Guarantees optimal solution
- Time Complexity: O(n * capacity)


================ STRING MATCHING ================

Naive Search
- Checks every possible position
- Time Complexity: O(n * m)

Rabin-Karp
- Uses hashing to speed up comparisons
- Average: O(n + m)

KMP (Knuth-Morris-Pratt)
- Uses prefix table to skip redundant comparisons
- Time Complexity: O(n + m)


================ P vs NP (Simplified) ================

P Problems:
- Can be solved quickly (polynomial time)
- Example: BFS, sorting

NP Problems:
- Hard to solve quickly
- But solutions can be verified quickly

Big Question:
- Is P = NP?
- Unknown, one of the biggest problems in computer science


================ PROJECT SUMMARY ================

This application demonstrates:

- Graph algorithms (BFS, DFS, Dijkstra, MST)
- Optimization techniques (Greedy vs Dynamic Programming)
- String matching algorithms
- Algorithm analysis and complexity

Built using Python and Tkinter.
"""

    text.insert(tk.END, content)
    text.config(state="disabled")