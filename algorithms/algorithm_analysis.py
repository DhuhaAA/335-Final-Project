# Algorithm Analysis and Complexity Information
# Author: Dhuha Abdulhussein


# ----------- ALGORITHM COMPLEXITIES DATABASE -----------

ALGORITHM_COMPLEXITIES = {
    'BFS': {
        'name': 'Breadth-First Search',
        'time': 'O(V + E)',
        'space': 'O(V)',
        'description': 'Explores graph level by level using a queue. Best for unweighted shortest paths.',
        'use_cases': ['Shortest path in unweighted graphs', 'Level-order traversal', 'Connected components'],
        'best_case': 'O(V + E)',
        'worst_case': 'O(V + E)',
        'average_case': 'O(V + E)'
    },
    'DFS': {
        'name': 'Depth-First Search',
        'time': 'O(V + E)',
        'space': 'O(V)',
        'description': 'Explores graph by going as deep as possible. Uses recursion or explicit stack.',
        'use_cases': ['Topological sorting', 'Cycle detection', 'Connected components'],
        'best_case': 'O(V + E)',
        'worst_case': 'O(V + E)',
        'average_case': 'O(V + E)'
    },
    'Dijkstra': {
        'name': "Dijkstra's Shortest Path",
        'time': 'O((V + E) log V)',
        'space': 'O(V)',
        'description': 'Finds shortest path in weighted graphs using min-heap. No negative weights allowed.',
        'use_cases': ['GPS navigation', 'Network routing', 'Shortest paths with positive weights'],
        'best_case': 'O((V + E) log V)',
        'worst_case': 'O((V + E) log V)',
        'average_case': 'O((V + E) log V)'
    },
    'Prim MST': {
        'name': "Prim's Minimum Spanning Tree",
        'time': 'O((V + E) log V)',
        'space': 'O(V + E)',
        'description': 'Finds minimum spanning tree using greedy approach with min-heap.',
        'use_cases': ['Network design', 'Minimum cost connections', 'Clustering'],
        'best_case': 'O((V + E) log V)',
        'worst_case': 'O((V + E) log V)',
        'average_case': 'O((V + E) log V)'
    },
    'Naive Search': {
        'name': 'Naive String Matching',
        'time': 'O((n - m + 1) * m)',
        'space': 'O(1)',
        'description': 'Brute force - check pattern at every position in text.',
        'use_cases': ['Small texts', 'Small patterns', 'Learning purposes'],
        'best_case': 'O(n)',
        'worst_case': 'O(n * m)',
        'average_case': 'O(n * m)'
    },
    'Rabin-Karp': {
        'name': 'Rabin-Karp Algorithm',
        'time': 'O(n + m) average, O(n * m) worst',
        'space': 'O(1)',
        'description': 'Uses rolling hash for pattern matching. Good average performance.',
        'use_cases': ['Multiple pattern matching', 'Plagiarism detection', 'DNA matching'],
        'best_case': 'O(n + m)',
        'worst_case': 'O(n * m)',
        'average_case': 'O(n + m)'
    },
    'KMP': {
        'name': 'Knuth-Morris-Pratt Algorithm',
        'time': 'O(n + m)',
        'space': 'O(m)',
        'description': 'Preprocesses pattern to avoid unnecessary comparisons. Linear time guaranteed.',
        'use_cases': ['Large texts', 'Real-time pattern matching', 'File searching'],
        'best_case': 'O(n + m)',
        'worst_case': 'O(n + m)',
        'average_case': 'O(n + m)'
    },
    'Greedy Scheduler': {
        'name': 'Greedy Task Scheduling',
        'time': 'O(n log n)',
        'space': 'O(n)',
        'description': 'Selects tasks by highest value-to-time ratio. Fast but not always optimal.',
        'use_cases': ['Task scheduling', 'Resource allocation', 'Quick approximations'],
        'best_case': 'O(n log n)',
        'worst_case': 'O(n log n)',
        'average_case': 'O(n log n)'
    },
    '0/1 Knapsack (DP)': {
        'name': '0/1 Knapsack Dynamic Programming',
        'time': 'O(n * W)',
        'space': 'O(n * W)',
        'description': 'Optimal solution using dynamic programming. Cannot select partial items.',
        'use_cases': ['Optimal resource allocation', 'Portfolio optimization', 'Study planning'],
        'best_case': 'O(n * W)',
        'worst_case': 'O(n * W)',
        'average_case': 'O(n * W)'
    }
}


