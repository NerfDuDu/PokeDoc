from PySide6.QtCore import Slot, QUrl
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkReply, QNetworkRequest
from PySide6.QtWidgets import QApplication, QLabel

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

if __name__ == "__main__":
    app = QApplication()
    img = Label_image("https://pixnio.com/free-images/2017/08/30/2017-08-30-07-06-43-1152x768.jpg")
    img.show()
    img.resize(1152,768)
    app.exec()
