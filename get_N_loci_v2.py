#!/usr/bin/python
import os
import sys
import random
from Bio.SeqIO import parse

infileName = sys.argv[1] # name of the (big?) fasta file
nLoci_to_get = int(sys.argv[2]) # number of loci to retain
threshold = float(sys.argv[3]) # threshold T. A locus is rejected if at least one individual has a proportion of missing data (N) greater than T.
minLoci = int(sys.argv[4]) # minimum number of loci an individual has to have for being considered

# get the number of total sequences
nSequences = int(os.popen("cat {infileName} | grep '>' | wc -l".format(infileName=infileName)).read().strip())

# get the list of all available loci
list_loci_tmp = [None]*nSequences
infile = parse(infileName, 'fasta')
cnt = 0
for seq in infile:
	loci_tmp = seq.id.split('|')[0]
	list_loci_tmp[cnt] = loci_tmp
	cnt += 1
list_loci_tmp = [ i for i in set(list_loci_tmp) ]

# get the number of available loci for each individuals
infile = parse(infileName, 'fasta')
individuals = {}
for seq in infile:
	ind_tmp = seq.id.split('|')[2]
	allele_tmp = seq.id.split('|')[3]
	if ind_tmp not in individuals:
		individuals[ind_tmp] = len(list_loci_tmp)
	
	if allele_tmp == "Allele_1":
		prop_missing_tmp = seq.seq.count('N')/len(seq.seq)
		if prop_missing_tmp > threshold:
			individuals[ind_tmp] -= 1

output = open("individuals.txt", "w")
output.write("# all individuals with less than {0} loci will be rejected\n".format(minLoci))
output.write("individual\tn_available_loci\n")
for ind_tmp in individuals:
	output.write("{individual}\t{nLoci}\n".format(individual=ind_tmp, nLoci=individuals[ind_tmp]))
output.close()

# get list of loci 
loci = {}
infile = parse(infileName, 'fasta')
for seq in infile:
	loci_tmp = seq.id.split('|')[0]
	ind_tmp = seq.id.split('|')[2]
	if individuals[ind_tmp]>minLoci:
		if loci_tmp not in loci:
			loci[loci_tmp] = 1
		prop_missing_tmp = seq.seq.count('N')/len(seq.seq)
		if prop_missing_tmp > threshold:
			loci[loci_tmp] = 0

# retain loci with a proportion of missing data below the threshold
list_of_loci = [ i for i in loci if loci[i]==1 ]
if len(list_of_loci) > 0:
	if len(list_of_loci) > nLoci_to_get:
		list_of_retained_loci = random.sample(list_of_loci, nLoci_to_get)
	else:
		list_of_retained_loci = [ i for i in list_of_loci ]
else:
	message = "\nthere is no available loci after applying the threshold of {threshold} ({nLoci} initially available, 0 after filtering for N)\n".format(threshold=threshold, nLoci=len(loci))
	raise ValueError(message)

output = open("retained_loci.txt", "w")
output.write("# n_total_loci: total number of different loci found in {0}\n".format(infileName))
output.write("# threshold_missing_data: arbitrary threshold set by the user. A sequence is rejected if it contains a proportion of missing data (N) greater than this threshold\n")
output.write("# n_available_loci: number of loci for which all RETAINED individuals succesfully pass throw the threshold\n")
output.write("# minLoci: minimum number of loci for a giver individual to reject it\n")
output.write("# n_available_individuals: number of retained individuals, with a number of available loci greater than minLoci ({0})\n".format(minLoci))

output.write("n_total_loci\tthreshold_missing_data\tn_available_loci\tn_total_individiuals\tminLoci\tn_available_individuals\n")
output.write("{0}\t{1}\t{2}\t{3}\t{4}\t{5}\n".format(len(list_loci_tmp), threshold, len(list_of_loci), len(individuals), minLoci, len( [ i for i in individuals if individuals[i]>minLoci ]) ))
output.close()


# read the fasta file in order to get the list of all loci
infile = parse(infileName, 'fasta')
outfile = open('{0}_filtered_subsampled.fasta'.format(infileName.split('.')[0]), "w")
for seq in infile:
	loci_tmp = seq.id.split('|')[0]
	ind_tmp = seq.id.split('|')[2]
	if individuals[ind_tmp]>minLoci:
		if loci_tmp in list_of_retained_loci:
			output = ">{idname}\n{seq}\n".format(idname=seq.id, seq=seq.seq)
			outfile.write(output)
outfile.close()

print('initial number of loci: {nLoci}\navailable loci after filtering: {nAvail}\nretained loci: {nRetained}'.format(nLoci=len(loci), nAvail=len(list_of_loci), nRetained=len(list_of_retained_loci)))

