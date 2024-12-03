import os
import re
import operator

with open(f"./inp/{os.path.basename(__file__).split('.')[0]}.txt") as f:
    inp = f.read()
    
def get_sum(inp):
    '''Get sum of all muls within a sequence'''
    match = re.findall(r'(mul\(\d+,\d+\))', inp)

    sm = 0
    for mul in match:
        match = re.match(r'mul\((\d+),(\d+)\)', mul).groups()
        sm += int(match[0]) * int(match[1])
    return sm
    
# Part A
print(get_sum(inp))

# Part B - remove all substrings that have don't() to do(), rerun
while True:
    dont_ind = inp.find("don't()")
    do_ind = inp.find("do()", dont_ind + len("don't()"))
    
    if dont_ind == -1 or do_ind == -1:
        break
    
    inp = inp[:dont_ind] + inp[do_ind + len("do()"):]

print(get_sum(inp))