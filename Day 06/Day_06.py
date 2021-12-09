with open("./Day 06/Day_06_input.txt", "r") as file:
    ages = list(map(int, file.readline().rstrip().split(",")))

def puzzle(ages, days):
    fishes = [0] * 9

    for age in ages:
        fishes[age] += 1

    for _ in range(days):
        fishes_age_0 = fishes[0]
        for i in range(1, len(fishes)):
            fishes[i - 1] = fishes[i]
        fishes[6] += fishes_age_0
        fishes[8] = fishes_age_0

    print("After ", days, " days, there are ", sum(fishes), " fishes")

puzzle(ages, 80)
puzzle(ages, 256)