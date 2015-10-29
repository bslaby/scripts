#!/usr/bin/python

### This script takes the output of samtools depth of a mapping of reads to an assembly and calculates the mean coverage for each contig.
### samtoolsout is the output of samtools depth
### beate.slaby@uni-wuerzburg.de

import sys, os, csv

def usage():
    print "Usage: avgcov_from_samtoolsout.py samtoolsout with samtoolsout as the output of 'samtools depth'"

if len(sys.argv) != 2:
    usage()
    exit()

with open(sys.argv[1], "rU") as samtoolsout:

### sumdict is a dictionary adding up the per-base coverages for each contig
### readcountdict is a dictionary counting the bases for each contig
    sumdict = {}
    readcountdict = {}
    for line in samtoolsout:
        contigname, _, coverage = line.split('\t', 3)      
        sumdict[contigname] = sumdict.get(contigname, 0) + int(coverage)
        readcountdict[contigname] = readcountdict.get(contigname, 0) + 1
        
### looping through the contigs in sumdict, the mean coverage per contig is calculated and written to standard output
    with open("coveragefile.csv", "wb") as csvfile:
        fp = csv.writer(csvfile, delimiter="\t")
        fp.writerow(["contig","mean.coverage"])
        for contig in sumdict:
            if readcountdict[contig] != 0:
                thevalue = float(sumdict[contig])/float(readcountdict[contig])
                fp.writerow([contig,thevalue])
