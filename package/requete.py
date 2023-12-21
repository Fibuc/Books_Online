import requests
from bs4 import BeautifulSoup

def recuperer_contenu_page(url):
    compteur = 0
    while compteur < 20:
        reponse = requests.get(url)
        if not reponse.ok:
            compteur += 1
            print(f"Tentative de connexion avec la page {compteur}/20")
            continue
        contenu_requete = reponse.content
        soup = BeautifulSoup(contenu_requete, "html.parser")
        return soup
    else:
        print("Erreur de connexion avec l'url")
        return False
    
def recuperer_image_page(url_image):
    compteur = 0
    while compteur < 20:
        reponse = requests.get(url_image)
        if not reponse.ok:
            compteur += 1
            print(f"Tentative de connexion avec la page {compteur}/20")
            continue
        return reponse.content