from functools import reduce


class Packet:
    def __init__(self, v, t):
        self.version = v
        self.type = t
        self.literal = None
        self.packet_children = []

    def set_literal(self, value):
        self.literal = value

    def add_child_packet(self, packet):
        self.packet_children.append(packet)

    def sum_versions(self):
        return self.version + sum(c.sum_versions() for c in self.packet_children)

    def value(self):
        if self.type == 0:
            # sum
            return sum((c.value() for c in self.packet_children))
        elif self.type == 1:
            # product
            return reduce(lambda x, y: x * y, (c.value() for c in self.packet_children))
        elif self.type == 2:
            # minimum
            return min(c.value() for c in self.packet_children)
        elif self.type == 3:
            # maximum
            return max(c.value() for c in self.packet_children)
        elif self.type == 4:
            return self.literal
        elif self.type == 5:
            # greather than
            return (
                1
                if self.packet_children[0].value() > self.packet_children[1].value()
                else 0
            )
        elif self.type == 6:
            # less than
            return (
                1
                if self.packet_children[0].value() < self.packet_children[1].value()
                else 0
            )
        elif self.type == 7:
            # equal to
            return (
                1
                if self.packet_children[0].value() == self.packet_children[1].value()
                else 0
            )


def get_ver(chain, idx):
    version = chain[idx : idx + 3]
    return (int(version, 2), idx + 3)


def get_type(chain, idx):
    type = chain[idx : idx + 3]
    return (int(type, 2), idx + 3)


def get_type_pack_id(chain, idx):
    type_id = chain[idx : idx + 1]
    return (int(type_id, 2), idx + 1)


def get_literal(chain, idx):
    literal = ""
    while True:
        digit = chain[idx : idx + 5]
        idx += 5
        literal += digit[1:]
        if digit[0] == "0":
            break
    return (int(literal, 2), idx)


def get_length_subpackets_bits(chain, idx):
    lenght = chain[idx : idx + 15]
    return (int(lenght, 2), idx + 15)


def get_number_subpackets(chain, idx):
    lenght = chain[idx : idx + 11]
    return (int(lenght, 2), idx + 11)


def decode_packet(chain, idx):
    version, idx = get_ver(chain, idx)
    type, idx = get_type(chain, idx)

    packet = Packet(version, type)

    if type != 4:
        type_id, idx = get_type_pack_id(chain, idx)
        if type_id == 0:
            length, idx = get_length_subpackets_bits(chain, idx)
            children_packets, idx = decode_subpackets_length_in_bits(chain, idx, length)
            for child in children_packets:
                packet.add_child_packet(child)
        else:
            number, idx = get_number_subpackets(chain, idx)
            children_packets, idx = decode_subpackets_num_of_packets(chain, idx, number)
            for child in children_packets:
                packet.add_child_packet(child)
    else:
        literal, idx = get_literal(chain, idx)
        packet.set_literal(literal)

    return (packet, idx)


def decode_subpackets_length_in_bits(chain, idx, length):
    packets = []
    bits = 0
    while bits < length:
        prev_idx = idx
        packet, idx = decode_packet(chain, idx)
        packets.append(packet)
        bits += idx - prev_idx
    return (packets, idx)


def decode_subpackets_num_of_packets(chain, idx, number):
    packets = []
    while len(packets) < number:
        packet, idx = decode_packet(chain, idx)
        packets.append(packet)
    return (packets, idx)


def puzzle1():
    hex = open("./Day 16/Day_16_input.txt").readline().rstrip("\n")
    bin = ""
    for h in hex:
        j = int(h, 16)
        bin += format(j, "0>4b")

    root_packet, _ = decode_packet(bin, 0)
    print("Puzzle 1:", root_packet.sum_versions())


def puzzle2():
    hex = open("./Day 16/Day_16_input.txt").readline().rstrip("\n")
    bin = ""
    for h in hex:
        j = int(h, 16)
        bin += format(j, "0>4b")

    root_packet, _ = decode_packet(bin, 0)
    print("Puzzle 2:", root_packet.value())


puzzle1()
puzzle2()
