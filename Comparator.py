import sys

from matplotlib import pyplot


# Read all the lines and add them to the dictionary {read_name, read_pos}
def parse_sam(fh):
    alignments = {}
    for ln in fh:
        if ln[0] == '@':
            # Info lines produced by BWA, skip them
            continue

        parts = ln.split()
        read_name = parts[0]
        read_pos = parts[3]
        alignments[read_name] = int(read_pos)

    return alignments


class Comparator:
    read_length = 85

    def __init__(self, ref_file_name, compared_file_name):
        self.ref_file_name = ref_file_name
        self.compared_file_name = compared_file_name

    def compare(self):
        try:
            file_ref = open(self.ref_file_name, "r")
            file_compared = open(self.compared_file_name, "r")
        except FileNotFoundError:
            print("The file {} is missing :( Exiting..".format(self.compared_file_name))
            sys.exit()

        ref_alignments = parse_sam(file_ref)
        compared_alignments = parse_sam(file_compared)

        large_dif_count = 0
        diffs = []
        for read_name, pos in compared_alignments.items():
            ref_pos = ref_alignments.get(read_name)
            diffs.append(ref_pos - pos)
            if abs(ref_pos - pos) > 1:
                large_dif_count += 1

        print("There were {}% differences in more than one alignment position."
              .format(100.0 * large_dif_count / len(diffs)))

        pyplot.plot(diffs)
        pyplot.legend()
        pyplot.show()
