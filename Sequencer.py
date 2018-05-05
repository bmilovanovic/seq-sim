from Read import Read


def parse_fasta(fh):
    fa = {}
    current_short_name = None
    # Part 1: compile list of lines per sequence
    for ln in fh:
        if ln[0] == '>':
            # new name line; remember current sequence's short name
            long_name = ln[1:].rstrip()
            current_short_name = long_name.split()[0]
            fa[current_short_name] = []
        else:
            # append nucleotides to current sequence
            fa[current_short_name].append(ln.rstrip())
    # Part 2: join lists into strings
    for short_name, nuc_list in fa.items():
        # join this sequence's lines into one long string
        fa[short_name] = ''.join(nuc_list)
    return fa


class Sequencer:
    def __init__(self, src_file_name, avg_quality, coverage):
        self.src_file_name = src_file_name
        self.avg_quality = avg_quality
        self.coverage = coverage
        self.reads_num = 5

    def simulate(self):
        file_src = open(self.src_file_name, "r")

        file_out1 = open("read1.fastq", "w")
        file_out2 = open("read2.fastq", "w")

        genome = parse_fasta(file_src)
        print("There are {} nucleotides in the source genome.".format(len(genome)))

        # Just write out the hardcoded files for now
        for i in range(0, self.reads_num):
            read = Read(genome, self.avg_quality, self.coverage)
            read.write_to_file(file_out1, 1)
            read.write_to_file(file_out2, 2)

        file_src.close()
        file_out1.close()
        file_out2.close()
