import pandas as pd
import sympy as sp

# Greedy Algorithm
def is_yellow(x, A, B):
    if 2*x in A or any(x + item in A for item in A):
        return False
    if 2*x in B or any(x + item in B for item in A):
        return True
    return False

A = set()
B = set()

for value in range(999, 110, -1):
    if is_yellow(value, A, B):
        A.add(value)
    else:
        B.add(value)

print(f"answer = {len(A)}")