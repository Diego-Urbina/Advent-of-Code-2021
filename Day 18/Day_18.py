import functools


class SnailfishNumber:
    def __init__(self, number, parent, depth):
        self.parent = parent
        self.depth = depth
        self.left_child = number[0]
        self.right_child = number[1]
        if isinstance(self.left_child, list):
            self.left_child = SnailfishNumber(number[0], self, self.depth + 1)
        if isinstance(self.right_child, list):
            self.right_child = SnailfishNumber(number[1], self, self.depth + 1)

    def get_number(self):
        """Represents the number as a list"""
        value_left = (
            self.left_child
            if isinstance(self.left_child, int)
            else self.left_child.get_number()
        )
        value_right = (
            self.right_child
            if isinstance(self.right_child, int)
            else self.right_child.get_number()
        )

        return [value_left, value_right]

    def magnitude(self):
        """Get the magnitude value"""
        value_left = (
            self.left_child
            if isinstance(self.left_child, int)
            else self.left_child.magnitude()
        )
        value_right = (
            self.right_child
            if isinstance(self.right_child, int)
            else self.right_child.magnitude()
        )

        return 3 * value_left + 2 * value_right

    def first_regular_number_to_left(self):
        """Search first regular number to the left"""
        aux = self
        aux_parent = aux.parent
        # up while i am the left child
        while aux_parent is not None and aux_parent.left_child == aux:
            aux = aux_parent
            aux_parent = aux.parent
        # down by left child, then right child to the end
        if aux_parent is not None:
            aux = aux_parent
            if isinstance(aux.left_child, int):
                aux.left_child += self.left_child
            elif isinstance(aux.left_child, SnailfishNumber):
                aux = aux.left_child
                while isinstance(aux.right_child, SnailfishNumber):
                    aux = aux.right_child

                return aux

        return None

    def first_regular_number_to_right(self):
        """Search first regular number to the rigth"""
        aux = self
        aux_parent = aux.parent
        # up while i am the right child
        while aux_parent is not None and aux_parent.right_child == aux:
            aux = aux_parent
            aux_parent = aux.parent
        # down by right child, then left child to the end
        if aux_parent is not None:
            aux = aux_parent
            if isinstance(aux.right_child, int):
                aux.right_child += self.right_child
            if isinstance(aux.right_child, SnailfishNumber):
                aux = aux.right_child
                while isinstance(aux.left_child, SnailfishNumber):
                    aux = aux.left_child

                return aux

        return None

    def explode(self):
        """Explode the given number"""
        aux = self.first_regular_number_to_left()
        if aux is not None:
            aux.right_child += self.left_child

        aux = self.first_regular_number_to_right()
        if aux is not None:
            aux.left_child += self.right_child

        if self.parent.left_child == self:
            self.parent.left_child = 0
        if self.parent.right_child == self:
            self.parent.right_child = 0

    def split(self):
        """Split the given number"""
        if isinstance(self.left_child, int) and self.left_child >= 10:
            left = self.left_child // 2
            right = self.left_child - left
            self.left_child = SnailfishNumber([left, right], self, self.depth + 1)
        elif isinstance(self.right_child, int) and self.right_child >= 10:
            left = self.right_child // 2
            right = self.right_child - left
            self.right_child = SnailfishNumber([left, right], self, self.depth + 1)

    def reduce_number(self):
        """Apply reduce operation to the given number"""
        while True:
            to_reduce, op = self.next_to_reduce()

            if to_reduce is None:
                break

            if op == "explode":
                to_reduce.explode()
            elif op == "split":
                to_reduce.split()

            # print(op, ":", self.get_number())

    def next_to_reduce(self):
        """Search the first number to reduce

        First, it looks for numbers to explode. If not, numbers to split"""
        to_reduce, op = self.next_to_explode()
        if to_reduce is None:
            to_reduce, op = self.next_to_split()

        return to_reduce, op

    def next_to_explode(self):
        """Search, from left to right, the first number to explode"""
        if self.depth >= 5:
            return self, "explode"

        if isinstance(self.left_child, SnailfishNumber):
            left_reduce = self.left_child.next_to_explode()
            if left_reduce[0] is not None:
                return left_reduce

        if isinstance(self.right_child, SnailfishNumber):
            right_child = self.right_child.next_to_explode()
            if right_child[0] is not None:
                return right_child

        return None, ""

    def next_to_split(self):
        """Search, from left to right, the first number to split"""
        if isinstance(self.left_child, int) and self.left_child >= 10:
            return self, "split"

        if isinstance(self.left_child, SnailfishNumber):
            left_reduce = self.left_child.next_to_split()
            if left_reduce[0] is not None:
                return left_reduce

        if isinstance(self.right_child, int) and self.right_child >= 10:
            return self, "split"

        if isinstance(self.right_child, SnailfishNumber):
            right_child = self.right_child.next_to_split()
            if right_child[0] is not None:
                return right_child

        return None, ""


def parse(input):
    # parse a string to a list
    stack = []
    for char in input:
        if char == ",":
            continue
        if char == "]":
            rigth_elem = stack.pop()
            left_elem = stack.pop()
            stack.pop()  # open bracket
            stack.append([left_elem, rigth_elem])
        else:
            if str.isnumeric(char):
                char = int(char)
            stack.append(char)

    return stack[0]


def read_numbers(path):
    return [SnailfishNumber(parse(line), None, 1) for line in open(path).readlines()]


def add(snailfish_1, snailfish_2):
    """Add two SnailfishNumber numbers"""
    result_list = [snailfish_1.get_number(), snailfish_2.get_number()]
    result = SnailfishNumber(result_list, None, 1)
    result.reduce_number()
    return result


def puzzle1():
    numbers = read_numbers("./Day 18/Day_18_input.txt")
    result = functools.reduce(add, numbers)
    print("Puzzle 1: magnitude =", result.magnitude())


def puzzle2():
    numbers = read_numbers("./Day 18/Day_18_input.txt")

    max_magnitude = 0
    for i, number1 in enumerate(numbers):
        for j, number2 in enumerate(numbers):
            if i != j:
                result = add(number1, number2)
                max_magnitude = max(max_magnitude, result.magnitude())

    print("Puzzle 2: max magnitude =", max_magnitude)


puzzle1()
puzzle2()
