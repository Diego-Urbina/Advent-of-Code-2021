def puzzle(path, func):
    def get_program(path):
        with open(path) as file:
            return [line.rstrip("\n").split(" ") for line in file.readlines()]

    def get_operands(state, op1, op2):
        op1 = state["wxyz".index(op1)]
        op2 = state["wxyz".index(op2)] if str.isalpha(op2) else int(op2)
        return op1, op2

    def add_new_state(new_state, new_model_number):
        new_state = tuple(new_state)
        if new_state in new_states:
            new_states[new_state] = func(new_states[new_state], new_model_number)
        else:
            new_states[new_state] = new_model_number

    states = {(0, 0, 0, 0): 0}
    for sentence in get_program(path):
        new_states = {}

        for state, model_number in states.items():
            cmd = sentence[0]
            new_state = [state[0], state[1], state[2], state[3]]
            if cmd == "inp":
                # create new states
                for i in range(1, 10):
                    new_model_number = model_number * 10 + i
                    new_state = [i, state[1], state[2], state[3]]
                    add_new_state(new_state, new_model_number)
            elif cmd == "add":
                op1, op2 = get_operands(new_state, sentence[1], sentence[2])
                new_state["wxyz".index(sentence[1])] = op1 + op2
                add_new_state(new_state, model_number)
            elif cmd == "mul":
                op1, op2 = get_operands(new_state, sentence[1], sentence[2])
                new_state["wxyz".index(sentence[1])] = op1 * op2
                add_new_state(new_state, model_number)
            elif cmd == "div":
                op1, op2 = get_operands(new_state, sentence[1], sentence[2])
                new_state["wxyz".index(sentence[1])] = op1 // op2
                add_new_state(new_state, model_number)
            elif cmd == "mod":
                op1, op2 = get_operands(new_state, sentence[1], sentence[2])
                new_state["wxyz".index(sentence[1])] = op1 % op2
                add_new_state(new_state, model_number)
            elif cmd == "eql":
                op1, op2 = get_operands(new_state, sentence[1], sentence[2])
                new_state["wxyz".index(sentence[1])] = int(op1 == op2)
                add_new_state(new_state, model_number)

        states = new_states

    print(func(map(states.get, filter(lambda x: x[3] == 0, states))))


# search largest model number
puzzle("./Day 24/Day_24_input.txt", max)

# search smallest model number
puzzle("./Day 24/Day_24_input.txt", min)

# Minimum: 18113181571611
# Maximum: 99429795993929
