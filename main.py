"""
TCAA - Titan Campus Algorithmic Assistant
CPSC 335 Final Project
Main entry point — tabbed notebook layout
"""

import tkinter as tk
from tkinter import ttk

# ── Palette ───────────────────────────────────────────────────────────────────
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
}


def main():
    root = tk.Tk()
    root.title("Titan Campus Algorithmic Assistant (TCAA)")
    root.geometry("1100x700")
    root.minsize(900, 600)
    root.configure(bg=C["bg"])

    # ── App header ────────────────────────────────────────────────────────────
    hdr = tk.Frame(root, bg=C["header_bg"], pady=10)
    hdr.pack(fill="x")
    tk.Label(hdr, text="Titan Campus Algorithmic Assistant",
             font=("Courier New", 20, "bold"),
             fg="#FFFFFF", bg=C["header_bg"]).pack()
    tk.Label(hdr, text="CPSC 335  ·  Algorithm Engineering  ·  Dr. Shah",
             font=("Courier New", 10),
             fg=C["border"], bg=C["header_bg"]).pack()

    # ── Notebook style ────────────────────────────────────────────────────────
    style = ttk.Style()
    style.theme_use("default")
    style.configure("TNotebook", background=C["bg"], borderwidth=0, tabmargins=[4, 4, 0, 0])
    style.configure("TNotebook.Tab",
                    background=C["panel"],
                    foreground=C["subtext"],
                    font=("Courier New", 10, "bold"),
                    padding=[18, 7],
                    borderwidth=0)
    style.map("TNotebook.Tab",
              background=[("selected", C["card"])],
              foreground=[("selected", C["accent2"])])

    nb = ttk.Notebook(root)
    nb.pack(fill="both", expand=True, padx=8, pady=8)

    # ── Load tabs ─────────────────────────────────────────────────────────────
    from modules.campus_navigator import build_campus_navigator_tab
    from modules.study_planner    import build_study_planner_tab
    from modules.string_matching  import build_string_matching_tab
    from modules.algorithm_info   import build_algorithm_info_tab

    nb.add(build_campus_navigator_tab(nb), text="  🗺  Campus Navigator  ")
    nb.add(build_study_planner_tab(nb),    text="  📚  Study Planner  ")
    nb.add(build_string_matching_tab(nb),  text="  🔍  Notes Search  ")
    nb.add(build_algorithm_info_tab(nb),   text="  ℹ  Algorithm Info  ")

    root.mainloop()


if __name__ == "__main__":
    main()
