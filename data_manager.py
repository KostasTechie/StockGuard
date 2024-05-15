import json
import os
from tkinter import messagebox
from constants import DATA_FILE

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r') as file:
                loaded_data = json.load(file)
                if isinstance(loaded_data, dict) and "products" in loaded_data and "locations" in loaded_data:
                    return loaded_data
                else:
                    raise ValueError("Incorrect JSON format")
        except (json.JSONDecodeError, ValueError):
            messagebox.showwarning("Error", "Error loading data from JSON file. The file may be corrupted or in the wrong format.")
            return {"products": [], "locations": []}
    return {"products": [], "locations": []}

def save_data(data):
    with open(DATA_FILE, 'w') as file:
        json.dump(data, file, indent=4)
