import tkinter as tk

#COLORES PARA USAR
BG = "#121212"
SIDEBAR = "#1f1f1f"
FG = "#ffffff"
ACCENT = "#4CAF50"

def boton_sidebar(parent, texto, comando):
    return tk.Button(
        parent,
        text=texto,
        command=comando,
        bg=SIDEBAR,
        fg=FG,
        activebackground=ACCENT,
        relief="flat",
        bd=0,
        anchor="w",
        padx=15,
        pady=10
    )

def limpiar_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()
