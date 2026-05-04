import tkinter as tk
from tkinter import ttk
from algorithms.graph_algorithms import bfs, dfs, dijkstra, prims_mst, CAMPUS_GRAPH


def launch():
    window = tk.Toplevel()
    window.title("Campus Navigator")
    window.geometry("700x600")
    window.configure(bg="#f0f4f7")

    # --- Title ---
    title = tk.Label(window, text="Campus Navigator", font=("Arial", 18, "bold"), bg="#f0f4f7")
    title.pack(pady=10)

    # --- Input Frame ---
    input_frame = tk.Frame(window, bg="#f0f4f7")
    input_frame.pack(pady=10)

    nodes = list(CAMPUS_GRAPH.keys())

    # Start Node
    tk.Label(input_frame, text="Start Node:", bg="#f0f4f7").grid(row=0, column=0, padx=10, pady=5)
    start_var = tk.StringVar()
    start_dropdown = ttk.Combobox(input_frame, textvariable=start_var, values=nodes, state="readonly")
    start_dropdown.grid(row=0, column=1, padx=10)

    # End Node
    tk.Label(input_frame, text="End Node:", bg="#f0f4f7").grid(row=1, column=0, padx=10, pady=5)
    end_var = tk.StringVar()
    end_dropdown = ttk.Combobox(input_frame, textvariable=end_var, values=nodes, state="readonly")
    end_dropdown.grid(row=1, column=1, padx=10)

    # Defaults
    if nodes:
        start_var.set(nodes[0])
        end_var.set(nodes[1] if len(nodes) > 1 else nodes[0])

    # --- Output Box ---
    output = tk.Text(
        window,
        height=15,
        width=80,
        bg="#1e1e1e",
        fg="#00ffcc",
        insertbackground="white",
        font=("Consolas", 10)
    )
    output.pack(pady=10)

    def display(text):
        output.delete("1.0", tk.END)
        output.insert(tk.END, text)

    def validate():
        if not start_var.get() or not end_var.get():
            display("❌ Please select both start and end nodes.")
            return False
        return True

    # --- BFS ---
    def run_bfs():
        if not validate():
            return

        path, hops, order = bfs(CAMPUS_GRAPH, start_var.get(), end_var.get())

        if not path:
            display(
                "=== BFS Result ===\n"
                "❌ No path found.\n\n"
                f"Visited:\n{', '.join(order)}"
            )
            return

        display(
            f"=== BFS Result ===\n"
            f"Path: {' -> '.join(path)}\n"
            f"Hops: {hops}\n\n"
            f"Visited:\n{', '.join(order)}"
        )

    # --- DFS ---
    def run_dfs():
        if not validate():
            return

        path, order, connected = dfs(CAMPUS_GRAPH, start_var.get(), end_var.get())

        display(
            f"=== DFS Result ===\n"
            f"Path: {' -> '.join(path) if path else 'None'}\n\n"
            f"Visited:\n{', '.join(order)}\n\n"
            f"Connected: {connected}"
        )

    # --- Dijkstra ---
    def run_dijkstra():
        if not validate():
            return

        path, dist = dijkstra(CAMPUS_GRAPH, start_var.get(), end_var.get())

        if dist == -1:
            display("=== Dijkstra Result ===\n❌ No path found.")
            return

        display(
            f"=== Dijkstra Result ===\n"
            f"Shortest Path: {' -> '.join(path)}\n"
            f"Distance: {dist}"
        )

    # --- Prim's MST ---
    def run_prim():
        if not start_var.get():
            display("❌ Please select a start node.")
            return

        edges, total = prims_mst(CAMPUS_GRAPH, start_var.get())

        edge_text = "\n".join([f"{u} - {v} (weight {w})" for u, v, w in edges])

        display(
            f"=== Prim's MST ===\n\n"
            f"{edge_text}\n\n"
            f"Total Weight: {total}"
        )

    # --- Buttons ---
    btn_frame = tk.Frame(window, bg="#f0f4f7")
    btn_frame.pack(pady=15)

    tk.Button(btn_frame, text="Run BFS", command=run_bfs,
              bg="#2ecc71", fg="white", width=14).grid(row=0, column=0, padx=6)

    tk.Button(btn_frame, text="Run DFS", command=run_dfs,
              bg="#3498db", fg="white", width=14).grid(row=0, column=1, padx=6)

    tk.Button(btn_frame, text="Run Dijkstra", command=run_dijkstra,
              bg="#9b59b6", fg="white", width=14).grid(row=0, column=2, padx=6)

    tk.Button(btn_frame, text="Run Prim's MST", command=run_prim,
              bg="#e67e22", fg="white", width=16).grid(row=0, column=3, padx=6)