import tkinter as tk
from algorithms.dynamic_programming import Task, greedy_scheduler, dp_knapsack_scheduler


def launch():
    window = tk.Toplevel()
    window.title("Study Planner")
    window.geometry("650x550")
    window.configure(bg="#f0f4f7")

    tasks = []

    # --- Inputs ---
    tk.Label(window, text="Task Name", bg="#f0f4f7").pack()
    name_entry = tk.Entry(window)
    name_entry.pack()

    tk.Label(window, text="Duration", bg="#f0f4f7").pack()
    duration_entry = tk.Entry(window)
    duration_entry.pack()

    tk.Label(window, text="Value", bg="#f0f4f7").pack()
    value_entry = tk.Entry(window)
    value_entry.pack()

    tk.Label(window, text="Available Time", bg="#f0f4f7").pack()
    time_entry = tk.Entry(window)
    time_entry.pack()

    # --- Output ---
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

    # --- Add Task ---
    def add_task():
        try:
            task = Task(
                name_entry.get(),
                float(duration_entry.get()),
                float(value_entry.get())
            )
            tasks.append(task)

            display(
                f"Added Task:\n"
                f"- {task.name} (time {task.duration}, value {task.value})"
            )

        except:
            display("❌ Invalid input. Enter numbers for duration and value.")

    # --- Greedy ---
    def run_greedy():
        try:
            result = greedy_scheduler(tasks, float(time_entry.get()))

            task_list = "\n".join(
                [f"- {t.name} (time {t.duration}, value {t.value})"
                 for t in result['selected_tasks']]
            )

            display(
                f"=== Greedy Result ===\n\n"
                f"Selected Tasks:\n{task_list}\n\n"
                f"Total Time: {result['total_time']}\n"
                f"Total Value: {result['total_value']}\n"
                f"Efficiency: {result['efficiency']:.2f}"
            )

        except:
            display("❌ Error running greedy")

    # --- DP ---
    def run_dp():
        try:
            result = dp_knapsack_scheduler(tasks, float(time_entry.get()))

            task_list = "\n".join(
                [f"- {t.name} (time {t.duration}, value {t.value})"
                 for t in result['selected_tasks']]
            )

            display(
                f"=== DP Optimal Result ===\n\n"
                f"Selected Tasks:\n{task_list}\n\n"
                f"Total Time: {result['total_time']}\n"
                f"Total Value: {result['total_value']}\n"
                f"Efficiency: {result['efficiency']:.2f}"
            )

        except:
            display("❌ Error running DP")

    # --- Buttons ---
    btn_frame = tk.Frame(window, bg="#f0f4f7")
    btn_frame.pack(pady=15)

    tk.Button(btn_frame, text="Add Task", command=add_task,
              bg="#2ecc71", fg="white", width=14).grid(row=0, column=0, padx=6)

    tk.Button(btn_frame, text="Run Greedy", command=run_greedy,
              bg="#3498db", fg="white", width=14).grid(row=0, column=1, padx=6)

    tk.Button(btn_frame, text="Run DP", command=run_dp,
              bg="#9b59b6", fg="white", width=14).grid(row=0, column=2, padx=6)