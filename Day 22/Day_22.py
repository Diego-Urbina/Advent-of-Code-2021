def get_reboot_steps(path):
    reboot_steps = []
    with open(path) as file:
        for line in file:
            command, coords = line.rstrip("\n").split(" ")
            coords = coords.split(",")
            reboot_steps.append([command])
            for coord in coords:
                coord = tuple(map(int, coord[coord.index("=") + 1 :].split("..")))
                reboot_steps[-1].append(coord)

    return reboot_steps


def get_reactor(size):
    return [[[0 for _ in range(size)] for _ in range(size)] for _ in range(size)]


def puzzle1(path):
    SIZE = 101
    OFFSET = 50

    reactor = get_reactor(SIZE)

    reboot_steps = get_reboot_steps(path)
    for step in reboot_steps:
        value = 1 if step[0] == "on" else 0
        x_interval = step[1]
        y_interval = step[2]
        z_interval = step[3]
        if (
            x_interval[0] < -OFFSET
            or x_interval[1] > OFFSET
            or y_interval[0] < -OFFSET
            or y_interval[1] > OFFSET
            or z_interval[0] < -OFFSET
            or z_interval[1] > OFFSET
        ):
            continue

        for x in range(x_interval[0] + OFFSET, x_interval[1] + OFFSET + 1):
            for y in range(y_interval[0] + OFFSET, y_interval[1] + OFFSET + 1):
                for z in range(z_interval[0] + OFFSET, z_interval[1] + OFFSET + 1):
                    reactor[x][y][z] = value

    count_on = 0
    for x in range(len(reactor)):
        for y in range(len(reactor[0])):
            for z in range(len(reactor[0][0])):
                if reactor[x][y][z] == 1:
                    count_on += 1

    print(count_on)


def puzzle2(path):
    reboot_steps = get_reboot_steps(path)


puzzle1("./Day 22/Day_22_input.txt")
puzzle2("./Day 22/Day_22_test.txt")
