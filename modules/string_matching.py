"""
TCAA - Notes Search Engine Module
Naive · Rabin-Karp · KMP · Compare All
Supports: TXT inline, PDF and DOCX via file upload
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sys, os, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from algorithms.string_algorithms import naive_search, rabin_karp, kmp

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
                     font=("Courier New", 9, "bold"), fg="#FFFFFF",
                     bg=color or C["accent"],
                     activebackground=C["accent2"], activeforeground="#FFFFFF",
                     relief="flat", bd=0, padx=10, pady=4, cursor="hand2")

def _sec(parent, title):
    f = tk.Frame(parent, bg=C["header_bg"])
    f.pack(fill="x", pady=(10, 0))
    tk.Label(f, text=f"  {title}", font=("Courier New", 10, "bold"),
             fg="#FFFFFF", bg=C["header_bg"], anchor="w", pady=4).pack(fill="x")


def load_text_from_file(filepath):
    """Load text from TXT, PDF, or DOCX file."""
    ext = os.path.splitext(filepath)[1].lower()
    try:
        if ext == ".txt":
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                return f.read()
        elif ext == ".pdf":
            try:
                import PyPDF2
                text = ""
                with open(filepath, "rb") as f:
                    reader = PyPDF2.PdfReader(f)
                    for page in reader.pages:
                        text += page.extract_text() or ""
                return text
            except ImportError:
                return None, "PyPDF2 not installed. Run: pip install PyPDF2"
        elif ext in (".docx", ".doc"):
            try:
                import docx
                doc = docx.Document(filepath)
                return "\n".join(p.text for p in doc.paragraphs)
            except ImportError:
                return None, "python-docx not installed. Run: pip install python-docx"
        else:
            return None, f"Unsupported file type: {ext}"
    except Exception as e:
        return None, str(e)


def build_string_matching_tab(notebook):
    tab = tk.Frame(notebook, bg=C["bg"])
    loaded_text = [None]   # mutable container

    # Header
    hdr = tk.Frame(tab, bg=C["header_bg"], pady=11)
    hdr.pack(fill="x")
    tk.Label(hdr, text="Notes Search Engine",
             font=("Courier New", 17, "bold"), fg="#FFFFFF", bg=C["header_bg"]).pack()
    tk.Label(hdr, text="Naive  ·  Rabin-Karp  ·  KMP  ·  Compare All",
             font=("Courier New", 10), fg=C["border"], bg=C["header_bg"]).pack()

    body = tk.Frame(tab, bg=C["bg"])
    body.pack(fill="both", expand=True, padx=12, pady=10)

    # ── Left panel ────────────────────────────────────────────────────────────
    left = tk.Frame(body, bg=C["panel"], width=280)
    left.pack(side="left", fill="y", padx=(0, 10))
    left.pack_propagate(False)

    _sec(left, "Load Document")

    file_lbl = tk.Label(left, text="No file loaded", font=("Courier New", 8),
                        fg=C["subtext"], bg=C["panel"], anchor="w",
                        padx=10, wraplength=250)
    file_lbl.pack(fill="x", pady=(4, 2))

    def upload_file():
        path = filedialog.askopenfilename(
            title="Select a document",
            filetypes=[("Supported files", "*.txt *.pdf *.docx"),
                       ("Text", "*.txt"), ("PDF", "*.pdf"), ("Word", "*.docx")]
        )
        if not path: return
        result = load_text_from_file(path)
        if isinstance(result, tuple):
            messagebox.showerror("Load Error", result[1])
            return
        loaded_text[0] = result
        fname = os.path.basename(path)
        chars = len(result)
        file_lbl.config(text=f"✔  {fname}\n{chars:,} characters loaded",
                        fg=C["green"])
        # Show preview in text area
        preview_txt.config(state="normal")
        preview_txt.delete("1.0", tk.END)
        preview_txt.insert(tk.END, result[:2000] + ("…" if len(result) > 2000 else ""))
        preview_txt.config(state="disabled")

    _btn(left, "📂  Upload File (PDF / DOCX / TXT)", upload_file, C["accent"]).pack(
        fill="x", padx=10, pady=(2, 6))

    _sec(left, "Or Type / Paste Text")
    paste_lbl = tk.Label(left, text="Type text directly below:",
                         font=("Courier New", 8), fg=C["subtext"],
                         bg=C["panel"], anchor="w", padx=10)
    paste_lbl.pack(fill="x", pady=(4, 2))
    paste_frame = tk.Frame(left, bg=C["border"], bd=1, relief="solid")
    paste_frame.pack(fill="x", padx=10, pady=(0, 4))
    paste_txt = tk.Text(paste_frame, font=("Courier New", 9), fg=C["text"],
                        bg=C["card"], relief="flat", bd=0, height=5,
                        padx=6, pady=4, wrap="word")
    paste_txt.pack(fill="x")
    paste_txt.insert(tk.END, "Enter or paste your text here...")
    paste_txt.bind("<FocusIn>", lambda e: paste_txt.delete("1.0", tk.END)
                   if paste_txt.get("1.0", tk.END).strip() == "Enter or paste your text here..."
                   else None)

    def use_pasted():
        txt = paste_txt.get("1.0", tk.END).strip()
        if not txt or txt == "Enter or paste your text here...":
            messagebox.showerror("Error", "Please paste some text first.")
            return
        loaded_text[0] = txt
        file_lbl.config(text=f"✔  Pasted text  ({len(txt):,} chars)", fg=C["green"])
        preview_txt.config(state="normal")
        preview_txt.delete("1.0", tk.END)
        preview_txt.insert(tk.END, txt[:2000])
        preview_txt.config(state="disabled")

    _btn(left, "Use Pasted Text", use_pasted, C["brown"]).pack(fill="x", padx=10, pady=(0, 6))

    _sec(left, "Search Pattern")
    pat_frame = tk.Frame(left, bg=C["panel"])
    pat_frame.pack(fill="x", padx=10, pady=8)
    tk.Label(pat_frame, text="Pattern:", font=("Courier New", 8),
             fg=C["subtext"], bg=C["panel"], anchor="w").pack(fill="x")
    pat_entry = tk.Entry(pat_frame, font=("Courier New", 10), fg=C["text"],
                         bg=C["card"], insertbackground=C["accent"],
                         relief="flat", bd=4)
    pat_entry.pack(fill="x", pady=(2, 6))

    # Algorithm selection
    algo_var = tk.StringVar(value="ALL")
    algo_frame = tk.Frame(left, bg=C["panel"])
    algo_frame.pack(fill="x", padx=10, pady=(0, 8))
    tk.Label(algo_frame, text="Algorithm:", font=("Courier New", 8),
             fg=C["subtext"], bg=C["panel"], anchor="w").pack(fill="x")
    for val, lbl in [("Naive","Naive  O(n·m)"), ("Rabin-Karp","Rabin-Karp  O(n+m)"),
                     ("KMP","KMP  O(n+m)"), ("ALL","Compare All")]:
        tk.Radiobutton(algo_frame, text=lbl, variable=algo_var, value=val,
                       font=("Courier New", 9), fg=C["text"], bg=C["panel"],
                       selectcolor=C["accent"], activebackground=C["panel"],
                       anchor="w").pack(fill="x")

    # ── Right panel ───────────────────────────────────────────────────────────
    right = tk.Frame(body, bg=C["bg"])
    right.pack(side="left", fill="both", expand=True)

    # Text preview
    prev_frame = tk.Frame(right, bg=C["card"], bd=1, relief="solid",
                          highlightbackground=C["border"])
    prev_frame.pack(fill="x", pady=(0, 6))
    tk.Label(prev_frame, text="  Document Preview",
             font=("Courier New", 9, "bold"), fg=C["subtext"],
             bg=C["panel"], anchor="w", pady=3).pack(fill="x")
    prev_sb = tk.Scrollbar(prev_frame, orient="vertical")
    prev_sb.pack(side="right", fill="y")
    preview_txt = tk.Text(prev_frame, font=("Courier New", 9), fg=C["text"],
                          bg=C["card"], relief="flat", bd=0, height=7,
                          padx=10, pady=6, wrap="word", state="disabled",
                          cursor="arrow", yscrollcommand=prev_sb.set)
    preview_txt.pack(fill="x")
    prev_sb.config(command=preview_txt.yview)

    # Results
    res_frame = tk.Frame(right, bg=C["card"], bd=1, relief="solid",
                         highlightbackground=C["border"])
    res_frame.pack(fill="both", expand=True)
    tk.Label(res_frame, text="  Search Results",
             font=("Courier New", 9, "bold"), fg=C["subtext"],
             bg=C["panel"], anchor="w", pady=3).pack(fill="x")
    res_sb = tk.Scrollbar(res_frame)
    res_sb.pack(side="right", fill="y")
    result_txt = tk.Text(res_frame, font=("Courier New", 10), fg=C["text"],
                         bg=C["card"], relief="flat", bd=0, padx=12, pady=8,
                         wrap="word", state="disabled", cursor="arrow",
                         yscrollcommand=res_sb.set)
    result_txt.pack(fill="both", expand=True)
    res_sb.config(command=result_txt.yview)

    result_txt.tag_configure("heading",  font=("Courier New", 10, "bold"), foreground=C["accent"])
    result_txt.tag_configure("match",    foreground=C["green"], font=("Courier New", 10, "bold"))
    result_txt.tag_configure("time_tag", foreground=C["brown"])
    result_txt.tag_configure("muted",    foreground=C["subtext"])
    result_txt.tag_configure("sep",      foreground=C["border"])
    result_txt.tag_configure("error",    foreground=C["red"])

    def display_results(lines):
        result_txt.config(state="normal")
        result_txt.delete("1.0", tk.END)
        for text, tag in lines:
            result_txt.insert(tk.END, text, tag)
        result_txt.config(state="disabled")

    def run_search():
        text = loaded_text[0]
        if not text:
            display_results([("❌ Load or paste a document first.\n", "error")])
            return
        pattern = pat_entry.get().strip()
        if not pattern:
            display_results([("❌ Enter a search pattern.\n", "error")])
            return

        algo = algo_var.get()
        lines = []

        def run_algo(name, fn, color_tag):
            t0 = time.perf_counter()
            matches = fn(text, pattern)
            elapsed = (time.perf_counter() - t0) * 1000
            lines.append((f"\n{name}\n", "heading"))
            lines.append(("─" * 40 + "\n", "sep"))
            lines.append((f"  Matches found : ", "muted"))
            lines.append((f"{len(matches)}\n", "match"))
            lines.append((f"  Time taken    : ", "muted"))
            lines.append((f"{elapsed:.4f} ms\n", "time_tag"))
            if matches:
                snippet_indices = matches[:5]
                lines.append((f"  First match at index {matches[0]}:\n", "muted"))
                for idx in snippet_indices:
                    start = max(0, idx - 20)
                    end   = min(len(text), idx + len(pattern) + 20)
                    ctx = text[start:end].replace("\n", " ")
                    lines.append((f"    …{ctx}…\n", "muted"))
                if len(matches) > 5:
                    lines.append((f"  + {len(matches)-5} more matches\n", "muted"))
            return matches, elapsed

        if algo == "ALL":
            lines.append(("=== Compare All Algorithms ===\n", "heading"))
            lines.append((f"Pattern: \"{pattern}\"   |   Text length: {len(text):,} chars\n", "muted"))
            nm, nt = run_algo("Naive Search   O(n·m)", naive_search, "muted")
            rm, rt = run_algo("Rabin-Karp   O(n+m) avg", rabin_karp, "muted")
            km, kt = run_algo("KMP   O(n+m)", kmp, "muted")
            lines.append(("\n─" * 40 + "\n", "sep"))
            agree = (nm == rm == km)
            lines.append(("\n  All algorithms agree: ", "muted"))
            lines.append((f"{'✔ YES' if agree else '✘ NO'}\n", "match" if agree else "error"))
            fastest = min([("Naive", nt), ("Rabin-Karp", rt), ("KMP", kt)], key=lambda x: x[1])
            lines.append((f"  Fastest this run    : {fastest[0]}  ({fastest[1]:.4f} ms)\n", "time_tag"))
        else:
            fn = {"Naive": naive_search, "Rabin-Karp": rabin_karp, "KMP": kmp}[algo]
            lines.append((f"=== {algo} Search ===\n", "heading"))
            lines.append((f"Pattern: \"{pattern}\"   |   Text length: {len(text):,} chars\n", "muted"))
            run_algo(algo, fn, "muted")

        display_results(lines)

    pat_entry.bind("<Return>", lambda e: run_search())
    _btn(left, "🔍  Search", run_search, C["accent"]).pack(fill="x", padx=10, pady=(4, 12))

    return tab


def launch():
    import tkinter as tk
    from tkinter import ttk
    root = tk.Toplevel()
    nb = ttk.Notebook(root)
    nb.pack(fill="both", expand=True)
    nb.add(build_string_matching_tab(nb), text="Notes Search")
    root.mainloop()
