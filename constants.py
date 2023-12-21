MENU_HEADER = """==================================================
       BIENVENUE SUR LE SCRAPER BOOK ONLINE
=================================================="""
MENU_OPTION ="""Choississez une option :
--------------------------------------------------
1. Récupérer les informations de tous les livres.
2. Récupérer les informations d'une catégorie.
3. Afficher les informations d'un livre.
4. Changer le dossier d'enregistrement.
5. Quitter l'application
--------------------------------------------------
"""

URL = "https://books.toscrape.com/"

etoiles = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5
}
repertoire_fichiers_enregistres = ""
extraction_images = False
repertoire_valide = False
lancement = True
categories_disponibles = {}
nombre_livre_total = 0
nom_livre_et_liens = {}
taux_correspondance = 0
nom_livre_correspondance = ""