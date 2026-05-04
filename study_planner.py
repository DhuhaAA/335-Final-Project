"""
TCAA - Study Planner Module
CPSC 335 Final Project - Titan Campus Algorithmic Assistant

Features:
  - Add / remove tasks (name, time, value)
  - Set available study time
  - Run Greedy Scheduler   O(n log n)
  - Run DP 0/1 Knapsack    O(n * W)
  - Side-by-side comparison with winner highlight
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

# Allow import from sibling algorthims/ package
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from algorthims.sheduling_algorthims import greedy_schedule, knapsack_dp


# ──────────────────────────────────────────────────────────────────────────────
# Color palette  — #81A6C6 / #AACDDC / #F3E3D0 / #D2C4B4
# ──────────────────────────────────────────────────────────────────────────────
C = {
    "bg":        "#F3E3D0",   # warm cream — main background
    "panel":     "#AACDDC",   # light blue — side panel / section headers
    "card":      "#ffffff",   # white — card / text area background
    "accent":    "#81A6C6",   # steel blue — primary accent, buttons
    "accent2":   "#5A86A8",   # darker blue — hover / active
    "green":     "#4A8C6F",   # muted green — value / positive
    "red":       "#B85C5C",   # muted red — delete / warning
    "yellow":    "#8B6F3E",   # warm brown — time / greedy
    "text":      "#1E2D3A",   # near-black — primary text
    "subtext":   "#5A7080",   # medium blue-grey — muted text
    "border":    "#D2C4B4",   # tan — borders / dividers
    "header_bg": "#81A6C6",   # steel blue — tab headers
    "entry_bg":  "#ffffff",   # white — entry fields
    "select":    "#AACDDC",   # light blue — selection
}


# ──────────────────────────────────────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────────────────────────────────────

def _label(parent, text, size=9, weight="normal", color=None, anchor="w", **kw):
    return tk.Label(
        parent, text=text,
        font=("Courier New", size, weight),
        fg=color or C["text"],
        bg=parent.cget("bg"),
        anchor=anchor, **kw
    )


def _entry(parent, width=18):
    e = tk.Entry(
        parent,
        font=("Courier New", 9),
        fg=C["text"],
        bg=C["entry_bg"],
        insertbackground=C["accent"],
        relief="flat",
        bd=4,
        width=width,
    )
    return e


def _button(parent, text, command, color=None):
    return tk.Button(
        parent, text=text, command=command,
        font=("Courier New", 9, "bold"),
        fg="#ffffff",
        bg=color or C["accent"],
        activebackground=C["accent2"],
        activeforeground="#ffffff",
        relief="flat",
        bd=0,
        padx=10, pady=4,
        cursor="hand2",
    )


def _section_header(parent, text):
    f = tk.Frame(parent, bg=C["header_bg"])
    f.pack(fill="x", pady=(10, 0))
    tk.Label(f, text=f"  {text}",
             font=("Courier New", 10, "bold"),
             fg=C["accent"], bg=C["header_bg"],
             anchor="w", pady=5).pack(fill="x")
    return f


# ──────────────────────────────────────────────────────────────────────────────
# Task Row widget  (used in the task table)
# ──────────────────────────────────────────────────────────────────────────────

class TaskRow(tk.Frame):
    COL_W = [24, 8, 8, 10]   # name, time, value, ratio

    def __init__(self, parent, idx, name, time, value, on_delete, bg):
        super().__init__(parent, bg=bg)
        self.idx = idx

        ratio = f"{value/time:.2f}"
        cells = [name, str(time), str(value), ratio]
        colors = [C["text"], C["yellow"], C["green"], C["accent2"]]

        for val, w, fg in zip(cells, self.COL_W, colors):
            tk.Label(self, text=val, font=("Courier New", 9),
                     fg=fg, bg=bg, width=w, anchor="center",
                     padx=4, pady=3).pack(side="left")

        tk.Button(self, text="✕", font=("Courier New", 8, "bold"),
                  fg=C["red"], bg=bg, activebackground=C["border"],
                  activeforeground=C["red"],
                  relief="flat", bd=0, cursor="hand2",
                  command=lambda: on_delete(idx)).pack(side="left", padx=4)


# ──────────────────────────────────────────────────────────────────────────────
# Results panel  (one column — Greedy or DP)
# ──────────────────────────────────────────────────────────────────────────────

class ResultPanel(tk.Frame):
    def __init__(self, parent, title, title_color):
        super().__init__(parent, bg=C["panel"], bd=1, relief="solid",
                         highlightbackground=C["border"])
        self.title_color = title_color

        tk.Label(self, text=title,
                 font=("Courier New", 11, "bold"),
                 fg=title_color, bg=C["panel"],
                 anchor="center", pady=7).pack(fill="x")
        tk.Frame(self, bg=C["border"], height=1).pack(fill="x")

        self.txt = tk.Text(
            self,
            font=("Courier New", 9),
            fg=C["text"], bg=C["card"],
            relief="flat", bd=0,
            padx=10, pady=8,
            state="disabled",
            cursor="arrow",
            wrap="word",
        )
        self.txt.pack(fill="both", expand=True, padx=6, pady=6)

        # Tags
        self.txt.tag_configure("heading",  font=("Courier New", 9, "bold"),  foreground=title_color)
        self.txt.tag_configure("task",     foreground=C["text"])
        self.txt.tag_configure("time",     foreground=C["yellow"])
        self.txt.tag_configure("value",    foreground=C["green"])
        self.txt.tag_configure("winner",   foreground=C["accent"],
                               font=("Courier New", 9, "bold"))
        self.txt.tag_configure("muted",    foreground=C["subtext"])
        self.txt.tag_configure("sep",      foreground=C["border"])

        # Footer bar
        self.footer = tk.Frame(self, bg=C["header_bg"])
        self.footer.pack(fill="x")
        self.time_lbl  = tk.Label(self.footer, text="Time:  —",
                                  font=("Courier New", 9, "bold"),
                                  fg=C["yellow"], bg=C["header_bg"], padx=8, pady=4)
        self.time_lbl.pack(side="left")
        self.value_lbl = tk.Label(self.footer, text="Value:  —",
                                  font=("Courier New", 9, "bold"),
                                  fg=C["green"], bg=C["header_bg"], padx=8)
        self.value_lbl.pack(side="left")
        self.badge = tk.Label(self.footer, text="",
                              font=("Courier New", 8, "bold"),
                              fg=C["bg"], bg=C["header_bg"], padx=8)
        self.badge.pack(side="right", padx=6, pady=4)

    def clear(self):
        self.txt.config(state="normal")
        self.txt.delete("1.0", tk.END)
        self.txt.config(state="disabled")
        self.time_lbl.config(text="Time:  —")
        self.value_lbl.config(text="Value:  —")
        self.badge.config(text="", bg=C["header_bg"])

    def show(self, chosen, total_time, total_value, available, is_winner=False):
        self.txt.config(state="normal")
        self.txt.delete("1.0", tk.END)

        if not chosen:
            self.txt.insert("end", "No tasks fit within the time budget.\n", "muted")
        else:
            self.txt.insert("end", f"{'Task':<22} {'Time':>5}  {'Value':>6}  {'Ratio':>6}\n", "heading")
            self.txt.insert("end", "─" * 44 + "\n", "sep")
            for name, t, val in chosen:
                ratio = val / t
                self.txt.insert("end", f"  {name:<20}", "task")
                self.txt.insert("end", f" {t:>5}", "time")
                self.txt.insert("end", f"  {val:>6}", "value")
                self.txt.insert("end", f"  {ratio:>6.2f}\n", "muted")

            self.txt.insert("end", "─" * 44 + "\n", "sep")
            unused = available - total_time
            self.txt.insert("end", f"\n  Tasks selected : {len(chosen)}\n", "muted")
            self.txt.insert("end", f"  Time used      : {total_time} / {available}", "time")
            self.txt.insert("end", f"  ({unused} unused)\n", "muted")
            self.txt.insert("end", f"  Total value    : {total_value}\n", "value")

        self.txt.config(state="disabled")
        self.time_lbl.config(text=f"Time:  {total_time} / {available}")
        self.value_lbl.config(text=f"Value:  {total_value}")

        if is_winner:
            self.badge.config(text="  ★ OPTIMAL  ", bg=C["accent"], fg="#ffffff")
        else:
            self.badge.config(text="", bg=C["header_bg"])


# ──────────────────────────────────────────────────────────────────────────────
# Main Study Planner Tab
# ──────────────────────────────────────────────────────────────────────────────

def build_study_planner_tab(notebook: ttk.Notebook) -> tk.Frame:
    """
    Build and return the Study Planner tab.

    Usage:
        tab = build_study_planner_tab(notebook)
        notebook.add(tab, text="Study Planner")
    """
    tab = _StudyPlannerTab(notebook)
    return tab


class _StudyPlannerTab(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=C["bg"])
        self.tasks = []          # list of (name, time, value)
        self._build_ui()

    # ──────────────────────────────────────────────────────────────────────────
    # UI Construction
    # ──────────────────────────────────────────────────────────────────────────

    def _build_ui(self):
        # ── Page header ───────────────────────────────────────────────────────
        hdr = tk.Frame(self, bg=C["header_bg"], pady=12)
        hdr.pack(fill="x")
        tk.Label(hdr, text="Study Planner",
                 font=("Courier New", 18, "bold"),
                 fg=C["accent"], bg=C["header_bg"]).pack()
        tk.Label(hdr, text="Greedy Scheduler  vs  DP 0/1 Knapsack — find the optimal study plan",
                 font=("Courier New", 11),
                 fg="#ffffff", bg=C["header_bg"]).pack()

        # ── Main body: left controls | right results ───────────────────────
        body = tk.Frame(self, bg=C["bg"])
        body.pack(fill="both", expand=True, padx=12, pady=10)

        left  = tk.Frame(body, bg=C["panel"], width=310)
        right = tk.Frame(body, bg=C["bg"])
        left.pack(side="left", fill="y", padx=(0, 10))
        right.pack(side="left", fill="both", expand=True)
        left.pack_propagate(False)

        self._build_input_panel(left)
        self._build_task_table(left)
        self._build_controls(left)
        self._build_results(right)

    # ── Left: task input ──────────────────────────────────────────────────────

    def _build_input_panel(self, parent):
        _section_header(parent, "Add Task")

        form = tk.Frame(parent, bg=C["panel"])
        form.pack(fill="x", padx=10, pady=8)

        fields = [("Task Name", 20), ("Study Time (hrs)", 10), ("Value / Priority", 10)]
        self.entries = {}

        for label, width in fields:
            row = tk.Frame(form, bg=C["panel"])
            row.pack(fill="x", pady=3)
            tk.Label(row, text=f"{label}:",
                     font=("Courier New", 8), fg=C["subtext"],
                     bg=C["panel"], width=18, anchor="w").pack(side="left")
            e = _entry(row, width=width)
            e.pack(side="left", fill="x", expand=True)
            self.entries[label] = e

        # Bind Enter key on last field to add task
        self.entries["Value / Priority"].bind("<Return>", lambda e: self._add_task())

        btn_row = tk.Frame(parent, bg=C["panel"])
        btn_row.pack(fill="x", padx=10, pady=(0, 8))
        _button(btn_row, "＋  Add Task", self._add_task, C["accent"]).pack(side="left")
        _button(btn_row, "Clear All", self._clear_all, C["red"]).pack(side="right")

    def _build_task_table(self, parent):
        _section_header(parent, "Task List")

        # Table header
        hdr = tk.Frame(parent, bg=C["header_bg"])
        hdr.pack(fill="x", padx=6, pady=(4, 0))
        for h, w in zip(["Name", "Time", "Value", "Ratio", ""], [24, 8, 8, 10, 4]):
            tk.Label(hdr, text=h, font=("Courier New", 8, "bold"),
                     fg=C["accent2"], bg=C["header_bg"],
                     width=w, anchor="center", pady=3).pack(side="left")

        # Scrollable task list
        list_outer = tk.Frame(parent, bg=C["border"], bd=1, relief="solid")
        list_outer.pack(fill="both", expand=True, padx=6, pady=(0, 4))

        canvas = tk.Canvas(list_outer, bg=C["card"], highlightthickness=0, height=160)
        sb = tk.Scrollbar(list_outer, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        canvas.pack(fill="both", expand=True)

        self._task_inner = tk.Frame(canvas, bg=C["card"])
        self._task_win = canvas.create_window((0, 0), window=self._task_inner, anchor="nw")
        self._task_inner.bind("<Configure>",
                              lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind("<Configure>",
                    lambda e: canvas.itemconfig(self._task_win, width=e.width))
        canvas.bind_all("<MouseWheel>",
                        lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))

        self._task_canvas = canvas

        # Task count badge
        self._task_count_lbl = tk.Label(parent,
                                        text="0 tasks", font=("Courier New", 8),
                                        fg=C["subtext"], bg=C["panel"], anchor="e", padx=8)
        self._task_count_lbl.pack(fill="x")

    def _build_controls(self, parent):
        _section_header(parent, "Run Schedulers")

        ctrl = tk.Frame(parent, bg=C["panel"])
        ctrl.pack(fill="x", padx=10, pady=8)

        # Available time
        time_row = tk.Frame(ctrl, bg=C["panel"])
        time_row.pack(fill="x", pady=(0, 8))
        tk.Label(time_row, text="Available time (hrs):",
                 font=("Courier New", 8), fg=C["subtext"],
                 bg=C["panel"], anchor="w").pack(side="left")
        self.avail_entry = _entry(time_row, width=6)
        self.avail_entry.insert(0, "10")
        self.avail_entry.pack(side="left", padx=(6, 0))

        # Run buttons
        btn_f = tk.Frame(ctrl, bg=C["panel"])
        btn_f.pack(fill="x", pady=2)
        _button(btn_f, "▶  Run Greedy",   self._run_greedy,  C["yellow"]).pack(fill="x", pady=2)
        _button(btn_f, "▶  Run DP Knapsack", self._run_dp,   C["green"]).pack(fill="x", pady=2)
        _button(btn_f, "⚡  Compare Both", self._run_both,   C["accent"]).pack(fill="x", pady=4)

        # Complexity reminder
        info = tk.Frame(parent, bg=C["card"], bd=1, relief="solid")
        info.pack(fill="x", padx=6, pady=(4, 8))
        for line, color in [
            ("Greedy  O(n log n)", C["yellow"]),
            ("  fast, not always optimal", C["subtext"]),
            ("DP      O(n × W)", C["green"]),
            ("  optimal, pseudo-polynomial", C["subtext"]),
        ]:
            tk.Label(info, text=f"  {line}",
                     font=("Courier New", 8), fg=color,
                     bg=C["card"], anchor="w", pady=1).pack(fill="x")

    # ── Right: results ────────────────────────────────────────────────────────

    def _build_results(self, parent):
        # Comparison status bar (hidden until both run)
        self._status_bar = tk.Frame(parent, bg=C["panel"], height=32)
        self._status_bar.pack(fill="x", pady=(0, 6))
        self._status_lbl = tk.Label(self._status_bar, text="",
                                    font=("Courier New", 9, "bold"),
                                    fg=C["accent"], bg=C["panel"], anchor="center")
        self._status_lbl.pack(fill="x", pady=6)

        # Two result panels side by side
        cols = tk.Frame(parent, bg=C["bg"])
        cols.pack(fill="both", expand=True)

        self.greedy_panel = ResultPanel(cols, "Greedy Scheduler", C["yellow"])
        self.dp_panel     = ResultPanel(cols, "DP 0/1 Knapsack",  C["green"])
        self.greedy_panel.pack(side="left", fill="both", expand=True, padx=(0, 5))
        self.dp_panel.pack(side="left", fill="both", expand=True, padx=(5, 0))

    # ──────────────────────────────────────────────────────────────────────────
    # Task Management
    # ──────────────────────────────────────────────────────────────────────────

    def _add_task(self):
        name  = self.entries["Task Name"].get().strip()
        t_str = self.entries["Study Time (hrs)"].get().strip()
        v_str = self.entries["Value / Priority"].get().strip()

        if not name:
            messagebox.showerror("Input Error", "Task name cannot be empty.")
            return
        try:
            t = int(t_str)
            v = int(v_str)
            if t <= 0 or v <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Input Error", "Time and Value must be positive integers.")
            return

        self.tasks.append((name, t, v))
        self._refresh_task_table()

        # Clear entries
        for e in self.entries.values():
            e.delete(0, tk.END)
        self.entries["Task Name"].focus()

    def _delete_task(self, idx):
        if 0 <= idx < len(self.tasks):
            self.tasks.pop(idx)
            self._refresh_task_table()
            self._clear_results()

    def _clear_all(self):
        if self.tasks and not messagebox.askyesno("Clear All", "Remove all tasks?"):
            return
        self.tasks.clear()
        self._refresh_task_table()
        self._clear_results()

    def _refresh_task_table(self):
        for w in self._task_inner.winfo_children():
            w.destroy()

        for i, (name, t, v) in enumerate(self.tasks):
            bg = C["card"] if i % 2 == 0 else C["panel"]
            TaskRow(self._task_inner, i, name, t, v, self._delete_task, bg).pack(fill="x")

        count = len(self.tasks)
        self._task_count_lbl.config(
            text=f"{count} task{'s' if count != 1 else ''}",
            fg=C["accent"] if count else C["subtext"]
        )

    def _clear_results(self):
        self.greedy_panel.clear()
        self.dp_panel.clear()
        self._status_lbl.config(text="")

    # ──────────────────────────────────────────────────────────────────────────
    # Run Algorithms
    # ──────────────────────────────────────────────────────────────────────────

    def _get_available(self):
        try:
            avail = int(self.avail_entry.get())
            if avail <= 0:
                raise ValueError
            return avail
        except ValueError:
            messagebox.showerror("Input Error", "Available time must be a positive integer.")
            return None

    def _run_greedy(self):
        if not self.tasks:
            messagebox.showerror("Error", "Add at least one task first.")
            return
        avail = self._get_available()
        if avail is None:
            return
        chosen, total_time, total_value = greedy_schedule(self.tasks, avail)
        self.greedy_panel.show(chosen, total_time, total_value, avail)
        self._status_lbl.config(text="Greedy complete — run DP to compare  ⚡")

    def _run_dp(self):
        if not self.tasks:
            messagebox.showerror("Error", "Add at least one task first.")
            return
        avail = self._get_available()
        if avail is None:
            return
        chosen, total_time, total_value = knapsack_dp(self.tasks, avail)
        self.dp_panel.show(chosen, total_time, total_value, avail, is_winner=True)
        self._status_lbl.config(text="DP complete — run Greedy to compare  ⚡")

    def _run_both(self):
        if not self.tasks:
            messagebox.showerror("Error", "Add at least one task first.")
            return
        avail = self._get_available()
        if avail is None:
            return

        g_chosen, g_time, g_value = greedy_schedule(self.tasks, avail)
        d_chosen, d_time, d_value = knapsack_dp(self.tasks, avail)

        # DP is always optimal — check if greedy matched it
        greedy_is_optimal = (g_value == d_value)

        self.greedy_panel.show(g_chosen, g_time, g_value, avail,
                               is_winner=greedy_is_optimal)
        self.dp_panel.show(d_chosen, d_time, d_value, avail, is_winner=True)

        # Status bar summary
        if greedy_is_optimal:
            msg = f"✔  Both algorithms agree — optimal value: {d_value}  (Greedy matched DP!)"
            color = C["green"]
        else:
            diff = d_value - g_value
            msg = (f"DP found better solution  |  "
                   f"DP value: {d_value}  vs  Greedy: {g_value}  "
                   f"(DP wins by +{diff})")
            color = C["accent"]

        self._status_lbl.config(text=msg, fg=color)


# ──────────────────────────────────────────────────────────────────────────────
# Standalone preview
# ──────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    root = tk.Tk()
    root.title("TCAA — Study Planner (Preview)")
    root.geometry("1050x680")
    root.configure(bg=C["bg"])

    style = ttk.Style()
    style.theme_use("default")
    style.configure("TNotebook", background=C["bg"], borderwidth=0)
    style.configure("TNotebook.Tab",
                    background=C["panel"], foreground=C["subtext"],
                    font=("Courier New", 10, "bold"), padding=[18, 7])
    style.map("TNotebook.Tab",
              background=[("selected", C["card"])],
              foreground=[("selected", C["accent"])])

    nb = ttk.Notebook(root)
    nb.pack(fill="both", expand=True, padx=6, pady=6)

    tab = build_study_planner_tab(nb)
    nb.add(tab, text="  Study Planner  ")

    root.mainloop()