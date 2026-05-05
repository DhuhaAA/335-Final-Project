"""
TCAA - Algorithm Info / About Module
CPSC 335 Final Project - Titan Campus Algorithmic Assistant

Displays:
  - Big-O complexities for all algorithms used in the project
  - P vs NP reflection / explanation
"""

import tkinter as tk
from tkinter import ttk


# ──────────────────────────────────────────────────────────────────────────────
# Color palette — #81A6C6 / #AACDDC / #F3E3D0 / #D2C4B4
# ──────────────────────────────────────────────────────────────────────────────
COLORS = {
    "bg":        "#F3E3D0",   # cream — main background
    "panel":     "#AACDDC",   # light blue — panels / section bg
    "card":      "#ffffff",   # white — cards / text areas
    "accent":    "#81A6C6",   # steel blue — headers / accent
    "accent2":   "#5A86A8",   # darker blue — sub-headers
    "green":     "#4A8C6F",   # muted green — efficient
    "red":       "#B85C5C",   # muted red — expensive
    "yellow":    "#8B6F3E",   # warm brown — moderate
    "text":      "#1E2D3A",   # near-black — primary text
    "subtext":   "#5A7080",   # blue-grey — muted text
    "border":    "#D2C4B4",   # tan — borders / dividers
    "header_bg": "#81A6C6",   # steel blue — tab/page headers
}

# (Algorithm, Best, Average, Worst, Space, color_key)
COMPLEXITY_DATA = {
    "Graph Algorithms": [
        ("BFS",               "O(V + E)",  "O(V + E)",   "O(V + E)",   "O(V)",     "green"),
        ("DFS",               "O(V + E)",  "O(V + E)",   "O(V + E)",   "O(V)",     "green"),
        ("Dijkstra (heap)",   "O(E log V)","O(E log V)", "O(E log V)", "O(V)",     "yellow"),
        ("Prim's MST (heap)", "O(E log V)","O(E log V)", "O(E log V)", "O(V + E)", "yellow"),
    ],
    "Sorting Algorithms": [
        ("Merge Sort",     "O(n log n)", "O(n log n)", "O(n log n)", "O(n)",     "green"),
        ("Quick Sort",     "O(n log n)", "O(n log n)", "O(n^2)",     "O(log n)", "yellow"),
        ("Bubble Sort",    "O(n)",       "O(n^2)",     "O(n^2)",     "O(1)",     "red"),
        ("Selection Sort", "O(n^2)",     "O(n^2)",     "O(n^2)",     "O(1)",     "red"),
    ],
    "Searching Algorithms": [
        ("Linear Search", "O(1)",     "O(n)",     "O(n)",     "O(1)", "yellow"),
        ("Binary Search", "O(1)",     "O(log n)", "O(log n)", "O(1)", "green"),
    ],
    "Data Structures (Operations)": [
        ("Hash Table",  "O(1)",     "O(1)",     "O(n)",     "O(n)", "green"),
        ("Heap insert", "O(log n)", "O(log n)", "O(log n)", "O(n)", "green"),
        ("Heap del min","O(log n)", "O(log n)", "O(log n)", "O(n)", "green"),
        ("Heap get min","O(1)",     "O(1)",     "O(1)",     "O(n)", "green"),
        ("AVL / RB Tree","O(log n)","O(log n)", "O(log n)", "O(n)", "green"),
    ],
    "Scheduling Algorithms": [
        ("Greedy Scheduler", "O(n log n)", "O(n log n)", "O(n log n)", "O(n)",    "yellow"),
        ("DP 0/1 Knapsack",  "O(n * W)",  "O(n * W)",   "O(n * W)",   "O(n * W)","yellow"),
    ],
    "String Matching Algorithms": [
        ("Naive Search", "O(n)",     "O(n * m)",  "O(n * m)", "O(1)", "red"),
        ("Rabin-Karp",   "O(n + m)", "O(n + m)",  "O(n * m)", "O(1)", "yellow"),
        ("KMP",          "O(n + m)", "O(n + m)",  "O(n + m)", "O(m)", "green"),
    ],
    "Divide & Conquer / Recursion": [
        ("Fibonacci (naive)", "O(2^n)", "O(2^n)", "O(2^n)", "O(n)",     "red"),
        ("Fibonacci (memo)",  "O(n)",   "O(n)",   "O(n)",   "O(n)",     "green"),
        ("Merge Sort (D&C)",  "O(n log n)","O(n log n)","O(n log n)","O(n)","green"),
        ("Permutations",      "O(n!)",  "O(n!)",  "O(n!)",  "O(n)",     "red"),
    ],
}

