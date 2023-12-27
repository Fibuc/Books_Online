from package.request import get_page_content
import csv
import constants
from pathlib import Path
from datetime import datetime

def convert_currency_gbp_to_eur(amont:float):
    content = get_page_content("https://www.boursorama.com/bourse/devises/taux-de-change-euro-livresterling-EUR-GBP/")
    exchange_rate = content.find("div", class_="c-faceplate__price--inline").find("span", class_="c-instrument--last").get_text()
    amount_in_euros = amont / float(exchange_rate)
    return round(amount_in_euros, 2)

def save_data_to_csv(data:list):
    file_name = (f"categorie_{(data[0]['category']).lower()} {str(datetime.now())[:-7]}.csv").replace(" ","_").replace(":","-")
    file_directory = directory_for_saving_csv_file() / file_name
    with open(file_directory,"w", encoding="UTF-8", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

def directory_for_saving_csv_file():
    path = Path(constants.saved_files_directory)
    return path

def save_image(category:str, file_name:str, content):
    path = Path(constants.saved_files_directory)
    image_folder = path / "Images" / category
    filtered_file_name = remove_special_characters(file_name)
    complete_directory = image_folder / f"{filtered_file_name}.jpg"
    image_folder.mkdir(parents=True, exist_ok=True)
    with open(complete_directory, "wb") as image_file:
        image_file.write(content)
    return complete_directory

def check_directory():
    path = Path(constants.saved_files_directory)
    if path.exists() == False:
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

def remove_special_characters(text:str):
    transTable = text.maketrans("""<>:“"'/|?*""", "  -  .    ")
    filtred_text = text.translate(transTable)
    return filtred_text

