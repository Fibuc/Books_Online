import requests
from bs4 import BeautifulSoup

URL = "https://books.toscrape.com/"
url = "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"

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
        return "Erreur de connexion avec l'url"

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
