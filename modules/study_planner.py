"""
TCAA - Study Planner Module
Greedy Scheduler · DP 0/1 Knapsack
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from algorithms.dynamic_programming import Task, greedy_scheduler, dp_knapsack_scheduler

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

def _entry(parent, width=16):
    return tk.Entry(parent, font=("Courier New", 9), fg=C["text"],
                    bg=C["entry_bg"], insertbackground=C["accent"],
                    relief="flat", bd=4, width=width)

def _btn(parent, text, cmd, color=None):
    return tk.Button(parent, text=text, command=cmd,
                     font=("Courier New", 9, "bold"), fg="#FFFFFF",
                     bg=color or C["accent"],
                     activebackground=C["accent2"], activeforeground="#FFFFFF",
                     relief="flat", bd=0, padx=10, pady=4, cursor="hand2")

def _sec(parent, title):
    f = tk.Frame(parent, bg=C["header_bg"])
    f.pack(fill="x", pady=(10, 0))
    tk.Label(f, text=f"  {title}", font=("Courier New", 10, "bold"),
             fg="#FFFFFF", bg=C["header_bg"], anchor="w", pady=4).pack(fill="x")


class ResultPanel(tk.Frame):
    def __init__(self, parent, title, color):
        super().__init__(parent, bg=C["panel"], bd=1, relief="solid",
                         highlightbackground=C["border"])
        tk.Label(self, text=title, font=("Courier New", 11, "bold"),
                 fg=color, bg=C["panel"], anchor="center", pady=6).pack(fill="x")
        tk.Frame(self, bg=C["border"], height=1).pack(fill="x")

        sb = tk.Scrollbar(self)
        sb.pack(side="right", fill="y")
        self.txt = tk.Text(self, font=("Courier New", 9), fg=C["text"],
                           bg=C["card"], relief="flat", bd=0, padx=10, pady=8,
                           yscrollcommand=sb.set, state="disabled",
                           cursor="arrow", wrap="word")
        self.txt.pack(fill="both", expand=True)
        sb.config(command=self.txt.yview)

        self.txt.tag_configure("heading", font=("Courier New", 9, "bold"), foreground=color)
        self.txt.tag_configure("task",    foreground=C["text"])
        self.txt.tag_configure("time",    foreground=C["brown"])
        self.txt.tag_configure("value",   foreground=C["green"])
        self.txt.tag_configure("muted",   foreground=C["subtext"])
        self.txt.tag_configure("sep",     foreground=C["border"])

        self.footer = tk.Frame(self, bg=C["header_bg"])
        self.footer.pack(fill="x")
        self.time_lbl  = tk.Label(self.footer, text="Time:  —",
                                  font=("Courier New", 9, "bold"),
                                  fg=C["brown"], bg=C["header_bg"], padx=8, pady=4)
        self.time_lbl.pack(side="left")
        self.val_lbl   = tk.Label(self.footer, text="Value:  —",
                                  font=("Courier New", 9, "bold"),
                                  fg=C["green"], bg=C["header_bg"], padx=8)
        self.val_lbl.pack(side="left")
        self.badge = tk.Label(self.footer, text="",
                              font=("Courier New", 8, "bold"),
                              fg="#FFFFFF", bg=C["header_bg"], padx=8)
        self.badge.pack(side="right", padx=6, pady=4)

    def clear(self):
        self.txt.config(state="normal")
        self.txt.delete("1.0", tk.END)
        self.txt.config(state="disabled")
        self.time_lbl.config(text="Time:  —")
        self.val_lbl.config(text="Value:  —")
        self.badge.config(text="", bg=C["header_bg"])

    def show(self, result, available, is_winner=False):
        selected = result["selected_tasks"]
        total_time  = result["total_time"]
        total_value = result["total_value"]

        self.txt.config(state="normal")
        self.txt.delete("1.0", tk.END)

        if not selected:
            self.txt.insert("end", "No tasks fit within the time budget.\n", "muted")
        else:
            self.txt.insert("end", f"{'Task':<22} {'Time':>5}  {'Value':>6}  {'Ratio':>6}\n", "heading")
            self.txt.insert("end", "─" * 44 + "\n", "sep")
            for t in selected:
                self.txt.insert("end", f"  {t.name:<20}", "task")
                self.txt.insert("end", f" {int(t.duration):>5}", "time")
                self.txt.insert("end", f"  {int(t.value):>6}", "value")
                self.txt.insert("end", f"  {t.ratio():>6.2f}\n", "muted")
            self.txt.insert("end", "─" * 44 + "\n", "sep")
            unused = available - total_time
            self.txt.insert("end", f"\n  Tasks selected : {len(selected)}\n", "muted")
            self.txt.insert("end", f"  Time used      : {total_time} / {available}", "time")
            self.txt.insert("end", f"  ({unused} unused)\n", "muted")
            self.txt.insert("end", f"  Total value    : {total_value}\n", "value")
            self.txt.insert("end", f"  Efficiency     : {result['efficiency']:.2f}\n", "muted")

        self.txt.config(state="disabled")
        self.time_lbl.config(text=f"Time:  {total_time} / {available}")
        self.val_lbl.config(text=f"Value:  {total_value}")
        if is_winner:
            self.badge.config(text="  ★ OPTIMAL  ", bg=C["accent"])
        else:
            self.badge.config(text="", bg=C["header_bg"])


def build_study_planner_tab(notebook):
    tab = tk.Frame(notebook, bg=C["bg"])
    tasks = []

    # Header
    hdr = tk.Frame(tab, bg=C["header_bg"], pady=11)
    hdr.pack(fill="x")
    tk.Label(hdr, text="Study Planner",
             font=("Courier New", 17, "bold"), fg="#FFFFFF", bg=C["header_bg"]).pack()
    tk.Label(hdr, text="Greedy Scheduler  vs  DP 0/1 Knapsack — find the optimal study plan",
             font=("Courier New", 10), fg=C["border"], bg=C["header_bg"]).pack()

    body = tk.Frame(tab, bg=C["bg"])
    body.pack(fill="both", expand=True, padx=12, pady=10)

    # ── Left panel ────────────────────────────────────────────────────────────
    left = tk.Frame(body, bg=C["panel"], width=300)
    left.pack(side="left", fill="y", padx=(0, 10))
    left.pack_propagate(False)

    _sec(left, "Add Task")
    form = tk.Frame(left, bg=C["panel"])
    form.pack(fill="x", padx=10, pady=8)

    entries = {}
    for label in ["Task Name", "Study Time (hrs)", "Value / Priority"]:
        row = tk.Frame(form, bg=C["panel"])
        row.pack(fill="x", pady=3)
        tk.Label(row, text=f"{label}:", font=("Courier New", 8), fg=C["subtext"],
                 bg=C["panel"], width=18, anchor="w").pack(side="left")
        e = _entry(row, width=12)
        e.pack(side="left", fill="x", expand=True)
        entries[label] = e

    # Task list canvas
    _sec(left, "Task List")

    hdr_row = tk.Frame(left, bg=C["header_bg"])
    hdr_row.pack(fill="x", padx=6, pady=(4, 0))
    for h, w in [("Name", 20), ("Time", 7), ("Value", 7), ("Ratio", 7)]:
        tk.Label(hdr_row, text=h, font=("Courier New", 8, "bold"),
                 fg="#FFFFFF", bg=C["header_bg"], width=w,
                 anchor="center", pady=2).pack(side="left")

    list_outer = tk.Frame(left, bg=C["border"], bd=1, relief="solid")
    list_outer.pack(fill="both", expand=True, padx=6, pady=(0, 4))
    canvas = tk.Canvas(list_outer, bg=C["card"], highlightthickness=0, height=140)
    sb2 = tk.Scrollbar(list_outer, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=sb2.set)
    sb2.pack(side="right", fill="y")
    canvas.pack(fill="both", expand=True)
    task_inner = tk.Frame(canvas, bg=C["card"])
    task_win = canvas.create_window((0, 0), window=task_inner, anchor="nw")
    task_inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.bind("<Configure>", lambda e: canvas.itemconfig(task_win, width=e.width))

    count_lbl = tk.Label(left, text="0 tasks", font=("Courier New", 8),
                         fg=C["subtext"], bg=C["panel"], anchor="e", padx=8)
    count_lbl.pack(fill="x")

    def refresh_task_list():
        for w in task_inner.winfo_children():
            w.destroy()
        for i, t in enumerate(tasks):
            bg = C["card"] if i % 2 == 0 else "#F8F5F2"
            row = tk.Frame(task_inner, bg=bg)
            row.pack(fill="x")
            tk.Label(row, text=t.name, font=("Courier New", 9), fg=C["text"],
                     bg=bg, width=20, anchor="w", padx=4, pady=2).pack(side="left")
            tk.Label(row, text=str(int(t.duration)), font=("Courier New", 9),
                     fg=C["brown"], bg=bg, width=7, anchor="center").pack(side="left")
            tk.Label(row, text=str(int(t.value)), font=("Courier New", 9),
                     fg=C["green"], bg=bg, width=7, anchor="center").pack(side="left")
            tk.Label(row, text=f"{t.ratio():.2f}", font=("Courier New", 9),
                     fg=C["accent2"], bg=bg, width=7, anchor="center").pack(side="left")
            idx = i
            tk.Button(row, text="✕", font=("Courier New", 8, "bold"),
                      fg=C["red"], bg=bg, activebackground=C["border"],
                      relief="flat", bd=0, cursor="hand2",
                      command=lambda i=idx: delete_task(i)).pack(side="left", padx=4)
        count = len(tasks)
        count_lbl.config(text=f"{count} task{'s' if count != 1 else ''}",
                         fg=C["accent"] if count else C["subtext"])

    def delete_task(idx):
        tasks.pop(idx)
        refresh_task_list()

    def add_task():
        name = entries["Task Name"].get().strip()
        t_s  = entries["Study Time (hrs)"].get().strip()
        v_s  = entries["Value / Priority"].get().strip()
        if not name:
            messagebox.showerror("Input Error", "Task name cannot be empty.")
            return
        try:
            t = int(t_s); v = int(v_s)
            if t <= 0 or v <= 0: raise ValueError
        except ValueError:
            messagebox.showerror("Input Error", "Time and Value must be positive integers.")
            return
        tasks.append(Task(name, t, v))
        refresh_task_list()
        for e in entries.values(): e.delete(0, tk.END)
        entries["Task Name"].focus()

    entries["Value / Priority"].bind("<Return>", lambda e: add_task())

    btn_row = tk.Frame(left, bg=C["panel"])
    btn_row.pack(fill="x", padx=10, pady=(0, 6))
    _btn(btn_row, "＋  Add Task", add_task, C["accent"]).pack(side="left")
    _btn(btn_row, "Clear All",
         lambda: [tasks.clear(), refresh_task_list()], C["red"]).pack(side="right")

    # Run buttons
    _sec(left, "Run Schedulers")
    ctrl = tk.Frame(left, bg=C["panel"])
    ctrl.pack(fill="x", padx=10, pady=8)

    time_row = tk.Frame(ctrl, bg=C["panel"])
    time_row.pack(fill="x", pady=(0, 8))
    tk.Label(time_row, text="Available time (hrs):", font=("Courier New", 8),
             fg=C["subtext"], bg=C["panel"], anchor="w").pack(side="left")
    avail_entry = _entry(time_row, width=6)
    avail_entry.insert(0, "10")
    avail_entry.pack(side="left", padx=(6, 0))

    # Complexity info
    info = tk.Frame(left, bg=C["card"], bd=1, relief="solid")
    info.pack(fill="x", padx=6, pady=(0, 8))
    for line, fg in [
        ("Greedy  O(n log n)", C["brown"]),
        ("  fast, not always optimal", C["subtext"]),
        ("DP      O(n × W)", C["green"]),
        ("  optimal, pseudo-polynomial", C["subtext"]),
    ]:
        tk.Label(info, text=f"  {line}", font=("Courier New", 8),
                 fg=fg, bg=C["card"], anchor="w", pady=1).pack(fill="x")

    # ── Right panel ───────────────────────────────────────────────────────────
    right = tk.Frame(body, bg=C["bg"])
    right.pack(side="left", fill="both", expand=True)

    status_bar = tk.Frame(right, bg=C["panel"], height=30)
    status_bar.pack(fill="x", pady=(0, 6))
    status_lbl = tk.Label(status_bar, text="", font=("Courier New", 9, "bold"),
                          fg=C["accent2"], bg=C["panel"], anchor="center")
    status_lbl.pack(fill="x", pady=5)

    cols = tk.Frame(right, bg=C["bg"])
    cols.pack(fill="both", expand=True)

    greedy_panel = ResultPanel(cols, "Greedy Scheduler", C["brown"])
    dp_panel     = ResultPanel(cols, "DP 0/1 Knapsack",  C["green"])
    greedy_panel.pack(side="left", fill="both", expand=True, padx=(0, 5))
    dp_panel.pack(side="left", fill="both", expand=True, padx=(5, 0))

    def get_avail():
        try:
            a = int(avail_entry.get())
            if a <= 0: raise ValueError
            return a
        except ValueError:
            messagebox.showerror("Input Error", "Available time must be a positive integer.")
            return None

    def run_greedy():
        if not tasks: messagebox.showerror("Error", "Add at least one task first."); return
        a = get_avail()
        if a is None: return
        greedy_panel.show(greedy_scheduler(tasks, a), a)
        status_lbl.config(text="Greedy complete — run DP to compare  ⚡", fg=C["brown"])

    def run_dp():
        if not tasks: messagebox.showerror("Error", "Add at least one task first."); return
        a = get_avail()
        if a is None: return
        dp_panel.show(dp_knapsack_scheduler(tasks, a), a, is_winner=True)
        status_lbl.config(text="DP complete — run Greedy to compare  ⚡", fg=C["green"])

    def run_both():
        if not tasks: messagebox.showerror("Error", "Add at least one task first."); return
        a = get_avail()
        if a is None: return
        gr = greedy_scheduler(tasks, a)
        dp = dp_knapsack_scheduler(tasks, a)
        same = gr["total_value"] == dp["total_value"]
        greedy_panel.show(gr, a, is_winner=same)
        dp_panel.show(dp, a, is_winner=True)
        if same:
            status_lbl.config(text=f"✔ Both agree — optimal value: {dp['total_value']}  (Greedy matched DP!)", fg=C["green"])
        else:
            diff = dp["total_value"] - gr["total_value"]
            status_lbl.config(text=f"DP found better solution  |  DP: {dp['total_value']}  vs  Greedy: {gr['total_value']}  (DP wins by +{diff})", fg=C["accent"])

    for text, cmd, color in [
        ("▶  Run Greedy",      run_greedy, C["brown"]),
        ("▶  Run DP Knapsack", run_dp,     C["green"]),
        ("⚡  Compare Both",   run_both,   C["accent"]),
    ]:
        _btn(ctrl, text, cmd, color).pack(fill="x", pady=2)

    return tab


def launch():
    import tkinter as tk
    from tkinter import ttk
    root = tk.Toplevel()
    nb = ttk.Notebook(root)
    nb.pack(fill="both", expand=True)
    nb.add(build_study_planner_tab(nb), text="Study Planner")
    root.mainloop()
