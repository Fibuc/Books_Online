from package.requete import recuperer_contenu_page
import csv
import constants
from pathlib import Path
from datetime import datetime 

def conversion_monnaie_gbp_en_eur(montant):
    contenu = recuperer_contenu_page("https://www.boursorama.com/bourse/devises/taux-de-change-euro-livresterling-EUR-GBP/")
    taux_de_change = contenu.find("div", class_="c-faceplate__price--inline").find("span", class_="c-instrument--last").get_text()
    montant_euros = montant / float(taux_de_change)
    return round(montant_euros, 2)

def enregistrement_des_donnees_csv(donnees):
    nom_fichier = (f"categorie_{(donnees[0]['category']).lower()} {str(datetime.now())[:-7]}.csv").replace(" ","_").replace(":","-")
    chemin_fichier = repertoire_enregistrement_fichier_csv() / nom_fichier
    with open(chemin_fichier,"w", encoding="UTF-8", newline="") as fichier_csv:
        writer = csv.DictWriter(fichier_csv, fieldnames=donnees[0].keys())
        writer.writeheader()
        writer.writerows(donnees)

def repertoire_enregistrement_fichier_csv():
    path = Path(constants.repertoire_fichier_csv)
    return path