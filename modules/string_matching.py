import tkinter as tk
from algorithms.string_algorithms import naive_search, rabin_karp, kmp


def launch():
    window = tk.Toplevel()
    window.title("String Matching")
    window.geometry("650x550")
    window.configure(bg="#f0f4f7")

    # --- Title ---
    title = tk.Label(
        window,
        text="String Matching Visualizer",
        font=("Arial", 18, "bold"),
        bg="#f0f4f7"
    )
    title.pack(pady=10)

    # --- Input Frame ---
    input_frame = tk.Frame(window, bg="#f0f4f7")
    input_frame.pack(pady=10)

    # Text input
    tk.Label(input_frame, text="Text:", bg="#f0f4f7").grid(row=0, column=0, padx=10, pady=5)
    text_entry = tk.Entry(input_frame, width=50)
    text_entry.grid(row=0, column=1)

    # Pattern input
    tk.Label(input_frame, text="Pattern:", bg="#f0f4f7").grid(row=1, column=0, padx=10, pady=5)
    pattern_entry = tk.Entry(input_frame, width=50)
    pattern_entry.grid(row=1, column=1)

    # --- Output Box ---
    output = tk.Text(
        window,
        height=15,
        width=75,
        bg="#1e1e1e",
        fg="#00ffcc",
        insertbackground="white",
        font=("Consolas", 10)
    )
    output.pack(pady=10)

    def display(text):
        output.delete("1.0", tk.END)
        output.insert(tk.END, text)

    # --- Highlight Matches ---
    def highlight_matches(text, pattern, indices):
        result = ""
        last = 0

        for i in indices:
            result += text[last:i]
            result += "[" + text[i:i+len(pattern)] + "]"
            last = i + len(pattern)

        result += text[last:]
        return result

    # --- Run Search ---
    def run_search():
        text = text_entry.get()
        pattern = pattern_entry.get()

        if not text or not pattern:
            display("❌ Please enter both text and pattern.")
            return

        naive = naive_search(text, pattern)
        rk = rabin_karp(text, pattern)
        kmp_result = kmp(text, pattern)

        highlighted = highlight_matches(text, pattern, naive)

        display(
            f"=== String Matching Results ===\n\n"
            f"Text:\n{highlighted}\n\n"
            f"Pattern: \"{pattern}\"\n\n"
            f"Naive Matches: {naive}\n"
            f"Rabin-Karp Matches: {rk}\n"
            f"KMP Matches: {kmp_result}\n\n"
            f"All Algorithms Agree: {naive == rk == kmp_result}"
        )

    # --- Button ---
    tk.Button(
        window,
        text="Run Search",
        command=run_search,
        bg="#3498db",
        fg="white",
        width=15
    ).pack(pady=10)