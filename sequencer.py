import random
import sys

import numpy

from Read import Read

qual_chars = "!\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~"
std_dev = 1.0
bases = ('A', 'C', 'G', 'T')


# Read all the lines. If the lines is not info/sequence name, append it to the result string.
def parse_fasta(fh):
    fa = {}
    sequence_name = None
    i = 0
    for ln in fh:
        sys.stdout.write("\r{} lines of the source genome file parsed".format(i))
        sys.stdout.flush()
        i += 1
        if ln[0] == '>':
            # new name line; remember current sequence's short name
            sequence_row = ln[1:].rstrip()
            sequence_name = sequence_row.split()[0]
            fa[sequence_name] = []
        else:
            # append nucleotides to the current sequence
            fa[sequence_name].append(ln.rstrip())
    print("\n")
    # Join lists into strings
    for short_name, nuc_list in fa.items():
        # join this sequence's lines into one long string
        fa[short_name] = ''.join(nuc_list)
    return ''.join(fa.values()).upper()


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


def apply_errors(sequence):
    sequence_size = len(sequence)
    for i in range(0, sequence_size):
        if random.random() <= Sequencer.error_rate_snip:
            bases_without_one = list(bases)
            if sequence[i] in bases_without_one:
                bases_without_one.remove(sequence[i])
            sequence = sequence[:i] + random.choice(bases_without_one) + sequence[i + 1:]
            continue
        if random.random() <= Sequencer.error_rate_deletion:
            sequence = sequence[:i] + sequence[i + 1:] + random.choice(bases)
            continue
        if random.random() <= Sequencer.error_rate_insertion:
            sequence = sequence[:i] + random.choice(bases) + sequence[i:sequence_size - 1]
            continue
    return sequence


def create_qualities(arr_length, target_mean_val, min_val, max_val):
    qual_ints = numpy.random.normal(target_mean_val, std_dev, arr_length)
    qualities = ''.join(chr(find_closest_char(int(e), max_val, min_val)) for e in qual_ints)

    return qualities


def reverse_complement(s):
    complement = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A', 'N': 'N'}
    t = ''
    for base in s:
        t = complement[base] + t
    return t


class Sequencer:
    read_length = 85
    insert_size = 270
    error_rate_snip = 0.005
    error_rate_deletion = 0.003
    error_rate_insertion = 0.001
    quality_max = ord('~')
    quality_min = ord('#')
    reads_1_file_name = "read1.fastq"
    reads_2_file_name = "read2.fastq"
    alignment_file_name = "alignment.sam"

    def __init__(self, src_file_name, avg_quality, coverage):
        self.src_file_name = src_file_name
        self.avg_quality = avg_quality
        self.coverage = coverage

    def create_read(self, dna_seq):
        nucleotides = apply_errors(dna_seq)
        qualities = create_qualities(self.read_length, self.avg_quality,
                                     self.quality_min, self.quality_max)

        return Read(nucleotides, qualities)

    def simulate(self):
        try:
            file_src = open(self.src_file_name, "r")
        except FileNotFoundError:
            print("The file {} is missing :( Exiting..".format(self.src_file_name))
            sys.exit()

        genome = parse_fasta(file_src)
        genome_size = len(genome)

        file_fq1 = open(self.reads_1_file_name, "w")
        file_fq2 = open(self.reads_2_file_name, "w")
        file_sam = open(self.alignment_file_name, "w")

        # Generate the reads and write out the files
        reads_num = int(self.coverage * genome_size / self.read_length)
        print("There are {} nucleotides in the source genome.".format(genome_size))
        print("{} reads with the length of {} should be generated to match the coverage of {}."
              .format(reads_num, self.read_length, self.coverage))
        for i in range(0, reads_num):
            sys.stdout.write("\r{}% reads generated".format(int((i + 1) * 100 / reads_num)))
            sys.stdout.flush()
            Read.read_index = Read.read_index + 1

            pos1 = random.randint(0, len(genome) - self.insert_size - 1)
            read1 = self.create_read(genome[pos1:pos1 + self.read_length])
            # The paired end read starts backwards from the end of the insert
            pos2 = pos1 + self.insert_size - self.read_length
            read2 = self.create_read(reverse_complement(genome[pos2:pos2 + self.read_length]))

            read1.write_to_fq(file_fq1, 1)
            read1.write_to_sam(file_sam, pos1 + 1, self.avg_quality, pos2 + 1, self.insert_size)
            read2.write_to_fq(file_fq2, 2)
            read2.write_to_sam(file_sam, pos2 + 1, self.avg_quality, pos1 + 1, -self.insert_size)
        print("\n")

        file_src.close()
        file_fq1.close()
        file_fq2.close()
        file_sam.close()
