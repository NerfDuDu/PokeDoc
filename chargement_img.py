import json
from PySide6.QtWidgets import QLabel
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtCore import QUrl, Slot, QRandomGenerator,Qt
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkReply, QNetworkRequest

class Image(QLabel):
    """
    Chargement et affichage d'une image.
    """

    def __init__(self, url: str = "", parent=None):
        super().__init__(parent)
        self.manager = QNetworkAccessManager(self)
        self.manager.finished.connect(self.image_loaded)
        self.placeholder = QPixmap("path/to/placeholder.png")  # Ensure a proper placeholder image is available
        self.setPixmap(self.placeholder)
        self.cache = {}  # Simple image cache

        if url:
            self.chrg_image(url)

    def chrg_image(self, url: str):
        """
        Charge l'image à partir d'internet.
        """
        # Clear the old image by setting the placeholder
        self.setPixmap(self.placeholder)

        if url in self.cache:
            self.setPixmap(self.cache[url])
            return

        qurl = QUrl.fromUserInput(url)
        self.manager.get(QNetworkRequest(qurl))

    @Slot(QNetworkReply)
    def chrg_fini(self, reply: QNetworkReply):
        """
        Affiche l'image après avoir été chargée.
        """
        if reply.error() != QNetworkReply.NoError:
            print(f"Error loading image: {reply.errorString()}")
            self.setPixmap(self.placeholder)
            return

        image = QImage()
        if not image.loadFromData(reply.readAll()):
            print("Failed to load image from data")
            self.setPixmap(self.placeholder)
            return

        # Scale the image to a smaller size (e.g., 100x150)
        pixmap = QPixmap.fromImage(image).scaled(100, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.cache[reply.url().toString()] = pixmap  # Cache the image
        self.setPixmap(pixmap)