#!/usr/bin/python
import os
import sys
import random
from Bio.SeqIO import parse

infileName = sys.argv[1] # name of the (big?) fasta file
nLoci_to_get = int(sys.argv[2]) # number of loci to retain

# 
commande = 'cat {infile} | grep ">" | cut -d "|" -f1 | uniq'.format(infile=infileName)
list_of_loci = os.popen(commande).read()
list_of_loci = [ i[1:] for i in list_of_loci.split('\n') ][:-1]

list_of_retained_loci =  random.sample(list_of_loci, nLoci_to_get)

# read the fasta file in order to get the list of all loci
infile = parse(infileName, 'fasta')
outfile = open('{0}_subsampled.fasta'.format(infileName.split('.')[0]), "w")
for seq in infile:
	loci_tmp = seq.id.split('|')[0]
	if loci_tmp in list_of_retained_loci:
		output = ">{idname}\n{seq}\n".format(idname=seq.id, seq=seq.seq)
		outfile.write(output)
outfile.close()

