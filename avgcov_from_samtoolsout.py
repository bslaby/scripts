#!/usr/bin/python

### This script takes the output of samtools depth of a mapping of reads to an assembly and calculates the mean coverage for each contig.
### samtoolsout is the output of samtools depth
### beate.slaby@uni-wuerzburg.de

import sys, os, csv

def usage():
    print "Usage: avgcov_from_samtoolsout.py samtoolsout assemblyfile"
    print "samtoolsout is the output of 'samtools depth'"

if len(sys.argv) != 3:
    usage()
    exit()

with open(sys.argv[1], "rU") as samtoolsout, open(sys.argv[2], "rU") as assemblyfile:
    contiglist = []
    for line in assemblyfile:
        if line.startswith(">"):
            contig = line.split(">")[1].split("\n")[0]
            contiglist.append(contig)

### sumdict is a dictionary adding up the per-base coverages for each contig
### readcountdict is a dictionary counting the bases for each contig
    sumdict = {}
    readcountdict = {}
    for line in samtoolsout:
        contigname, _, coverage = line.split('\t', 3)      
        sumdict[contigname] = sumdict.get(contigname, 0) + int(coverage)
        readcountdict[contigname] = readcountdict.get(contigname, 0) + 1
    for contig in contiglist:
        if contig in sumdict:
            pass
        else:
            sumdict[contig] = 0
            readcountdict[contig] = 1
        
### looping through the contigs in sumdict, the mean coverage per contig is calculated and written to standard output
filename = sys.argv[1].split(".txt")[0]
with open("coveragefile.csv", "wb") as csvfile:
    fp = csv.writer(csvfile, delimiter="\t")
    fp.writerow(["contig","mean.coverage"])
    for contig in contiglist:
        if readcountdict[contig] != 0:
            thevalue = float(sumdict[contig])/float(readcountdict[contig])
            fp.writerow([contig,thevalue])
