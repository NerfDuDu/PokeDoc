 # ui/search_bar.py
from typing import List
from PySide6.QtWidgets import QWidget, QLineEdit, QVBoxLayout, QLabel, QPushButton, QGridLayout, QTextEdit, QDialog, QHBoxLayout, QComboBox
from PySide6.QtCore import QUrl, Signal, Slot, Qt, QTimer
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
from PySide6.QtGui import QImage, QPixmap, QFont
from boite import Liste_Vignette
from detail import AnimeDetailsDialog

class SearchBarWithResults(QWidget):
    """Widget for search bar and displaying anime results."""
    search = Signal(str, str, str, str)  # Emits query, type_filter, status_filter, sort_by

    def __init__(self, anime_data, favorites, recently_viewed):
        super().__init__()
        self.setWindowTitle("Anime Search Results")
        self.setMinimumSize(800, 600)  # Set minimum window size
        self.setMaximumSize(1200, 800)  # Set maximum window size

        self.layout = QVBoxLayout()

        # Search bar
        self.search_bar = QLineEdit(self)
        self.search_bar.setPlaceholderText("Search your favorite anime...")
        self.search_bar.setStyleSheet("""
            QLineEdit {
                font-family: 'Arial';
                font-size: 14px;
                padding: 10px;
                border: 2px solid #ccc;
                border-radius: 5px;
            }
            QLineEdit:focus {
                border: 2px solid #0078d7;
            }
        """)
        self.layout.addWidget(self.search_bar)

        # Filters
        self.add_filters()

        # Results list
        self.result_list = Liste_Vignette(self)
        self.layout.addWidget(self.result_list)

        # Page number bar
        self.page_bar = QHBoxLayout()
        self.page_buttons = []  # Store page number buttons
        self.layout.addLayout(self.page_bar)

        # Random anime button
        self.add_random_button()

        self.data = anime_data
        self.favorites = favorites
        self.recently_viewed = recently_viewed
        self.current_page_group = 0  # Tracks the current group of pages (e.g., 1-5, 6-10, etc.)
        self.pages_per_group = 5  # Number of page buttons to show at a time

        # Use a QTimer to delay search updates
        self.search_timer = QTimer(self)
        self.search_timer.setInterval(500)  # 500ms delay
        self.search_timer.setSingleShot(True)
        self.search_timer.timeout.connect(self.emit_search_signal)

        self.search_bar.textChanged.connect(self.start_search_timer)
        self.result_list.itemClicked.connect(self.display_image)

        self.setLayout(self.layout)
        self.update_page()

    def add_filters(self):
        """Add filters for type, status, and sorting."""
        filter_layout = QHBoxLayout()

        # Type filter
        self.type_filter = QComboBox()
        self.type_filter.addItems(["All", "TV", "MOVIE", "OVA", "SPECIAL"])
        filter_layout.addWidget(QLabel("Type:"))
        filter_layout.addWidget(self.type_filter)

        # Status filter
        self.status_filter = QComboBox()
        self.status_filter.addItems(["All", "FINISHED", "ONGOING"])
        filter_layout.addWidget(QLabel("Status:"))
        filter_layout.addWidget(self.status_filter)

        # Sort by
        self.sort_by = QComboBox()
        self.sort_by.addItems(["Title", "Rating", "Year"])
        filter_layout.addWidget(QLabel("Sort by:"))
        filter_layout.addWidget(self.sort_by)

        self.layout.addLayout(filter_layout)

        # Connect filters to search
        self.type_filter.currentTextChanged.connect(self.emit_search_signal)
        self.status_filter.currentTextChanged.connect(self.emit_search_signal)
        self.sort_by.currentTextChanged.connect(self.emit_search_signal)

    def add_random_button(self):
        """Add a button to show a random anime."""
        random_button = QPushButton("Random Anime")
        random_button.clicked.connect(self.show_random_anime)
        self.layout.addWidget(random_button)

    def show_random_anime(self):
        """Show a random anime from the dataset."""
        import random
        random_anime = random.choice(self.data.anime_data)
        self.details_dialog = AnimeDetailsDialog(random_anime, self)
        self.details_dialog.show()

    def start_search_timer(self):
        """Start the search timer when text in the search bar changes."""
        self.search_timer.start()

    def emit_search_signal(self):
        """Emit the search signal with filters and sorting options."""
        query = self.search_bar.text().lower()
        type_filter = self.type_filter.currentText()
        status_filter = self.status_filter.currentText()
        sort_by = self.sort_by.currentText()
        self.search.emit(query, type_filter, status_filter, sort_by)

    def update_results(self, filtered_data: List[dict]):
        """Update the list of results based on the filtered data."""
        self.result_list.clear()
        for item in filtered_data:
            self.result_list.addItem(item)

    def display_image(self, item):
        """Display the image and details of the selected anime."""
        if item:
            self.details_dialog = AnimeDetailsDialog(item, self)
            self.details_dialog.show()

    def update_page(self):
        """Update the displayed anime list and page number bar."""
        query = self.search_bar.text().lower()
        type_filter = self.type_filter.currentText()
        status_filter = self.status_filter.currentText()
        sort_by = self.sort_by.currentText()

        # Load filtered and sorted data
        filtered_data = self.data.load(
            title=query,
            type_filter=type_filter,
            status_filter=status_filter,
            sort_by=sort_by
        )
        self.update_results(filtered_data)

        # Clear existing page buttons
        for button in self.page_buttons:
            self.page_bar.removeWidget(button)
            button.deleteLater()
        self.page_buttons.clear()

        # Calculate total pages
        total_items = len(self.data.filtered_data)
        total_pages = (total_items // self.data.items_per_page) + 1

        # Calculate the range of pages to display
        start_page = self.current_page_group * self.pages_per_group + 1
        end_page = min(start_page + self.pages_per_group - 1, total_pages)

        # Add "Previous" button if not on the first group
        if self.current_page_group > 0:
            prev_button = QPushButton("<<", self)
            prev_button.setStyleSheet("""
                QPushButton {
                    font-family: 'Arial';
                    font-size: 14px;
                    padding: 5px 10px;
                    background-color: #0078d7;
                    color: white;
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: #005bb5;
                }
            """)
            prev_button.clicked.connect(self.previous_group)
            self.page_bar.addWidget(prev_button)
            self.page_buttons.append(prev_button)

        # Add page number buttons
        for page in range(start_page, end_page + 1):
            page_button = QPushButton(str(page), self)
            page_button.setStyleSheet("""
                QPushButton {
                    font-family: 'Arial';
                    font-size: 14px;
                    padding: 5px 10px;
                    background-color: #f0f0f0;
                    color: #333;
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: #0078d7;
                    color: white;
                }
            """)
            page_button.clicked.connect(lambda _, p=page: self.go_to_page(p))
            self.page_bar.addWidget(page_button)
            self.page_buttons.append(page_button)

        # Add "Next" button if not on the last group
        if end_page < total_pages:
            next_button = QPushButton(">>", self)
            next_button.setStyleSheet("""
                QPushButton {
                    font-family: 'Arial';
                    font-size: 14px;
                    padding: 5px 10px;
                    background-color: #0078d7;
                    color: white;
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: #005bb5;
                }
            """)
            next_button.clicked.connect(self.next_group)
            self.page_bar.addWidget(next_button)
            self.page_buttons.append(next_button)

    def go_to_page(self, page: int):
        """Navigate to a specific page."""
        self.data.current_page = page - 1
        self.update_page()

    def next_group(self):
        """Move to the next group of pages."""
        self.current_page_group += 1
        self.update_page()

    def previous_group(self):
        """Move to the previous group of pages."""
        self.current_page_group -= 1
        self.update_page()