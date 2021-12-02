def get_final_coords_part1(commands):
    x = 0
    y = 0
    for command in commands:
        move = command[0]
        units = int(command[1])
        if move == "forward":
            x += units
        elif move == "down":
            y += units
        else:
            y -= units

    return (x, y)

def get_final_coords_part2(commands):
    x = 0
    y = 0
    aim = 0
    for command in commands:
        move = command[0]
        units = int(command[1])
        if move == "forward":
            x += units
            y += aim * units
        elif move == "down":
            aim += units
        else:
            aim -= units

    return (x, y)

with open("./Day 02/Day_02_input.txt", "r") as file:
    commands = []
    for line in file:
        commands.append(line.split(" "))

coords = get_final_coords_part1(commands)
print(coords)
print(coords[0] * coords[1])

coords = get_final_coords_part2(commands)
print(coords)
print(coords[0] * coords[1])