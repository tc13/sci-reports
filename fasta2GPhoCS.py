#!/usr/bin/python

#convert directory of fasta files to GPhoCS sequence file
#from sys import argv
import re
import glob
from sys import argv
import argparse

#Argparse
parser = argparse.ArgumentParser(description="Create G-PhoCS input file from directory of fasta alignments")
parser.add_argument("Directory", metavar="<dir>",type=str,help="fasta directory")
args = parser.parse_args()

#Take in argument from command line
path = str(argv[1]) + "*"
files = glob.glob(path)

#Header at top of file - # of loci
def loci_count(glob):
        return(len(glob))
print loci_count(files)

#function to count sequences in file
def seq_count(filename):
        clock =0
        with open(filename) as fname:
                for line in fname:
                        if ">" in line:
                                clock +=1
                        else:
				pass
        return clock

#The catenator
#Transforms FASTA files with sequences over multiple lines into single line
def catenator(filename, seq_num):
	with open(filename) as fname:
		cat = ""
		lines = fname.read().rstrip()
		a= lines.split(">")
		for i in range(1,int(seq_num)):
			seq = ">" + a[i]
			header= seq.split()[0]
			tail = "".join(seq.split()[1:])
			out = str(header + "\n" +tail+"\n")
			cat += out
		return cat.split()

#function to count length of sequence
def len_seq(filename, seq_count):
	for line in catenator(filename, seq_count):
		if ">" in line:
			pass
		else:
			return(len(line))
			break

#Read in file from stdin
for locus in files:
        f = locus
	#Store these numbers as variables
	try:
		N = seq_count(f)
		K = len_seq(f, N)
	#Regex to simplify file name
		newname = re.sub(r'\...*','', re.sub(r'..*\/','', f))
		#Print header of each locus
		loci_head = str(newname + "\t" + str(N) + "\t" +  str(K))
		print "\n" + loci_head
		#print locus in GPhoCS format
                with open(f) as fname:
			lines = fname.read().rstrip()
                	a= lines.split(">")
			for i in range(1,N+1):
				seq=a[i]
				header= seq.split()[0]
                        	tail = "".join(seq.split()[1:])
                        	out = str(header + "\t" +tail)
				print out
	except TypeError:
		pass
