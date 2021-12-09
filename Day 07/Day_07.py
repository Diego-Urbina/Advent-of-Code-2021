import math

def get_crabs_pos(path):
    with open(path, "r") as file:
        positions =  list(map(int, file.readline().rstrip().split(",")))
        positions.sort()
        return positions

def puzzle1(path):
    """ Median is the best position """
    crabs_pos = get_crabs_pos(path)
    long = len(crabs_pos)
    if long % 2 == 0:
        # Average of the two center elements
        median = (crabs_pos[long // 2 - 1] + crabs_pos[long // 2]) // 2
    else:
        median = crabs_pos[long // 2]

    return sum(abs(x - median) for x in crabs_pos)

def puzzle2(path):
    """ Average is the best position """
    crabs_pos = get_crabs_pos(path)
    average = sum(crabs_pos) / len(crabs_pos)

    m1 = math.floor(average)
    d1 = [abs(m1 - x) for x in crabs_pos]
    ret1 = sum(d * (d + 1) // 2 for d in d1)

    m2 = math.ceil(average)
    d2 = [abs(m2 - x) for x in crabs_pos]
    ret2 = sum(d * (d + 1) // 2 for d in d2)

    return min(ret1, ret2)

assert puzzle1("./Day 07/Day_07_test.txt") == 37
print(puzzle1("./Day 07/Day_07_input.txt"))

assert puzzle2("./Day 07/Day_07_test.txt") == 168
print(puzzle2("./Day 07/Day_07_input.txt"))
