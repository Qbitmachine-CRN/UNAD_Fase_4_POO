# -*- coding: utf-8 -*-
"""Widgets reutilizables y estilo ttk para la interfaz oscura."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk

BG = "#121212"
SIDEBAR = "#1f1f1f"
FG = "#ffffff"
ACCENT = "#4CAF50"
FIELD_BG = "#2a2a2a"


def aplicar_estilo_oscuro_ttk(maestro: tk.Misc) -> ttk.Style:
    """Configura tema clam y estilos para Combobox acorde al fondo oscuro."""
    style = ttk.Style(maestro)
    try:
        style.theme_use("clam")
    except tk.TclError:
        pass
    style.configure(
        "Dark.TCombobox",
        fieldbackground=FIELD_BG,
        background=FIELD_BG,
        foreground=FG,
        arrowcolor=FG,
        borderwidth=1,
        lightcolor="#3d3d3d",
        darkcolor="#1a1a1a",
    )
    style.map(
        "Dark.TCombobox",
        fieldbackground=[("readonly", FIELD_BG), ("disabled", "#1a1a1a")],
        selectbackground=[("readonly", ACCENT)],
        selectforeground=[("readonly", "#ffffff")],
    )
    return style


def combobox_oscuro(
    parent: tk.Misc,
    textvariable: tk.StringVar,
    values: tuple[str, ...] | list[str],
    *,
    width: int = 32,
    state: str = "readonly",
) -> ttk.Combobox:
    """Combobox de solo lectura con estilo oscuro."""
    cb = ttk.Combobox(
        parent,
        textvariable=textvariable,
        values=values,
        width=width,
        state=state,
        style="Dark.TCombobox",
    )
    return cb


def boton_sidebar(parent: tk.Misc, texto: str, comando) -> tk.Button:
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
        pady=10,
    )


def limpiar_frame(frame: tk.Frame) -> None:
    for widget in frame.winfo_children():
        widget.destroy()
