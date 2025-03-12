import json
from PySide6.QtWidgets import (QGraphicsView, QMainWindow, QWidget, QApplication, 
                               QHBoxLayout, QPushButton, QVBoxLayout, QLabel, 
                               QGraphicsScene, QGraphicsPixmapItem, QGraphicsRectItem,QGridLayout)
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtCore import QUrl, Slot, QRandomGenerator, Signal,Qt
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkReply, QNetworkRequest
from chargement_img import Image

class Boite(QWidget):
    """Permet de mettre une image et le nom du pokemon."""
    clicked = Signal(dict)

    def __init__(self, *arg):
        super().__init__(*arg)
        self.item = {}
        self.layout = QVBoxLayout()
        self.layout.setSpacing(5)  # Reduce spacing between image and title
        self.layout.setContentsMargins(5, 5, 5, 5)  # Reduce margins

        # Image part
        self.image_label = Image("", self)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.image_label)

        # Title part
        self.title_label = QLabel("", self)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setWordWrap(True)  # Enable word wrap for long titles
        self.title_label.setStyleSheet("""
            QLabel {
                font-family: 'Arial';
                font-size: 12px;
                font-weight: bold;
                color: #333;
                padding: 5px;
                background-color: rgba(255, 255, 255, 0.8);
                border-radius: 5px;
            }
        """)
        self.layout.addWidget(self.title_label)

        # Favorite button
        self.favorite_button = QPushButton("⭐")
        self.favorite_button.clicked.connect(self.toggle_favorite)
        self.layout.addWidget(self.favorite_button)

        self.setLayout(self.layout)
        self.setStyleSheet("""
            Vignette {
                background-color: #f0f0f0;
                border-radius: 8px;
                border: 1px solid #ddd;
            }
            Vignette:hover {
                background-color: #e0e0e0;
                border: 1px solid #ccc;
            }
        """)  # Add hover effect

    def setItem(self, item: dict):
        """Set the item data (title, image URL, and additional info)."""
        self.item = item
        if item:
            self.title_label.setText(self.item['title'])
            self.image_label.load_image(self.item["picture"])
            self.setToolTip(f"Title: {item['title']}\nRating: {item.get('rating', 'N/A')}\nGenre: {', '.join(item.get('genres', []))}")
        else:
            self.title_label.setText("")
            self.image_label.setPixmap(self.image_label.placeholder)

    def toggle_favorite(self):
        """Toggle the favorite status of the anime."""
        self.favorite_button.setText("★" if self.favorite_button.text() == "⭐" else "⭐")
        self.clicked.emit(self.item)

    def mouseReleaseEvent(self, ev):
        """Emit the clicked signal when vignette is clicked."""
        self.clicked.emit(self.item)
        return super().mouseReleaseEvent(ev)
    
class Liste_boite(QWidget):
    itemClicked = Signal(dict)

    def __init__(self, *arg):
        super().__init__(*arg)
        self.layout = QGridLayout()
        self.layout.setSpacing(10)  # Reduce spacing between items
        self.layout.setContentsMargins(10, 10, 10, 10)  # Reduce margins
        self.setLayout(self.layout)
        self.vignettes[Boite] = []

    def clear(self):
        """Remove all Vignette widgets from the layout."""
        for vignette in self.vignettes:
            vignette.setItem({})
        self.vignettes.clear()

    def addItem(self, item: dict):
        index = len(self.vignettes)
        if index >= 15:  # Limit to 15 items per page
            return

        row = index // 5  # Adjust rows dynamically
        col = index % 5

        vignette = Boite()
        vignette.setItem(item)
        vignette.clicked.connect(self.selected)
        self.layout.addWidget(vignette, row, col)
        self.vignettes.append(vignette)

    def selected(self, item):
        self.itemClicked.emit(item)    


