def get_data(path):
    with open(path) as file:
        return [[char for char in row.rstrip("\n")] for row in file]


def puzzle1(path):
    bottom_sea = get_data(path)

    steps = 0
    while True:
        steps += 1
        move_right = move(bottom_sea, ">")
        move_down = move(bottom_sea, "v")
        if move_right + move_down == 0:
            break

    print(steps)


def move(bottom_sea, cucumber):
    to_move = []
    width = len(bottom_sea[0])
    height = len(bottom_sea)
    for row_idx, row in enumerate(bottom_sea):
        for col_idx, cell in enumerate(row):
            if cell == cucumber:
                if cucumber == ">":
                    if bottom_sea[row_idx][(col_idx + 1) % width] == ".":
                        to_move.append((row_idx, col_idx))
                elif cucumber == "v":
                    if bottom_sea[(row_idx + 1) % height][col_idx] == ".":
                        to_move.append((row_idx, col_idx))

    for move in to_move:
        if cucumber == ">":
            bottom_sea[move[0]][move[1]] = "."
            bottom_sea[move[0]][(move[1] + 1) % width] = ">"
        elif cucumber == "v":
            bottom_sea[move[0]][move[1]] = "."
            bottom_sea[(move[0] + 1) % height][move[1]] = "v"

    return len(to_move)


puzzle1("./Day 25/Day_25_input.txt")
