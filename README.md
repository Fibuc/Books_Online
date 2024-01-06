# Scraper Books Online

Ce scraper permet de récupérer l'intégralité des données des livres sur le site [Books to Scrape](https://books.toscrape.com/) et de les extraire dans des fichiers CSV classés par catégorie. Vous aurez également la possibilité de télécharger les images des livres.

Lors du lancement, vous aurez la possibilité de sélectionner l'extraction des données de tous les livres ou bien les données des livres d'une seule catégorie.
## Installation

Le script principal utilise les match cases. Pour cela, vous aurez donc besoin d'une version minimum de python 3.10 pour pouvoir le lancer.

De plus, vous aurez besoin de créer un environnement virtuel que vous devrez nommer "env" afin d'éviter de le push dans le repository. Si toutefois, vous désirer utiliser un autre nom d'environnement, merci de bien vouloir l'ajouter au ".gitignore".

Vous aurez également besoin d'installer les packages essentiels pour le lancement disponibles dans le fichier requirements.txt.

```bash
    pip install -r requirements.txt
```
    
Veillez également à bien vous situer sur la branche "main" lors de l'execution de script.py.