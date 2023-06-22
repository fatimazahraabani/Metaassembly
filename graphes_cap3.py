import numpy as np
import matplotlib.pyplot as plt

# Données pour les paramètres avant CAP3
n50_before = [0, 838, 10454, 939]  
longest_contig_before = [0, 18603, 11845, 17759]
num_contigs_before = [0, 37553, 16, 14069]
l50_before = [0, 3676, 3, 2402]
total_length_before = [0, 10217836, 61118, 8694625]

# Données pour les paramètres après CAP3
n50_after = [803, 960, 10454, 859]  
longest_contig_after = [22557, 23412, 11845, 20070]
num_contigs_after = [142963, 20936, 16, 10980]
l50_after = [10665, 3036, 3, 1902]
total_length_after = [28764505, 10094234, 61118, 6475695]

# Étiquettes des assembleurs
assemblers = ['Megahit_snakevir', 'Megahit', 'MetaviralSpades', 'RnaSpades']
x = np.arange(len(assemblers))  # Positions en x pour chaque assembleur

# Couleurs des barres
colors = ['blue', 'orange']

# Largeur des barres
bar_width = 0.35

# Création des graphiques
plt.figure(figsize=(12, 10))

# Graphe N50
plt.subplot(2, 3, 1)
for i in range(2):
    plt.bar(x + i * bar_width - bar_width/2, [n50_before[j] if i == 0 else n50_after[j] for j in range(len(assemblers))],
            width=bar_width, label='Avant CAP3' if i == 0 else 'Après CAP3', color=colors[i])
plt.xlabel('Assembleurs')
plt.ylabel('N50')
plt.xticks(x, assemblers)
plt.legend()

# Graphe Longest Contig
plt.subplot(2, 3, 2)
for i in range(2):
    plt.bar(x + i * bar_width - bar_width/2, [longest_contig_before[j] if i == 0 else longest_contig_after[j] for j in range(len(assemblers))],
            width=bar_width, label='Avant CAP3' if i == 0 else 'Après CAP3', color=colors[i])
plt.xlabel('Assembleurs')
plt.ylabel('Longest Contig')
plt.xticks(x, assemblers)
plt.legend()

# Graphe Nombre de Contigs
plt.subplot(2, 3, 3)
for i in range(2):
    plt.bar(x + i * bar_width - bar_width/2, [num_contigs_before[j] if i == 0 else num_contigs_after[j] for j in range(len(assemblers))],
            width=bar_width, label='Avant CAP3' if i == 0 else 'Après CAP3', color=colors[i])
plt.xlabel('Assembleurs')
plt.ylabel('Nombre de Contigs')
plt.xticks(x, assemblers)
plt.legend()

# Graphe L50
plt.subplot(2, 3, 4)
for i in range(2):
    plt.bar(x + i * bar_width - bar_width/2, [l50_before[j] if i == 
0 else l50_after[j] for j in range(len(assemblers))],
            width=bar_width, label='Avant CAP3' if i == 0 else 'Après CAP3', color=colors[i])
plt.xlabel('Assembleurs')
plt.ylabel('L50')
plt.xticks(x, assemblers)
plt.legend()

# Graphe Longueur totale de l'assemblage
plt.subplot(2, 3, 5)
for i in range(2):
    plt.bar(x + i * bar_width - bar_width/2, [total_length_before[j] if i == 0 else total_length_after[j] for j in range(len(assemblers))],
            width=bar_width, label='Avant CAP3' if i == 0 else 'Après CAP3', color=colors[i])
plt.xlabel('Assembleurs')
plt.ylabel("Longueur totale de l'assemblage")
plt.xticks(x, assemblers)
plt.legend()

# Ajustement de l'espacement entre les sous-graphiques
plt.tight_layout()

# Sauvegarde des graphiques
plt.savefig('plots.png')

# Affichage des graphiques
plt.show()

