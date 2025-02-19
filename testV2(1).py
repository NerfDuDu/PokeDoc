import json
from PySide6.QtWidgets import (QGraphicsView, QMainWindow, QWidget, QApplication, 
                               QHBoxLayout, QPushButton, QVBoxLayout, QLabel, 
                               QGraphicsScene, QGraphicsPixmapItem, QGraphicsRectItem,QGridLayout)
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtCore import QUrl, Slot, QRandomGenerator, Signal,Qt
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkReply, QNetworkRequest

class Scene(QGraphicsScene):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.fond=QGraphicsRectItem(0,0,0,0)
        self.addItem(self.fond)
        self.ajoute(self.imge())

    def imge(self):
        with open('pokedex.json', encoding="utf8") as f:
            contenu = json.load(f)
        pokemon = contenu[196]["image"]["thumbnail"]
        return pokemon       

    def get_type(self):
        with open('pokedex.json', encoding="utf8") as f:
            contenu = json.load(f)
        pokemon_type = contenu[196]["type"][0]
        return pokemon_type
    
    def get_nom(self):
        with open('pokedex.json', encoding="utf8") as f:
            contenu = json.load(f)
        nom_pokemon = contenu[197]["name"]["french"]
        return nom_pokemon
    
    def ajoute(self,url: str):
        self.manager = QNetworkAccessManager()
        self.manager.finished.connect(self.chargement_fini)
        url = QUrl.fromUserInput(url)
        self.manager.get(QNetworkRequest(url))

    @Slot(QNetworkReply)
    def chargement_fini(self, reponse: QNetworkReply):
        image = QImage()
        image.loadFromData(reponse.readAll())
        pixmap = QPixmap.fromImage(image)
        pixmap_item = QGraphicsPixmapItem(pixmap)
        pixmap_item.setPos(80,60)
        self.addItem(pixmap_item)

        

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.menu()
    
    def menue(self):
        self.centralWidget = MENUS()
        self.setCentralWidget(self.centralWidget)
        self.centralWidget.btn_inventaire.clicked.connect(self.inventaire)
    
    def inventaire(self):
        self.centralWidget = SAKA_DHO()
        self.setCentralWidget(self.centralWidget)
        self.centralWidget.btn_menu.clicked.connect(self.menu)

    def menu(self):
        self.centraleWidget = QWidget()
        self.setCentralWidget(self.centraleWidget)

        self.layoutPrincipal = QVBoxLayout(self.centraleWidget)

        self.layoutView = QHBoxLayout()
        self.scene = Scene()
        self.view = QGraphicsView(self.scene)
    
        self.layoutButtons = QHBoxLayout()
        self.btn_deck = QPushButton("Deck")
        self.btn_inventaire = QPushButton("Inventaire")
        self.btn_ouvrir = QPushButton("Ouvrir")

        self.layoutButtons.addWidget(self.btn_deck)
        self.layoutButtons.addWidget(self.btn_ouvrir)
        self.layoutButtons.addWidget(self.btn_inventaire)

        type = Scene.get_type(self)
        if type == "Grass" or type == "Bug":
            pixmap = QPixmap("images/pokemon-carte-herbe.png")
            pixmap_rezise = pixmap.scaled(300, 400,Qt.KeepAspectRatio)
        elif type == "Normal":
            pixmap = QPixmap("images/pokemon-carte-normale.png")
            pixmap_rezise = pixmap.scaled(300, 400,Qt.KeepAspectRatio)
        elif type == "Water" or type == "Ice":
            pixmap = QPixmap("images/pokemon-carte-eau.png")
            pixmap_rezise = pixmap.scaled(300, 400,Qt.KeepAspectRatio)
        elif type == "Fire":
            pixmap = QPixmap("imagespokemon-carte-feu.png")
            pixmap_rezise = pixmap.scaled(300, 400,Qt.KeepAspectRatio)
        elif type == "Electric":
            pixmap = QPixmap("images/pokemon-carte-elec.png")
            pixmap_rezise = pixmap.scaled(300, 400,Qt.KeepAspectRatio)
        elif type == "Psychic" or type == "Poison" or type == "Fairy" or type == "Ghost":
            pixmap = QPixmap("images/pokemon-carte-psy.png")
            pixmap_rezise = pixmap.scaled(300, 400,Qt.KeepAspectRatio)
        elif type == "Fighting" or type == "Ground" or type == "Rock":
            pixmap = QPixmap("images/pokemon-carte-combat.png")
            pixmap_rezise = pixmap.scaled(300, 400,Qt.KeepAspectRatio)
        elif type == "Steel":
            pixmap = QPixmap("images/pokemon-carte-acier.png")
            pixmap_rezise = pixmap.scaled(300, 400,Qt.KeepAspectRatio)
        elif type == "Dragon":
            pixmap = QPixmap("images/pokemon-carte-dragon.png")
            pixmap_rezise = pixmap.scaled(300, 400,Qt.KeepAspectRatio)
        elif type == "Dark":
            pixmap = QPixmap("images/pokemon-carte-dark.png")
            pixmap_rezise = pixmap.scaled(300, 400,Qt.KeepAspectRatio)
            
        self.pixmap_item = QGraphicsPixmapItem(pixmap_rezise)
        self.scene.addItem(self.pixmap_item)
        self.view.setScene(self.scene)
        self.layoutView.addWidget(self.view)
        self.resize(pixmap.width(), pixmap.height())
        
        self.layoutPrincipal.addLayout(self.layoutView)
        self.layoutPrincipal.addLayout(self.layoutButtons)
        self.resize(800,700)

        self.btn_inventaire.clicked.connect(self.inventaire)

       

