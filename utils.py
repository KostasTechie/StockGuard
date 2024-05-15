import customtkinter as ctk
from tkinter import ttk

def apply_theme_to_treeview():
    if ctk.get_appearance_mode() == "Light":
        style.configure("Treeview", background="white", fieldbackground="white", foreground="black")
        style.configure("Treeview.Heading", background="white", foreground="black")
    else:
        style.configure("Treeview", background="#383838", fieldbackground="#383838", foreground="white")
        style.configure("Treeview.Heading", background="#383838", foreground="white")

def style_theme(root):
    root.option_add("*TCombobox*Listbox*Foreground", "black" if ctk.get_appearance_mode() == "Light" else "white")
    root.option_add("*TCombobox*Listbox*Background", "white" if ctk.get_appearance_mode() == "Light" else "#383838")
