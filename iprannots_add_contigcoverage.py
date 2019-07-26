#!/usr/bin/python

### This script takes an InterPro annotation table (tsv) and adds contig coverage information.
### The coverage information is the output table of the script avgcov_from_samtoolsout.py - actually, any kind of additional contig-level information can be added using this script.
### contact: bslaby@geomar.de

import sys, os, csv

def usage():
  print("Usage: iprannots_add_contigcoverage.py covtable iprannots outfile")
  print("covtable: the output table of the script avgcov_from_samtoolsout.py, first line is header - actually, any kind of additional contig-level information can be added")
  print("iprannots: InterPro annotation table in tsv format, first line is header")
  print("outfile: name of the output file")

if len(sys.argv) != 4:
  usage()
  exit()

covtable = sys.argv[1]
iprannots = sys.argv[2]
outfile = sys.argv[3]

if os.path.exists(outfile):
  print(outfile+" exists - provide a different name")
  exit()

### making a dictionary of the coverage information per contig
covdict = {}
with open(covtable, "r") as coverages:
  headercovs = coverages.readline().strip().split("\t")
  for line in coverages:
    if line.startswith("c_00"):
      contig = line.split("\t")[0]
      covlist = line.strip().split("\t")
      covdict[contig] = covlist

### going through the annotations, adding the respective coverages and writing to output
with open(iprannots, "r") as annots, open(outfile, "wb") as csvfile:
  headerannots = annots.readline().strip().split("\t")
  headerlen = len(headerannots)
  headers = headerannots+headercovs
  out = csv.writer(csvfile, delimiter="\t")
  out.writerow(headers) # writing the header line
  for line in annots:
    if line.startswith("c_00"):
      contig = "c_"+line.split("_")[1]
      covlist = covdict[contig]
      annotlist = line.strip().split("\t")
      if len(annotlist)<headerlen: # accounting for lines that are missing annotations
        diff = headerlen-len(annotlist)
        for i in range(diff):
          annotlist.append("NA")
      outlist = annotlist+covlist
      out.writerow(outlist)
