#!/usr/bin/python

### This script takes the output of samtools depth of a mapping of reads to an assembly,
### calculates the mean coverage for each contig and merges these output files to a coverage table.
### contact: bslaby@geomar.de

import sys, os, csv

def usage():
  print("Usage: avgcov_from_samtoolsout.py depthfiles assemblyfile outdir covtable")
  print("depthfiles: a directory containing the samtools depth output files for all samples named SAMPLENAME_depth.txt")
  print("assemblyfile: the (meta)genomic assembly that the reads were mapped to")
  print("outdir: name of the output directory")
  print("covtable: name of the output coverage table")

if len(sys.argv) != 5:
  usage()
  exit()

depthfiles = sys.argv[1]
assemblyfile = sys.argv[2]

covtable = sys.argv[4]
if os.path.exists(covtable):
  print(covtable+" exists - provide a different name")
  exit()
  
outdir = sys.argv[3]
if not os.path.isdir(outdir):
  os.mkdir(outdir)

### making a list of all contigs in the assembly
contiglist = []
with open(assemblyfile, "rU") as assembly:
  for line in assembly:
    if line.startswith(">"):
      contig = line.split(">")[1].split("\n")[0]
      contiglist.append(contig)

superdict = {}
for depthfile in os.listdir(depthfiles):
  filename = depthfile.split("_depth.txt")[0]
  with open(depthfiles+"/"+depthfile, "rU") as samtoolsout:
    sumdict = {} # a dictionary adding up the per-base coverages for each contig
    readcountdict = {} # a dictionary counting the bases for each contig
### summing up coverage values and number of bases for each contig to calculate mean
    for line in samtoolsout:
      contigname, _, coverage = line.split('\t', 3)      
      sumdict[contigname] = sumdict.get(contigname, 0) + int(coverage)
      readcountdict[contigname] = readcountdict.get(contigname, 0) + 1
### adding zero count for contigs that are not covered by this read set
    for contig in contiglist:
      if contig in sumdict:
        pass
      else:
        sumdict[contig] = 0
        readcountdict[contig] = 1     
### looping through the contigs in sumdict, the mean coverage per contig is calculated and written to a coverage file in the output directory (separately for each depth file)
### and creating a dictionary with all mean values
    with open(outdir+"/"+filename+"_cov.csv", "wb") as csvfile:
      fp = csv.writer(csvfile, delimiter="\t")
      fp.writerow(["contig","mean.coverage"])
      thedict = {}
      for contig in contiglist:
        thevalue = float(sumdict[contig])/float(readcountdict[contig])
        fp.writerow([contig,thevalue])
        thedict[contig] = thevalue    
      superdict[filename] = thedict
### looping through superdict and writing the coverage table
with open(covtable, "wb") as csvfile:
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
  fp.writerow(namelist)
  for contig in contiglist:
    outdict = outsuperdict[contig]
    outlist = []
    for name in namelist:
      cov = str(outdict[name])
      outlist.append(cov)
    fp.writerow([contig,"\t".join(outlist)])
os.system("sed 's/\"//g' -i "+covtable) # to get rid of '"' in the output table
