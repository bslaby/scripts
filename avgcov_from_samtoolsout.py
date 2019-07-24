#!/usr/bin/python

### This script takes the output of samtools depth of a mapping of reads to an assembly,
### calculates the mean coverage for each contig and merges these output files to a coverage table.
### contact: bslaby@geomar.de

import sys, os, csv

def usage():
  print("Usage: avgcov_from_samtoolsout.py depthfiles assemblyfile outdir")
  print("depthfiles is a directory containing the samtools depth output files for all samples named SAMPLENAME_depth.txt")
  print("assemblyfile: the (meta)genomic assembly that the reads were mapped to")
  print("outdir is the output directory")

if len(sys.argv) != 4:
  usage()
  exit()

depthfiles = sys.argv[1]
outdir = sys.argv[3]

for depthfile in os.listdir(depthfiles):
  with open(depthfiles+"/"+depthfile, "rU") as samtoolsout, open(sys.argv[2], "rU") as assemblyfile:
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
  filename = depthfile.split("_depth.txt")[0]
  with open(outdir+"/"+filename+"_cov.csv", "wb") as csvfile:
    fp = csv.writer(csvfile, delimiter="\t")
    fp.writerow(["contig","mean.coverage"])
    for contig in contiglist:
      if readcountdict[contig] != 0:
        thevalue = float(sumdict[contig])/float(readcountdict[contig])
        fp.writerow([contig,thevalue])

superdict = {}
### reading all input files and making dictionaries
for xfile in os.listdir(outdir):
  with open(outdir+"/"+xfile, "rU") as thefile:
    name = xfile.split(".")[0]
    thedict = {}
    for line in thefile:
      if line.startswith("contig"):
        pass
      else:
        contig, cov = line.strip().split("\t", 2)
        thedict[contig] = cov    
    superdict[name] = thedict
#print(superdict)

with open("combined_coverage.csv", "wb") as csvfile:
  fp = csv.writer(csvfile, delimiter="\t")
  namelist = []
  outsuperdict = {}
  for name in superdict:
    namelist.append(name)
    thedict = superdict[name]
    for contig in thedict:
      cov = thedict[contig]
      if contig in outsuperdict:
        outdict = outsuperdict[contig]
      else:
        outdict = {}
      outdict[name] = cov
      outsuperdict[contig] = outdict
#  print(outsuperdict)
  fp.writerow(namelist)
  for contig in contiglist:
    outdict = outsuperdict[contig]
    outlist = []
    for name in namelist:
      cov = outdict[name]
      outlist.append(cov)
    fp.writerow([contig,"\t".join(outlist)])
os.system("sed 's/\"//g' -i combined_coverage.csv") # to get rid of '"' in the output table
