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

stars = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5
}
saved_files_directory = ""
extract_images = False
valid_directory = False
start = True
available_categories = {}
number_of_books_total = 0