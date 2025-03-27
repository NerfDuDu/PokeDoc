import json
import os
import random
from PySide6.QtWidgets import (QGraphicsView, QMainWindow, QWidget, QApplication, 
                               QHBoxLayout, QPushButton, QVBoxLayout, QLabel, 
                               QGraphicsScene, QGraphicsPixmapItem, QGraphicsRectItem, QGridLayout, QLineEdit)
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtCore import QUrl, Slot, Qt
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkReply, QNetworkRequest

class Scene(QGraphicsScene):
    def __init__(self, index=0, random_pokemon=None, parent=None):
        super().__init__(parent)
        self.index = index
        self.fond = QGraphicsRectItem(0, 0, 0, 0)
        self.addItem(self.fond)

        # Charger le JSON une seule fois
        with open(os.path.join('pokedex.json'), encoding="utf8") as f:
            self.contenu = json.load(f)

        # Si un Pokémon aléatoire est fourni, l'ajouter à la scène
        if random_pokemon:
            self.ajoute_pokemon_aleatoire(random_pokemon)

        # Ajouter le Pokémon courant
        self.ajoute(self.get_image())

    def get_image(self):
        return self.contenu[self.index]["image"]["thumbnail"]
    
    def get_type(self):
        return self.contenu[self.index]["type"][0]
    
    def get_nom(self):
        return self.contenu[self.index]["name"]["french"]
    
    def ajoute(self, url: str):
        self.manager = QNetworkAccessManager(self)
        self.manager.finished.connect(self.chargement_fini)
        self.manager.get(QNetworkRequest(QUrl.fromUserInput(url)))

    @Slot(QNetworkReply)
    def chargement_fini(self, reponse: QNetworkReply):
        if reponse.error() == QNetworkReply.NoError:
            image = QImage()
            image.loadFromData(reponse.readAll())
            pixmap = QPixmap.fromImage(image)
            self.pixmap_item = QGraphicsPixmapItem(pixmap)
            self.pixmap_item.setPos(0, 0)
            self.addItem(self.pixmap_item)
        reponse.deleteLater()

    def ajoute_pokemon_aleatoire(self, pokemon):
        # Ajouter un Pokémon aléatoire en haut de la scène
        name = pokemon["name"]["french"]
        image_url = pokemon["image"]["thumbnail"]

        # Charger l'image du Pokémon aléatoire
        request = QNetworkRequest(QUrl(image_url))
        self.manager = QNetworkAccessManager(self)
        reply = self.manager.get(request)
        reply.finished.connect(lambda r=reply, name=name: self.afficher_pokemon_aleatoire(r, name))

    @Slot(QNetworkReply, str)
    def afficher_pokemon_aleatoire(self, reponse: QNetworkReply, name: str):
        if reponse.error() == QNetworkReply.NoError:
            image = QImage()
            image.loadFromData(reponse.readAll())
            pixmap = QPixmap.fromImage(image).scaled(100, 100, Qt.KeepAspectRatio)

            # Créer un QGraphicsPixmapItem pour afficher l'image du Pokémon aléatoire
            self.random_pokemon_item = QGraphicsPixmapItem(pixmap)
            self.random_pokemon_item.setPos(80, 20)  # Positionner l'image du Pokémon aléatoire

            # Ajouter le QGraphicsPixmapItem à la scène
            self.addItem(self.random_pokemon_item)

        reponse.deleteLater()


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.page_index = 0
        self.total_pages = 45
        self.recherche_texte = ""  # Texte de recherche

        # Charger le Pokédex une seule fois
        with open(os.path.join('pokedex.json'), encoding="utf8") as f:
            self.pokedex = json.load(f)

        self.menu()

    def menu(self):
        # Passer texte de recherche et Pokémon aléatoire au menu
        random_pokemon = self.get_random_pokemon()
        self.centralWidget = MENUS(self.recherche_texte, random_pokemon, self.pokedex)
        self.setCentralWidget(self.centralWidget)
        self.centralWidget.btn_inventaire.clicked.connect(self.inventaire)

    def inventaire(self):
        self.centralWidget = SAKA_DHO(self.page_index, self.total_pages, self.recherche_texte, self.pokedex)
        self.setCentralWidget(self.centralWidget)
        
        self.centralWidget.btn_menu.clicked.connect(self.menu)
        self.centralWidget.btn_prec.clicked.connect(self.page_precedente)
        self.centralWidget.btn_suiv.clicked.connect(self.page_suivante)

    def page_suivante(self):
        if self.page_index < self.total_pages - 1:
            self.page_index += 1
            self.inventaire()

    def page_precedente(self):
        if self.page_index > 0:
            self.page_index -= 1
            self.inventaire()

    def get_random_pokemon(self):
        # Sélectionner un Pokémon aléatoire
        return random.choice(self.pokedex)

