import copy
import heapq
import timeit


class State:
    """Represents a game state"""

    AMPHIPODS = ["A", "B", "C", "D"]
    COSTS = {"A": 1, "B": 10, "C": 100, "D": 1000}
    END_ROOMS = {"A": 2, "B": 4, "C": 6, "D": 8}
    SOLUTION = [
        [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
        ["#", "#", "A", "#", "B", "#", "C", "#", "D", "#", "#"],
        ["#", "#", "A", "#", "B", "#", "C", "#", "D", "#", "#"],
    ]

    def __init__(self, board, g=0, parent=None):
        self.board = board
        self.g = g
        self.parent = parent
        self.h = self.calc_h_cost()

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __lt__(self, other):
        return self.f_cost() < other.f_cost()

    def __hash__(self):
        return hash(str(self.board))

    def __str__(self):
        string = ""
        for row in self.board:
            string += "".join(row) + "\n"
        return string

    def print_path(self):
        path = []
        aux = self
        while aux is not None:
            path.append(aux)
            aux = aux.parent

        path.reverse()
        for state in path:
            print(state)

    def g_cost(self):
        """Return actual cost"""
        return self.g

    def h_cost(self):
        """Return the remaining moves cost"""
        return self.h

    def calc_h_cost(self):
        cost = 0
        for row in range(3):
            for col in range(11):
                cell = self.board[row][col]
                if cell in State.AMPHIPODS:
                    if col != State.END_ROOMS[cell]:
                        cost += State.COSTS[cell] * (
                            row + abs(col - State.END_ROOMS[cell]) + row
                        )
        return cost

    def f_cost(self):
        """Return total cost"""
        return self.g_cost() + self.h_cost()

    def is_solution(self):
        for row in range(3):
            for col in range(11):
                if self.board[row][col] != State.SOLUTION[row][col]:
                    return False

        return True

    def get_neighbours(self):
        neighbours = []

        for amphipod in self.find_amphipods():
            moves = []
            pod = amphipod[0]
            row, col = amphipod[1]
            if col == State.END_ROOMS[pod]:
                # in my room
                if row == 2:
                    continue
                elif row == 1:
                    if self.board[2][col] != pod:
                        # it has to leave
                        moves.extend(self.exit_room(pod, (row, col)))
            elif row == 0:
                # in hallway
                move_to_my_room = self.to_my_room(pod, (row, col))
                if move_to_my_room is not None:
                    moves.append(move_to_my_room)
            else:
                # in other room
                for r in range(0, row):
                    if self.board[r][col] != ".":
                        break
                else:
                    move_to_my_room = self.to_my_room(pod, (row, col))
                    if move_to_my_room is not None:
                        moves.append(move_to_my_room)
                    else:
                        moves.extend(self.exit_room(pod, (row, col)))

            for move in moves:
                new_row, new_col = move
                new_board = copy.deepcopy(self.board)
                new_board[row][col] = "."
                new_board[new_row][new_col] = pod
                g = State.COSTS[pod] * (row + abs(col - new_col) + new_row) + self.g
                new_state = State(new_board, g, self)
                neighbours.append(new_state)

        return neighbours

    def to_my_room(self, amphipod, pos):
        col = pos[1]
        col_target = State.END_ROOMS[amphipod]
        r = (
            range(col + 1, col_target + 1)
            if col < col_target
            else range(col - 1, col_target - 1, -1)
        )
        for c in r:
            if self.board[0][c] != ".":
                break
        else:
            if self.board[2][col_target] == ".":
                return (2, col_target)
            elif (
                self.board[2][col_target] == amphipod
                and self.board[1][col_target] == "."
            ):
                return (1, col_target)

        return None

    def exit_room(self, amphipod, pos):
        moves = []

        col = pos[1]
        for c in range(col, 11):
            if self.board[0][c] != ".":
                break
            elif c not in [2, 4, 6, 8]:
                moves.append((0, c))

        for c in range(col, -1, -1):
            if self.board[0][c] != ".":
                break
            elif c not in [2, 4, 6, 8]:
                moves.append((0, c))

        return moves

    def find_amphipods(self):
        amphipods = []
        for row in range(3):
            for col in range(11):
                cell = self.board[row][col]
                if cell in State.AMPHIPODS:
                    amphipods.append((cell, (row, col)))

        return amphipods


def a_star(initial_state):
    open_nodes = [initial_state]
    visited_nodes = {initial_state: 0}

    while True:
        current = heapq.heappop(open_nodes)

        if current.is_solution():
            print("Cost =", current.f_cost())
            # current.print_path()
            break

        for neighbour in current.get_neighbours():
            if neighbour not in visited_nodes or visited_nodes[neighbour] > neighbour.g:
                visited_nodes[neighbour] = neighbour.g
                heapq.heappush(open_nodes, neighbour)


def puzzle1():
    initial = [
        [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
        ["#", "#", "D", "#", "A", "#", "D", "#", "C", "#", "#"],
        ["#", "#", "C", "#", "A", "#", "B", "#", "B", "#", "#"],
    ]

    state1 = State(initial)
    a_star(state1)


print(timeit.timeit(puzzle1, number=1))
