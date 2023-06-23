#!/usr/bin/env python
# coding: utf-8


# Import librarie for parsing data frame and fasta
import pandas as pd
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
from Bio.Seq import Seq


# Function for fasta file
def fasta2dict(filename):
	"""
	Function that take a file name (fasta), and return a dictionnary of sequence

	"""
	with open(filename, "rU") as fastaFile:
		return SeqIO.to_dict(SeqIO.parse(fastaFile, "fasta"))


# Open all file (assembly output, Diamond result, and taxonkit result) (example : Megahit, we will do the same for the other assemblers)
diamond = pd.read_csv('result_diamond.tsv',sep='\t' ,header=None )
diamond.columns = ["qseqid","sseqid","qlen","slen","length","qstart","qend","sstart","send","qcovhsp","pident","evalue","bitscore","staxids"]
taxon = pd.read_csv('taxonkit_megahit.tsv',sep='\t')
fasta = fasta2dict('final.contigs.fa')


# Merge taxid information à diamond result
data = diamond.merge(taxon, right_on="taxid",left_on='staxids')
# Retrieve sequence liste with hit on Virus
list_seq_virus = list(set(data[data['rank'] == "Viruses"]['qseqid']))
# Generate data frame with only Virus seq
data = data.query('qseqid in @list_seq_virus')
print('Contig with match on Viruses and other rank: \n')

# Iterator for know the number of Virus with other match in other rank
nb = 0
# Iterator for know the number of sequence which are finaly not a Virus
nb_remove = 0


for qseqid in set(data.query('rank != "Viruses"')["qseqid"]):
    dico_rank = dict(data.query('qseqid == @qseqid')['rank'].value_counts())
    # Check if they have two Rank for the same sequence
    if len(dico_rank) >= 2:
        nb += 1 
        print(f"\t* {qseqid} ({dico_rank})")
        # Check if they have more hit in other Rank than Virus
        if dico_rank['Viruses'] < 0.5*sum(dico_rank.values()): 
            # Remove the Seq from the virus list if hey have more hit in other Rank than Virus
            list_seq_virus.remove(qseqid)
            nb_remove +=1

print(f"\nIn this data set they have {nb} sequence with some match in other Rank than Viruses and {nb_remove} sequence that aren't Viruses (more than 50% of diamond hit aren't Viruses")
print()
print(f'They have {len(list_seq_virus)} virals contigs in the data set')

# Write virus fasta file
with open(f'contig_virus.fasta','w') as f :
    for seq_id in list_seq_virus:
        SeqIO.write(fasta[seq_id],f, "fasta")
        
# Create a data frame with all information about Diamond and taxid
data = diamond.merge(taxon, right_on="taxid",left_on='staxids')
# Sort data frame in function of qseqid and pident
data = data.sort_values(['qseqid','pident'],ascending = [True,False])
# Keep only the first line for each sequence (best pident)
data.drop_duplicates(subset=['qseqid'], keep='first',inplace=True)
# Create a dict with all information about Rank
dico_plot = dict(data['rank'].value_counts())

# libraries
import matplotlib.pyplot as plt
import squarify    # pip install squarify (algorithm for treemap)
import pandas as pd
# Create treemap
squarify.plot(sizes=dico_plot.values(), label=dico_plot.keys(), alpha=.8 )

# Show information
dico_plot

#save the result
plt.savefig('treemap.png')

