class Board:

    def __init__(self, size):
        self._numbers = [[None] * size for _ in range(size)]

    def add_number(self, row, col, number):
        self._numbers[row][col] = number

    def mark(self, row, col):
        self._numbers[row][col] = None

    def bingo(self, row, col):
        # Check if there is bingo in the given row or column
        # A marked position has None value
        row = self._numbers[row]
        column = [self._numbers[r][col] for r in range(len(self._numbers))]
        return all(x is None for x in row) or all(x is None for x in column)

    def score(self):
        return sum([value for row in self._numbers for value in row if value is not None])

class BoardManager:

    def __init__(self):
        self._boards = []
        self._number_appearance = {}

    def add_board(self, values):
        board = Board(5)
        board_id = len(self._boards)

        for row, row_data in enumerate(values):
            for col, number in enumerate(row_data):
                board.add_number(row, col, number)

                if not number in self._number_appearance:
                    self._number_appearance[number] = []

                self._number_appearance[number].append((board_id, row, col))

        self._boards.append(board)

    def mark(self, number):
        # Mark number in all boards
        # Return all the wining boards and remove them
        winning_boards = []
        if number in self._number_appearance:
            for board_id, row, col in self._number_appearance[number]:
                if self._boards[board_id] is not None:
                    self._boards[board_id].mark(row, col)
                    if self._boards[board_id].bingo(row, col):
                        winning_boards.append(self._boards[board_id])
                        self._boards[board_id] = None
        return winning_boards

def read_data(draw_numbers, board_man):
    with open("./Day 04/Day_04_input.txt", "r") as file:
        lines = file.readlines()
        values = []

        for line_num, line in enumerate(lines):
            if line_num == 0:
                for val in line.split(","):
                    draw_numbers.append(int(val))
            else:
                line = line.rstrip()
                if line == "":
                    if len(values) > 0:
                        board_man.add_board(values)
                    values.clear()
                else:
                    values.append(list(map(int, line.split())))

def puzzle1():
    draw_numbers = []
    board_man = BoardManager()
    read_data(draw_numbers, board_man)

    for num in draw_numbers:
        winning_boards = board_man.mark(num)
        if len(winning_boards) > 0:
            # Bingo!!
            final_score = winning_boards[0].score() * num
            print(final_score)
            break

def puzzle2():
    draw_numbers = []
    board_man = BoardManager()
    read_data(draw_numbers, board_man)

    for number in draw_numbers:
        winning_boards = board_man.mark(number)
        if len(winning_boards) > 0:
            # Bingo!!
            final_score = winning_boards[-1].score() * number
            print(final_score)

puzzle1()
puzzle2()
