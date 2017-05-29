#!/usr/bin/python

### bslaby@geomar.de
### The binning software CONCOCT suggests to split large contigs (>20 000 bp) into sub-contigs of 10 000 bp with a script that they provide with the program to give long contigs more weight. 
### After binning and before creating fasta files for each bin, I prefer to merge these sub-contigs again.
### This script assigns the contigs that were split for binning to a bin based on the placement of the majority of the respective sub-contigs.
### It was written for SPAdes and IDBA-UD assemblies and may need adjustments for other contig naming systems.

import sys, os

# input files:

def usage():
	  print "Usage: merge_contigs_concoctclustering.py clustering"

if len(sys.argv) != 2:
	  usage()
	  exit()

with open(sys.argv[1], "rU") as clustering:
    filename = sys.argv[1].split(".csv")[0]
    nodecountdict = {}
    for line in clustering:
        node = line.split("_")[0]+"_"+line.split("_")[1].split(",")[0] #last split only for idba-ud assembly
        if "." in node: #only for idba-ud assembly
            node = node.split(".")[0]        
        nodecountdict[node] = nodecountdict.get(node, 0) + 1
#    print nodecountdict
with open(sys.argv[1], "rU") as clustering:  
    thedict = {}
    for line in clustering:
        contig, thebin = line.strip().split(",", 2)
        node = line.split("_")[0]+"_"+line.split("_")[1].split(",")[0] #last split only for idba-ud assembly
        if "." in node: #only for idba-ud assembly
            node = node.split(".")[0]  
        thecount = nodecountdict[node]
#        print thecount
        if thecount != 1:
            contig = contig.rsplit(".", 1)[0]
#        print contig
        if contig in thedict:
            bindict = thedict[contig]
        else:
            bindict = {}
        bindict[thebin] = bindict.get(thebin, 0) + 1
        thedict[contig] = bindict
#print thedict
with open(filename+"_merged.csv", "w") as outfile:
    outdict = {}
    ambicount = 0
    for contig in thedict:
        bindict = thedict[contig]
        themax = 0
        for bin in bindict:
            thecount = int(bindict[bin])
            if thecount == themax:
                oldbin = outdict[contig]
                thebin = str(oldbin)+" or "+str(bin)
                ambicount = ambicount+1
            if thecount > themax:
                themax = thecount
                thebin = bin
            outdict[contig] = thebin
#    print outdict
    if ambicount > 0:
        print "WARNING: One or more contigs could not be placed unambiguously"
    for contig in outdict:
        thebin = outdict[contig]
        outfile.write(contig+","+thebin+"\n")
