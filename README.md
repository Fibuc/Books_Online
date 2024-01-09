
# Scraper Books Online

Ce scraper permet de récupérer l'intégralité des données des livres sur le site [Books to Scrape](https://books.toscrape.com/) et de les extraire dans des fichiers csv classés par catégorie. Vous aurez également la possibilité de télécharger les images des livres.

Lors du lancement, vous aurez la possibilité de sélectionner l'extraction des données de tous les livres ou bien les données d'une seule catégorie.
## Installation

IMPORTANT : Le script principal utilise les match cases. Pour cela, vous aurez donc besoin d'une version minimum de python 3.10 pour pouvoir le lancer.

### Cloner le dépôt

Pour cloner le dépôt, vous devrez ouvrir le terminal et effectuer la commande suivante dans le dossier de votre choix :
```bash
    git clone https://github.com/Fibuc/Books_Online
```

### Créer un environnement virtuel

Ensuite, vous aurez besoin de créer un environnement virtuel que vous devrez nommer "env" afin d'éviter de le push dans le repository. Si toutefois, vous désirer utiliser un autre nom d'environnement, merci de bien vouloir l'ajouter au ".gitignore".


Ouvrir le terminal et se rendre dans le dossier du dépôt local "Books_Online" puis taper la commande suivante :
```bash
    python -m venv env
```

### Activer votre environnement virtuel

Pour activer votre environnement virtuel la méthode est différente selon votre système d'exploitation.

Linux & MacOS :
```bash
    source chemin_vers_votre_env/bin/activate
```
Windows : 
```bash
    chemin_vers_votre_env\Scripts\activate
```

### Installer les packages

Enfin, lorsque vous aurez activé votre environnement virtuel, vous aurez également besoin d'installer les packages essentiels pour le lancement disponibles dans le requirements.txt

```bash
    pip install -r requirements.txt
```
    
Veillez également à bien vous situer sur la branche "main" lors de l'execution de script.py.