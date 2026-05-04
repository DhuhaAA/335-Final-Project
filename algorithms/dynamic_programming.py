"""
Dynamic Programming and Greedy Algorithms
Greedy Task Scheduling, 0/1 Knapsack
Author: Dhuha Abdulhussein
"""

from typing import List, Dict


# ----------- TASK CLASS -----------

class Task:
    def __init__(self, name, duration, value):
        self.name = name
        self.duration = duration
        self.value = value
    
    def ratio(self):
        # value per unit time for greedy scheduling
        return self.value / self.duration if self.duration > 0 else 0
    
    def __repr__(self):
        return f"Task({self.name}, duration={self.duration}, value={self.value})"


# ----------- GREEDY TASK SCHEDULING -----------
# select tasks based on value-to-time ratio (highest first)
# TIME COMPLEXITY:  O(n log n) due to sorting
# SPACE COMPLEXITY: O(n)

def greedy_scheduler(tasks, available_time):
    
    if not tasks or available_time <= 0:
        return {
            'selected_tasks': [],
            'total_time': 0,
            'total_value': 0,
            'efficiency': 0
        }
    
    # sort by value-to-time ratio in descending order
    sorted_tasks = sorted(tasks, key=lambda t: t.ratio(), reverse=True)
    
    selected = []
    total_time = 0
    total_value = 0
    
    for task in sorted_tasks:
        if total_time + task.duration <= available_time:
            selected.append(task)
            total_time += task.duration
            total_value += task.value
    
    efficiency = total_value / total_time if total_time > 0 else 0
    
    return {
        'selected_tasks': selected,
        'total_time': total_time,
        'total_value': total_value,
        'efficiency': efficiency
    }


# ----------- DYNAMIC PROGRAMMING: 0/1 KNAPSACK -----------
# find maximum value subset of tasks that fits in available_time
# TIME COMPLEXITY:  O(n * available_time)
# SPACE COMPLEXITY: O(n * available_time)

def dp_knapsack_scheduler(tasks, available_time):
    
    if not tasks or available_time <= 0:
        return {
            'selected_tasks': [],
            'total_time': 0,
            'total_value': 0,
            'efficiency': 0
        }
    
    n = len(tasks)
    capacity = int(available_time)
    
    # dp[i][w] = max value using first i tasks with capacity w
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    
    # fill the dp table
    for i in range(1, n + 1):
        task = tasks[i - 1]
        task_time = int(task.duration)
        
        for w in range(capacity + 1):
            # option 1: don't take this task
            dp[i][w] = dp[i - 1][w]
            
            # option 2: take this task (if it fits)
            if task_time <= w:
                dp[i][w] = max(
                    dp[i][w],
                    dp[i - 1][w - task_time] + task.value
                )
    
    # backtrack to find which tasks were selected
    selected = []
    w = capacity
    
    for i in range(n, 0, -1):
        # if value comes from including this task
        if dp[i][w] != dp[i - 1][w]:
            task = tasks[i - 1]
            selected.append(task)
            w -= int(task.duration)
    
    selected.reverse()
    
    total_time = sum(int(t.duration) for t in selected)
    total_value = sum(t.value for t in selected)
    efficiency = total_value / total_time if total_time > 0 else 0
    
    return {
        'selected_tasks': selected,
        'total_time': total_time,
        'total_value': total_value,
        'efficiency': efficiency
    }


# ----------- COMPARE BOTH APPROACHES -----------

def compare_schedulers(tasks, available_time):
    
    greedy_result = greedy_scheduler(tasks, available_time)
    dp_result = dp_knapsack_scheduler(tasks, available_time)
    
    # calculate improvement
    improvement = dp_result['total_value'] - greedy_result['total_value']
    improvement_percent = (improvement / greedy_result['total_value'] * 100) if greedy_result['total_value'] > 0 else 0
    
    return {
        'greedy': greedy_result,
        'dp': dp_result,
        'improvement': improvement,
        'improvement_percent': improvement_percent,
        'greedy_better': greedy_result['total_value'] >= dp_result['total_value']
    }
