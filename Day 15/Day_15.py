import timeit


class Node:
    """Represents a node in a grid"""

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.g = 0
        self.parent = None

    def g_cost(self):
        """Return actual cost"""
        return self.g

    def h_cost(self, target):
        """Return the remaining path cost (heuristic)"""
        return abs(self.x - target.x) + abs(self.y - target.y)

    def f_cost(self, target):
        """Return total cost"""
        return self.g_cost() + self.h_cost(target)


def get_risk_matrix(path):
    with open(path) as file:
        return [[int(x) for x in line] for line in file.read().split("\n")]


def multiply_tile(tile, times):
    w_tile = len(tile)
    h_tile = len(tile[0])
    aux = [[0 for _ in range(h_tile * times)] for _ in range(w_tile * times)]
    for x in range(len(aux)):
        for y in range(len(aux[0])):
            aux[x][y] = tile[x % w_tile][y % h_tile] + (x // w_tile) + (y // h_tile)
            while aux[x][y] > 9:
                aux[x][y] -= 9

    return aux


def get_cave_map(width, height):
    return [[Node(x, y) for y in range(height)] for x in range(width)]


def get_neighbours(node, cave_map):
    """horizontal and vertical neighbors"""
    neighbours = []
    if node.x - 1 >= 0:
        neighbours.append(cave_map[node.x - 1][node.y])
    if node.x + 1 < len(cave_map):
        neighbours.append(cave_map[node.x + 1][node.y])
    if node.y - 1 >= 0:
        neighbours.append(cave_map[node.x][node.y - 1])
    if node.y + 1 < len(cave_map[0]):
        neighbours.append(cave_map[node.x][node.y + 1])
    return neighbours


def a_star(cave_map, risk):
    start_node = cave_map[0][0]
    end_node = cave_map[-1][-1]

    open_nodes = [start_node]  # maybe use a min heap is faster
    closed_nodes = set()

    while True:
        current = min(open_nodes, key=lambda node: Node.f_cost(node, end_node))
        open_nodes.remove(current)
        closed_nodes.add(current)

        if current == end_node:
            print("Cost =", current.f_cost(end_node))
            break

        for neighbour in get_neighbours(current, cave_map):
            if neighbour in closed_nodes:
                continue

            g_through_current = current.g + risk[neighbour.y][neighbour.x]
            if neighbour.g > g_through_current or neighbour not in open_nodes:
                neighbour.g = g_through_current
                neighbour.parent = current
                if neighbour not in open_nodes:
                    open_nodes.append(neighbour)


def puzzle1():
    """A* pathfinding algorithm"""
    risk = get_risk_matrix("./Day 15/Day_15_input.txt")
    risk = multiply_tile(risk, 1)
    cave_map = get_cave_map(len(risk), len(risk[0]))
    a_star(cave_map, risk)


def puzzle2():
    """A* pathfinding algorithm"""
    risk = get_risk_matrix("./Day 15/Day_15_input.txt")
    risk = multiply_tile(risk, 5)
    cave_map = get_cave_map(len(risk), len(risk[0]))
    a_star(cave_map, risk)


print(timeit.timeit(puzzle1, number=1))
print(timeit.timeit(puzzle2, number=1))
