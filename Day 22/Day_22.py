import functools


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


def puzzle1(path):
    SIZE = 101
    OFFSET = 50

    reactor = [[[0 for _ in range(SIZE)] for _ in range(SIZE)] for _ in range(SIZE)]
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


class Cuboid:
    def __init__(self, x1, x2, y1, y2, z1, z2):
        self.x1, self.y1, self.z1 = (x1, y1, z1)
        self.x2, self.y2, self.z2 = (x2, y2, z2)
        self.sizes = (x2 - x1, y2 - y1, z2 - z1)

    def volume(self):
        return functools.reduce(lambda a, b: a * b, self.sizes)

    def overlap(self, other):
        return (
            other.x1 < self.x2
            and self.x1 < other.x2
            and other.y1 < self.y2
            and self.y1 < other.y2
            and other.z1 < self.z2
            and self.z1 < other.z2
        )

    def sustract(self, other):
        """Using @juanplopes's code from
        https://github.com/juanplopes/advent-of-code-2021/blob/main/day22b.py
        with a little modifications"""
        if not self.overlap(other):
            yield self
        else:
            common = Cuboid(
                max(other.x1, self.x1),
                min(other.x2, self.x2),
                max(other.y1, self.y1),
                min(other.y2, self.y2),
                max(other.z1, self.z1),
                min(other.z2, self.z2),
            )

            # Not common across X-axis. Myself across Y and Z axes
            yield Cuboid(self.x1, common.x1, self.y1, self.y2, self.z1, self.z2)
            # Not common across X-axis. Myself across Y and Z axes
            yield Cuboid(common.x2, self.x2, self.y1, self.y2, self.z1, self.z2)
            # Common across X-axis. Not common across Y-axis. Myself across Z-axis
            yield Cuboid(common.x1, common.x2, self.y1, common.y1, self.z1, self.z2)
            # Common across X-axis. Not common across Y-axis. Myself across Z-axis
            yield Cuboid(common.x1, common.x2, common.y2, self.y2, self.z1, self.z2)
            # Common across X-axis. Common across Y-axis. Not common across Z-axis
            yield Cuboid(common.x1, common.x2, common.y1, common.y2, self.z1, common.z1)
            # Common across X-axis. Common across Y-axis. Not common across Z-axis
            yield Cuboid(common.x1, common.x2, common.y1, common.y2, common.z2, self.z2)


def create_cuboid(x, y, z):
    x1 = x[0]
    x2 = x[1] + 1
    y1 = y[0]
    y2 = y[1] + 1
    z1 = z[0]
    z2 = z[1] + 1
    return Cuboid(x1, x2, y1, y2, z1, z2)


def puzzle2(path):
    cuboids = set()
    reboot_steps = get_reboot_steps(path)
    for step in reboot_steps:
        new_cuboid = create_cuboid(*step[1:])

        overlaped = list(filter(new_cuboid.overlap, cuboids))
        if len(overlaped) > 0:
            for cuboid in overlaped:
                """For every overlaped cuboid:
                - remove from the cuboids list
                - split the cuboid
                - add not empty pieces"""
                cuboids.remove(cuboid)
                subcuboids = [x for x in cuboid.sustract(new_cuboid) if x.volume() > 0]
                cuboids.update(subcuboids)

        if step[0] == "on":
            cuboids.add(new_cuboid)

    count_on = 0
    for cuboid in cuboids:
        count_on += cuboid.volume()

    print(count_on)


puzzle1("./Day 22/Day_22_input.txt")
puzzle2("./Day 22/Day_22_input.txt")
