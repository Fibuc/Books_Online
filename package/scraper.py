from package import request, utils
import constants

def fetch_book_informations(book_url: str):
    """Récupère l'intégralité des informations d'un livre sous forme de dictionnaire.
    Si l'option de télécharger les images a été validé, il parsera également l'image du livre.

    Args:
        book_url (str): Entrer l'adresse url de la page html du livre.

    Returns:
        all_book_informations (dict): Retourne toutes les informations du livre sous forme de dictionnaire.
    """
    page_content = request.get_page_content(book_url).find_all("div", class_="page_inner")[1] # Récupère le contenu de la page
    category = page_content.find("ul", "breadcrumb").find_all("a")[2].get_text()
    title = page_content.find("ul", "breadcrumb").find_all("li")[-1].get_text()
    product_page = page_content.find("article", class_="product_page")
    image_url = constants.URL + product_page.find("div", class_="item active").find("img")["src"][6:]
    product_description = product_page.find_all("p")[3].get_text()
    if product_description == "\n\n\n\n\n\n":
        product_description = "Pas de description"
    specific_information = product_page.find("table", "table table-striped").find_all("td")
    universal_product_code = specific_information[0].get_text()
    price_including_tax = utils.convert_currency_gbp_to_eur(float(specific_information[3].get_text().strip("£")))
    price_excluding_tax = utils.convert_currency_gbp_to_eur(float(specific_information[2].get_text().strip("£")))
    number_available = int("".join([character for character in specific_information[5].get_text() if character.isdigit()]))
    review_rating = constants.stars[product_page.find("p", class_="star-rating")["class"][1]]
    all_book_informations = {
        "product_page_url": book_url,
        "universal_product_code": universal_product_code,
        "title": title,
        "price_including_tax": price_including_tax,
        "price_excluding_tax": price_excluding_tax,
        "number_available": number_available,
        "product_description": product_description,
        "category": category,
        "review_rating": review_rating,
        "image_url": image_url,
    }
    if constants.extract_images:
        all_book_informations["image_directory"] = extract_images(image_url, category, title) # Ajoute au dictionnaire le lien répertoire    
    return all_book_informations

def extract_informations_from_books_for_a_category(category_url: str):
    """Récupère l'intégralité des informations de tous les livres d'une catégorie et enregistre en csv grâce à la fonction save_data_to_csv()

    Args:
        category_url (str): Entrer l'adresse url de la page html de la catégorie.
        """
    all_books_links = []
    all_books_informations_for_category = []
    page_number = 1
    current_book_number = 0
    current_book_number_of_page = 0
    category_page_content = request.get_page_content(category_url) # Récupère le contenu de la page
    category_name = category_page_content.title.get_text().replace("\n","")[4:-33]
    total_number_of_books_in_category = int(category_page_content.find("form", class_="form-horizontal").find("strong").get_text()) # Récupère nombre total livre de la catégorie
    try:
        number_of_pages = int(category_page_content.find("li", class_="current").get_text().replace(" ","").replace("\n","")[-1:])
    except AttributeError:
        number_of_pages = 1
    while current_book_number < total_number_of_books_in_category:
        if number_of_pages == 1:
            category_pages_url = category_page_content
            number_of_books_in_current_page = category_pages_url.find("form", class_="form-horizontal").find_all("strong")
        else:
            category_pages_url = request.get_page_content(category_url.replace("index.html",f"page-{page_number}.html"))
            number_of_books_in_current_page = category_pages_url.find("form", class_="form-horizontal").find_all("strong")[2:]
        books_in_page = category_pages_url.find_all("li", class_="col-xs-6 col-sm-4 col-md-3 col-lg-3")
        books_links = []
        for book in books_in_page:  # Boucle pour récupérer les liens des livres de la page
            books_links.append(book.find("a")["href"].replace("../../../", constants.URL + "catalogue/"))
            current_book_number += 1
            all_books_links.append(books_links)
        for link in books_links:    # Boucle pour exécuter l'extraction des pages produits
            if current_book_number_of_page < 20:
                current_book_number_of_page += 1
            else:
                current_book_number_of_page = 1
            current_book_number_of_page_str = (str(current_book_number_of_page) if current_book_number_of_page > 9 else f"0{current_book_number_of_page}")
            number_of_books_in_page = int(number_of_books_in_current_page[0].get_text()) - 20 * (page_number -1)
            number_of_books_in_page_str = (str(number_of_books_in_page) if number_of_books_in_page > 9 else f"0{number_of_books_in_page}")
            print(f"Extraction des données du livre {current_book_number_of_page_str}/{number_of_books_in_page_str} - Catégorie \"{category_name}\" - Page {page_number} sur {number_of_pages}")
            all_books_informations_for_category.append(fetch_book_informations(link)) # Récupère info livres dans une liste de dictionnaires
        page_number += 1
    utils.save_data_to_csv(all_books_informations_for_category) # Enregistre au format CSV

def extract_all_categories():
    """Extrait toutes les catégories disponible sur le site.
    """
    page_content = request.get_page_content(constants.URL)
    all_categories = page_content.find("ul", class_="nav nav-list").find_all("a")[1:]
    for category in all_categories:
        extract_informations_from_books_for_a_category(str(constants.URL + category["href"]))

def extract_images(image_url: str, book_category: str, book_name: str):
    """Extrait l'image de l'adresse url. 

    Args:
        image_url (str): Entrer l'url de l'image.
        book_category (str): Entrer la catégorie du livre associé à l'image.
        book_name (str): Entrer le nom du livre associé à l'image.
    """
    content = request.get_page_image(image_url)
    return utils.save_image(book_category, book_name, content)
    
def fetch_available_categories():
    """Recherche et affiche toutes les catégories disponible sur le site.

    Returns:
        categories_list (list): Retourne une liste comprenant toutes les catégories du site.
    """
    categories_names_and_links = {}
    categories_list = []
    page_content = request.get_page_content(constants.URL)
    all_categories = page_content.find("ul", class_="nav nav-list").find_all("a")[1:]
    for category in all_categories:
        categories_names_and_links[category.string.lower().replace("\n", "")[60:-52]] = (constants.URL + category["href"])
    constants.available_categories = categories_names_and_links
    for key in categories_names_and_links:
        categories_list.append(key)
    return categories_list
