from Sequencer import Sequencer

if __name__ == '__main__':
    print("Hello. I'm a SeqSim from School of Electrical Engineering in Belgrade, Serbia.")
    print("I can create Illumina paired-end reads for you.")
    print("To do that, I need some help.\n")

    source_genome = input("What is the name of the source genomic sequence file? ")

    print("What is the average quality of the nucleotides?")
    while True:
        try:
            avg_quality = int(input())
            if avg_quality < 0 or avg_quality > 128:
                raise ValueError()
            break
        except ValueError:
            print("Error in input. I need integer value from 0 to 128. Try again...")

    print("What coverage do you want?")
    while True:
        try:
            coverage = int(input())
            if coverage < 0 or coverage > 100:
                raise ValueError()
            break
        except ValueError:
            print("Error in input. I need integer value from 0 to 100. Try again...")

    print("Started sequencing with the average nucleotide quality of {} and the coverage of {}."
          .format(avg_quality, coverage))

    my_sequencer = Sequencer(source_genome, avg_quality, coverage)
    my_sequencer.simulate()

    input("The reads are ready! Check your folder...")
