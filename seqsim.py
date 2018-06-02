"""
Illumina paired-end sequencing simulator.

Usage:
  seqsim.py seq <reference> [--quality=<qual>] [--coverage=<cov>]
  seqsim.py cmp <aln_trgt> [--aln_src=<src>]
  seqsim.py -h | --help

 Options:
   -h --help            Show this message.
   --coverage=<cov>     Coverage of the referent genome [default: 1].
   --quality=<qual>     Mean quality of the nucleotides [default: 60].
   --aln_src=<src>      Source alignment file [default: alignment.sam].
"""

from docopt import docopt

from comparator import Comparator
from sequencer import Sequencer

if __name__ == '__main__':

    argv = docopt(__doc__)

    if argv['seq']:
        source_genome = argv['<reference>']

        avg_quality = int(argv['--quality'])
        if avg_quality < Sequencer.quality_min or avg_quality > Sequencer.quality_max:
            raise ValueError("Average quality of nucleotides must be from {} to {}. Try again..."
                             .format(Sequencer.quality_min, Sequencer.quality_max))

        coverage = float(argv['--coverage'])
        if coverage < 0 or coverage > 2:
            raise ValueError("Coverage must be real value from 0 to 2.")

        print("Started sequencing with the average nucleotide quality of {} and the coverage of {}."
              .format(avg_quality, coverage))

        my_sequencer = Sequencer(source_genome, avg_quality, coverage)
        my_sequencer.simulate()

        print("The reads are ready! Check your folder...")
    elif argv['cmp']:
        my_comparator = Comparator(argv['--aln_src'], argv['<aln_trgt>'], )
        my_comparator.compare()