class SAKA_DHO(QWidget):
    def __init__(self, page_index, total_pages, recherche_texte="", pokedex=None):
        super().__init__()
        self.page_index = page_index
        self.total_pages = total_pages
        self.recherche_texte = recherche_texte  # Garde l'état de la recherche
        self.pokedex = pokedex  # Utiliser le Pokédex fourni

        self.layoutsakado = QVBoxLayout(self)
        self.barre = QLineEdit(self)
        self.barre.setText(self.recherche_texte)  # Garder le texte de recherche actuel
        self.barre.setPlaceholderText("Rechercher un Pokémon")
        self.barre.textChanged.connect(self.rechercher_pokemon)  # Filtre les Pokémon lors de la recherche
        self.layoutsakado.addWidget(self.barre)

        self.vue = QWidget()
        self.gridlayout = QGridLayout()
        self.vue.setLayout(self.gridlayout)

        self.network_manager = QNetworkAccessManager(self)

        self.afficher_pokemons()

        self.layoutsakado.addWidget(self.vue)

        self.pa = QLabel("Page")
        self.layoutsakado.addWidget(self.pa)

        self.page = QLabel(str(self.page_index + 1))
        self.layoutsakado.addWidget(self.page)

        self.menu = QWidget()
        
        self.layoutButtons = QHBoxLayout()
        self.menu.setLayout(self.layoutButtons)

        self.btn_prec = QPushButton("<")
        self.btn_prec.setEnabled(self.page_index > 0)
        self.layoutButtons.addWidget(self.btn_prec)

        self.btn_menu = QPushButton("Menu")
        self.layoutButtons.addWidget(self.btn_menu)

        self.btn_suiv = QPushButton(">")
        self.btn_suiv.setEnabled(self.page_index < self.total_pages - 1)
        self.layoutButtons.addWidget(self.btn_suiv)

        self.layoutsakado.addWidget(self.menu)

    def afficher_pokemons(self, pokemons=None):
        if pokemons is None:
            pokemons = self.pokedex

        # Vider le layout pour ajouter les nouveaux éléments
        for i in reversed(range(self.gridlayout.count())):
            self.gridlayout.itemAt(i).widget().setParent(None)

        # Générer les Pokémon 20 par page
        for i in range(5):
            for j in range(4):
                num = i * 4 + j + self.page_index * 20

                if num < len(pokemons): 
                    pokemon = pokemons[num]
                    name = pokemon["name"]["french"]
                    image_url = pokemon["image"]["thumbnail"]

                    widget_pokemon = QWidget()
                    layout_pokemon = QVBoxLayout(widget_pokemon)

                    label_image = QLabel()
                    label_image.setAlignment(Qt.AlignCenter)

                    request = QNetworkRequest(QUrl(image_url))
                    reply = self.network_manager.get(request)
                    reply.finished.connect(lambda r=reply, l=label_image: self.charger_image(r, l))

                    label_nom = QLabel(name)
                    label_nom.setAlignment(Qt.AlignCenter)

                    layout_pokemon.addWidget(label_image)
                    layout_pokemon.addWidget(label_nom)

                    self.gridlayout.addWidget(widget_pokemon, i, j)

    @Slot(QNetworkReply, QLabel)
    def charger_image(self, reponse: QNetworkReply, label: QLabel):
        if reponse.error() == QNetworkReply.NoError: #vérifie si la réponse réseau ne contient pas d'erreur, puis charge les données de limage
            image = QImage()
            image.loadFromData(reponse.readAll())
            pixmap = QPixmap.fromImage(image).scaled(100, 100, Qt.KeepAspectRatio)
            label.setPixmap(pixmap)
        reponse.deleteLater()
        """
        Remarque:
            - Si une erreur est détectée dans la réponse réseau, l'image ne sera pas chargée.
            - La méthode appelle `deleteLater()` sur l'objet `reponse` pour libérer les ressources.
        """

    @Slot()
    def rechercher_pokemon(self):
        self.recherche_texte = self.barre.text().strip().lower()  # Met à jour le texte de recherche
        if self.recherche_texte:
            pokemons_filtres = [pokemon for pokemon in self.pokedex if self.recherche_texte in pokemon["name"]["french"].lower()]
            self.afficher_pokemons(pokemons_filtres)
        else:
            self.afficher_pokemons()  # Afficher tous les Pokémon si aucun texte de recherche

