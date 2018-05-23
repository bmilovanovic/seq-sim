from Sequencer import Sequencer
from Comparator import Comparator

if __name__ == '__main__':
    print("______________________________________________________________________________")
    print("Hello. I'm a SeqSim from School of Electrical Engineering in Belgrade, Serbia.")
    print("I can create Illumina paired-end reads for you.")
    print("To do that, I need some help.\n")

    # source_genome = input("What is the name of the source genomic sequence file? ")
    #
    # print("What is the average quality of the nucleotides?")
    # while True:
    #     try:
    #         avg_quality = int(input())
    #         if avg_quality < Sequencer.quality_min or avg_quality > Sequencer.quality_max:
    #             raise ValueError()
    #         break
    #     except ValueError:
    #         print("Error in input. I need integer value from {} to {}. Try again..."
    #               .format(Sequencer.quality_min, Sequencer.quality_max))
    #
    # print("What coverage do you want?")
    # while True:
    #     try:
    #         coverage = float(input())
    #         if coverage < 0 or coverage > 2:
    #             raise ValueError()
    #         break
    #     except ValueError:
    #         print("Error in input. I need real value from 0 to 2. Try again...")
    #
    # print("Started sequencing with the average nucleotide quality of {} and the coverage of {}."
    #       .format(avg_quality, coverage))
    #
    # my_sequencer = Sequencer(source_genome, avg_quality, coverage)
    # my_sequencer.simulate()
    #
    # print("The reads are ready! Check your folder...")
    #
    print("Do you want to compare produced alignment file with some other? y/n")
    while True:
        try:
            compare_alignments = input()
            if compare_alignments != 'y' and compare_alignments != 'n':
                raise ValueError()
            break
        except ValueError:
            print("Error in input. I need 'y' or 'n'. Try again...")

    if compare_alignments == 'y':
        compared_file_name = input("Can you write me that filename? ")
        my_comparator = Comparator(Sequencer.alignment_file_name, compared_file_name)
        my_comparator.compare()

    print("That's all folks! Go and bring the light to the people.")