# ----------- HELPER FUNCTIONS -----------

def get_algorithm_info(algorithm_name):
    """Get detailed info about an algorithm"""
    return ALGORITHM_COMPLEXITIES.get(algorithm_name, {})


def get_all_algorithms():
    """Get all algorithm complexities"""
    return ALGORITHM_COMPLEXITIES


def get_complexity_chart():
    """Generate complexity comparison chart"""
    chart = "ALGORITHM COMPLEXITY COMPARISON\n"
    chart += "=" * 80 + "\n"
    chart += f"{'Algorithm':<20} {'Time Complexity':<20} {'Space Complexity':<20}\n"
    chart += "-" * 80 + "\n"
    
    for algo_name, details in ALGORITHM_COMPLEXITIES.items():
        chart += f"{algo_name:<20} {details['time']:<20} {details['space']:<20}\n"
    
    return chart


# ----------- P VS NP ANALYSIS -----------

def get_p_vs_np_explanation():
    """Get P vs NP explanation"""
    return {
        'P_definition': 'Problems solvable in polynomial time by deterministic algorithms',
        'P_characteristics': [
            'Decision problems with YES/NO answers',
            'Solution can be found in polynomial time',
            'Examples: Sorting, searching, shortest path'
        ],
        'NP_definition': 'Problems verifiable in polynomial time by non-deterministic algorithms',
        'NP_characteristics': [
            'Decision problems with YES/NO answers',
            'Solution can be verified in polynomial time (if one exists)',
            'Examples: Traveling Salesman Problem, Knapsack, Satisfiability'
        ],
        'P_subset_NP': 'All P problems are NP (every solvable problem is verifiable)',
        'P_equals_NP': 'Open question: Does P = NP? (Million dollar question)',
        'NP_Complete': 'Hardest problems in NP; if one is solved, all NP problems can be solved',
        'examples': {
            'P_problems': [
                'Sorting: O(n log n)',
                'Binary search: O(log n)',
                'Dijkstra shortest path: O((V + E) log V)'
            ],
            'NP_problems': [
                'Traveling Salesman Problem (TSP)',
                'Subset Sum',
                '0/1 Knapsack (as decision problem)',
                'Boolean Satisfiability (SAT)'
            ]
        }
    }


def get_knapsack_p_vs_np():
    """Explain knapsack in P vs NP context"""
    return {
        'optimization_version': {
            'classification': 'NP-Hard (optimization problem)',
            'complexity': 'O(n * W) with dynamic programming',
            'note': 'DP solution is pseudo-polynomial (depends on input value W)'
        },
        'decision_version': {
            'classification': 'NP-Complete',
            'question': 'Can we achieve value >= V with weight <= W?',
            'verification': 'If YES solution exists, can verify in polynomial time'
        },
        'practical_note': 'While theoretically hard, DP provides practical solution for reasonable sizes'
    }


def complexity_classes_summary():
    """Get complexity classes explanation"""
    summary = "COMPLEXITY CLASSES SUMMARY\n"
    summary += "=" * 80 + "\n\n"
    
    summary += "CLASS P (Polynomial Time)\n"
    summary += "-" * 80 + "\n"
    summary += "• Solvable in polynomial time\n"
    summary += "• Deterministic polynomial-time algorithms\n"
    summary += "• Examples: Sorting, Searching, Shortest Path\n\n"
    
    summary += "CLASS NP (Non-deterministic Polynomial Time)\n"
    summary += "-" * 80 + "\n"
    summary += "• Verifiable in polynomial time\n"
    summary += "• Non-deterministic polynomial-time algorithms\n"
    summary += "• Examples: TSP, Knapsack, SAT\n\n"
    
    summary += "NP-COMPLETE\n"
    summary += "-" * 80 + "\n"
    summary += "• Hardest problems in NP\n"
    summary += "• If one NP-Complete problem is solved in P-time, all NP problems are solvable\n"
    summary += "• Examples: TSP (decision), SAT, Knapsack (decision)\n\n"
    
    summary += "NP-HARD\n"
    summary += "-" * 80 + "\n"
    summary += "• At least as hard as NP-Complete problems\n"
    summary += "• May not be in NP themselves\n"
    summary += "• Examples: Knapsack (optimization), TSP (optimization)\n"
    
    return summary
