import customtkinter as ctk
from tkinter import Menu
from gui import create_main_frame, load_locations, load_products
from data_manager import load_data
from handlers import select_user, open_settings, show_about, create_backup, restore_backup, add_location, delete_location

# Load existing data
data = load_data()

# Set appearance mode and color theme
ctk.set_appearance_mode("System")  # Modes: system (default), light, dark
ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

# GUI setup
root = ctk.CTk()
root.withdraw()  # Hide the main window until user is selected

# Select user
current_user = select_user(root)
if current_user is None:
    exit()

root.deiconify()  # Show the main window after user is selected
root.title("Warehouse Management System")

# Create the menu bar
menu_bar = Menu(root)
root.config(menu=menu_bar)

# Create File menu
file_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Create Backup", command=create_backup)
file_menu.add_command(label="Restore Backup", command=restore_backup)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)

# Create Location menu
location_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Location", menu=location_menu)
location_menu.add_command(label="Add Location", command=lambda: add_location(data))
location_menu.add_command(label="Delete Location", command=lambda: delete_location(data))

# Create Help menu
help_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Help", menu=help_menu)
help_menu.add_command(label="About", command=show_about)

# Create Settings menu
settings_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Settings", menu=settings_menu)
settings_menu.add_command(label="Preferences", command=open_settings)

# Create main frame
frame = create_main_frame(root, data)

# Load initial data
load_locations(data)
load_products(data)

root.mainloop()
