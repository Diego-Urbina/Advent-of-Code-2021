with open("./Day 17/Day_17_input.txt") as file:
    _, _, x, y = file.readline().rstrip("\n").split(" ")
    target_x = tuple(map(int, x[2:-1].split("..")))
    target_y = tuple(map(int, y[2:].split("..")))


def position(y_0, v_0, delta, a):
    speeds = [v_0 + a * delta for delta in range(delta)]
    return y_0 + sum(speeds)


def puzzle1():
    a_y = -1

    y_pos = [(0, speed) for speed in range(1000)]
    highest_y_pos = [0] * 1000
    valid_y_speeds = set()
    for _ in range(1, 1000):
        # update pos_y
        for idx, pos_speed in enumerate(y_pos):
            y_pos[idx] = (pos_speed[0] + pos_speed[1], pos_speed[1] + a_y)
            highest_y_pos[idx] = max(highest_y_pos[idx], y_pos[idx][0])
            if target_y[1] >= y_pos[idx][0] >= target_y[0]:
                valid_y_speeds.add(idx)

    print("Highest y position:", max([highest_y_pos[idx] for idx in valid_y_speeds]))


def puzzle2():
    a_x = -1
    a_y = -1

    x_pos = [(0, speed) for speed in range(320)]

    y_speed_offset = 1000
    y_pos = [(0, speed) for speed in range(0 - y_speed_offset, 1 + y_speed_offset, 1)]
    valid_speeds = set()
    for _ in range(1, 1000):
        valid_x_speeds = set()
        valid_y_speeds = set()

        # update pos_x
        for idx, pos_speed in enumerate(x_pos):
            x_pos[idx] = (pos_speed[0] + pos_speed[1], max(0, pos_speed[1] + a_x))
            if target_x[0] <= x_pos[idx][0] <= target_x[1]:
                valid_x_speeds.add(idx)

        # update pos_y
        for idx, pos_speed in enumerate(y_pos):
            y_pos[idx] = (pos_speed[0] + pos_speed[1], pos_speed[1] + a_y)
            if target_y[1] >= y_pos[idx][0] >= target_y[0]:
                valid_y_speeds.add(idx - y_speed_offset)

        valid_time_t = set([(x, y) for y in valid_y_speeds for x in valid_x_speeds])
        valid_speeds = valid_speeds.union(valid_time_t)

    print("Distinct initial velocity values:", len(valid_speeds))


puzzle1()
puzzle2()
