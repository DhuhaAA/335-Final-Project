import tkinter as tk
from tkinter import ttk

def open_campus_navigator():
    from modules.campus_navigator import launch
    launch()

def open_study_planner():
    from modules.study_planner import launch
    launch()

def open_algorithm_info():
    from modules.algorithm_info import launch
    launch()

def open_string_matching():
    from modules.string_matching import launch
    launch()

root = tk.Tk()
root.title("Titan Campus Algorithmic Assistant")
root.geometry("500x400")

title = tk.Label(root, text="TCAA", font=("Arial", 20))
title.pack(pady=20)

btn1 = ttk.Button(root, text="Campus Navigator", command=open_campus_navigator)
btn1.pack(pady=10)

btn2 = ttk.Button(root, text="Study Planner", command=open_study_planner)
btn2.pack(pady=10)

btn3 = ttk.Button(root, text="Algorithm Info", command=open_algorithm_info)
btn3.pack(pady=10)

btn4 = ttk.Button(root, text="String Matching", command=open_string_matching)
btn4.pack(pady=10)

root.mainloop()