class MENUS(QWidget):
    def __init__(self, recherche_texte="", random_pokemon=None, pokedex=None):
        super().__init__()
        self.layoutPrincipal = QVBoxLayout(self)
        self.pokedex = pokedex  # Stocker le Pokédex
        self.random_pokemon = random_pokemon  # Stocker le Pokémon aléatoire actuel

        # Créer une scène et une vue pour la carte
        self.scene = QGraphicsScene(self)
        self.view = QGraphicsView(self.scene)
        self.view.setFixedSize(800, 600)  # Redimensionner la carte
        self.layoutPrincipal.addWidget(self.view)

        # Ajouter un Pokémon aléatoire sur la carte
        if self.random_pokemon:
            self.afficher_fond_carte(self.random_pokemon)
            self.afficher_pokemon_aleatoire(self.random_pokemon)

        # Layout pour les boutons
        self.layoutButtons = QHBoxLayout()
        self.btn_inventaire = QPushButton("Inventaire")
        self.btn_inventaire.setFixedHeight(30)
        self.btn_ouvrir = QPushButton("⤿Tirer")
        self.btn_ouvrir.clicked.connect(self.tirer_pokemon_aleatoire)  # Connecter le bouton à la méthode

        self.layoutButtons.addWidget(self.btn_ouvrir)
        self.layoutButtons.addWidget(self.btn_inventaire)

        # Ajouter les boutons au layout principal
        self.layoutPrincipal.addLayout(self.layoutButtons)

    def afficher_fond_carte(self, pokemon):
        # Charger l'image du fond de carte en fonction du type de Pokémon
        type = pokemon["type"][0]  # Prendre le premier type du Pokémon
        if type == "Grass" or type == "Bug":
            pixmap = QPixmap("images/pokemon-carte-herbe.png")
        elif type == "Normal":
            pixmap = QPixmap("images/pokemon-carte-normale.png")
        elif type == "Water" or type == "Ice":
            pixmap = QPixmap("images/pokemon-carte-eau.png")
        elif type == "Fire":
            pixmap = QPixmap("images/pokemon-carte-feu.png")
        elif type == "Electric":
            pixmap = QPixmap("images/pokemon-carte-elec.png")
        elif type == "Psychic" or type == "Poison" or type == "Fairy" or type == "Ghost":
            pixmap = QPixmap("images/pokemon-carte-psy.png")
        elif type == "Fighting" or type == "Ground" or type == "Rock":
            pixmap = QPixmap("images/pokemon-carte-combat.png")
        elif type == "Steel":
            pixmap = QPixmap("images/pokemon-carte-acier.png")
        elif type == "Dragon":
            pixmap = QPixmap("images/pokemon-carte-dragon.png")
        elif type == "Dark":
            pixmap = QPixmap("images/pokemon-carte-dark.png")
        else:
            pixmap = QPixmap()  # Fond par défaut si le type n'est pas reconnu

        # Redimensionner l'image et l'ajouter à la scène
        if not pixmap.isNull():
            pixmap = pixmap.scaled(800, 570, Qt.KeepAspectRatio)
            self.scene.clear()  # Supprimer l'ancien fond
            self.scene.addPixmap(pixmap)

    def afficher_pokemon_aleatoire(self, pokemon):
        # Charger l'image du Pokémon
        self.network_manager = QNetworkAccessManager(self)
        request = QNetworkRequest(QUrl(pokemon["image"]["thumbnail"]))
        reply = self.network_manager.get(request)
        reply.finished.connect(lambda r=reply: self.charger_image_pokemon(r, pokemon))

    @Slot(QNetworkReply)
    def charger_image_pokemon(self, reponse: QNetworkReply, pokemon):
        if reponse.error() == QNetworkReply.NoError:
            image = QImage()
            image.loadFromData(reponse.readAll())
            pixmap = QPixmap.fromImage(image).scaled(100,100, Qt.KeepAspectRatio)

            # Créer un QGraphicsPixmapItem pour afficher l'image du Pokémon
            pokemon_item = QGraphicsPixmapItem(pixmap)
            pokemon_item.setPos(150, 100)  # Déplacer le Pokémon 50px à droite (x = 150)
            self.scene.addItem(pokemon_item)

        reponse.deleteLater()

    def tirer_pokemon_aleatoire(self):
        # Tirer un nouveau Pokémon aléatoire
        self.random_pokemon = random.choice(self.pokedex)
        self.afficher_fond_carte(self.random_pokemon)
        self.afficher_pokemon_aleatoire(self.random_pokemon)

if __name__ == "__main__":
    app = QApplication([])
    win = MyWindow()
    win.show()
    win.resize(800, 700)
    app.exec()
