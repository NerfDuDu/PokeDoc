import json
from PySide6.QtWidgets import QGraphicsView, QMainWindow, QWidget, QApplication, QHBoxLayout, QLabel, QListWidgetItem, QListWidget, QListWidgetItem
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtCore import QUrl, Slot
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkReply, QNetworkRequest



class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        centraleWidget = QWidget()
        self.setCentralWidget(centraleWidget)
        self.view = QGraphicsView()


        layout = QHBoxLayout(centraleWidget)
        layout.addWidget(self.view)

class Label_image(QLabel):

    def __init__(self, url:str, parent=None):
        super().__init__(parent)
        self.manager = QNetworkAccessManager()
        self.manager.finished.connect(self.chargement_fini)
        url = QUrl.fromUserInput(url)
        self.manager.get(QNetworkRequest(url))

    @Slot(QNetworkReply)
    def chargement_fini(self, reponse:QNetworkReply):
        image = QImage()
        image.loadFromData(reponse.readAll())
        pixmap = QPixmap.fromImage(image)
        self.setPixmap(pixmap)


class liste(QListWidget):
    def __init__(self):
        super().__init__()
        newItem = QListWidgetItem()
        newItem.setText("test1")
        self.insertItem(0, newItem)
        newItem = QListWidgetItem()
        newItem.setText("test2")
        self.insertItem(1, newItem)
        self.newItem = QListWidgetItem()
        self.newItem.setText("test3")
        self.addItem(self.newItem)
        test = self.takeItem(1)

with open('pokedex.json', encoding="utf8") as f:
    contenu = json.load(f)
for i in range(15):
    print(contenu[i]["name"]["french"])

if __name__ == "__main__":
    app = QApplication()
    #win = MyWindow()
    win = liste()
    #win = Label_image(contenu[897]["image"]["thumbnail"])

    win.show()
    win.resize(500,500)
    app.exec()




# QListWidgetItem *newItem = new QListWidgetItem;
#    newItem->setText(itemText);
#    listWidget->insertItem(row, newItem);