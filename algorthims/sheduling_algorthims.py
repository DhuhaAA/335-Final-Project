# Greedy Task Sechduler & 0/1 KNAPSCAK (DP)
# author: Dhuha Abddulhussein 


#-------- Greedy sechduler ------
# sechdule tasks by greedily by value-per-time ratio 

def greedy_sechduler(tasks, available_time):
    
   sorted_tasks = sorted(tasks, key=lambda t: t["value"] / t["time"], reverse=True)
   
   chosen_tasks = []
   total_time = 0
   total_value = 0
   
   for task in sorted_tasks:
       
       if total_time + task["time"] <= available_time:
           chosen_tasks.append(task)
           total_time += task["time"]
           total_value += task["value"]
           
   return chosen_tasks, total_time, total_value



# --------- 0/1 Knapsack ------------
# solve 0/ 1 optimally using DP 

def knapsack_dp(tasks, available_time):
    
    n = len(tasks)
    W = available_time
    
    dp = [[0] * (W +1) for _ in range(n +1)]
    
    for i in range(1, n + 1):
        task = tasks[i - 1] 
        t = tasks["time"]
        v = tasks["value"]
        
        for w in range(W + 1):
            dp[i][w] = dp[i-1][w]
            
            if t <= w:
                value_if_taken = v + dp[i-1][w-t]
                
                if value_if_taken > dp[i][w]:
                    dp[i][w] = value_if_taken
                    
    
    chosen_tasks = []
    w = W
    for i in range(n , 0, -1):
        if dp[i][w] != dp[i-1][w]:
            chosen_tasks.append(tasks[i-1])
            w -= tasks[i -1]["time"]
            
    chosen_tasks.reverse()
    
    total_time = sum(t["time"] for t in chosen_tasks)
    total_value = dp[n][W]
    
    return chosen_tasks, total_time, total_value
    