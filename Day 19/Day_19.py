from collections import defaultdict
from collections import deque
import timeit


class Scanner:
    def __init__(self, idx):
        self.idx = idx
        self.beacons = set()
        self.rotated_beacons = set()
        self.position = (0, 0, 0)

    def add_beacon(self, beacon):
        self.beacons.add(beacon)

    def rotate(self, rotation):
        self.rotated_beacons.clear()
        for x, y, z in self.beacons:
            # +X
            if rotation == 0:
                self.rotated_beacons.add((x, y, z))
            elif rotation == 1:
                self.rotated_beacons.add((x, -z, y))
            elif rotation == 2:
                self.rotated_beacons.add((x, -y, -z))
            elif rotation == 3:
                self.rotated_beacons.add((x, z, -y))

            # -X
            elif rotation == 4:
                self.rotated_beacons.add((-x, y, -z))
            elif rotation == 5:
                self.rotated_beacons.add((-x, z, y))
            elif rotation == 6:
                self.rotated_beacons.add((-x, -y, z))
            elif rotation == 7:
                self.rotated_beacons.add((-x, -z, -y))

            # +Y
            elif rotation == 8:
                self.rotated_beacons.add((y, x, -z))
            elif rotation == 9:
                self.rotated_beacons.add((y, z, x))
            elif rotation == 10:
                self.rotated_beacons.add((y, -x, z))
            elif rotation == 11:
                self.rotated_beacons.add((y, -z, -x))

            # -Y
            elif rotation == 12:
                self.rotated_beacons.add((-y, x, z))
            elif rotation == 13:
                self.rotated_beacons.add((-y, -z, x))
            elif rotation == 14:
                self.rotated_beacons.add((-y, -x, -z))
            elif rotation == 15:
                self.rotated_beacons.add((-y, z, -x))

            # +Z
            elif rotation == 16:
                self.rotated_beacons.add((z, x, y))
            elif rotation == 17:
                self.rotated_beacons.add((z, -y, x))
            elif rotation == 18:
                self.rotated_beacons.add((z, -x, -y))
            elif rotation == 19:
                self.rotated_beacons.add((z, y, -x))

            # -Z
            elif rotation == 20:
                self.rotated_beacons.add((-z, x, -y))
            elif rotation == 21:
                self.rotated_beacons.add((-z, y, x))
            elif rotation == 22:
                self.rotated_beacons.add((-z, -x, y))
            elif rotation == 23:
                self.rotated_beacons.add((-z, -y, -x))

    def overlap(self, other):
        overlapping = False

        distances = defaultdict(int)
        for x1, y1, z1 in self.beacons:
            for x2, y2, z2 in other.rotated_beacons:
                distances[(x1 - x2, y1 - y2, z1 - z2)] += 1

        overlapping = set(filter(lambda x: distances[x] >= 12, distances))
        if overlapping:
            assert len(overlapping) == 1, "More than one overlapping relative position"
            relative_pos = overlapping.pop()
            other.commit_rotation()
            other.set_relative_pos(relative_pos)
            return True

        return False

    def commit_rotation(self):
        self.beacons = set(self.rotated_beacons)
        self.rotated_beacons.clear()

    def set_relative_pos(self, relative_pos):
        self.position = relative_pos
        self.beacons = set(
            (
                beacon[0] + relative_pos[0],
                beacon[1] + relative_pos[1],
                beacon[2] + relative_pos[2],
            )
            for beacon in self.beacons
        )

    def merge(self, other):
        for beacon in other.beacons:
            self.add_beacon(beacon)


def read_scanners(path):
    scanners = []
    with open(path) as file:
        for line in file.read().split("\n"):
            if not line:
                continue
            if line.startswith("---"):
                scanners.append(Scanner(len(scanners)))
            else:
                scanners[-1].add_beacon(tuple(map(int, line.split(","))))

    return scanners


def puzzles(path):
    queue = deque(read_scanners(path))
    ref_scanner = queue.popleft()
    located_scanners = [ref_scanner]
    while queue:
        scanner = queue.popleft()
        for rotation in range(24):
            scanner.rotate(rotation)
            if ref_scanner.overlap(scanner):
                ref_scanner.merge(scanner)
                located_scanners.append(scanner)
                break
        else:
            queue.append(scanner)

    print(f"Total beacons = {len(ref_scanner.beacons)}")

    max_manhattan = 0
    for i in range(len(located_scanners)):
        for j in range(i + 1, len(located_scanners)):
            x1, y1, z1 = located_scanners[i].position
            x2, y2, z2 = located_scanners[j].position
            manhattan = abs(x1 - x2) + abs(y1 - y2) + abs(z1 - z2)
            max_manhattan = max(max_manhattan, manhattan)

    print(f"Max Manhattan = {max_manhattan}")


puzzles("./Day 19/Day_19_input.txt")
