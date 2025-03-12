import json

class pokemon:
    def __init__(self, file_path='pokedex.json'):
        self.file_path = file_path
        self.anime_data = []
        self.filtered_data = []
        self.current_page = 0
        self.items_per_page = 15  # Number of items per page
        self.load_anime_data()

    def load_anime_data(self):
        """Loads anime data from the JSON file."""
        try:
            with open(self.file_path, encoding="utf8") as f:
                content = json.load(f)
            self.anime_data = content.get('data', [])
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading data: {e}")