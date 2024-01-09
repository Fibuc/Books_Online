import csv
from pathlib import Path
from datetime import datetime

from package.request import get_page_content
import constants

def convert_currency_gbp_to_eur(amont: float):
    """Convertisseur de devise entre GBP et EUR

    Args:
        amont (float): Entrer le montant de devise.

    Returns:
        round(amount_in_euros, 2): Retourne le montant converti en arrondissant au centième.
    """
    content = get_page_content("https://www.boursorama.com/bourse/devises/taux-de-change-euro-livresterling-EUR-GBP/")
    exchange_rate = content.find("div", class_="c-faceplate__price--inline").find("span", class_="c-instrument--last").get_text()
    amount_in_euros = amont / float(exchange_rate)
    return round(amount_in_euros, 2)

def save_data_to_csv(data:list):
    """Enregistre les données d'une catégorie en fichier CSV.

    Args:
        data (list): Entrer les données en liste.
    """
    file_name = (f"{(data[0]['category']).lower()} {str(datetime.now())[:-7]}.csv").replace(" ","_").replace(":","-")
    file_directory = directory_for_saving_csv_file() / file_name
    with open(file_directory,"w", encoding="UTF-8", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

def directory_for_saving_csv_file():
    """Sélectionne le chemin pour l'enregistrement des fichiers CSV.

    Returns:
        path(Path): Retourne un chemin de type Path.
    """
    path = Path(constants.saved_files_directory)
    return path

def save_image(category:str, file_name:str, content):
    """Enregistre l'image dans le dossier sélectionné avec une limite de longueur du répertoire de 256 caractères.

    Args:
        category (str): Entrer le nom de la catégorie.
        file_name (str): Entrer le nom du fichier.
        content (_type_): Contenu du lien url de l'image.

    Returns:
        complete_directory (path): Retourne le chemin complet de l'image dans le dossier local.
    """
    path = Path(constants.saved_files_directory)
    image_folder = path / "Images" / category
    filtered_file_name = filter_filename_characters(file_name)
    complete_directory = image_folder / f"{filtered_file_name}.jpg"
    lenght_directory = len(str(complete_directory))
    lenght_max_directory = 256
    if lenght_directory > lenght_max_directory:
        complete_directory = Path(str(complete_directory)[:-(lenght_directory - lenght_max_directory) - len(complete_directory.suffix)] + ".jpg")
    image_folder.mkdir(parents=True, exist_ok=True)
    with open(complete_directory, "wb") as image_file:
        image_file.write(content)
    return complete_directory

def check_directory():
    """Vérifie si le dossier est valide ou non et demande si l'on veut la création s'il n'est pas présent.
    """
    path = Path(constants.saved_files_directory)
    if not path.exists():
        while str(path.parent) == ".":
            print("Chemin de répertoire non valide.")
            return False
        double_decline = False
        creation_choice = input("Le chemin n'existe pas, voulez-vous le créer ? (y/n) : ")
        match creation_choice:
            case "y":
                constants.valid_directory = True
            case "n":
                while double_decline == False:
                    select_different_directory = input("Voulez-vous choisir un autre répertoire ? (y/n) : ")
                    match select_different_directory:
                        case "y":
                            constants.valid_directory = False
                            return
                        case "n":
                            double_decline = True
                        case _:
                            print("Veuillez choisir une option valide.\n")
                else:
                    print("Fermeture de l'application")
                    constants.valid_directory = True
                    constants.start = False       
    constants.valid_directory = True

def image_download_choice():
    """Demande si l'on veut enregistrer les images lors de l'extraction des informations des livres.
    """
    image_download_choice = ""
    while image_download_choice != "y" or "n":
        image_download_choice = input("Voulez-vous télécharger les images ? (y/n) : ")
        match image_download_choice:
            case "y":
                constants.extract_images = True
                break
            case "n":
                constants.extract_images = False
                break
            case _ :
                print("Veuillez choisir une option valide.")

def filter_filename_characters(text: str):
    """Filtre les caractères invalides pour la création de fichiers dans le système d'exploitation.
    """
    transtable = text.maketrans("""<>:“"'/|?*""", "  -  .    ")
    filtred_text = text.translate(transtable)
    return filtred_text