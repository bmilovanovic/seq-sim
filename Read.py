import random


class Read:
    def __init__(self, genome, avg_quality, coverage):
        self.genome = genome
        self.avg_quality = avg_quality
        self.coverage = coverage
        self.session_name = "ETF-SEQ-SIM"
        self.x = random.randint(0, len(genome))
        self.y = random.randint(0, len(genome))

    def write_to_file(self, file, file_index):
        file.write("@{}:13M111GI:2018:3255:17:{}:{} {}:N:0:1\n".format(self.session_name, self.x, self.y, file_index))
        file.write("CNTTTTTTACTTTTTTTCCAATCAAGGTACATTCANGATCCTAATAAAATTCCANNAACACTGGACANTGATACNA\n")
        file.write("+\n")
        file.write("@#==>DA?CDHGHHHHHEHGGGGGFFHFHGDCDCA#@CCBBBB@BGFGGG;795##:011?@??@###########\n")
