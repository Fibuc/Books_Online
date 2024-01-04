import constants
from package import utils, scraper

print(constants.MENU_HEADER)

while not constants.valid_directory:
    constants.saved_files_directory = input("Veuillez insérer le répertoire d'enregistrement : ")
    utils.check_directory()

while constants.start:
    print(constants.MENU_OPTION)
    user_choice = input("Quel est votre choix ? : ")
    match user_choice:
        case "1":
            utils.image_download_choice()
            scraper.extract_all_categories()
        case "2":
            category_list = scraper.fetch_available_categories()
            print(category_list)
            selected_category = input("Veuillez choisir la catégorie : ").lower()
            while selected_category not in category_list:
                print("La catégorie indiquée n'existe pas.")
                selected_category = input("Veuillez choisir la catégorie : ").lower()
            utils.image_download_choice()
            scraper.extract_informations_from_books_for_a_category(constants.available_categories[selected_category])
            print("")
        case "3":
            old_directory = constants.saved_files_directory
            constants.saved_files_directory = input("Veuillez indiquer le nouveau répertoire : ")
            if constants.saved_files_directory == "q":
                constants.saved_files_directory = old_directory
            utils.check_directory()
        case "4":
            print("Fermeture de l'application")
            constants.start = False
        case _:
            print("Veuillez choisir une option valide.\n")