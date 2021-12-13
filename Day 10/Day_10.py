def read_data(path):
    return open(path).read().strip().split("\n")

def puzzles():
    data = read_data("./Day 10/Day_10_input.txt")

    open_close_symbols = {"(" : ")",
                          "[" : "]",
                          "{" : "}",
                          "<" : ">"}

    syntax_scores = {")" : 3,
                     "]" : 57,
                     "}" : 1197,
                     ">" : 25137}

    autocomplete_scores = {")" : 1,
                           "]" : 2,
                           "}" : 3,
                           ">" : 4}

    final_syntax_score = 0
    final_autocomplete_scores = []
    for line in data:
        stack = []
        for symbol in line:
            if symbol in open_close_symbols:
                # opening symbol
                stack.append(symbol)
            else:
                # closing symbol
                stacked_symbol = stack.pop()
                if open_close_symbols[stacked_symbol] != symbol:
                    # corrupted line
                    final_syntax_score += syntax_scores[symbol]
                    break
        else:
            # complete the line
            autocomplete_score = 0
            while stack:
                stacked_symbol = stack.pop()
                autocomplete_score *= 5
                autocomplete_score += autocomplete_scores[open_close_symbols[stacked_symbol]]

            final_autocomplete_scores.append(autocomplete_score)

    final_autocomplete_scores.sort()

    print("Puzzle 1:", final_syntax_score)
    print("Puzzle 2:", final_autocomplete_scores[len(final_autocomplete_scores) // 2])

puzzles()
