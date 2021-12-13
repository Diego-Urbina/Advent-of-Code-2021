def find_nums(nums):
    n1 = [x for x in nums if len(x) == 2][0]
    n4 = [x for x in nums if len(x) == 4][0]
    n7 = [x for x in nums if len(x) == 3][0]
    n8 = [x for x in nums if len(x) == 7][0]
    n9 = [x for x in nums if len(x) == 6 and all(y in x for y in n4)][0]
    n0 = [x for x in nums if len(x) == 6 and x != n9 and all(y in x for y in n1)][0]
    n6 = [x for x in nums if len(x) == 6 and x != n9 and x != n0][0]
    n3 = [x for x in nums if len(x) == 5 and all(y in x for y in n1)][0]
    n5 = [x for x in nums if len(x) == 5 and x != n3 and all(y in n9 for y in x)][0]
    n2 = [x for x in nums if len(x) == 5 and x != n3 and x != n5][0]
    return [n0, n1, n2, n3, n4, n5, n6, n7, n8, n9]


data = open("./Day 08/Day_08_input.txt").read().strip().split("\n")
lines = [[["".join(sorted(z)) for z in y.split()] for y in x.split(" | ")] for x in data]
p1 = p2 = 0
for nums, digits in lines:
    nums = find_nums(nums)
    p1 += sum(1 for x in digits if x in [nums[y] for y in [1, 4, 7, 8]])
    p2 += int("".join([str(nums.index(x)) for x in digits]))
print(f"Part 1: {p1}")
print(f"Part 2: {p2}")