class SAKA_DHO(QWidget):
    def __init__(self):
        super().__init__()

        self.layoutsakado = QVBoxLayout(self)

        #Vue
        self.vue = QWidget()
        self.gridlayout = QGridLayout()
        self.vue.setLayout(self.gridlayout)
            #ligne 0
        self.gridlayout.addWidget(QLabel("1"), 0, 0) 
        self.gridlayout.addWidget(QLabel("2"), 0, 1)
        self.gridlayout.addWidget(QLabel("3"), 0, 2)
        self.gridlayout.addWidget(QLabel("4"), 0, 3)
        self.gridlayout.addWidget(QLabel("5"), 0, 4)
            #ligne 1
        self.gridlayout.addWidget(QLabel("6"), 1, 0)
        self.gridlayout.addWidget(QLabel("7"), 1, 1)
        self.gridlayout.addWidget(QLabel("8"), 1, 2)
        self.gridlayout.addWidget(QLabel("9"), 1, 3)
        self.gridlayout.addWidget(QLabel("10"), 1, 4)
            #ligne 2
        self.gridlayout.addWidget(QLabel("11"), 2, 0)
        self.gridlayout.addWidget(QLabel("12"), 2, 1)
        self.gridlayout.addWidget(QLabel("13"), 2, 2)
        self.gridlayout.addWidget(QLabel("14"), 2, 3)
        self.gridlayout.addWidget(QLabel("15"), 2, 4)
            #ligne 3
        self.gridlayout.addWidget(QLabel("16"), 3, 0)
        self.gridlayout.addWidget(QLabel("17"), 3, 1)
        self.gridlayout.addWidget(QLabel("18"), 3, 2)
        self.gridlayout.addWidget(QLabel("19"), 3, 3)
        self.gridlayout.addWidget(QLabel("20"), 3, 4)

        self.layoutsakado.addWidget(self.vue)

        #Menu
        self.menu = QWidget()
        self.menu.setFixedHeight(40)
        self.layoutButtons = QHBoxLayout()
        self.menu.setLayout(self.layoutButtons)

        self.btn_menu = QPushButton("Menu")
        self.layoutButtons.addWidget(self.btn_menu)
        self.btn_prec = QPushButton("<")
        self.layoutButtons.addWidget(self.btn_prec)
        self.btn_suiv = QPushButton(">")
        self.layoutButtons.addWidget(self.btn_suiv)

         
        self.layoutsakado.addWidget(self.menu)
class MENUS(QWidget):
    def __init__(self):
        super().__init__()

        self.layoutPrincipal = QVBoxLayout(self)

        self.layoutView = QHBoxLayout()
        self.view = QGraphicsView()
        self.layoutView.addWidget(self.view)

        self.layoutButtons = QHBoxLayout()
        self.btn_deck = QPushButton("Deck")
        self.btn_inventaire = QPushButton("Inventaire")
        self.btn_ouvrir = QPushButton("Ouvrir")

        self.layoutButtons.addWidget(self.btn_deck)
        self.layoutButtons.addWidget(self.btn_ouvrir)
        self.layoutButtons.addWidget(self.btn_inventaire)

        
        self.layoutPrincipal.addLayout(self.layoutView)
        self.layoutPrincipal.addLayout(self.layoutButtons)
#for i in range(15):
#    print(contenu[i]["name"]["french"])

if __name__ == "__main__":
    app = QApplication([])
    win = MyWindow()
    win.show()
    win.resize(800, 700)
    app.exec()
