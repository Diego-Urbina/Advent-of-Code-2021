from collections import defaultdict


def get_player_positions(path):
    with open(path) as file:
        lines = file.read().split("\n")
        return int(lines[0][-1]) - 1, int(lines[1][-1]) - 1


def get_deterministic_die():
    """Generate an infinite sequence from 1 to 100"""
    value = 0
    while True:
        yield (value % 100) + 1
        value += 1


def get_dirac_die_values():
    return [(3, 1), (4, 3), (5, 6), (6, 7), (7, 6), (8, 3), (9, 1)]


def puzzle1(path):
    score_to_win = 1000
    p1_pos, p2_pos = get_player_positions(path)
    p1_score = 0
    p2_score = 0
    die_rolls = 0
    turn = 1

    die = get_deterministic_die()
    while True:
        rolls = (next(die), next(die), next(die))
        die_rolls += 3

        if turn == 1:
            p1_pos = (p1_pos + sum(rolls)) % 10
            p1_score += p1_pos + 1
            turn = 2
            if p1_score >= score_to_win:
                break
        else:
            p2_pos = (p2_pos + sum(rolls)) % 10
            p2_score += p2_pos + 1
            turn = 1
            if p2_score >= score_to_win:
                break

    print("Puzzle 1 =", min(p1_score, p2_score) * die_rolls)


def puzzle2(path):
    score_to_win = 21
    p1_pos, p2_pos = get_player_positions(path)
    p1_score = 0
    p2_score = 0
    turn = 1

    states = defaultdict(int)
    states[(p1_pos, p1_score, p2_pos, p2_score, turn)] = 1

    p1_wins = 0
    p2_wins = 0
    while len(states) > 0:
        new_states = defaultdict(int)
        for state, count in states.items():
            p1_pos, p1_score, p2_pos, p2_score, turn = state
            for roll in get_dirac_die_values():
                if turn == 1:
                    p1_new_pos = (p1_pos + roll[0]) % 10
                    p1_new_score = p1_score + p1_new_pos + 1
                    if p1_new_score >= score_to_win:
                        p1_wins += count * roll[1]
                    else:
                        new_state = (
                            p1_new_pos,
                            p1_new_score,
                            p2_pos,
                            p2_score,
                            2,
                        )

                        new_states[new_state] += count * roll[1]
                else:
                    p2_new_pos = (p2_pos + roll[0]) % 10
                    p2_new_score = p2_score + p2_new_pos + 1
                    if p2_new_score >= score_to_win:
                        p2_wins += count * roll[1]
                    else:
                        new_state = (
                            p1_pos,
                            p1_score,
                            p2_new_pos,
                            p2_new_score,
                            1,
                        )

                        new_states[new_state] += count * roll[1]

        states = new_states

    print("Puzzle 2 =", max(p1_wins, p2_wins))


puzzle1("./Day 21/Day_21_input.txt")
puzzle2("./Day 21/Day_21_input.txt")
