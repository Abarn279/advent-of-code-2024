import heapq
from collections import deque

class PriorityQueue:
    def __init__(self):
        self.elements = []
    
    def empty(self):
        return len(self.elements) == 0
    
    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))
    
    def get(self):
        return heapq.heappop(self.elements)[1]

class SearchResponse:
    def __init__(self, found, cost = None, final_node = None, visited = None, all_final_nodes = None):
        self.found = found
        self.cost = cost
        self.final_node = final_node
        self.visited = visited
        self.all_final_nodes = all_final_nodes

def bfs(start, is_goal_fn, get_neighbors_fn, get_key_fn, find_all_goals = False):
    q = deque()
    visited = set()
    q.append((start, 0))
    goals = []

    while len(q) > 0:
        current, cost = q.popleft()
        visited.add(get_key_fn(current))

        if is_goal_fn(current):
            if not find_all_goals:
                return SearchResponse(True, cost, current, visited)
            else: 
                goals.append(current)
                continue

        for neighbor in get_neighbors_fn(current):

            if neighbor not in visited:
                q.append((neighbor, cost + 1))
    
    if find_all_goals and goals:
        return SearchResponse(True, None, None, visited, goals)

    return SearchResponse(False, None, None, visited)

def dfs(start, is_goal_fn, get_neighbors_fn, get_key_fn, find_all_goals = False):
    q = deque()
    visited = set()
    q.appendleft((start, 0))
    goals = []

    while len(q) > 0:
        current, cost = q.popleft()
        visited.add(get_key_fn(current))

        if is_goal_fn(current):
            if not find_all_goals:
                return SearchResponse(True, cost, current, visited)
            else: 
                goals.append(current)
                continue

        for neighbor in get_neighbors_fn(current):

            if neighbor not in visited:
                q.appendleft((neighbor, cost + 1))
    
    if find_all_goals and goals:
        return SearchResponse(True, None, None, visited, goals)

    return SearchResponse(False, None, None, visited)


def astar(start, is_goal_fn, heuristic_fn, cost_fn, get_neighbors_fn, get_key_fn):
    queue = PriorityQueue()
    queue.put(start, 0)
    
    last_node = dict()
    cost_from_start = dict()

    last_node[get_key_fn(start)] = None
    cost_from_start[get_key_fn(start)] = 0

    found = False
    while not queue.empty():
        current = queue.get()

        if is_goal_fn(current):
            found = True
            break 

        for neighbor in get_neighbors_fn(current):
            new_cost = cost_from_start[get_key_fn(current)] + cost_fn(current, neighbor)
            if get_key_fn(neighbor) not in cost_from_start or new_cost < cost_from_start[get_key_fn(neighbor)]:
                cost_from_start[get_key_fn(neighbor)] = new_cost
                priority = new_cost + heuristic_fn(neighbor)
                queue.put(neighbor, priority)
                last_node[get_key_fn(neighbor)] = current

    if found:
        return SearchResponse(True, cost_from_start[get_key_fn(current)], current)
    return SearchResponse(False)
