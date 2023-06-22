import pandas as pd
import matplotlib.pyplot as plt
import squarify

# Lecture du fichier TSV et extraction des colonnes pertinentes
df = pd.read_csv("taxonkit_rnaspades.tsv", sep="\t")
df["rank_category"] = df["rank"].apply(lambda x: "Virus" if x == "Viruses" else ("Eucaryotes" if x == "Eukaryota" else "Others"))

# Calcul des pourcentages pour chaque catégorie de rang
percentages = df["rank_category"].value_counts(normalize=True) * 100

# Couleurs dégradées du rose
colors = ["#800020", "#B22222", "#DC143C"]

# Création du diagramme à secteurs carré
fig, ax = plt.subplots()
ax.axis('off')
squarify.plot(sizes=percentages, label=percentages.index, color=colors, alpha=0.8)

# Ajout du titre
plt.title("Catégories de rang obtenues avec RnaSpades")

# Sauvegarde de l'image du résultat
plt.savefig('b.png')
plt.close()

print("L'image du camembert a été sauvegardée dans 'b.png'.")



