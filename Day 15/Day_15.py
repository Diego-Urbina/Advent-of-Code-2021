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
    if times == 1:
        return tile

    height_tile = len(tile)
    width_tile = len(tile[0])
    aux = [[0 for _ in range(width_tile * times)] for _ in range(height_tile * times)]
    for y in range(len(aux)):
        for x in range(len(aux[0])):
            aux[y][x] = tile[y % height_tile][x % width_tile]
            y_tile = y // height_tile
            x_tile = x // width_tile
            increments = y_tile + x_tile
            aux[y][x] += increments
            while aux[y][x] > 9:
                aux[y][x] -= 9

    return aux


def get_cave_map(height, width):
    return [[Node(x, y) for x in range(width)] for y in range(height)]


def get_neighbours(node, cave_map):
    """horizontal and vertical neighbors"""
    neighbours = []
    if node.y - 1 >= 0:
        neighbours.append(cave_map[node.y - 1][node.x])
    if node.y + 1 < len(cave_map):
        neighbours.append(cave_map[node.y + 1][node.x])
    if node.x - 1 >= 0:
        neighbours.append(cave_map[node.y][node.x - 1])
    if node.x + 1 < len(cave_map[0]):
        neighbours.append(cave_map[node.y][node.x + 1])
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
