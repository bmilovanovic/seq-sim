import numpy
from matplotlib import pyplot as plt
from scipy import stats


class Comparator:
    read_length = 85

    def __init__(self, ref_file_name, compared_file_name):
        self.ref_file_name = ref_file_name
        self.compared_file_name = compared_file_name

    def compare(self):
        file_ref = open(self.ref_file_name, "r")
        file_compared = open(self.compared_file_name, "r")

        # Sample from a normal distribution using numpy's random number generator
        samples = numpy.random.normal(size=10000)

        # Compute a histogram of the sample
        bins = numpy.linspace(-5, 5, 30)
        histogram, bins = numpy.histogram(samples, bins=bins, normed=True)

        bin_centers = 0.5 * (bins[1:] + bins[:-1])

        # Compute the PDF on the bin centers from scipy distribution object
        pdf = stats.norm.pdf(bin_centers)
        plt.figure(figsize=(6, 4))
        plt.plot(bin_centers, histogram, label="Histogram of samples")
        plt.plot(bin_centers, pdf, label="PDF")
        plt.legend()
        plt.show()
