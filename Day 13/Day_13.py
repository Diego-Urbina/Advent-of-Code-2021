def read_data(path):
    dots = []
    folds = []
    width = 0
    height = 0
    with open(path) as file:
        for line in file.read().strip().split("\n"):
            if line:
                if line[0].isdigit():
                    dot = tuple(map(int, line.split(",")))
                    dots.append(dot)
                    width = max(width, dot[0] + 1)
                    height = max(height, dot[1] + 1)
                else:
                    axis, value = line.split(" ")[2].split("=")
                    folds.append((axis, int(value)))

    paper = [[" " for _ in range(width)] for _ in range(height)]
    for dot in dots:
        paper[dot[1]][dot[0]] = "#"

    return paper, folds

def fold_paper(paper, axis, value):
    height = len(paper) if axis == "x" else value
    width = len(paper[0]) if axis == "y" else value
    paper_fold = [[" " for _ in range(width)] for _ in range(height)]

    for y in range(len(paper)):
        for x in range(len(paper[y])):
            if paper[y][x] == "#":
                new_x = x if axis == "y" else (x if x < value else value - (x - value))
                new_y = y if axis == "x" else (y if y < value else value - (y - value))
                paper_fold[new_y][new_x] = "#"

    return paper_fold

def puzzle1():
    paper, folds = read_data("./Day 13/Day_13_input.txt")
    paper = fold_paper(paper, *folds[0])
    print(len([y for x in paper for y in x if y == "#"]))

def puzzle2():
    paper, folds = read_data("./Day 13/Day_13_input.txt")

    for fold in folds:
        paper = fold_paper(paper, *fold)

    for row in paper:
        print("".join(row))

puzzle1()
puzzle2()
