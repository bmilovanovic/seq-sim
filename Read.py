import random


class Read:
    def __init__(self, nucleotides, quality):
        self.nucleotides = nucleotides
        self.quality = quality
        self.x = random.randint(0, 32000)
        self.y = random.randint(0, 32000)

    def write_to_file(self, file, file_index):
        file.write("@ETF-SEQ-SIM:13M111GI:2018:3255:17:{}:{} {}:N:0:1\n".format(self.x, self.y, file_index))
        file.write("{}\n".format(self.nucleotides))
        file.write("+\n")
        file.write("{}\n".format(self.quality))
