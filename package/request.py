import requests
from bs4 import BeautifulSoup

def get_page_content(page_url:str):
    """Récupère le contenu de la page html entrée en argument et permet de la parser. 

    Args:
        page_url (str): Entrer l'adresse url de la page html.

    Returns:
        soup (BeautifulSoup): Retourne un objet de type BeautifulSoup contenant les éléments à parser.
    """
    counter = 0
    while counter < 20:
        response = requests.get(page_url)
        if not response.ok:
            counter += 1
            print(f"Tentative de connexion avec la page {counter}/20")
            continue
        request_content = response.content
        soup = BeautifulSoup(request_content, "html.parser")
        return soup
    else:
        print("Erreur de connexion avec l'url")
        return False
    
def get_page_image(image_url:str):
    """Récupère le contenu de la page html entrée en argument et permet de récupérer l'image.

    Args:
        image_url (str): Entrer l'adresse url de l'image.

    Returns:
        soup (BeautifulSoup): Retourne un objet de type BeautifulSoup contenant l'image à télécharger.
    """
    counter = 0
    while counter < 20:
        response = requests.get(image_url)
        if not response.ok:
            counter += 1
            print(f"Tentative de connexion avec la page {counter}/20")
            continue
        return response.content