COLOR_LEGEND = [
    ("green",  "Efficient"),
    ("yellow", "Moderate"),
    ("red",    "Worst-case expensive"),
]

SPECTRUM = [
    ("O(1)       Constant",     "green",  "FAST"),
    ("O(log n)   Logarithmic",  "green",  "FAST"),
    ("O(n)       Linear",       "green",  "FAST"),
    ("O(n log n) Linearithmic", "yellow", "OK  "),
    ("O(n^2)     Quadratic",    "yellow", "OK  "),
    ("O(n^3)     Cubic",        "yellow", "SLOW"),
    ("O(2^n)     Exponential",  "red",    "SLOW"),
    ("O(n!)      Factorial",    "red",    "SLOW"),
]

PVSNP_SECTIONS = [
    # ── The Main Question ────────────────────────────────────────────────────
    ("heading",    "1. The Main Question\n"),
    ("muted",      "─────────────────────\n"),
    ("normal",     "The famous P versus NP question asks whether every problem whose answer "
                   "can be VERIFIED quickly can also be SOLVED quickly. The answer is still "
                   "unknown.\n\n"
                   "In plain language:\n"),
    ("green",      "  P           =  fast to SOLVE\n"),
    ("yellow",     "  NP          =  fast to CHECK\n"),
    ("red",        "  NP-complete =  fast to check, but as hard as any problem in NP\n\n"),

    # ── Class P ──────────────────────────────────────────────────────────────
    ("heading",    "2. Class P  (Polynomial Time)\n"),
    ("muted",      "──────────────────────────────\n"),
    ("normal",     "A problem is in P if there is an algorithm that solves it in polynomial "
                   "time: O(n), O(n^2), O(n^3), or O(n log n). Polynomial time is the "
                   "standard notion of TRACTABLE computation — these algorithms scale to "
                   "large inputs.\n\n"),
    ("sub",        "P examples from this project:\n"),
    ("green",      "  BFS / DFS          O(V + E)       in P  (graph traversal)\n"),
    ("green",      "  Dijkstra           O(E log V)     in P  (shortest path)\n"),
    ("green",      "  Prim's MST         O(E log V)     in P  (minimum spanning tree)\n"),
    ("green",      "  KMP Search         O(n + m)       in P  (string matching)\n"),
    ("green",      "  Greedy Scheduler   O(n log n)     in P  (task scheduling)\n\n"),

    # ── Class NP ─────────────────────────────────────────────────────────────
    ("heading",    "3. Class NP  (Verification)\n"),
    ("muted",      "────────────────────────────\n"),
    ("normal",     "A problem is in NP if a CANDIDATE SOLUTION can be verified in polynomial "
                   "time. Verification is often much cheaper than search — if someone hands "
                   "you an answer, you can test it without exploring the whole search space.\n\n"
                   "Key insight: P is a subset of NP. Every problem that can be solved "
                   "quickly can also be checked quickly (just re-run the algorithm).\n\n"),
    ("sub",        "Verification example — Knapsack Decision:\n"),
    ("normal",     "  Given a proposed subset of items, you can check in O(n) that weights "
                   "fit the capacity and values meet the target — even though finding that "
                   "subset in the first place may take exponential time.\n\n"),

    # ── NP-Complete ───────────────────────────────────────────────────────────
    ("heading",    "4. NP-Complete Problems\n"),
    ("muted",      "────────────────────────\n"),
    ("normal",     "NP-complete problems are the HARDEST problems in NP. A problem is "
                   "NP-complete if:\n"
                   "  (a) it is in NP (solutions are verifiable in polynomial time), AND\n"
                   "  (b) every problem in NP can be reduced to it in polynomial time.\n\n"),
    ("sub",        "Classic NP-complete problems:\n"),
    ("red",        "  3-SAT              Boolean formula satisfiability\n"),
    ("red",        "  Circuit-SAT        Logic circuit input assignment\n"),
    ("red",        "  TSP Decision       Tour of cities within distance K\n"),
    ("red",        "  Knapsack Decision  Subset fitting capacity & value target\n"),
    ("red",        "  Graph Coloring     Color vertices with k colors, no two adjacent same\n\n"),
    ("sub",        "TSP — why brute force fails:\n"),
    ("normal",     "  Brute force checks every permutation: O(n!)\n"),
    ("yellow",     "    10 cities  ->     3,628,800 routes\n"),
    ("red",        "    20 cities  ->  2,400,000,000,000,000,000 routes\n\n"),
    ("normal",     "Practical solutions: approximation algorithms, greedy heuristics, "
                   "branch-and-bound — the same strategies used when any NP problem is "
                   "too large to solve exactly.\n\n"),

    # ── Reductions ───────────────────────────────────────────────────────────
    ("heading",    "5. Reductions\n"),
    ("muted",      "──────────────\n"),
    ("normal",     "A reduction transforms one problem into another. If problem A reduces "
                   "to problem B, then a fast algorithm for B would give a fast algorithm "
                   "for A.\n\n"
                   "  As a design idea:   reuse a known method to solve a new problem.\n"
                   "  As a hardness proof: show a known hard problem maps into the new one.\n\n"
                   "If a known NP-complete problem reduces to a new problem AND that new "
                   "problem is in NP, the new problem is also NP-complete.\n\n"),

    # ── Relevance to TCAA ────────────────────────────────────────────────────
    ("heading",    "6. Relevance to This Project (TCAA)\n"),
    ("muted",      "─────────────────────────────────────\n"),
    ("normal",     "Our DP 0/1 Knapsack runs in O(n * W) — this is PSEUDO-POLYNOMIAL "
                   "(polynomial in the numeric value of W, not its bit-length). When W is "
                   "very large the approach becomes infeasible, which is exactly the NP "
                   "boundary.\n\n"
                   "Our Greedy Scheduler is a polynomial-time HEURISTIC: fast but not always "
                   "optimal. Comparing Greedy vs. DP output shows the tradeoff between "
                   "tractability and optimality — the practical heart of P vs NP.\n\n"
                   "When a problem is NP-complete, practitioners use:\n"),
    ("yellow",     "  Approximation  — provably close to optimal\n"),
    ("yellow",     "  Heuristics     — work well in practice, no worst-case guarantee\n"),
    ("yellow",     "  Restricted DP  — exact solution when input has special structure\n"),
    ("yellow",     "  Pruned search  — branch-and-bound for small or bounded instances\n\n"),

    # ── Conclusion ───────────────────────────────────────────────────────────
    ("heading",    "7. Key Takeaway\n"),
    ("muted",      "────────────────\n"),
    ("sub",        "P vs NP is the boundary between efficient SOLVING and efficient CHECKING.\n\n"),
    ("normal",     "Finding that a problem is NP-complete does not mean give up. It means "
                   "choose the right response: approximation, heuristics, restricted DP, "
                   "or pruned exponential search for small instances.\n\n"
                   "The three questions to ask for any new problem:\n"),
    ("green",      "  1. Can I SOLVE it efficiently?  (Is it in P?)\n"),
    ("yellow",     "  2. Can I VERIFY a solution efficiently?  (Is it in NP?)\n"),
    ("red",        "  3. Is it hard? Can I reduce a known hard problem to it?\n\n"),

    # ── Our Reflection ───────────────────────────────────────────────────────
    ("heading",    "8. Our Reflection — What Building TCAA Taught Us\n"),
    ("muted",      "───────────────────────────────────────────────────\n"),
    ("sub",        "Observation 1: Greedy vs. DP on the same task set\n"),
    ("normal",     "When we ran both schedulers on identical inputs, the Greedy result was "
                   "always fast but sometimes left value on the table. The DP result was "
                   "always optimal but noticeably slower as the number of tasks or available "
                   "time (W) grew. This was P vs NP made visible — not as a theorem, but as "
                   "a gap we could actually measure in our own app.\n\n"),
    ("sub",        "Observation 2: The pseudo-polynomial wall\n"),
    ("normal",     "Our DP Knapsack runs in O(n * W). With small W it felt instant. But as "
                   "we increased W, the table grew and the delay became real. This showed us "
                   "exactly why 'pseudo-polynomial' is not the same as truly polynomial — the "
                   "algorithm is efficient on typical inputs but can still blow up when W is "
                   "large, just as NP theory predicts.\n\n"),
    ("sub",        "Observation 3: Dijkstra vs. brute-force routing\n"),
    ("normal",     "Dijkstra found the shortest campus path almost instantly across all "
                   "building combinations. Thinking about what a brute-force permutation "
                   "search would cost — O(V!) — made it clear why having a polynomial-time "
                   "algorithm is not just academically nice but practically essential.\n\n"),
    ("sub",        "Observation 4: String matching — O(n*m) vs O(n+m)\n"),
    ("normal",     "Running all three search algorithms on the same document and pattern "
                   "showed the Naive approach slowing down on longer texts while KMP stayed "
                   "flat. That timing difference is the Big-O gap made tangible — the same "
                   "result, but one algorithm lives in P comfortably while the other edges "
                   "toward its worst case.\n\n"),
    ("sub",        "What P vs NP means to us as developers\n"),
    ("normal",     "Before this project, P vs NP felt like an abstract theory problem. "
                   "After implementing Greedy, DP, Dijkstra, KMP, and Rabin-Karp side by "
                   "side — and watching their runtimes diverge on real inputs — the "
                   "classification became a practical engineering tool. Knowing a problem "
                   "is NP-complete tells you to stop searching for a perfect polynomial "
                   "solution and start designing smart approximations instead.\n"),
]


