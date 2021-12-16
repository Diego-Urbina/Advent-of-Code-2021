class Entry:
    def __init__(self, signals, outputs):
        self.signals = signals
        self.outputs = outputs
        self.segments = {}

    def num_unique_segments_outputs(self):
        """Return how many outputs have unique segments

        - Number 1 => 2 segments
        - Number 7 => 3 segments
        - Number 4 => 4 segments
        - Number 8 => 7 segments
        """
        count = 0
        for output in self.outputs:
            if (
                len(output) == 2
                or len(output) == 3
                or len(output) == 4
                or len(output) == 7
            ):
                count += 1
        return count

    def get_output_value(self):
        self.decode_segments()

        value = 0
        for output in self.outputs:
            signal = "".join(self.segments[x] for x in output)
            value = value * 10 + DigitDecoder(signal).get_value()
        return value

    def decode_segments(self):
        """Get the equivalence between segments named abcdefg
          and segments named 0123456 using de input signals

             0
          -------
        1 |  3  | 2
          -------
        4 |  6  | 5
          -------
        """
        self.segments = {}
        all_segs = {"a", "b", "c", "d", "e", "f", "g"}
        segs_num_1 = set(list(filter(lambda x: len(x) == 2, self.signals))[0])
        segs_num_7 = set(list(filter(lambda x: len(x) == 3, self.signals))[0])
        segs_num_4 = set(list(filter(lambda x: len(x) == 4, self.signals))[0])
        segs_num_8 = set(list(filter(lambda x: len(x) == 7, self.signals))[0])

        seg_0 = segs_num_7 - segs_num_1

        in_4_not_in_1 = segs_num_4 - segs_num_1

        # Get segments from numbers 0, 6 and 9
        segs_nums_069 = list(filter(lambda x: len(x) == 6, self.signals))
        # Get common segments
        common_segs_nums_069 = (
            set(segs_nums_069[0])
            .intersection(set(segs_nums_069[1]))
            .intersection(set(segs_nums_069[2]))
        )
        # Get difference segments
        diff_segs_nums_069_0 = set(segs_nums_069[0]) - common_segs_nums_069
        diff_segs_nums_069_1 = set(segs_nums_069[1]) - common_segs_nums_069
        diff_segs_nums_069_2 = set(segs_nums_069[2]) - common_segs_nums_069

        seg_3 = (
            in_4_not_in_1.intersection(diff_segs_nums_069_0)
            .union(in_4_not_in_1.intersection(diff_segs_nums_069_1))
            .union(in_4_not_in_1.intersection(diff_segs_nums_069_2))
        )
        seg_1 = in_4_not_in_1 - seg_3

        seg_2 = set()
        diff_segs_nums_069 = [
            diff_segs_nums_069_0,
            diff_segs_nums_069_1,
            diff_segs_nums_069_2,
        ]
        for aux in diff_segs_nums_069:
            if len(aux.intersection(seg_3)) > 0:
                seg_2 = aux.intersection(segs_num_1)
                if len(seg_2) > 0:
                    break

        seg_5 = segs_num_1 - seg_2

        seg_4 = set()
        diff_segs_nums_069 = [
            diff_segs_nums_069_0,
            diff_segs_nums_069_1,
            diff_segs_nums_069_2,
        ]
        for aux in diff_segs_nums_069:
            if len(aux.intersection(seg_3)) > 0:
                seg_4 = aux - seg_3 - seg_2
                if len(seg_4) > 0:
                    break

        seg_6 = all_segs - seg_0 - seg_1 - seg_2 - seg_3 - seg_4 - seg_5

        self.segments[list(seg_0)[0]] = "0"
        self.segments[list(seg_1)[0]] = "1"
        self.segments[list(seg_2)[0]] = "2"
        self.segments[list(seg_3)[0]] = "3"
        self.segments[list(seg_4)[0]] = "4"
        self.segments[list(seg_5)[0]] = "5"
        self.segments[list(seg_6)[0]] = "6"


class DigitDecoder:

    digits = {
        "012456": 0,
        "25": 1,
        "02346": 2,
        "02356": 3,
        "1235": 4,
        "01356": 5,
        "013456": 6,
        "025": 7,
        "0123456": 8,
        "012356": 9,
    }

    def __init__(self, segments):
        self._unsorted_segments = segments

    def get_value(self):
        segments = list(self._unsorted_segments)
        segments.sort()
        segments = "".join(segments)
        return DigitDecoder.digits[segments]


def get_data(path):
    entries = []
    with open(path, "r") as file:
        for line in file:
            data = line.rstrip().split("|")
            signals = data[0].strip().split(" ")
            outputs = data[1].strip().split(" ")
            entry = Entry(signals, outputs)
            entries.append(entry)
    return entries


def puzzle1():
    entries = get_data("./Day 08/Day_08_input.txt")
    print(sum([entry.num_unique_segments_outputs() for entry in entries]))


def puzzle2():
    entries = get_data("./Day 08/Day_08_input.txt")
    print(sum([entry.get_output_value() for entry in entries]))


puzzle1()
puzzle2()
