#!/usr/bin/python

### This script takes the comma-separated output table of a binning tool ["contigname,binname", e.g. concoct (https://github.com/BinPro/CONCOCT, http://www.nature.com/nmeth/journal/v11/n11/full/nmeth.3103.html)] and and the binned assembly fasta and creates a fasta file and a list of contigs for each bin.
### clusterfile is the comma-separated binning output table
### contigfasta is the assembly fasta that was used for binning
### beate.slaby@uni-wuerzburg.de

import sys, os
from Bio import SeqIO

# input files:

def usage():
    print "Usage: mkBinFasta.py clusterfile contigfasta"
    print "clusterfile: a comma-separated binning output table ('contigname,binname')"
    print "contigfasta: the assembly fasta that was used for binning"

if len(sys.argv) != 3:
    usage()
    exit()

with open(sys.argv[1], "rU") as clusterfile, open(sys.argv[2], "rU") as contigfasta:
    clusters = clusterfile.read().splitlines()

### bindict is a dictionary containing a list of contigs for each bin
    bindict = {}
    for cluster in clusters:
        thebin = cluster.split(",")[1]
        thecontig = cluster.split(",")[0]
        if bindict.has_key(thebin):
            contiglist = bindict[thebin]
            contiglist.append(thecontig)
        else:
            contiglist = list(thecontig)
        bindict[thebin] = contiglist

### for each bin in the dictionary, we loop through the sequences in contigfasta and add the sequence to the output file, if it belongs to the bin
    records = list(SeqIO.parse(contigfasta, "fasta"))
    for thebin in bindict:
        contiglist = bindict[thebin]
        seqlist = []
        for seq in records:
            if seq.name in contiglist:
                seqlist.append(seq)
        with open("bin" + thebin + ".fasta", "w") as outfile:
            SeqIO.write(seqlist, outfile, "fasta")
