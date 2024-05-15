import customtkinter as ctk
from tkinter import simpledialog, messagebox, filedialog, Toplevel, StringVar
from data_manager import save_data, load_data
from datetime import datetime
import shutil
from constants import DATA_FILE, BACKUP_FOLDER

# Define global variables
current_user = None
tree = None
context_menu = None

def create_backup():
    if not os.path.exists(BACKUP_FOLDER):
        os.makedirs(BACKUP_FOLDER)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = os.path.join(BACKUP_FOLDER, f'warehouse_backup_{timestamp}.json')
    shutil.copy(DATA_FILE, backup_file)
    messagebox.showinfo("Backup", f"Backup created successfully at {backup_file}")

def restore_backup():
    backup_file = filedialog.askopenfilename(initialdir=BACKUP_FOLDER, title="Select backup file", filetypes=(("JSON files", "*.json"),))
    if backup_file:
        shutil.copy(backup_file, DATA_FILE)
        global data
        data = load_data()
        load_products(data)
        load_locations(data)
        messagebox.showinfo("Restore", "Data restored successfully")

# Other functions from previous `handlers.py`

def select_user(root):
    users = ["Alice", "Bob"]  # Add more users if needed
    user = simpledialog.askstring("User Selection", "Enter your name:", initialvalue=users[0])
    if user in users:
        return user
    else:
        messagebox.showerror("User Error", "Invalid user. Please restart and enter a valid name.")
        root.quit()
        exit()

def open_settings():
    settings_window = ctk.CTkToplevel(root)
    settings_window.title("Settings")
    settings_window.geometry("400x200")
    settings_frame = ctk.CTkFrame(settings_window, corner_radius=10)
    settings_frame.pack(pady=20, padx=20, fill="both", expand=True)

    def change_theme(selected_theme):
        ctk.set_appearance_mode(selected_theme)
        apply_theme_to_treeview()
        style_theme()

    ctk.CTkLabel(settings_frame, text="Select Theme:", font=("Arial", 12)).pack(pady=10)
    
    theme_var = StringVar(value=ctk.get_appearance_mode())
    theme_light = ctk.CTkRadioButton(settings_frame, text="Light", variable=theme_var, value="Light", command=lambda: change_theme("Light"))
    theme_light.pack(pady=5)
    theme_dark = ctk.CTkRadioButton(settings_frame, text="Dark", variable=theme_var, value="Dark", command=lambda: change_theme("Dark"))
    theme_dark.pack(pady=5)

def show_about():
    about_window = ctk.CTkToplevel(root)
    about_window.title("About")
    about_window.geometry("400x200")
    about_frame = ctk.CTkFrame(about_window, corner_radius=10)
    about_frame.pack(pady=20, padx=20, fill="both", expand=True)
    ctk.CTkLabel(about_frame, text="Warehouse Management System", font=("Arial", 16)).pack(pady=10)
    ctk.CTkLabel(about_frame, text="Version 1.0", font=("Arial", 12)).pack(pady=5)
    ctk.CTkLabel(about_frame, text="Developed by [Your Name]", font=("Arial", 12)).pack(pady=5)

def add_product(data, entry_name, entry_quantity, combo_location):
    name = entry_name.get().strip()
    quantity = entry_quantity.get().strip()
    location = combo_location.get().strip()
    
    if name and quantity.isdigit() and location:
        for product in data["products"]:
            if product["name"].lower() == name.lower() and product["location"] == location:
                product["quantity"] += int(quantity)
                record_history(product["id"], f"Updated quantity to {product['quantity']}")
                save_data(data)
                load_products(data)
                entry_name.delete(0, ctk.END)
                entry_quantity.delete(0, ctk.END)
                combo_location.set('')
                return

        product_id = len(data["products"]) + 1
        data["products"].append({"id": product_id, "name": name, "quantity": int(quantity), "location": location, "history": []})
        record_history(product_id, f"Added product with quantity {quantity}")
        save_data(data)
        entry_name.delete(0, ctk.END)
        entry_quantity.delete(0, ctk.END)
        combo_location.set('')
        load_products(data)
    else:
        messagebox.showwarning("Input error", "Please provide a valid name, quantity, and location")

def delete_product(data):
    try:
        selected_item = tree.selection()[0]
        item_id = int(tree.item(selected_item)['values'][0])
        for product in data["products"]:
            if product["id"] == item_id:
                record_history(item_id, "Deleted product")
                data["products"].remove(product)
                break
        save_data(data)
        tree.delete(selected_item)
    except IndexError:
        messagebox.showwarning("Selection error", "Please select an item to delete")

def edit_product(data):
    try:
        selected_item = tree.selection()[0]
        item_id = int(tree.item(selected_item)['values'][0])
        for product in data["products"]:
            if product["id"] == item_id:
                new_name = simpledialog.askstring("Edit Product", "Enter new name:", initialvalue=product["name"])
                new_quantity = simpledialog.askinteger("Edit Product", "Enter new quantity:", initialvalue=product["quantity"])
                new_location = simpledialog.askstring("Edit Product", "Enter new location:", initialvalue=product["location"])
                if new_name and new_quantity is not None and new_location:
                    product["name"] = new_name
                    product["quantity"] = new_quantity
                    product["location"] = new_location
                    record_history(item_id, f"Edited product to name: {new_name}, quantity: {new_quantity}, location: {new_location}")
                    save_data(data)
                    load_products(data)
                break
    except IndexError:
        messagebox.showwarning("Selection error", "Please select an item to edit")

def search_product(data, entry_search):
    search_term = entry_search.get().lower().strip()
    for row in tree.get_children():
        tree.delete(row)
    for index, product in enumerate(data["products"]):
        if search_term in product["name"].lower() or search_term in product["location"].lower():
            tree.insert("", ctk.END, values=(product["id"], product["name"], product["quantity"], product["location"]),
                        tags=('oddrow' if index % 2 == 0 else 'evenrow',))

def show_history(data):
    try:
        selected_item = tree.selection()[0]
        item_id = int(tree.item(selected_item)['values'][0])
        for product in data["products"]:
            if product["id"] == item_id:
                history_window = ctk.CTkToplevel(root)
                history_window.title("Product History")
                history_listbox = ctk.CTkTextbox(history_window, width=500, height=300)
                history_listbox.pack(pady=20)
                for entry in product.get("history", []):
                    history_listbox.insert("end", f"{entry['timestamp']} by {entry['user']}: {entry['action']}\n")
                break
    except IndexError:
        messagebox.showwarning("Selection error", "Please select an item to view history")

def show_context_menu(event):
    try:
        selected_item = tree.identify_row(event.y)
        if selected_item:
            tree.selection_set(selected_item)
            context_menu.post(event.x_root, event.y_root)
    finally:
        context_menu.grab_release()

def record_history(product_id, action):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for product in data["products"]:
        if product["id"] == product_id:
            if "history" not in product:
                product["history"] = []
            product["history"].append({"timestamp": timestamp, "action": action, "user": current_user})
            break
