# scripts
A collection of free-to-use scripts

# avgcov_from_samtoolsout.py
This script takes the output of samtools depth of a mapping of reads to an assembly and calculates the mean coverage for each contig.
samtoolsout is the output of samtools depth

# mkBinFasta.py
This script takes the comma-separated output table of a binning tool ["contigname,binname", e.g. concoct (https://github.com/BinPro/CONCOCT, http://www.nature.com/nmeth/journal/v11/n11/full/nmeth.3103.html)] and the binned assembly fasta and creates a fasta file and a list of contigs for each bin.
clusterfile is the comma-separated binning output table, contigfasta is the assembly fasta that was used for binning

# bingenomecov_covfile.py
This script takes the comma-separated output table of a binning tool ["contigname,binname", e.g. concoct (https://github.com/BinPro/CONCOCT, http://www.nature.com/nmeth/journal/v11/n11/full/nmeth.3103.html)] and the tab-separated coverage table used for this binning and calculates the mean genome/bin coverage for each bin.

# merge_contigs_concoctclustering.py
The binning software CONCOCT suggests to split large contigs (>20 000 bp) into sub-contigs of 10 000 bp with a script that they provide with the program to give long contigs more weight. After binning and before creating fasta files for each bin, I prefer to merge these sub-contigs again. This script assigns the contigs that were split for binning to a bin based on the placement of the majority of the respective sub-contigs. It was written for SPAdes and IDBA-UD assemblies and may need adjustments for other contig naming systems.
