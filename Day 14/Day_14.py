def get_data(path):
    rules = {}
    with open(path) as file:
        lines = file.readlines()
        template = lines[0].rstrip("\n")
        for i in range(2, len(lines)):
            rule = lines[i].rstrip("\n").split(" -> ")
            key = rule[0]
            values = [key[0] + rule[1], rule[1] + key[1]]
            rules[key] = values

    return (template, rules)


def break_polymer(template):
    return [template[i - 1] + template[i] for i in range(1, len(template))]


def puzzle(iterations):
    template, rules = get_data("./Day 14/Day_14_input.txt")

    rule_to_index = {}
    index_to_rule = []
    i = 0
    for rule in rules:
        rule_to_index[rule] = i
        index_to_rule.append(rule)
        i += 1

    # initial state
    encoded_polymer = [0] * len(rule_to_index)
    initial_rule = ""
    for rule in break_polymer(template):
        encoded_polymer[rule_to_index[rule]] += 1
        if not initial_rule:
            initial_rule = rule

    # iterations
    for _ in range(iterations):
        aux = [0] * len(encoded_polymer)
        for idx, value in enumerate(encoded_polymer):
            input_pair = index_to_rule[idx]
            for output_pair in rules[input_pair]:
                aux[rule_to_index[output_pair]] += value

        encoded_polymer = aux
        initial_rule = rules[initial_rule][0]

    # count chars
    # for each pair, only count the second char
    char_appearances = {}
    for idx, value in enumerate(encoded_polymer):
        rule = index_to_rule[idx]
        if not rule[1] in char_appearances:
            char_appearances[rule[1]] = 0
        char_appearances[rule[1]] += value

    # add the initial char
    char_appearances[initial_rule[0]] += 1

    key_max = max(char_appearances, key=char_appearances.get)
    key_min = min(char_appearances, key=char_appearances.get)
    print("After", iterations, "iterations")
    print(
        "The most common element is",
        key_max,
        "(occurring",
        char_appearances[key_max],
        "times)",
    )
    print(
        "The least common element is",
        key_min,
        "(occurring",
        char_appearances[key_min],
        "times)",
    )
    print("Answer:", char_appearances[key_max] - char_appearances[key_min], end="\n\n")


puzzle(10)
puzzle(40)
