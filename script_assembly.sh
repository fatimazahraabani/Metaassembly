#!/bin/sh
## BY FATIMA-ZAHRA ABANI

#SBATCH --job-name=metaspades2
#SBATCH --mail-user=fatima-zahra.abani@cirad.fr
#SBATCH --mail-type=ALL
#SBATCH --partition=long
#SBATCH --cpus-per-task=8
#SBATCH --mem=160G

#concatenation des fichiers
cat ARBO*_notCombined_1.fastq > ARBO_notCombined_sort_1.fastq
cat ARBO*_notCombined_2.fastq >	ARBO_notCombined_sort_2.fastq

#importer spades
module load spades/3.15.5

# Assemblage avec metaspades

rnaspades.py -t 8 -1 ARBO_notCombined_sort_1.fastq -2 ARBO_notCombined_sort_2.fastq -o output_metaspades_sort_ --only-assembler

#Importation du module
module load cap3-10.2011

#lacer cap3
cap3 transcripts.fasta

#importer quast
module load quast/5.0.2

#Analyse des résultats de rnaspades avec quast
quast.py -o quast_results_cap3 transcripts_cap3_concat.fasta

# Chargement du module Diamond
module load diamond

diamond blastx -b 10.0 -c 1 -p 16  -d /shared/ifbstor1/bank/nr/current/diamond/nr --taxonmap prot.accession2taxid.gz --more-sensitive --query transcripts_cap3_concat.fasta --max-hsps 1 --max-target-seqs 5  -f 6 qseqid sseqid qlen slen length qstart qend sstart send qcovhsp pident evalue bitscore staxids --out result_diamond_cap3.tsv

#Extaction de la colonne 14 (Tax-Id)
cut -f 14 result_diamond.tsv | sort | uniq > tax_id.txt

#Téléchargement de l'ensemble de fichiers contenant les informations taxonomiques de la base de données de taxonomie du NCBI.

mkdir taxonomie
cd taxonomie
wget ftp://ftp.ncbi.nih.gov/pub/taxonomy/taxdump.tar.gz
tar -zxvf taxdump.tar.gz
cp names.dmp nodes.dmp delnodes.dmp merged.dmp ~/.taxonkit

#Commande de création d'un fichier tsv qui va contenir la taxonomie des taxid donnés par diamond
echo -e "taxid\trank\tname\tlineage\tkingdom\tphylum\tclass\torder\tfamily\tgenus\tspecies\tstrain" > taxonkit_megahit.tsv ; cat tax_id.txt | ./taxonkit reformat -I 1 -r "Unassigned" -f "{k}\t{p}\t{c}\t{o}\t{f}\t{g}\t{s}\t{t}" >> taxonkit_megahit.tsv


