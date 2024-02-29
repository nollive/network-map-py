import json
import os


# Chargement du fichier JSON contenant les détails de la colocation
path = os.getcwd()
with open(path+'/template-bdd-coloc', 'r') as json_file:
    colocation_data = json.load(json_file)


# Chargement du fichier JSON contenant les données des personnes
with open(path+'/template-bdd-relation', 'r') as json_file:
    individu_data = json.load(json_file)


# Parcourir la base de données de la colocation
for colocation in colocation_data:
    nom_colocation = colocation.get("roommates", {}).get("name")
    members_colocation = [member["name"].lower() for member in colocation.get("roommates", {}).get("members", [])]
    print(nom_colocation)
    print(members_colocation)
    #i = len(members_colocation)
    #j = 0
    # Parcourir les données des personnes
    for personne in individu_data:
        # Vérifier si la personne fait partie de la colocation
        if personne["personne"].lower() in members_colocation:
            personne["colocation"] = nom_colocation
            print(personne["personne"]," assignée à ",personne["colocation"])
            #j+=1
    #print (j," personnes mappées parmis les ",i," membres de la colocation")   
            

# Écrire les données dans un nouveau fichier JSON contenant les liens et les colocations
with open('bdd-lien.json', 'w', encoding='utf-8') as json_file:
    json.dump(individu_data, json_file, indent=4, ensure_ascii=False)
