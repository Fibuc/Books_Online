MENU_HEADER = """==================================================
       BIENVENUE SUR LE SCRAPER BOOK ONLINE
=================================================="""
MENU_OPTION ="""Choississez une option :
--------------------------------------------------
1. Récupérer les informations de tous les livres.
2. Récupérer les informations d'une catégorie.
3. Changer le dossier d'enregistrement.
4. Quitter l'application
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