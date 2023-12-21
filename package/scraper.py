from package import requete
from package import utilitaires
import constants

def recuperer_information_livre(url_livre):
    contenu_page = requete.recuperer_contenu_page(url_livre).find_all("div", class_="page_inner")[1]
    categorie = contenu_page.find("ul", "breadcrumb").find_all("a")[2].get_text()
    titre = contenu_page.find("ul", "breadcrumb").find_all("li")[-1].get_text()
    page_produit = contenu_page.find("article", class_="product_page")
    url_image_livre = constants.URL + page_produit.find("div", class_="item active").find("img")["src"][6:]
    description = page_produit.find_all("p")[3].get_text()
    if description == "\n\n\n\n\n\n":
        description = "Pas de description"
    informations_specifiques = page_produit.find("table", "table table-striped").find_all("td")
    upc = informations_specifiques[0].get_text()
    prix_ttc = utilitaires.conversion_monnaie_gbp_en_eur(float(informations_specifiques[3].get_text().strip("£")))
    prix_ht = utilitaires.conversion_monnaie_gbp_en_eur(float(informations_specifiques[2].get_text().strip("£")))
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
    if constants.extraction_images == True:
        toutes_les_informations_du_livre["image_directory"] = extraction_images(url_image_livre, categorie, titre.replace(":","-"))
        

    return toutes_les_informations_du_livre

def extraire_informations_des_livres_pour_une_categorie(url_categorie):
    nombre_total_livre_site = recuperer_nombre_total_livre()
    tous_les_liens_livres = []
    toutes_les_informations_livres_de_categorie = []
    numero_page = 1
    numero_livre_en_cours = 0
    numero_livre_page = 0
    contenu_page_categorie = requete.recuperer_contenu_page(url_categorie)
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
            url_pages_categorie = requete.recuperer_contenu_page(url_categorie.replace("index.html",f"page-{numero_page}.html"))
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
            print(f"""Extraction des données du livre {"0" + str(numero_livre_page) if numero_livre_page < 10 else numero_livre_page}/{int(nombre_livre_page_courante[0].get_text()) - 20 * (numero_page -1) if int(nombre_livre_page_courante[0].get_text()) - 20 * (numero_page -1) > 9 else "0" + str(int(nombre_livre_page_courante[0].get_text()) - 20 * (numero_page -1))} - Catégorie "{nom_categorie}" - Page {numero_page} sur {nombre_page}... {round(numero_livre_en_cours / nombre_total_livre_site * 100, None)}%""")
            toutes_les_informations_livres_de_categorie.append(recuperer_information_livre(lien))
        numero_page += 1
    utilitaires.enregistrement_des_donnees_csv(toutes_les_informations_livres_de_categorie)

def extraction_toutes_les_categories():
    contenu_page = requete.recuperer_contenu_page(constants.URL)
    toutes_les_categories = contenu_page.find("ul", class_="nav nav-list").find_all("a")[1:]
    for categorie in toutes_les_categories:
        extraire_informations_des_livres_pour_une_categorie(str(constants.URL + categorie["href"]))

def extraction_images(url_image, categorie_livre, nom_livre):
    contenu = requete.recuperer_image_page(url_image)
    return utilitaires.enregistrement_image(categorie_livre, nom_livre, contenu)
    
def recuperer_categories_disponibles():
    categories = {}
    liste_categorie = []
    contenu_page = requete.recuperer_contenu_page(constants.URL)
    toutes_les_categories = contenu_page.find("ul", class_="nav nav-list").find_all("a")[1:]
    for categorie in toutes_les_categories:
        categories[categorie.string.lower().replace("\n", "")[60:-52]] = (constants.URL + categorie["href"])
    constants.categories_disponibles = categories
    for cle in categories:
        liste_categorie.append(cle)
    return liste_categorie

def recuperer_titres_livres():
    nombre_livres = recuperer_nombre_total_livre()
    page_courante = 1
    numero_livre_en_cours = 0
    contenu_page = requete.recuperer_contenu_page(constants.URL)
    nombre_pages = int(contenu_page.find("li", class_="current").get_text().replace(" ","").replace("\n","")[7:])
    for i in range(nombre_pages):
        if page_courante == 1:
            contenu_page_courante = contenu_page
        else:
            contenu_page_courante = requete.recuperer_contenu_page(constants.URL + f"catalogue/page-{page_courante}.html")
        livre_in_page = contenu_page_courante.find_all("li", class_="col-xs-6 col-sm-4 col-md-3 col-lg-3")
        for livre in livre_in_page:
            nom = livre.find("h3").find("a")["title"]
            lien = str(constants.URL + livre.find("h3").find("a")["href"])
            constants.nom_livre_et_liens[nom] = lien
            numero_livre_en_cours += 1
        page_courante += 1
        print(f"Récupération des données en cours ... {round(numero_livre_en_cours / nombre_livres * 100, None)}%")

def recuperer_nombre_total_livre():
    contenu_page = requete.recuperer_contenu_page(constants.URL)
    constants.nombre_livre_total = int(contenu_page.find("form", class_="form-horizontal").find("strong").get_text())
    return constants.nombre_livre_total



