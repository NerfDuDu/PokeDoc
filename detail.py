from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QTextEdit, QGridLayout, QHBoxLayout
from PySide6.QtCore import Qt
from chargement_img import Image

class AnimeDetailsDialog(QDialog):
    """Dialog to display detailed information about an anime."""
    def __init__(self, item: dict, parent=None):
        super().__init__(parent)
        self.setWindowTitle(item['title'])
        self.setGeometry(100, 100, 600, 500)  # Larger dialog size

        layout = QVBoxLayout()

        # Display image (larger size)
        self.image_label = Image(item.get('picture', ''), self)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setFixedSize(200, 300)  # Larger image size
        layout.addWidget(self.image_label)

        # Display title
        self.title_label = QLabel(item['title'], self)
        self.title_label.setStyleSheet("""
            QLabel {
                font-family: 'Arial';
                font-size: 20px;
                font-weight: bold;
                color: #333;
                padding: 10px;
                background-color: rgba(255, 255, 255, 0.8);
                border-radius: 5px;
            }
        """)
        layout.addWidget(self.title_label)

        # Display type, status, episodes, season, and duration
        details_layout = QGridLayout()

        # Type
        details_layout.addWidget(QLabel("Type:"), 0, 0)
        self.type_label = QLabel(item.get('type', 'N/A'))
        details_layout.addWidget(self.type_label, 0, 1)

        # Status
        details_layout.addWidget(QLabel("Status:"), 1, 0)
        self.status_label = QLabel(item.get('status', 'N/A'))
        details_layout.addWidget(self.status_label, 1, 1)

        # Episodes
        details_layout.addWidget(QLabel("Episodes:"), 2, 0)
        self.episodes_label = QLabel(str(item.get('episodes', 'N/A')))
        details_layout.addWidget(self.episodes_label, 2, 1)

        # Season and Year
        details_layout.addWidget(QLabel("Season:"), 3, 0)
        season = item.get('animeSeason', {})
        season_text = f"{season.get('season', 'N/A')} {season.get('year', 'N/A')}"
        self.season_label = QLabel(season_text)
        details_layout.addWidget(self.season_label, 3, 1)

        # Duration
        details_layout.addWidget(QLabel("Duration:"), 4, 0)
        duration = item.get('duration', {})
        duration_text = f"{duration.get('value', 'N/A')} {duration.get('unit', '')}"
        self.duration_label = QLabel(duration_text)
        details_layout.addWidget(self.duration_label, 4, 1)

        layout.addLayout(details_layout)

        # Display synopsis
        self.synopsis_label = QTextEdit(item.get('synopsis', 'No synopsis available'), self)
        self.synopsis_label.setStyleSheet("""
            QTextEdit {
                font-family: 'Arial';
                font-size: 14px;
                color: #555;
                padding: 10px;
                background-color: rgba(255, 255, 255, 0.8);
                border-radius: 5px;
                border: 1px solid #ddd;
            }
        """)
        self.synopsis_label.setReadOnly(True)
        layout.addWidget(self.synopsis_label)

        # Display tags/genres
        tags_layout = QHBoxLayout()
        tags_layout.addWidget(QLabel("Tags:"))
        self.tags_label = QLabel(", ".join(item.get('tags', [])))
        tags_layout.addWidget(self.tags_label)
        layout.addLayout(tags_layout)

        # Display related anime
        related_layout = QVBoxLayout()
        related_layout.addWidget(QLabel("Related Anime:"))
        self.related_label = QTextEdit("\n".join(item.get('relatedAnime', [])))
        self.related_label.setReadOnly(True)
        related_layout.addWidget(self.related_label)
        layout.addLayout(related_layout)

        # Display sources (external links)
        sources_layout = QVBoxLayout()
        sources_layout.addWidget(QLabel("Sources:"))
        self.sources_label = QTextEdit("\n".join(item.get('sources', [])))
        self.sources_label.setReadOnly(True)
        sources_layout.addWidget(self.sources_label)
        layout.addLayout(sources_layout)

        self.setLayout(layout)