from collections import defaultdict
from math import sqrt

v2Cache = {}
class Vector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.cached_string = f'{self.x},{self.y}'
    @staticmethod
    def create(x, y):
        if (x, y) in v2Cache:
            return v2Cache[(x, y)]
        v = Vector2(x, y)
        v2Cache[(x, y)] = v
        return v
    def to_tuple(self):
        return (self.x, self.y)
    def to_yx_tuple(self):
        return (self.y, self.x)
    def manhattan_distance(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)
    def sqr_magnitude(self):
        return self.x ** 2 + self.y ** 2
    def magnitude(self):
        return sqrt(self.sqr_magnitude())
    def normalized(self):
        m = self.magnitude()
        return Vector2(self.x / m, self.y / m)
    def rounded(self):
        return Vector2(int(round(self.x)), int(round(self.y)))
    def clamped(self, lower, upper):
        return Vector2(lower if self.x < lower else upper if self.x > upper else self.x, lower if self.y < lower else upper if self.y > upper else self.y)
    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)
    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y)
    def __mul__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return Vector2(self.x * other, self.y * other)
        if isinstance(other, Vector2):
            return Vector2(self.x * other.x, self.y * other.y)
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    def __lt__(self, other):
        return self.sqr_magnitude() < other.sqr_magnitude()
    def __hash__(self):
        return hash(self.cached_string)
    def __repr__(self):
        return 'x: ' + str(self.x) + ', y: ' + str(self.y)
    def __str__(self):
        return self.__repr__()

class Vector3:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z
    def to_tuple(self):
        return (self.x, self.y, self.z)
    def manhattan_distance(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y) + abs(self.z - other.z)
    def clone(self):
        return Vector3(self.x, self.y, self.z)
    def __add__(self, other):
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)
    def __mul__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return Vector3(self.x * other, self.y * other, self.z * other)
        if isinstance(other, Vector3):
            return Vector3(self.x * other.x, self.y * other.y, self.z * other.z)
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z
    def __hash__(self):
        return hash(f'{self.x},{self.y},{self.z}')
    def __repr__(self):
        return 'x: ' + str(self.x) + ', y: ' + str(self.y) + ', z: ' + str(self.z)
    def __str__(self):
        return self.__repr__()

class Vector4(Vector3):
    def __init__(self, x, y, z, t):
        self.t = t
        super().__init__(x, y, z)
    def to_tuple(self):
        return (self.x, self.y, self.z, self.t)
    def manhattan_distance(self, other):
        return super().manhattan_distance(other) + abs(self.t - other.t)
    def __repr__(self):
        return super().__repr__() + ', t: ' + str(self.t)
    def __add__(self, other):
        return Vector4(self.x + other.x, self.y + other.y, self.z + other.z, self.t + other.t)
    def __hash__(self):
        return hash(f'{self.x},{self.y},{self.z},{self.t}')
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z, self.t == other.t

class Grid2d:
    ''' A 2d grid that has 0,0 at the top-left corner. '''

    def __init__(self, default_val, initial_values = None):
        self.__grid = defaultdict(lambda: default_val)
        self.__max_x = 0
        self.__min_x = 0
        self.__max_y = 0
        self.__min_y = 0
        self.__default_val = default_val

        if initial_values is not None:
            for y in range(len(initial_values)):
                for x in range(len(initial_values[y])):
                    self.__grid[Vector2.create(x, y)] = initial_values[y][x]
                    self.__max_x = max(self.__max_x, x)
                    self.__min_x = min(self.__min_x, x)
                    self.__max_y = max(self.__max_y, y)
                    self.__min_y = min(self.__min_y, y)

    def copy(self):
        copy = Grid2d(self.__default_val)
        min_b, max_b = self.get_bounds()
        for y in range(min_b.y, max_b.y + 1):
            for x in range(min_b.x, max_b.x + 1):
                copy[Vector2.create(x, y)] = self.__grid[Vector2.create(x, y)]
        return copy

    def get_bounds(self):
        ''' Get position bounds of this grid. Tuple of min position (x,y) and max position (x,y) '''
        return (Vector2.create(self.__min_x, self.__min_y), Vector2.create(self.__max_x, self.__max_y))

    def keys(self):
        return self.__grid.keys()

    def values(self):
        return self.__grid.values()

    def items(self):
        return self.__grid.items()

    def get_cardinal_neighbors(self, v):
        return [v + d for d in [Vector2(0, 1), Vector2(1, 0), Vector2(-1, 0), Vector2(0, -1)] if v + d in self.__grid]
    
    def get_diagonal_neighbors(self, v):
        return [v + d for d in [Vector2(1, 1), Vector2(1, -1), Vector2(-1, -1), Vector2(-1, 1)] if v + d in self.__grid]
    
    def get_all_neighbors(self, v):
        return self.get_cardinal_neighbors(v) + self.get_diagonal_neighbors(v)

    def recompute_bounds(self):
        '''
        used to recompute minimums for the purpose of printing when the printed grid is far away from (0, 0)
        '''
        keys = self.__grid.keys()
        self.__max_x = max(i.x for i in keys)
        self.__min_x = min(i.x for i in keys)
        self.__max_y = max(i.y for i in keys)
        self.__min_y = min(i.y for i in keys)

    def __contains__(self, key: Vector2):
        return key in self.__grid

    def __setitem__(self, pos: Vector2, val):
        self.__grid[pos] = val
        self.__max_x = max(self.__max_x, pos.x)
        self.__min_x = min(self.__min_x, pos.x)
        self.__max_y = max(self.__max_y, pos.y)
        self.__min_y = min(self.__min_y, pos.y)
        
    def __getitem__(self, key: Vector2):
        return self.__grid[key]
    def __str__(self):
        st = ""
        for y in range(self.__min_y, self.__max_y + 1):
            line = ""
            for x in range(self.__min_x, self.__max_x + 1):
                line += str(self.__grid[Vector2.create(x, y)])
            line += '\n'
            st += line
        return st
    def __repr__(self):
        return self.__str__()

def id_gen(start_at):
    while True:
        yield start_at
        start_at += 1