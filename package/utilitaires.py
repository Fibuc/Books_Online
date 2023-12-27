from package.requete import recuperer_contenu_page
import csv
import constants
from pathlib import Path
from datetime import datetime
import re

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
    path = Path(constants.repertoire_fichiers_enregistres)
    return path

def enregistrement_image(categorie, nom_fichier, contenu):
    path = Path(constants.repertoire_fichiers_enregistres)
    dossier_image = path / "Images" / categorie
    nom_fichier_filtre = suppression_carateres_speciaux(nom_fichier)
    chemin_complet = dossier_image / f"{(nom_fichier_filtre)}.jpg"
    dossier_image.mkdir(parents=True, exist_ok=True)
    with open(chemin_complet, "wb") as fichier_image:
        fichier_image.write(contenu)
    return chemin_complet

def verification_repertoire():
    path = Path(constants.repertoire_fichiers_enregistres)
    if path.exists() == False:
        while str(path.parent) == ".":
            print("Chemin de répertoire non valide.")
            return False
        double_refus = False
        choix_creation = input("Le chemin n'existe pas, voulez-vous le créer ? (y/n) : ")
        match choix_creation:
            case "y":
                constants.repertoire_valide = True
            case "n":
                while double_refus == False:
                    choix_autre_repertoire = input("Voulez-vous choisir un autre répertoire ? (y/n) : ")
                    match choix_autre_repertoire:
                        case "y":
                            constants.repertoire_valide = False
                            return
                        case "n":
                            double_refus = True
                        case _:
                            print("Veuillez choisir une option valide.\n")
                else:
                    print("Fermeture de l'application")
                    constants.repertoire_valide = True
                    constants.lancement = False       
    constants.repertoire_valide = True

def choix_telechargement_images():
    choix_telecharger_image = ""
    while choix_telecharger_image != "y" or "n":
        choix_telecharger_image = input("Voulez-vous télécharger les images ? (y/n) : ")
        match choix_telecharger_image:
            case "y":
                constants.extraction_images = True
                break
            case "n":
                constants.extraction_images = False
                break
            case _ :
                print("Veuillez choisir une option valide.")

def suppression_carateres_speciaux(texte:str):
    transTable = texte.maketrans("""<>:“"'/|?*""", "  -  .    ")
    nom_fichier = texte.translate(transTable)
    return nom_fichier