# ──────────────────────────────────────────────────────────────────────────────
# Complexity table widget
# ──────────────────────────────────────────────────────────────────────────────

class ComplexityTable(tk.Frame):
    HEADERS = ["Algorithm", "Best Case", "Average Case", "Worst Case", "Space"]
    COL_W   = [22, 12, 14, 12, 12]

    def __init__(self, parent, category, rows):
        super().__init__(parent, bg=COLORS["card"])

        tk.Label(
            self, text=f"  {category}",
            font=("Courier New", 11, "bold"),
            fg=COLORS["accent"], bg=COLORS["card"], anchor="w",
        ).pack(fill="x", pady=(10, 4))

        tbl = tk.Frame(self, bg=COLORS["border"], bd=1, relief="solid")
        tbl.pack(fill="x", padx=4)

        # Header
        hdr = tk.Frame(tbl, bg=COLORS["header_bg"])
        hdr.pack(fill="x")
        for i, (h, w) in enumerate(zip(self.HEADERS, self.COL_W)):
            tk.Label(
                hdr, text=h,
                font=("Courier New", 9, "bold"),
                fg="#ffffff", bg=COLORS["header_bg"],
                width=w, anchor="center", padx=6, pady=5,
            ).grid(row=0, column=i, sticky="nsew", padx=1)

        # Rows
        for ridx, (algo, best, avg, worst, space, ck) in enumerate(rows):
            row_bg = COLORS["card"] if ridx % 2 == 0 else "#F0F5F8"
            rf = tk.Frame(tbl, bg=row_bg)
            rf.pack(fill="x")
            for cidx, (val, w) in enumerate(zip([algo, best, avg, worst, space], self.COL_W)):
                fg = COLORS[ck] if cidx > 0 else COLORS["text"]
                tk.Label(
                    rf, text=val,
                    font=("Courier New", 9),
                    fg=fg, bg=row_bg,
                    width=w,
                    anchor="center" if cidx > 0 else "w",
                    padx=6, pady=4,
                ).grid(row=0, column=cidx, sticky="nsew", padx=1)


