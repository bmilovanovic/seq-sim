import random

name_format = "@ETF-SEQ-SIM:13M111GI:2018:3255:17:{}"
fq_format = "{} BWA-MEM-FORMAT:{}:{}/{}\n"
sam_format = "{} FLAG	SEQUENCE_NAME	{}	{}  CIGAR	{}	{}	{}	{} BWA_PARAMS\n"


class Read:
    read_index = 0

    def __init__(self, nucleotides, quality):
        self.nucleotides = nucleotides
        self.quality = quality
        self.x = random.randint(0, 32000)
        self.y = random.randint(0, 32000)
        self.name = name_format.format(Read.read_index)

    def write_to_fq(self, file, file_index):
        file.write(fq_format.format(self.name, self.x, self.y, file_index))
        file.write("{}\n".format(self.nucleotides))
        file.write("+\n")
        file.write("{}\n".format(self.quality))

    def write_to_sam(self, file, pos, avg_quality, mate_pos, mate_distance):
        file.write(sam_format
                   .format(self.name, pos, avg_quality, mate_pos, mate_distance, self.nucleotides, self.quality))
