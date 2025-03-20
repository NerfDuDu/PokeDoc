# Pokemon TCG


## Description


Notre projet vise à présenter une variété de Pokémon en extrayant leurs données d'un fichier JSON. Chaque Pokémon sera introduit en spécifiant son nom.
Les images appropriées seront automatiquement récupérées sur le web afin de fournir une interface graphique captivante.
Le but est de concevoir une application interactive qui facilite la navigation et la découverte de divers Pokémon, notamment grâce à l'ajout d'une barre de recherche.


## Fonctionnalités


- **Affichage du Pokédex** : Recherche de Pokémon grâce au nom.
- **Interface utilisateur** : Navigation fluide entre les différentes scènes via une barre d'outils.


## Installation


### Prérequis


- Python 3.8+
- PySide6
- Requests
- JSON (intégré à Python)


### Étapes d'installation


1. Clonez ce dépôt :
   ```sh
   git clone https://github.com/sltcvtfk/pokemon-tcg-pyside6git
   cd pokemon-tcg-pyside6
   ```
2. Installez les dépendances :
   ```sh
   pip install -r requirements.txt
   ```


## Utilisation


Lancez l'application avec la commande :


```sh
python main.py
```


## Architecture du Projet


```
📂 PokeDoc      
│── 📂 image                 # Icônes et images
│── 📂 json                # Fichiers JSON (Pokedex)
│── 📂 UML                 # Diagramme de classe
│── 📜 LICENSE             # Fichier de la LICENSE utilisé
│── 📜 README.md           # Documentation      
│── 📜 main.py             # Fichier Python principal
│── 📜 requirements.txt    # Dépendances obligatoires
|── 📜 COPYING.LESSER      # Copie complète de la licence LGPL v3 
```


## Technologies utilisées


- **Python** (PySide6, JSON, Requests)
- **PlantUML** (Diagrammes UML pour la conception)
- **GitHub** (Partage du projet)


## Informations supplémentaires


- **pokemon.json** Correction d'un problème avec le nom de certains pokémons


## Auteurs
-<span style="color:purple">
**Marco Onet**
</span> || [**@NerfDuDu**](https://github.com/NerfDuDu)


**Tâches** : Je me suis occupé de la disposition des différentes scènes et images dans l'inventaire, de l'affichage du Pokémon dans le menu, ainsi que de l'interaction avec le bouton "Tirer", qui change aléatoirement le Pokémon affiché à l'accueil.


-<span style="color:cyan">
**Zishaan Mellon**
</span> || [**@ZWN410**](https://github.com/ZWN410)


**Tâches** : Je me suis occupé de la disposition des différentes scènes et images dans l'inventaire, de l'affichage des Pokémon, ainsi que de l'implémentation des boutons permettant la navigation entre les différentes pages. J'ai également contribué à la liaison de la base de données au <span style="color:orange"> **Main**</span>, en veillant à assurer une synchronisation fluide des données et une récupération efficace des informations stockées.


## Licence

Ce projet est sous licence GNU Lesser General Public License version 3.  
Voir le fichier `LICENSE` pour plus de détails.
