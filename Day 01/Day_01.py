def count_increments(measures):
    count = 0

    for i in range(1, len(measures)):
        if measures[i] > measures[i - 1]:
            count += 1

    return count

def get_simple_measures(path):
    measures = []

    with open(path, "r") as file:
        for line in file:
            measures.append(int(line))

    return measures

def get_windowed_measures(path, window_size):
    measures = []

    with open(path, "r") as file:
        for line_number, line in enumerate(file):
            measures.append(0)
            value = int(line)
            for i in range(window_size):
                index = line_number - i
                if index >= 0:
                    measures[index] += value

    # delete last (window_size - 1) elements
    return measures[0:len(measures) - (window_size - 1)]

# part 1
print(count_increments(get_simple_measures("./Day 01/Day_01_input.txt")))

# part 2
print(count_increments(get_windowed_measures("./Day 01/Day_01_input.txt", 3)))
