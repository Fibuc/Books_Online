from pprint import pprint
import requests
from bs4 import BeautifulSoup
import csv

URL = "https://books.toscrape.com/"
url = "https://books.toscrape.com/catalogue/category/books/classics_6/index.html"
url2 = "https://books.toscrape.com/catalogue/category/books/romance_8/index.html"

etoiles = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5
}

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

def recuperer_information_livre(url):
    elements_page = recuperer_contenu_page(url).find_all("div", class_="page_inner")[1]
    categorie = elements_page.find("ul", "breadcrumb").find_all("a")[2].get_text()
    titre = elements_page.find("ul", "breadcrumb").find_all("li")[-1].get_text()
    url_page_livre = url
    page_produit = elements_page.find("article", class_="product_page")
    url_image_livre = URL + page_produit.find("div", class_="item active").find("img")["src"][6:]
    description = page_produit.find_all("p")[3].get_text()
    informations_specifiques = page_produit.find("table", "table table-striped").find_all("td")
    upc = informations_specifiques[0].get_text()
    prix_ttc = conversion_monnaie_gbp_en_eur(float(informations_specifiques[3].get_text().strip("£")))
    prix_ht = conversion_monnaie_gbp_en_eur(float(informations_specifiques[2].get_text().strip("£")))
    quantite_disponible = int("".join([caractere for caractere in informations_specifiques[5].get_text() if caractere.isdigit()]))
    note = etoiles[page_produit.find("p", class_="star-rating")["class"][1]]
    toutes_les_informations_du_livre = {
        "product_page_url": url_page_livre,
        "universal_product_code": upc,
        "title": titre,
        "price_including_tax": prix_ttc,
        "price_excluding_tax": prix_ht,
        "number_available": quantite_disponible,
        "product_description": description,
        "category": categorie,
        "review_rating": note,
        "image_url": url_image_livre,
    }
    return toutes_les_informations_du_livre


def conversion_monnaie_gbp_en_eur(montant):
    contenu = recuperer_contenu_page("https://www.boursorama.com/bourse/devises/taux-de-change-euro-livresterling-EUR-GBP/")
    taux_de_change = contenu.find("div", class_="c-faceplate__price--inline").find("span", class_="c-instrument--last").get_text()
    montant_euros = montant / float(taux_de_change)
    return round(montant_euros, 2)

def extraire_informations_des_livres_pour_une_categorie(url):
    tous_les_liens_livres = []
    toutes_les_informations_livres_de_categorie = []
    numero_page = 1
    numero_livre_en_cours = 0
    numero_livre_page = 0
    url_categorie = recuperer_contenu_page(url)
    nom_categorie = url_categorie.title.get_text().replace("\n","")[4:-33]
    nombre_total_livre_categorie = int(url_categorie.find("form", class_="form-horizontal").find("strong").get_text())
    boucle_lien = 0
    boucle_livre = 0
    try:
        nombre_page = int(url_categorie.find("li", class_="current").get_text().replace(" ","").replace("\n","")[-1:])
    except AttributeError:
        nombre_page = 1
    while numero_livre_en_cours < nombre_total_livre_categorie:
        if nombre_page == 1:
            url_pages_categorie = url_categorie
            nombre_livre_page_courante = url_pages_categorie.find("form", class_="form-horizontal").find_all("strong")
        else:
            url_pages_categorie = recuperer_contenu_page(url.replace("index.html",f"page-{numero_page}.html"))
            nombre_livre_page_courante = url_pages_categorie.find("form", class_="form-horizontal").find_all("strong")[2:]
        livres_page = url_pages_categorie.find_all("li", class_="col-xs-6 col-sm-4 col-md-3 col-lg-3")
        liens_livres = []
        for livre in livres_page:
            liens_livres.append(livre.find("a")["href"].replace("../../../", URL + "catalogue/"))
            numero_livre_en_cours += 1
            boucle_livre += 1
            tous_les_liens_livres.append(liens_livres)
        for lien in liens_livres:
            if numero_livre_page < 20:
                numero_livre_page += 1
            else:
                numero_livre_page = 1
            boucle_lien += 1
            print(f"""Extractions des données du livre {str(0) + str(numero_livre_page) if numero_livre_page < 10 else numero_livre_page}/{int(nombre_livre_page_courante[0].get_text()) - 20 * (numero_page -1)} - Catégorie "{nom_categorie}" - Page {numero_page} sur {nombre_page}""")
            toutes_les_informations_livres_de_categorie.append(recuperer_information_livre(lien))
        numero_page += 1
        
    
    return enregistrement(toutes_les_informations_livres_de_categorie)


def enregistrement_des_donnees_csv(donnees):
    with open("fichier.csv","w", encoding="UTF-8", newline="") as fichier_csv:
        writer = csv.DictWriter(fichier_csv, fieldnames=donnees[0].keys())
        writer.writeheader()
        writer.writerows(donnees)
