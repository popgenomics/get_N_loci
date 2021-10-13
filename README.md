# get_N_loci  
You are sad during your PhD?  
Files are too big for you?  
i HAVE the solution: get_N_loci.py !

## how to launch it:  
like that little rabbit:  
```
python3 /home/croux/Programmes/get_N_loci/get_N_loci.py longiflora_grandiflora.fasta 2000  
```

## BREAKING NEWS: the second version V2 is now AVAILABLE  
modificaitons:  
1. now, two filters:  
  - *threshold*: proportion of missing data. If a locus has a proportion of missing data greater than the threshold, then, the locus is rejected.  
  - *minLoci*: if an individual has a number of retained loci smaller than *minLoci*, then reject the individual.  
2. write some files containing informations.  
  
## Example:  
```
python3 /home/croux/Programmes/get_N_loci/get_N_loci_v2.py [input file, in a fasta format] [number of loci to sample] [maximum of tolerated missing data per sequence (between 0 and 1)] [minimum number of retained loci (passing the previous threshold). If an individual has less available loci that this number, then the individual is rejected]   
python3 /home/croux/Programmes/get_N_loci/get_N_loci_v2.py longiflora_grandiflora.fasta 5000 0.5 2000  
```
