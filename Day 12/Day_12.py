def get_caves_graph(path):
    """ Return caves connections as a bidirected graph """
    caves_graph = {}

    with open(path) as file:
        for line in file:
            cave_1, cave_2 = line.rstrip("\n").split("-")

            if cave_1 not in caves_graph:
                caves_graph[cave_1] = set()
            if cave_2 not in caves_graph:
                caves_graph[cave_2] = set()

            caves_graph[cave_1].add(cave_2)
            caves_graph[cave_2].add(cave_1)

    return caves_graph

def dfs(node, graph, valid_cave, path, all_paths):
    path.append(node)
    if node == "end":
        all_paths.append(path)
    else:
        if valid_cave(node, path):
            for neighbour in graph[node]:
                dfs(neighbour, graph, valid_cave, path.copy(), all_paths)

def cave_is_small(cave):
    """ A cave is small if its name is in lowercase """
    return cave.islower()

def puzzle1():
    def valid_cave_1(cave, visited):
        """
        Big caves can be visited any number of times.
        Small caves can be visited at most once
        """
        if not cave_is_small(cave):
            return True

        return visited.count(cave) <= 1

    caves_graph = get_caves_graph("./Day 12/Day_12_input.txt")
    all_paths = []
    dfs("start", caves_graph, valid_cave_1, [], all_paths)
    print("There are", len(all_paths), "different paths:")

def puzzle2():
    def valid_cave_2 (cave, visited):
        """
        Big caves can be visited any number of times.
        A single small cave can be visited at most twice,
        and the remaining small caves can be visited at most once.
        However, the caves named start and end can only be visited exactly once each
        """
        if not cave_is_small(cave):
            return True

        # start and end only once
        if cave in ["start", "end"]:
            return visited.count(cave) <= 1

        # at the most, only one small cave repeated
        small_caves_visited = list(filter(str.islower, visited))
        if len(small_caves_visited) <= len(set(small_caves_visited)) + 1:
            return True

        return False

    caves_graph = get_caves_graph("./Day 12/Day_12_input.txt")
    all_paths = []
    dfs("start", caves_graph, valid_cave_2, [], all_paths)
    print("There are", len(all_paths), "different paths:")

puzzle1()
puzzle2()
