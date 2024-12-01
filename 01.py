from collections import Counter, defaultdict

with open('./inp/01.txt') as f:
    lines = [i.split() for i in f.read().split('\n')]

l1 = list(sorted([int(i[0]) for i in lines]))
l2 = list(sorted([int(i[1]) for i in lines]))

# Part A
sm = sum(abs(l2[i] - l1[i]) for i in range(len(l1)))
print(sm)

# Part B
l2_counts = defaultdict(lambda: 0, dict(Counter(l2)))
sm = sum(l1[i] * l2_counts[l1[i]] for i in range(len(l1)))
print(sm)