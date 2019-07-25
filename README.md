# scripts
A collection of free-to-use scripts

# avgcov_from_samtoolsout.py
This script takes the output of samtools depth of a mapping of reads to an assembly, calculates the mean coverage for each contig and merges these output files to a coverage table.

Usage: avgcov_from_samtoolsout.py depthfiles assemblyfile outdir covtable
depthfiles: a directory containing the samtools depth output files for all samples named SAMPLENAME_depth.txt
assemblyfile: the (meta)genomic assembly to which the reads were mapped
outdir: name of the output directory
covtable: name of the output coverage table

# iprannots_add_contigcoverage.py
This script takes an InterPro annotation table (tsv) and adds contig coverage information.
The coverage information is the output table of the script avgcov_from_samtoolsout.py.

Usage: iprannots_add_contigcoverage.py covtable iprannots outfile
covtable: the output table of the script avgcov_from_samtoolsout.py, first line is header
iprannots: InterPro annotation table in tsv format, first line is header
outfile: name of the output file

# mkBinFasta.py
This script takes the comma-separated output table of a binning tool ["contigname,binname", e.g. concoct (https://github.com/BinPro/CONCOCT, http://www.nature.com/nmeth/journal/v11/n11/full/nmeth.3103.html)] and the binned assembly fasta and creates a fasta file and a list of contigs for each bin.
clusterfile is the comma-separated binning output table, contigfasta is the assembly fasta that was used for binning

# bingenomecov_covfile.py
This script takes the comma-separated output table of a binning tool ["contigname,binname", e.g. concoct (https://github.com/BinPro/CONCOCT, http://www.nature.com/nmeth/journal/v11/n11/full/nmeth.3103.html)] and the tab-separated coverage table used for this binning and calculates the mean genome/bin coverage for each bin.

# merge_contigs_concoctclustering.py
The binning software CONCOCT suggests to split large contigs (>20 000 bp) into sub-contigs of 10 000 bp with a script that they provide with the program to give long contigs more weight. After binning and before creating fasta files for each bin, I prefer to merge these sub-contigs again. This script assigns the contigs that were split for binning to a bin based on the placement of the majority of the respective sub-contigs. It was written for SPAdes and IDBA-UD assemblies and may need adjustments for other contig naming systems.
