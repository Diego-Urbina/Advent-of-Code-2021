def get_most_common_bit(codes, bit):
    """ Return the most common bit
        If 0 and 1 are equally common, return 1
    """
    numbers = len(codes)
    ones = sum([int(code[bit]) for code in codes])
    zeros = numbers - ones
    return "0" if zeros > ones else "1"

def puzzle1(codes):
    len_codes = len(codes[0])
    gamma_bin = ""
    epsilon_bin = ""
    for bit in range(len_codes):
        b = get_most_common_bit(codes, bit)
        gamma_bin += b
        epsilon_bin += str(int(not int(b)))

    gamma_dec = int(gamma_bin, 2)
    epsilon_dec = int(epsilon_bin, 2)
    print("gamma: bin = " + gamma_bin + ". dec = " + str(gamma_dec))
    print("epsilon: bin = " + epsilon_bin + ". dec = " + str(epsilon_dec))

    power_consumption = gamma_dec * epsilon_dec
    print("power consumption = " + str(power_consumption))

def puzzle2(codes):
    len_codes = len(codes[0])
    oxygen_bin = codes
    co2_bin = codes
    for bit in range(len_codes):
        if len(oxygen_bin) > 1:
            b = get_most_common_bit(oxygen_bin, bit)
            oxygen_bin = list(filter(lambda n, : n[bit] != b, oxygen_bin))

        if len(co2_bin) > 1:
            b = str(int(not int(get_most_common_bit(co2_bin, bit))))
            co2_bin = list(filter(lambda n : n[bit] != b, co2_bin))

    # Flat lists
    oxygen_bin = oxygen_bin[0]
    co2_bin = co2_bin[0]

    oxygen_dec = int(oxygen_bin, 2)
    co2_dec = int(co2_bin, 2)
    print("oxygen: bin = " + oxygen_bin + ". dec = " + str(oxygen_dec))
    print("co2: bin = " + co2_bin + ". dec = " + str(co2_dec))

    life_suppport = oxygen_dec * co2_dec
    print("life suppport = " + str(life_suppport))

with open("./Day 03/Day_03_input.txt", "r") as file:
    codes = []
    for line in file:
        codes.append(line.rstrip())

puzzle1(codes)
puzzle2(codes)