# ──────────────────────────────────────────────────────────────────────────────
# Public entry point
# ──────────────────────────────────────────────────────────────────────────────

def build_algorithm_info_tab(notebook: ttk.Notebook) -> tk.Frame:
    """
    Build and return the Algorithm Info tab frame.

    Usage:
        tab = build_algorithm_info_tab(notebook)
        notebook.add(tab, text="Algorithm Info")
    """
    tab = tk.Frame(notebook, bg=COLORS["bg"])

    # Page header
    hdr = tk.Frame(tab, bg=COLORS["header_bg"], pady=14)
    hdr.pack(fill="x")
    tk.Label(hdr, text="Algorithm Info & Analysis",
             font=("Courier New", 18, "bold"),
             fg="#ffffff", bg=COLORS["header_bg"]).pack()
    tk.Label(hdr, text="Big-O Complexities  ·  P vs NP  ·  Algorithm Classification",
             font=("Courier New", 9), fg="#F3E3D0", bg=COLORS["header_bg"]).pack()

    # Inner notebook
    style = ttk.Style()
    style.configure("Info.TNotebook", background=COLORS["bg"], borderwidth=0)
    style.configure("Info.TNotebook.Tab",
                    background=COLORS["panel"], foreground=COLORS["subtext"],
                    font=("Courier New", 10, "bold"), padding=[16, 6], borderwidth=0)
    style.map("Info.TNotebook.Tab",
              background=[("selected", COLORS["card"])],
              foreground=[("selected", COLORS["accent"])])

    inner = ttk.Notebook(tab, style="Info.TNotebook")
    inner.pack(fill="both", expand=True, padx=10, pady=10)

    _build_complexity_tab(inner)
    _build_pvsnp_tab(inner)

    return tab


