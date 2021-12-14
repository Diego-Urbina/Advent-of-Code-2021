from collections import deque

def get_octopuses(path):
    """ Read initial energy levels """
    data = open(path).read().strip().split("\n")
    return [[int(y) for y in x] for x in data]

def get_octopuses_to_flash(octopuses, center_point = (0, 0), size = 1000000):
    """ Return the location of the octopuses ready to flash
        into the submatrix from center_point with the given size """
    points = []

    for row in range(max(0, center_point[0] - size), min(len(octopuses), center_point[0] + size + 1)):
        for col in range(max(0, center_point[1] - size), min(len(octopuses[row]), center_point[1] + size + 1)):
            if octopuses[row][col] == 10:
                points.append((row, col))

    return points

def increment_energy(octopuses, center_point = (0, 0), size = 1000000):
    """ Add 1 energy to each octopus into the submatrix
        from center_point with the given size """
    for row in range(max(0, center_point[0] - size), min(len(octopuses), center_point[0] + size + 1)):
        for col in range(max(0, center_point[1] - size), min(len(octopuses[row]), center_point[1] + size + 1)):
            octopuses[row][col] += 1

def flash(octopuses):
    """ Propagate flashes """
    flashes = 0
    queue = deque(get_octopuses_to_flash(octopuses))

    while queue:
        flashes += 1
        octopus = queue.popleft()
        increment_energy(octopuses, octopus, 1)
        for octopus in get_octopuses_to_flash(octopuses, octopus, 1):
            queue.append(octopus)

    return flashes

def reset_energy(octopuses):
    """ Reset energy to every octopus that have flashed """
    for row in range(len(octopuses)):
        for col in range(len(octopuses[row])):
            if octopuses[row][col] >= 10:
                octopuses[row][col] = 0

def all_flashing(octopuses):
    """ All octopuses are flashing if all have an energy level greater or equal than 10 """
    return all(y >= 10 for x in octopuses for y in x)

def puzzle1():
    octopuses = get_octopuses("./Day 11/Day_11_input.txt")
    flashes = 0
    steps = 100
    for _ in range(1, steps + 1):
        increment_energy(octopuses)
        flashes += flash(octopuses)
        reset_energy(octopuses)

    print("Total flashes =", flashes)

def puzzle2():
    octopuses = get_octopuses("./Day 11/Day_11_input.txt")
    flashes = 0
    step = 1
    while True:
        increment_energy(octopuses)
        flashes += flash(octopuses)
        if all_flashing(octopuses):
            break
        reset_energy(octopuses)
        step += 1

    print("All flashing in step =", step)

puzzle1()
puzzle2()
