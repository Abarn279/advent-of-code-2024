import os
import operator

with open(f"./inp/{os.path.basename(__file__).split('.')[0]}.txt") as f:
    lines = [list(map(int, i.split())) for i in f.read().split('\n')]
    
def is_safe(line):
    differences = [line[i-1] - line[i] for i in range(1, len(line))]
    
    if (all(i > 0 for i in differences) or all(i < 0 for i in differences)) and all(abs(i) in [1, 2, 3] for i in differences):
        return True
    return False

# Part A 
safe = 0
for line in lines: 
    if is_safe(line): safe += 1
   
print(safe)

# Part B 
def array_without_elements(arr):
    return [arr[:i] + arr[i+1:] for i in range(len(arr))]

safe = 0
for line in lines: 
    arys = array_without_elements(line)
    if any(is_safe(a) for a in arys):
        safe += 1
        
print(safe)