from collections import deque
import functools

def read_heightmap(path):
    data = open(path).read().strip().split("\n")
    heightmap = [[int(y) for y in x] for x in data]
    return heightmap

def get_lower_hor(heightmap):
    """ Return a matrix with same size as heightmap
        An element with value of 1 represents that it is lower
        than the element of its left and the element of its rigth
    """
    lower = []
    for row_hm in heightmap:
        row_ret = []
        for x in range(len(row_hm)):
            row_ret.append(0)
            if x == 0:
                row_ret[x] = 1
            elif row_hm[x] < row_hm[x-1]:
                row_ret[x-1] = 0
                row_ret[x] = 1
        lower.append(row_ret)
    return lower

def get_lower_ver(heightmap):
    """ Return a matrix with same size as heightmap
        An element with value of 1 represents that it is lower
        than the element above and the element below
    """
    transposed = list(zip(*heightmap))
    result = get_lower_hor(transposed)
    return list(zip(*result))

def get_risk(heightmap, point):
    return heightmap[point[0]][point[1]] + 1

def point_in_range(matrix, point):
    return 0 <= point[0] < len(matrix) and 0 <= point[1] < len(matrix[0])

def puzzle1():
    heightmap = read_heightmap("./Day 09/Day_09_input.txt")

    hor = get_lower_hor(heightmap)
    ver = get_lower_ver(heightmap)

    rows = len(heightmap)
    cols = len(heightmap[0])
    low_points = [(row, col) for row in range(rows) for col in range(cols) if hor[row][col] == ver[row][col] == 1]
    print(sum(get_risk(heightmap, point) for point in low_points))

def puzzle2():
    heightmap = read_heightmap("./Day 09/Day_09_input.txt")
    flood_map = [[-1 if pos != 9 else 9 for pos in row] for row in heightmap]

    hor = get_lower_hor(heightmap)
    ver = get_lower_ver(heightmap)

    rows = len(heightmap)
    cols = len(heightmap[0])
    low_points = [(row, col) for row in range(rows) for col in range(cols) if hor[row][col] == ver[row][col] == 1]

    sizes = []
    for idx_point, point in enumerate(low_points):
        size = 0
        queue = deque([point])
        while queue:
            point = queue.popleft()
            if point_in_range(flood_map, point) and flood_map[point[0]][point[1]] == -1:
                flood_map[point[0]][point[1]] = idx_point
                size += 1
                queue.append((point[0] - 1, point[1])) # left point
                queue.append((point[0] + 1, point[1])) # rigth point
                queue.append((point[0], point[1] - 1)) # top point
                queue.append((point[0], point[1] + 1)) # bottom point
        sizes.append(size)

    sizes.sort(reverse=True)
    print(functools.reduce(lambda a,b: a*b, sizes[0:3]))

puzzle1()
puzzle2()
