# String Matching Algorithms
# Naive, Rabin-Karp, KMP
# Author: Dhuha Abdulhussein

import time


# ----------- NAIVE STRING MATCHING -----------
# brute force - check pattern at every position
# TIME COMPLEXITY:  O((n - m + 1) * m) = O(n*m) worst case
# SPACE COMPLEXITY: O(1)

def naive_search(text, pattern):
    
    matches = []
    n = len(text)
    m = len(pattern)
    
    if m == 0 or m > n:
        return matches
    
    # check pattern at each position
    for i in range(n - m + 1):
        match = True
        for j in range(m):
            if text[i + j] != pattern[j]:
                match = False
                break
        
        if match:
            matches.append(i)
    
    return matches


# ----------- RABIN-KARP ALGORITHM -----------
# rolling hash - compute hash of pattern and text windows
# TIME COMPLEXITY:  O(n + m) average, O(n*m) worst case
# SPACE COMPLEXITY: O(1)

def rabin_karp(text, pattern, prime=101):
    
    matches = []
    n = len(text)
    m = len(pattern)
    
    if m == 0 or m > n:
        return matches
    
    # base for hashing (number of chars in alphabet)
    base = 256
    
    # precompute hash values
    pattern_hash = 0
    window_hash = 0
    
    # compute base^(m-1) % prime
    power = 1
    for _ in range(m - 1):
        power = (power * base) % prime
    
    # calculate hash of pattern and first window
    for i in range(m):
        pattern_hash = (base * pattern_hash + ord(pattern[i])) % prime
        window_hash = (base * window_hash + ord(text[i])) % prime
    
    # roll the hash window through text
    for i in range(n - m + 1):
        # check if hashes match
        if pattern_hash == window_hash:
            # verify actual match (to handle hash collisions)
            if text[i:i + m] == pattern:
                matches.append(i)
        
        # calculate hash for next window
        if i < n - m:
            # remove first char, add last char
            window_hash = (base * (window_hash - ord(text[i]) * power) + ord(text[i + m])) % prime
            
            # handle negative hash
            if window_hash < 0:
                window_hash += prime
    
    return matches


# ----------- KMP ALGORITHM -----------
# Knuth-Morris-Pratt - use failure function to avoid backtracking
# TIME COMPLEXITY:  O(n + m)
# SPACE COMPLEXITY: O(m)

def kmp(text, pattern):
    
    matches = []
    n = len(text)
    m = len(pattern)
    
    if m == 0 or m > n:
        return matches
    
    # build failure function (lps array - longest proper prefix which is also suffix)
    failure = [0] * m
    j = 0
    
    for i in range(1, m):
        while j > 0 and pattern[i] != pattern[j]:
            j = failure[j - 1]
        
        if pattern[i] == pattern[j]:
            j += 1
        
        failure[i] = j
    
    # search for pattern in text
    j = 0
    for i in range(n):
        while j > 0 and text[i] != pattern[j]:
            j = failure[j - 1]
        
        if text[i] == pattern[j]:
            j += 1
        
        if j == m:
            matches.append(i - m + 1)
            j = failure[j - 1]
    
    return matches


# ----------- COMPARE ALL ALGORITHMS -----------

def search_all(text, pattern):
    
    naive_matches = naive_search(text, pattern)
    rk_matches = rabin_karp(text, pattern)
    kmp_matches = kmp(text, pattern)
    
    return {
        'naive': naive_matches,
        'rabin_karp': rk_matches,
        'kmp': kmp_matches,
        'all_match': naive_matches == rk_matches == kmp_matches,
        'match_count': len(naive_matches)
    }
