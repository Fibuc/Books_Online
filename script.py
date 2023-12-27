import constants
from package import utilitaires
from package import scraper

print(constants.MENU_HEADER)

while constants.repertoire_valide == False:
    constants.repertoire_fichiers_enregistres = input("Veuillez insérer le répertoire d'enregistrement : ")
    utilitaires.verification_repertoire()

while constants.lancement == True:
    print(constants.MENU_OPTION)
    choix_utilisateur = input("Quel est votre choix ? : ")
    match choix_utilisateur:
        case "1":
            utilitaires.choix_telechargement_images()
            scraper.extraction_toutes_les_categories()
        case "2":
            liste_categorie = scraper.recuperer_categories_disponibles()
            print(liste_categorie)
            categorie_choisie = input("Veuillez choisir la catégorie : ").lower()
            while categorie_choisie not in liste_categorie:
                print("La catégorie indiquée n'existe pas.")
                categorie_choisie = input("Veuillez choisir la catégorie : ").lower()
            utilitaires.choix_telechargement_images()
            scraper.extraire_informations_des_livres_pour_une_categorie(constants.categories_disponibles[categorie_choisie])
            print("")
        case "3":
            ancien_repertoire = constants.repertoire_fichiers_enregistres
            constants.repertoire_fichiers_enregistres = input("Veuillez indiquer le nouveau répertoire : ")
            if constants.repertoire_fichiers_enregistres == "q":
                constants.repertoire_fichiers_enregistres = ancien_repertoire
            utilitaires.verification_repertoire()
        case "4":
            print("Fermeture de l'application")
            constants.lancement = False
        case _:
            print("Veuillez choisir une option valide.\n")