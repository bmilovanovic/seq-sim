import random
from Read import Read

max_iterations_for_quality = 3
qual_chars = "!\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~"


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


def find_closest_char(target_val, max_val, min_val):
    if chr(target_val) in qual_chars:
        return target_val
    for i in range(1, max(max_val - target_val, target_val - min_val)):
        if target_val - i > 0 and chr(target_val - i) in qual_chars:
            return target_val - i
        if chr(target_val + i) in qual_chars:
            return target_val + 1
    else:
        raise ValueError("Error in quality assurance. There must be some char in qual_chars! {}".format(target_val))


def create_random_qualities(arr_length, target_mean_val, min_val, max_val):
    array = [ord(random.choice(qual_chars)) for _ in range(arr_length)]
    for _ in range(0, max_iterations_for_quality):
        mean_val = sum(array) / len(array)
        print(mean_val)
        target_difference = target_mean_val - mean_val
        if int(mean_val) == target_mean_val:
            break
        for x in array:
            target_x = x + target_difference
            if target_x < min_val:
                target_x = min_val
            elif target_x > max_val:
                target_x = max_val
            elif chr(int(target_x)) not in qual_chars:
                target_x = find_closest_char(int(target_x), max_val, min_val)

            if chr(int(target_x)) not in qual_chars:
                raise ValueError(
                    "Error in quality assurance. There must be some char in qual_chars! {}".format(target_x))
            array[array.index(x)] = target_x
    return array


class Sequencer:
    read_length = 85
    quality_max = ord('~')
    quality_min = ord('#')

    def __init__(self, src_file_name, avg_quality, coverage):
        self.src_file_name = src_file_name
        self.avg_quality = avg_quality
        self.coverage = coverage
        self.reads_num = 5

    def create_read(self, genome):
        random_gene = random.choice(list(genome.values()))
        pos = random.randint(0, len(random_gene) - self.read_length - 1)
        nucleotides = random_gene[pos:pos + self.read_length]

        qualities = create_random_qualities(self.read_length, self.avg_quality,
                                            self.quality_min, self.quality_max)

        print(qualities)
        qualities_str = ''.join([chr(int(x)) for x in qualities])
        return Read(nucleotides, qualities_str)

    # GCF_000766835.1_Aquila_chrysaetos-1.0.2_cds_from_genomic.fa
    def simulate(self):
        file_src = open(self.src_file_name, "r")
        file_out1 = open("read1.fastq", "w")
        file_out2 = open("read2.fastq", "w")

        genome = parse_fasta(file_src)
        print("There are {} nucleotides in the source genome.".format(len(genome)))

        # Just write out the hardcoded files for now
        for i in range(0, self.reads_num):
            read = self.create_read(genome)
            read.write_to_file(file_out1, 1)
            read.write_to_file(file_out2, 2)

        file_src.close()
        file_out1.close()
        file_out2.close()
