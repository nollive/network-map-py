import argparse
import networkx as nx
import matplotlib.pyplot as plt
import json
import os




# Fonction pour lire les arguments de la ligne de commande
def parse_arguments():
    parser = argparse.ArgumentParser(description='Graph Visualization with Node Link Limits')
    parser.add_argument('--min', type=int, default=0, help='Minimum number of links for a node to be displayed')
    parser.add_argument('--max', type=int, default=float('inf'), help='Maximum number of links for a node to be displayed')
    parser.add_argument('--keep', choices=['min', 'max', 'both'], default='both', help='Keep nodes based on minimum, maximum, or both links')
    parser.add_argument('--out', type=str, default='graph.png', help='Output image file name')
    parser.add_argument('--dpi', type=int, default=100, help='DPI (dots per inch) for the output image')
    parser.add_argument('--method', choices=['spring', 'spectral', 'circular', 'fruchterman'], default='spring', help='Choose your graph display method')
    parser.add_argument('--graph', type=bool, default=True, help='Display the graph or not')
    return parser.parse_args()

# Lire les arguments de la ligne de commande
args = parse_arguments()


# Récuperation du wd où sont placés le fichier python ainsi que les bases de données .json
path = os.getcwd()
# Chargement du fichier JSON contenant les liens entre les noeuds
with open(path+'/template-bdd-liens.json', 'r') as json_file:
    personnes_data = json.load(json_file)

# Chargement du fichier JSON contenant les détails des correspondances de couleurs
with open(path+'/template-bdd-couleurs.json', 'r') as json_file:
    couleurs_data = json.load(json_file)
    

# Création du graphe
G = nx.Graph()

# Ajout des arêtes 
for personne in personnes_data:
    nom_personne = personne["personne"]
    lien_amis = personne["liens"]
    for ami in lien_amis:
        G.add_edge(nom_personne, ami)


# Filtrer les nœuds en fonction des limites de liens spécifiés (args.keep, args.min et args.max)
nodes_to_keep = set()
for node, degree in dict(G.degree()).items():
    if args.keep == 'min' and degree >= args.min:
        nodes_to_keep.add(node)
    elif args.keep == 'max' and degree <= args.max:
        nodes_to_keep.add(node)
    elif args.keep == 'both' and args.min <= degree <= args.max:
        # Ajouter le nœud et tous ses voisins au graphe filtré
        nodes_to_keep.add(node)
        nodes_to_keep.update(G.neighbors(node))

# Créer un sous-graphe avec les nœuds filtrés
G_filtered = G.subgraph(nodes_to_keep)

# Détermination des couleurs des nœuds en fonction de la liste de chaque personne
couleurs_noeuds = []
for node in G_filtered.nodes:
    caract = [personne["liste"][0] for personne in personnes_data if personne["personne"] == node and personne["liste"]]
    if caract:
        couleur = [Liste["couleur"] for Liste in couleurs_data if Liste["liste"] == caract[0]]
        couleur = couleur[0]
    else:
        couleur = 'grey'  # Valeur par défaut si la caractéristique n'est pas trouvée ou la liste est vide
    couleurs_noeuds.append(couleur)


# Sélection de la méthode de disposition du graphe
if args.method == 'spring':
    layout = nx.spring_layout(G_filtered, scale=4, iterations=1000, k=2) # Augmente l'échelle, rajouter k ??
elif args.method == 'spectral':
    layout = nx.spectral_layout(G_filtered, scale=4) #Used to position highly clustered nodes together
elif args.method == 'circular':
    layout = nx.circular_layout(G_filtered) #Circular, better for small graph
elif args.method == 'fruchterman':
    layout = nx.fruchterman_reingold_layout(G_filtered)


# Affichage du graphe avec la méthode de disposition sélectionnée
nx.draw(G_filtered, pos=layout, node_color=couleurs_noeuds, with_labels=True, node_size=150, font_size=5, font_weight='bold')
plt.savefig(args.out, format='PNG', dpi=args.dpi)
# Affichage du graphique
plt.show()





