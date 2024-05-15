import customtkinter as ctk
from tkinter import ttk
from handlers import add_product, search_product, edit_product, delete_product, show_history, show_context_menu

def create_main_frame(root, data):
    frame = ctk.CTkFrame(root)
    frame.pack(pady=20, padx=20, fill="both", expand=True)

    # Create product entry frame
    entry_frame = ctk.CTkFrame(frame)
    entry_frame.pack(pady=10, padx=10, fill="x")

    entry_name = ctk.CTkEntry(entry_frame, placeholder_text="Product Name")
    entry_name.grid(row=0, column=0, padx=10, pady=10)

    entry_quantity = ctk.CTkEntry(entry_frame, placeholder_text="Quantity")
    entry_quantity.grid(row=0, column=1, padx=10, pady=10)

    combo_location = ctk.CTkComboBox(entry_frame)
    combo_location.grid(row=0, column=2, padx=10, pady=10)

    btn_add_product = ctk.CTkButton(entry_frame, text="Add Product", command=lambda: add_product(data, entry_name, entry_quantity, combo_location))
    btn_add_product.grid(row=0, column=3, padx=10, pady=10)

    # Create search frame
    search_frame = ctk.CTkFrame(frame)
    search_frame.pack(pady=10, padx=10, fill="x")

    entry_search = ctk.CTkEntry(search_frame, placeholder_text="Search")
    entry_search.grid(row=0, column=0, padx=10, pady=10)

    btn_search = ctk.CTkButton(search_frame, text="Search", command=lambda: search_product(data, entry_search))
    btn_search.grid(row=0, column=1, padx=10, pady=10)

    # Create treeview
    global tree
    tree = ttk.Treeview(frame, columns=("ID", "Name", "Quantity", "Location"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Name", text="Name")
    tree.heading("Quantity", text="Quantity")
    tree.heading("Location", text="Location")
    tree.pack(pady=20, padx=20, fill="both", expand=True)

    # Apply theme to treeview
    style = ttk.Style()
    style.theme_use('clam')
    apply_theme_to_treeview()
    style_theme()

    # Create context menu
    context_menu = Menu(tree, tearoff=0)
    context_menu.add_command(label="Edit", command=lambda: edit_product(data))
    context_menu.add_command(label="Delete", command=lambda: delete_product(data))
    context_menu.add_command(label="History", command=lambda: show_history(data))

    tree.bind("<Button-3>", show_context_menu)

    return frame

def load_locations(data):
    combo_location.configure(values=data["locations"])
    combo_location.set('')  # Clear the current selection

def load_products(data):
    for row in tree.get_children():
        tree.delete(row)
    for index, product in enumerate(data["products"]):
        tree.insert("", ctk.END, values=(product["id"], product["name"], product["quantity"], product["location"]),
                    tags=('oddrow' if index % 2 == 0 else 'evenrow',))

def apply_theme_to_treeview():
    if ctk.get_appearance_mode() == "Light":
        style.configure("Treeview", background="white", fieldbackground="white", foreground="black")
        style.configure("Treeview.Heading", background="white", foreground="black")
    else:
        style.configure("Treeview", background="#383838", fieldbackground="#383838", foreground="white")
        style.configure("Treeview.Heading", background="#383838", foreground="white")

def style_theme():
    root.option_add("*TCombobox*Listbox*Foreground", "black" if ctk.get_appearance_mode() == "Light" else "white")
    root.option_add("*TCombobox*Listbox*Background", "white" if ctk.get_appearance_mode() == "Light" else "#383838")
