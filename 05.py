import os
from collections import defaultdict
from functools import cmp_to_key

with open(f"./inp/{os.path.basename(__file__).split('.')[0]}.txt") as f:
    rules, to_produce = f.read().split('\n\n')
    rules = rules.split('\n')
    to_produce = to_produce.split('\n')
    
# set up rules dictionary
afters_dict = defaultdict(lambda: set())
for r in rules:
    i, j = r.split('|')
    afters_dict[int(i)].add(int(j))
    
failed = []    

# Part A
sm = 0
for production in to_produce:
    production = list(map(int, production.split(',')))
    fail = False
    
    # iterate through by index
    for my_index in range(len(production)):
        
        # step backwards, check if any of these show up in the list of 'afters'
        for check_index in range(my_index - 1, -1, -1):
            if production[check_index] in afters_dict[production[my_index]]:
                fail = True
                break
        
    # if it didn't fail, add up the middle element
    if not fail: 
        sm += production[len(production) // 2]
        
    else:
        failed.append(production)
        
print(sm)

# Part B
def comparator(x, y):
    if y in afters_dict[x]:
        return -1
    if x in afters_dict[y]:
        return 1
    return 0

sm = 0
for production in failed:
    production = list(sorted(production, key=cmp_to_key(comparator)))
    sm += production[len(production) // 2 ]
print(sm)