#!/usr/bin/python

### This script takes the binning output table of CONCOCT and the coverage file used for the binning, and calculates the average coverage for each bin/genome
### I wrote it for my combined assembly from 6 datasets - therefore it considers 6 coverage values
### bslaby@geomar.de

import sys, os, csv

def usage():
    print "Usage: bingenomecov_covfile.py clusterfile covfile"

if len(sys.argv) != 3:
    usage()
    exit()

bindict = {}
sumdict = {}
countdict = {}
with open(sys.argv[1], "rU") as clusterfile: # clusterfile is the concoct output table usually named "clustering_gt1000.csv"
    for line in clusterfile:
        header, binno = line.strip().split(',',2)
        bindict[header] = binno

with open(sys.argv[2], "rU") as covfile: # covfile is the input table used for the binning
    for line in covfile:
        if not line.startswith("#"):
            header, no1, no2, no3, no4, no5, no6 = line.strip().split('\t', 7) # adapt this line for the number of coverage values in the table
            contiglen = header.split('_')[3]
            if not int(contiglen)<1001:
                cov = float(no1)+float(no2)+float(no3)+float(no4)+float(no5)+float(no6) # and also this line summing up those values
                binno = bindict[header]
                sumdict[binno] = sumdict.get(binno, 0) + cov
                countdict[binno] = countdict.get(binno, 0) + 1
        
with open("bin_coveragefile.csv", "wb") as csvfile:
	fp = csv.writer(csvfile, delimiter="\t")
	fp.writerow(["bin","mean.coverage"])
        for binno in sumdict:
            covsum = sumdict[binno]
            count = float(countdict[binno])
            meancov = covsum/count
            fp.writerow([binno,meancov])
