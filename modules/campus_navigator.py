"""
TCAA - Campus Navigator Module
BFS · DFS · Dijkstra · Prim's MST
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from algorithms.graph_algorithms import bfs, dfs, dijkstra, prims_mst, CAMPUS_GRAPH

C = {
    "bg":        "#F3E3D0",
    "panel":     "#AACDDC",
    "card":      "#FFFFFF",
    "accent":    "#81A6C6",
    "accent2":   "#5A86A8",
    "green":     "#4A8C6F",
    "red":       "#B85C5C",
    "brown":     "#8B6F3E",
    "text":      "#1E2D3A",
    "subtext":   "#5A7080",
    "border":    "#D2C4B4",
    "header_bg": "#81A6C6",
    "entry_bg":  "#FFFFFF",
}

def _btn(parent, text, cmd, color=None):
    return tk.Button(parent, text=text, command=cmd,
                     font=("Courier New", 9, "bold"),
                     fg="#FFFFFF", bg=color or C["accent"],
                     activebackground=C["accent2"], activeforeground="#FFFFFF",
                     relief="flat", bd=0, padx=12, pady=5, cursor="hand2")


def build_campus_navigator_tab(notebook):
    tab = tk.Frame(notebook, bg=C["bg"])

    # Header
    hdr = tk.Frame(tab, bg=C["header_bg"], pady=11)
    hdr.pack(fill="x")
    tk.Label(hdr, text="Campus Navigator",
             font=("Courier New", 17, "bold"), fg="#FFFFFF", bg=C["header_bg"]).pack()
    tk.Label(hdr, text="BFS  ·  DFS  ·  Dijkstra Shortest Path  ·  Prim's MST",
             font=("Courier New", 9), fg=C["border"], bg=C["header_bg"]).pack()

    body = tk.Frame(tab, bg=C["bg"])
    body.pack(fill="both", expand=True, padx=12, pady=10)

    # ── Left panel: controls ──────────────────────────────────────────────────
    left = tk.Frame(body, bg=C["panel"], width=260)
    left.pack(side="left", fill="y", padx=(0, 10))
    left.pack_propagate(False)

    nodes = list(CAMPUS_GRAPH.keys())

    # Section header helper
    def sec(parent, title):
        f = tk.Frame(parent, bg=C["header_bg"])
        f.pack(fill="x", pady=(10, 0))
        tk.Label(f, text=f"  {title}", font=("Courier New", 10, "bold"),
                 fg="#FFFFFF", bg=C["header_bg"], anchor="w", pady=4).pack(fill="x")

    sec(left, "Select Nodes")

    form = tk.Frame(left, bg=C["panel"])
    form.pack(fill="x", padx=10, pady=8)

    start_var = tk.StringVar(value=nodes[0])
    end_var   = tk.StringVar(value=nodes[1] if len(nodes) > 1 else nodes[0])

    for label, var in [("Start Node:", start_var), ("End Node:", end_var)]:
        row = tk.Frame(form, bg=C["panel"])
        row.pack(fill="x", pady=3)
        tk.Label(row, text=label, font=("Courier New", 8), fg=C["subtext"],
                 bg=C["panel"], width=11, anchor="w").pack(side="left")
        cb = ttk.Combobox(row, textvariable=var, values=nodes,
                          state="readonly", width=14,
                          font=("Courier New", 9))
        cb.pack(side="left")

    sec(left, "Run Algorithm")

    btn_f = tk.Frame(left, bg=C["panel"])
    btn_f.pack(fill="x", padx=10, pady=8)

    # Buttons created after output widget (forward ref via lambda)
    output_ref = [None]

    def display(text):
        out = output_ref[0]
        out.config(state="normal")
        out.delete("1.0", tk.END)
        # insert with tags
        for line in text.split("\n"):
            if line.startswith("==="):
                out.insert(tk.END, line + "\n", "heading")
            elif line.startswith("  "):
                out.insert(tk.END, line + "\n", "indent")
            elif "→" in line or "->" in line:
                out.insert(tk.END, line + "\n", "path")
            elif "❌" in line:
                out.insert(tk.END, line + "\n", "error")
            elif any(k in line for k in ["Distance:", "Hops:", "Total", "Connected:"]):
                out.insert(tk.END, line + "\n", "stat")
            else:
                out.insert(tk.END, line + "\n")
        out.config(state="disabled")

    def validate():
        if not start_var.get() or not end_var.get():
            messagebox.showerror("Input Error", "Please select both start and end nodes.")
            return False
        return True

    def run_bfs():
        if not validate(): return
        path, hops, order = bfs(CAMPUS_GRAPH, start_var.get(), end_var.get())
        if not path:
            display("=== BFS Result ===\n❌ No path found.\n\nVisited:\n  " + ", ".join(order))
            return
        display(
            f"=== BFS (Fewest Hops) ===\n\n"
            f"Path:    {' → '.join(path)}\n"
            f"Hops:    {hops}\n\n"
            f"Visited order:\n  {', '.join(order)}"
        )

    def run_dfs():
        if not validate(): return
        path, order, connected = dfs(CAMPUS_GRAPH, start_var.get(), end_var.get())
        display(
            f"=== DFS Traversal ===\n\n"
            f"Path:      {' → '.join(path) if path else 'None'}\n"
            f"Connected: {connected}\n\n"
            f"Visited order:\n  {', '.join(order)}"
        )

    def run_dijkstra():
        if not validate(): return
        path, dist = dijkstra(CAMPUS_GRAPH, start_var.get(), end_var.get())
        if dist == -1:
            display("=== Dijkstra Result ===\n❌ No path found.")
            return
        display(
            f"=== Dijkstra Shortest Path ===\n\n"
            f"Path:     {' → '.join(path)}\n"
            f"Distance: {dist}"
        )

    def run_prim():
        if not start_var.get():
            messagebox.showerror("Input Error", "Please select a start node.")
            return
        edges, total = prims_mst(CAMPUS_GRAPH, start_var.get())
        edge_lines = "\n".join(f"  {u}  —  {v}   (weight {w})" for u, v, w in edges)
        display(
            f"=== Prim's MST ===\n\n"
            f"MST Edges:\n{edge_lines}\n\n"
            f"Total Weight: {total}"
        )

    for text, cmd, color in [
        ("▶  Run BFS",        run_bfs,      C["green"]),
        ("▶  Run DFS",        run_dfs,      C["accent"]),
        ("▶  Run Dijkstra",   run_dijkstra, C["brown"]),
        ("▶  Run Prim's MST", run_prim,     C["red"]),
    ]:
        _btn(btn_f, text, cmd, color).pack(fill="x", pady=2)

    # Complexity reminder box
    sec(left, "Complexities")
    info = tk.Frame(left, bg=C["card"], bd=1, relief="solid")
    info.pack(fill="x", padx=6, pady=(4, 12))
    for line, fg in [
        ("BFS / DFS   O(V + E)", C["green"]),
        ("Dijkstra    O(E log V)", C["brown"]),
        ("Prim's MST  O(E log V)", C["red"]),
    ]:
        tk.Label(info, text=f"  {line}", font=("Courier New", 8),
                 fg=fg, bg=C["card"], anchor="w", pady=2).pack(fill="x")

    # ── Right panel: output ───────────────────────────────────────────────────
    right = tk.Frame(body, bg=C["bg"])
    right.pack(side="left", fill="both", expand=True)

    # Campus graph map (static visual)
    map_frame = tk.Frame(right, bg=C["card"], bd=1, relief="solid",
                         highlightbackground=C["border"])
    map_frame.pack(fill="x", pady=(0, 8))

    canvas = tk.Canvas(map_frame, bg=C["card"], height=260, highlightthickness=0)
    canvas.pack(fill="x", padx=4, pady=4)

    # Draw campus graph visually
    NODE_POS = {
        "Library":   (160, 110),
        "Gym":       (370, 55),
        "Dorms":     (155, 210),
        "ECS":       (300, 210),
        "Cafeteria": (510, 100),
        "Quad":      (530, 210),
        "Science":   (420, 210),
    }

    def draw_graph(highlight_path=None):
        canvas.delete("all")
        hp = set()
        if highlight_path:
            for i in range(len(highlight_path) - 1):
                hp.add((highlight_path[i], highlight_path[i+1]))
                hp.add((highlight_path[i+1], highlight_path[i]))

        drawn = set()
        for node, neighbors in CAMPUS_GRAPH.items():
            x1, y1 = NODE_POS[node]
            for nb, w in neighbors:
                if (node, nb) not in drawn:
                    x2, y2 = NODE_POS[nb]
                    is_path = (node, nb) in hp
                    canvas.create_line(x1, y1, x2, y2,
                                       fill=C["green"] if is_path else C["border"],
                                       width=3 if is_path else 1)
                    mx, my = (x1+x2)//2, (y1+y2)//2
                    canvas.create_text(mx, my, text=str(w),
                                       font=("Courier New", 9, "bold"), fill=C["subtext"],
                                       tags="weight")
                    drawn.add((node, nb)); drawn.add((nb, node))

        for node, (x, y) in NODE_POS.items():
            in_path = highlight_path and node in highlight_path
            color = C["green"] if in_path else C["accent"]
            canvas.create_oval(x-28, y-16, x+28, y+16,
                               fill=color, outline=C["accent2"], width=2)
            canvas.create_text(x, y, text=node,
                               font=("Courier New", 8, "bold"), fill="#FFFFFF")

    draw_graph()

    # Output text area
    out_frame = tk.Frame(right, bg=C["card"], bd=1, relief="solid",
                         highlightbackground=C["border"])
    out_frame.pack(fill="both", expand=True)

    tk.Label(out_frame, text="  Output", font=("Courier New", 9, "bold"),
             fg=C["subtext"], bg=C["panel"], anchor="w", pady=3).pack(fill="x")

    out_sb = tk.Scrollbar(out_frame)
    out_sb.pack(side="right", fill="y")

    output = tk.Text(
        out_frame,
        font=("Courier New", 10),
        fg=C["text"], bg=C["card"],
        relief="flat", bd=0, padx=12, pady=8,
        yscrollcommand=out_sb.set,
        state="disabled", cursor="arrow", wrap="word",
    )
    output.pack(fill="both", expand=True)
    out_sb.config(command=output.yview)
    output_ref[0] = output

    # Text tags
    output.tag_configure("heading", font=("Courier New", 10, "bold"), foreground=C["accent"])
    output.tag_configure("path",    foreground=C["green"])
    output.tag_configure("stat",    foreground=C["brown"])
    output.tag_configure("indent",  foreground=C["subtext"])
    output.tag_configure("error",   foreground=C["red"])

    display("Select start and end nodes, then run an algorithm.\n\nBFS  — fewest hops\nDFS  — traversal + connectivity\nDijkstra — shortest weighted path\nPrim's   — minimum spanning tree")

    return tab


# Backwards compat: old code called launch()
def launch():
    import tkinter as tk
    from tkinter import ttk
    root = tk.Toplevel()
    nb = ttk.Notebook(root)
    nb.pack(fill="both", expand=True)
    tab = build_campus_navigator_tab(nb)
    nb.add(tab, text="Campus Navigator")
    root.mainloop()