# ──────────────────────────────────────────────────────────────────────────────

def _build_complexity_tab(nb):
    frame = tk.Frame(nb, bg=COLORS["card"])
    nb.add(frame, text="  Big-O Complexities  ")

    canvas = tk.Canvas(frame, bg=COLORS["card"], highlightthickness=0)
    sb = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=sb.set)
    sb.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)

    inner = tk.Frame(canvas, bg=COLORS["card"])
    cw = canvas.create_window((0, 0), window=inner, anchor="nw")

    canvas.bind("<Configure>", lambda e: canvas.itemconfig(cw, width=e.width))
    canvas.bind_all("<MouseWheel>",
                    lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
    inner.bind("<Configure>",
               lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    # Intro
    tk.Label(inner,
             text="Time and space complexities for every algorithm in TCAA.\n"
                  "Cells are colour-coded by efficiency class.",
             font=("Courier New", 9), fg=COLORS["subtext"], bg=COLORS["card"],
             justify="left", padx=10, pady=6).pack(anchor="w", padx=10)

    # Legend
    leg = tk.Frame(inner, bg=COLORS["card"])
    leg.pack(anchor="w", padx=14, pady=(0, 6))
    tk.Label(leg, text="Key: ", font=("Courier New", 8, "bold"),
             fg=COLORS["subtext"], bg=COLORS["card"]).pack(side="left")
    for ck, desc in COLOR_LEGEND:
        tk.Label(leg, text="●", font=("Courier New", 11, "bold"),
                 fg=COLORS[ck], bg=COLORS["card"]).pack(side="left", padx=(6, 2))
        tk.Label(leg, text=desc, font=("Courier New", 8),
                 fg=COLORS["subtext"], bg=COLORS["card"]).pack(side="left", padx=(0, 10))

    # Tables
    for cat, rows in COMPLEXITY_DATA.items():
        ComplexityTable(inner, cat, rows).pack(fill="x", padx=10, pady=(0, 8))

    # Notation reference
    ref = tk.LabelFrame(inner, text="  Notation Reference  ",
                        font=("Courier New", 10, "bold"),
                        fg=COLORS["accent"], bg=COLORS["card"],
                        bd=1, relief="solid")
    ref.pack(fill="x", padx=10, pady=(8, 6))
    for sym, meaning in [
        ("n", "text length / number of tasks"),
        ("m", "pattern length"),
        ("V", "number of vertices (buildings)"),
        ("E", "number of edges (paths)"),
        ("W", "max weight / available study time"),
    ]:
        r = tk.Frame(ref, bg=COLORS["card"])
        r.pack(fill="x", padx=8, pady=2)
        tk.Label(r, text=f"  {sym:<4}", font=("Courier New", 9, "bold"),
                 fg=COLORS["accent2"], bg=COLORS["card"], width=5, anchor="w").pack(side="left")
        tk.Label(r, text=f"->  {meaning}", font=("Courier New", 9),
                 fg=COLORS["text"], bg=COLORS["card"], anchor="w").pack(side="left")

    # Big Eight efficiency classes (from Week 2 slides)
    eight = tk.LabelFrame(inner, text="  The Big Eight Efficiency Classes  ",
                          font=("Courier New", 10, "bold"),
                          fg=COLORS["accent"], bg=COLORS["card"],
                          bd=1, relief="solid")
    eight.pack(fill="x", padx=10, pady=(0, 6))

    big_eight = [
        ("O(1)",       "green",  "Constant",      "Array index lookup, hash table get"),
        ("O(log n)",   "green",  "Logarithmic",   "Binary search on sorted data"),
        ("O(n)",       "green",  "Linear",        "Sequential scan, linear search"),
        ("O(n log n)", "yellow", "Linearithmic",  "Merge sort, quick sort (avg), heap sort"),
        ("O(n^2)",     "yellow", "Quadratic",     "Bubble sort, selection sort, naive string match"),
        ("O(n^3)",     "yellow", "Cubic",         "Naive matrix multiply, triple nested loops"),
        ("O(2^n)",     "red",    "Exponential",   "Subset generation, naive Fibonacci"),
        ("O(n!)",      "red",    "Factorial",     "Permutation generation, brute-force TSP"),
    ]

    hdr8 = tk.Frame(eight, bg=COLORS["header_bg"])
    hdr8.pack(fill="x", padx=4, pady=(4, 0))
    for h, w in [("Notation", 12), ("Class", 14), ("Example Use", 36)]:
        tk.Label(hdr8, text=h, font=("Courier New", 8, "bold"),
                 fg="#ffffff", bg=COLORS["header_bg"],
                 width=w, anchor="center", padx=4, pady=3).pack(side="left")

    for ridx, (notation, ck, cls, example) in enumerate(big_eight):
        row_bg = COLORS["card"] if ridx % 2 == 0 else "#F0F5F8"
        r8 = tk.Frame(eight, bg=row_bg)
        r8.pack(fill="x", padx=4)
        tk.Label(r8, text=notation, font=("Courier New", 9, "bold"),
                 fg=COLORS[ck], bg=row_bg, width=12, anchor="center", padx=4, pady=3).pack(side="left")
        tk.Label(r8, text=cls, font=("Courier New", 9),
                 fg=COLORS["text"], bg=row_bg, width=14, anchor="w", padx=4).pack(side="left")
        tk.Label(r8, text=example, font=("Courier New", 8),
                 fg=COLORS["subtext"], bg=row_bg, width=36, anchor="w", padx=4).pack(side="left")

    # Real-world examples (from professor's slides)
    rw = tk.LabelFrame(inner, text="  Real-World Connections (from lectures)  ",
                       font=("Courier New", 10, "bold"),
                       fg=COLORS["accent"], bg=COLORS["card"],
                       bd=1, relief="solid")
    rw.pack(fill="x", padx=10, pady=(0, 14))

    real_world = [
        ("GPS Navigation",       "Dijkstra's shortest path",    "Boston->NY->Philadelphia: greedy min-distance"),
        ("Library Book Search",  "Binary Search  O(log n)",     "Start middle, eliminate half each step"),
        ("Coin Change",          "Greedy Scheduler",            "Minimize coins — but greedy isn't always optimal"),
        ("DNA Sequence Align",   "DP / String Matching",        "Find longest common subsequence: AGGTA vs GXTXAYB"),
        ("Network Cable Layout", "Prim's MST",                  "Connect all buildings at minimum total cable cost"),
        ("File Text Search",     "KMP / Rabin-Karp / Naive",    "Pattern search in notes — O(n+m) vs O(n*m)"),
        ("Task Scheduling",      "Greedy vs DP Knapsack",       "Greedy: fast approx. DP: exact but O(n*W)"),
        ("Social Network",       "BFS / DFS",                   "Friend recommendations, connectivity checking"),
    ]

    for ridx, (context, algo, note) in enumerate(real_world):
        row_bg = COLORS["card"] if ridx % 2 == 0 else "#F0F5F8"
        rr = tk.Frame(rw, bg=row_bg)
        rr.pack(fill="x", padx=4)
        tk.Label(rr, text=f"  {context:<24}", font=("Courier New", 8, "bold"),
                 fg=COLORS["accent"], bg=row_bg, anchor="w", pady=3).pack(side="left")
        tk.Label(rr, text=f"{algo:<28}", font=("Courier New", 8),
                 fg=COLORS["green"], bg=row_bg, anchor="w").pack(side="left")
        tk.Label(rr, text=note, font=("Courier New", 8),
                 fg=COLORS["subtext"], bg=row_bg, anchor="w").pack(side="left")


def _build_pvsnp_tab(nb):
    frame = tk.Frame(nb, bg=COLORS["panel"])
    nb.add(frame, text="  P vs NP  ")

    left  = tk.Frame(frame, bg=COLORS["panel"])
    right = tk.Frame(frame, bg=COLORS["panel"], width=260)
    left.pack(side="left", fill="both", expand=True, padx=(10, 4), pady=10)
    right.pack(side="right", fill="y", padx=(4, 10), pady=10)
    right.pack_propagate(False)

    # Scrollable text
    tf = tk.Frame(left, bg=COLORS["card"], bd=1, relief="solid",
                  highlightbackground=COLORS["border"])
    tf.pack(fill="both", expand=True)
    tsb = tk.Scrollbar(tf)
    tsb.pack(side="right", fill="y")
    txt = tk.Text(
        tf, wrap="word", font=("Courier New", 9),
        fg=COLORS["text"], bg=COLORS["card"],
        relief="flat", bd=0, padx=14, pady=10,
        yscrollcommand=tsb.set, cursor="arrow",
    )
    txt.pack(fill="both", expand=True)
    tsb.config(command=txt.yview)

    # Tags
    txt.tag_configure("heading", font=("Courier New", 10, "bold"), foreground=COLORS["accent"])
    txt.tag_configure("sub",     font=("Courier New", 9, "bold"),  foreground=COLORS["accent2"])
    txt.tag_configure("green",   foreground=COLORS["green"])
    txt.tag_configure("red",     foreground=COLORS["red"])
    txt.tag_configure("muted",   foreground=COLORS["subtext"])

    for tag, content in PVSNP_SECTIONS:
        txt.insert("end", content, tag if tag != "normal" else ())
    txt.config(state="disabled")

    # Summary cards
    tk.Label(right, text="Quick Reference",
             font=("Courier New", 10, "bold"), fg=COLORS["text"],
             bg=COLORS["panel"]).pack(pady=(0, 6))

    def card(title, body, title_color):
        f = tk.Frame(right, bg=COLORS["card"], bd=1, relief="solid",
                     highlightbackground=COLORS["border"])
        f.pack(fill="x", pady=(0, 8))
        tk.Label(f, text=title, font=("Courier New", 9, "bold"),
                 fg=title_color, bg=COLORS["card"], anchor="w",
                 padx=8, pady=4).pack(fill="x")
        tk.Frame(f, bg=COLORS["border"], height=1).pack(fill="x")
        tk.Label(f, text=body, font=("Courier New", 8),
                 fg=COLORS["text"], bg=COLORS["card"], anchor="nw",
                 justify="left", padx=8, pady=6, wraplength=225).pack(fill="x")

    card("P  —  Fast to Solve",
         "Solvable in polynomial time.\n\nBFS, DFS, Dijkstra,\nPrim's MST, KMP, Greedy.", COLORS["green"])
    card("NP  —  Fast to Check",
         "Solutions verifiable in\npolynomial time.\nP is a subset of NP.\n\n3-SAT, TSP, Knapsack.", COLORS["yellow"])
    card("NP-Hard  —  Hard (via reduction)",
         "At least as hard as every\nNP problem via reduction.\nMay not itself be in NP.", COLORS["red"])
    card("NP-Complete  —  Hardest in NP",
         "In NP AND NP-Hard.\n\n3-SAT, Circuit-SAT,\nTSP decision, Knapsack\ndecision, Graph Coloring.", COLORS["red"])

    # Complexity spectrum
    tk.Label(right, text="Complexity Spectrum",
             font=("Courier New", 9, "bold"), fg=COLORS["text"],
             bg=COLORS["panel"]).pack(pady=(8, 4))

    for label, ck, tag in SPECTRUM:
        r = tk.Frame(right, bg=COLORS["panel"])
        r.pack(fill="x", pady=1)
        tk.Label(r, text="|", font=("Courier New", 9, "bold"),
                 fg=COLORS[ck], bg=COLORS["panel"]).pack(side="left", padx=(2,4))
        tk.Label(r, text=label, font=("Courier New", 8),
                 fg=COLORS["text"], bg=COLORS["panel"], anchor="w", width=20).pack(side="left")
        tk.Label(r, text=tag, font=("Courier New", 7, "bold"),
                 fg=COLORS[ck], bg=COLORS["panel"]).pack(side="left")


# ──────────────────────────────────────────────────────────────────────────────
# Preview: run this file directly
# ──────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    root = tk.Tk()
    root.title("TCAA — Algorithm Info Module")
    root.geometry("1050x700")
    root.configure(bg=COLORS["bg"])

    style = ttk.Style()
    style.theme_use("default")
    style.configure("TNotebook", background=COLORS["bg"], borderwidth=0)
    style.configure("TNotebook.Tab",
                    background=COLORS["panel"], foreground=COLORS["subtext"],
                    font=("Courier New", 10, "bold"), padding=[18, 7])
    style.map("TNotebook.Tab",
              background=[("selected", COLORS["card"])],
              foreground=[("selected", COLORS["accent"])])

    nb = ttk.Notebook(root)
    nb.pack(fill="both", expand=True, padx=6, pady=6)

    tab = build_algorithm_info_tab(nb)
    nb.add(tab, text="  Algorithm Info  ")

    root.mainloop()


def launch():
    import tkinter as tk
    from tkinter import ttk
    root = tk.Toplevel()
    nb = ttk.Notebook(root)
    nb.pack(fill="both", expand=True)
    nb.add(build_algorithm_info_tab(nb), text="Algorithm Info")
    root.mainloop()
