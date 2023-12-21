from package.requete import recuperer_contenu_page
from package.utilitaires import enregistrement_des_donnees_csv, conversion_monnaie_gbp_en_eur
import constants

def recuperer_information_livre(url_livre):
    contenu_page = recuperer_contenu_page(url_livre).find_all("div", class_="page_inner")[1]
    categorie = contenu_page.find("ul", "breadcrumb").find_all("a")[2].get_text()
    titre = contenu_page.find("ul", "breadcrumb").find_all("li")[-1].get_text()
    page_produit = contenu_page.find("article", class_="product_page")
    url_image_livre = constants.URL + page_produit.find("div", class_="item active").find("img")["src"][6:]
    description = page_produit.find_all("p")[3].get_text()
    if description == "\n\n\n\n\n\n":
        description = "Pas de description"
    informations_specifiques = page_produit.find("table", "table table-striped").find_all("td")
    upc = informations_specifiques[0].get_text()
    prix_ttc = conversion_monnaie_gbp_en_eur(float(informations_specifiques[3].get_text().strip("£")))
    prix_ht = conversion_monnaie_gbp_en_eur(float(informations_specifiques[2].get_text().strip("£")))
    quantite_disponible = int("".join([caractere for caractere in informations_specifiques[5].get_text() if caractere.isdigit()]))
    note = constants.etoiles[page_produit.find("p", class_="star-rating")["class"][1]]
    toutes_les_informations_du_livre = {
        "product_page_url": url_livre,
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

def extraire_informations_des_livres_pour_une_categorie(url_categorie):
    tous_les_liens_livres = []
    toutes_les_informations_livres_de_categorie = []
    numero_page = 1
    numero_livre_en_cours = 0
    numero_livre_page = 0
    contenu_page_categorie = recuperer_contenu_page(url_categorie)
    nom_categorie = contenu_page_categorie.title.get_text().replace("\n","")[4:-33]
    nombre_total_livre_categorie = int(contenu_page_categorie.find("form", class_="form-horizontal").find("strong").get_text())
    try:
        nombre_page = int(contenu_page_categorie.find("li", class_="current").get_text().replace(" ","").replace("\n","")[-1:])
    except AttributeError:
        nombre_page = 1
    while numero_livre_en_cours < nombre_total_livre_categorie:
        if nombre_page == 1:
            url_pages_categorie = contenu_page_categorie
            nombre_livre_page_courante = url_pages_categorie.find("form", class_="form-horizontal").find_all("strong")
        else:
            url_pages_categorie = recuperer_contenu_page(url_categorie.replace("index.html",f"page-{numero_page}.html"))
            nombre_livre_page_courante = url_pages_categorie.find("form", class_="form-horizontal").find_all("strong")[2:]
        livres_page = url_pages_categorie.find_all("li", class_="col-xs-6 col-sm-4 col-md-3 col-lg-3")
        liens_livres = []
        for livre in livres_page:
            liens_livres.append(livre.find("a")["href"].replace("../../../", constants.URL + "catalogue/"))
            numero_livre_en_cours += 1
            tous_les_liens_livres.append(liens_livres)
        for lien in liens_livres:
            if numero_livre_page < 20:
                numero_livre_page += 1
            else:
                numero_livre_page = 1
            # print(f"""Extractions des données du livre {str(0) + str(numero_livre_page) if numero_livre_page < 10 else numero_livre_page}/{int(nombre_livre_page_courante[0].get_text()) - 20 * (numero_page -1)} - Catégorie "{nom_categorie}" - Page {numero_page} sur {nombre_page}""")
            print(f"""Extraction des données du livre {"0" + str(numero_livre_page) if numero_livre_page < 10 else numero_livre_page}/{int(nombre_livre_page_courante[0].get_text()) - 20 * (numero_page -1) if int(nombre_livre_page_courante[0].get_text()) - 20 * (numero_page -1) > 10 else "0" + str(int(nombre_livre_page_courante[0].get_text()) - 20 * (numero_page -1))} - Catégorie "{nom_categorie}" - Page {numero_page} sur {nombre_page}""")
            toutes_les_informations_livres_de_categorie.append(recuperer_information_livre(lien))
        numero_page += 1
    enregistrement_des_donnees_csv(toutes_les_informations_livres_de_categorie)

def extraction_toutes_les_categories():
    contenu_page = recuperer_contenu_page(constants.URL)
    toutes_les_categories = contenu_page.find("ul", class_="nav nav-list").find_all("a")[1:]
    for categorie in toutes_les_categories:
        extraire_informations_des_livres_pour_une_categorie(str(constants.URL + categorie["href"]))