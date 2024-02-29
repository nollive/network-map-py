import json
import unicodedata
import os

path = os.getcwd()

# Définition de la fonction pour retirer les accents d'une chaîne de caractères
def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])


# Chargement de la BDD (sous format JSON)
with open(path+'/bdd-template-coloc.json', 'r', encoding='utf-8') as file:
    data = json.load(file)


# Parcours des éléments de la BDD (sous forme de liste)
for item in data:
    # Récupération de roomates (contient le nom de la colocation, les membres...)
    roommates = item.get("roommates", {}) 
    
    # Récupération de la liste des membres d'une colocation (members appartient à roommates)
    members = roommates.get("members", []) 
    
    # Parcours des membres de la colocation et suppression des accents dans les noms (dans members)
    for member in members:
        member_name = member.get("name", "") 
        member["name"] = remove_accents(member_name)

# Écriture des modifications dans le fichier JSON
with open('bdd-coloc-revised.json', 'w', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=4)

