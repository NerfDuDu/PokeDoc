import json
from PySide6.QtWidgets import (QGraphicsView, QMainWindow, QWidget, QApplication, 
                               QHBoxLayout, QPushButton, QVBoxLayout, QLabel)
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtCore import QUrl, Slot
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkReply, QNetworkRequest

class Label_image(QLabel):
    def __init__(self, url: str, parent=None):
        super().__init__(parent)
        self.manager = QNetworkAccessManager()
        self.manager.finished.connect(self.chargement_fini)
        url = QUrl.fromUserInput(url)
        self.manager.get(QNetworkRequest(url))

    @Slot(QNetworkReply)
    def chargement_fini(self, reponse: QNetworkReply):
        image = QImage()
        image.loadFromData(reponse.readAll())
        pixmap = QPixmap.fromImage(image)
        self.setPixmap(pixmap)

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.centraleWidget = QWidget()
        self.setCentralWidget(self.centraleWidget)

        self.layoutPrincipal = QVBoxLayout(self.centraleWidget)

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

        if self.btn_inventaire.clicked:
            
            self.btn_inventaire.clicked.connect(self.Reset_pour_inv)
            self.layoutView = QHBoxLayout()
            self.view = QGraphicsView()
            self.layoutView.addWidget(self.view)
            
            self.layoutButtons = QHBoxLayout()
            self.btn_deck = QPushButton("Deck")

    def Reset_pour_inv(self):
        self.setCentralWidget(QWidget())


with open('pokedex.json', encoding="utf8") as f:
    contenu = json.load(f)
for i in range(15):
    print(contenu[i]["name"]["french"])

if __name__ == "__main__":
    app = QApplication([])
    win = MyWindow()
    win.show()
    win.resize(500, 500)
    app.exec()
