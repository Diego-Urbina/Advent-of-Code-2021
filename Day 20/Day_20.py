def get_input(path):
    with open(path) as file:
        lines = file.read().split("\n")
        algorithm = lines[0]
        image = [list(line) for line in lines[2:]]

    return algorithm, image


def get_enhancement_values(algorithm):
    alg_dict = {}
    for idx, char in enumerate(algorithm):
        alg_dict[idx] = char

    return alg_dict


def pixel_value(image, point, pixel_out_of_range_value):
    """Return the integer pixel value by looking at a
    3x3 square of pixels centered at the given point"""
    value = ""
    for y in range(point[1] - 1, point[1] + 2):
        for x in range(point[0] - 1, point[0] + 2):
            if 0 <= x < len(image[0]) and 0 <= y < len(image):
                value += image[y][x]
            else:
                value += pixel_out_of_range_value

    value = value.replace(".", "0").replace("#", "1")
    return int(value, 2)


def enhance_image(image, enhancement_values, pixel_out_of_range_value):
    new_width = len(image[0]) + 2
    new_height = len(image) + 2
    new_image = [[None for _ in range(new_width)] for _ in range(new_height)]

    for idx_y in range(new_height):
        for idx_x in range(new_width):
            value = pixel_value(image, (idx_x - 1, idx_y - 1), pixel_out_of_range_value)
            new_image[idx_y][idx_x] = enhancement_values[value]

    return new_image


def save_image(image, steps):
    path = "./Day 20/" + str(steps) + "_steps.txt"
    with open(path, "w") as file:
        for row in image:
            file.write("".join(row) + "\n")


def puzzle(path, steps):
    algorithm, image = get_input(path)
    enhancement_values = get_enhancement_values(algorithm)

    # First, pixels out of range are pure darkness
    pixel_out_of_range_value = "."
    for _ in range(steps):
        image = enhance_image(image, enhancement_values, pixel_out_of_range_value)

        # Then, pixels out of range can change!
        if pixel_out_of_range_value == ".":
            pixel_out_of_range_value = enhancement_values[0]
        elif pixel_out_of_range_value == "#":
            pixel_out_of_range_value = enhancement_values[511]

    print(len([v for row in image for v in row if v == "#"]))
    save_image(image, steps)


puzzle("./Day 20/Day_20_input.txt", 2)
puzzle("./Day 20/Day_20_input.txt", 50)
