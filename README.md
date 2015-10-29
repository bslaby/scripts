# scripts
A collection of free-to-use scripts

# avgcov_from_samtoolsout.py
This script takes the output of samtools depth of a mapping of reads to an assembly and calculates the mean coverage for each contig.
samtoolsout is the output of samtools depth

# mkBinFasta.py
This script takes the comma-separated output table of a binning tool ["contigname,binname", e.g. concoct (https://github.com/BinPro/CONCOCT, http://www.nature.com/nmeth/journal/v11/n11/full/nmeth.3103.html)] and and the binned assembly fasta and creates a fasta file and a list of contigs for each bin.
clusterfile is the comma-separated binning output table
contigfasta is the assembly fasta that was used for binning
