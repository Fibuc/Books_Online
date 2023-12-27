import requests
from bs4 import BeautifulSoup

def get_page_content(page_url:str):
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
    counter = 0
    while counter < 20:
        response = requests.get(image_url)
        if not response.ok:
            counter += 1
            print(f"Tentative de connexion avec la page {counter}/20")
            continue
        return response.content