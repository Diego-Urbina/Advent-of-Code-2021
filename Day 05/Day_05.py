with open("./Day 05/Day_05_input.txt", "r") as file:
    vents = []
    max_x = 0
    max_y = 0
    for line in file:
        points = line.rstrip().split(" -> ")
        x1, y1 = map(int, points[0].split(","))
        x2, y2 = map(int, points[1].split(","))
        start = (x1, y1)
        end = (x2, y2)
        vents.append((start, end))

        max_x = max(max_x, x1, x2)
        max_y = max(max_y, y1, y2)


def is_horizontal(vent):
    """Same y-coord"""
    return vent[0][1] == vent[1][1]


def is_vertical(vent):
    """Same x-coord"""
    return vent[0][0] == vent[1][0]


def is_diagonal(vent):
    """Exactly 45 degrees"""
    return abs(vent[0][0] - vent[1][0]) == abs(vent[0][1] - vent[1][1])


ocean_map_1 = [[0 for _ in range(max_y + 1)] for _ in range(max_x + 1)]
ocean_map_2 = [[0 for _ in range(max_y + 1)] for _ in range(max_x + 1)]

for vent in vents:
    x1 = vent[0][0]
    x2 = vent[1][0]
    y1 = vent[0][1]
    y2 = vent[1][1]

    if is_horizontal(vent):
        for offset in range(abs(x2 - x1) + 1):
            x = x1 + offset if x1 < x2 else x1 - offset
            ocean_map_1[x][y1] += 1
            ocean_map_2[x][y1] += 1

    if is_vertical(vent):
        for offset in range(abs(y2 - y1) + 1):
            y = y1 + offset if y1 < y2 else y1 - offset
            ocean_map_1[x1][y] += 1
            ocean_map_2[x1][y] += 1

    if is_diagonal(vent):
        for offset in range(abs(x2 - x1) + 1):
            x = x1 + offset if x1 < x2 else x1 - offset
            y = y1 + offset if y1 < y2 else y1 - offset
            ocean_map_2[x][y] += 1

print(sum(1 for i in ocean_map_1 for j in i if j >= 2))
print(sum(1 for i in ocean_map_2 for j in i if j >= 2))
