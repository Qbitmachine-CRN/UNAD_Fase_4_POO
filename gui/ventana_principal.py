# -*- coding: utf-8 -*-
"""
Interfaz Tkinter alineada con core (Cliente, Reserva), servicios concretos y utils.
"""

from __future__ import annotations

import tkinter as tk
from tkinter import messagebox

from core.cliente import Cliente
from core.reserva import Reserva
from .componentes import aplicar_estilo_oscuro_ttk, boton_sidebar, combobox_oscuro, limpiar_frame
from servicios.asesoria import Asesoria
from servicios.base_servicio import Servicio
from servicios.equipo import AlquilerEquipo
from servicios.sala import ReservaSala
from utils.excepciones import SoftwareFJError
from utils.logger import registrar_evento, registrar_excepcion

BG = "#121212"
SIDEBAR = "#1f1f1f"
CARD = "#1e1e1e"
FG = "#ffffff"
ACCENT = "#4CAF50"
INPUT_BG = "#2a2a2a"

# Etiquetas visibles del combobox -> código interno para servicios
_OPCIONES_SERVICIO: tuple[tuple[str, str], ...] = (
    ("Asesoría especializada", "asesoria"),
    ("Alquiler de equipo", "equipo"),
    ("Reserva de sala", "sala"),
)
_ETIQUETAS_SERVICIO: tuple[str, ...] = tuple(x[0] for x in _OPCIONES_SERVICIO)
_NIVELES_ASESORIA: tuple[str, ...] = ("Junior", "Semi", "Senior")


def _codigo_servicio_desde_etiqueta(etiqueta: str) -> str:
    for label, code in _OPCIONES_SERVICIO:
        if label == etiqueta:
            return code
    return "asesoria"


def _nivel_asesoria_desde_etiqueta(etiqueta: str) -> str:
    return etiqueta.strip().lower()


def _id_cliente_desde_combo(linea: str) -> str:
    """El combo muestra 'ID | nombre'; devuelve solo el identificador."""
    if not linea.strip():
        return ""
    return linea.split(" | ", 1)[0].strip()


_cliente_seq = 0
_reserva_seq = 0
clientes_guardados: list[Cliente] = []
reservas_guardadas: list[Reserva] = []


def _siguiente_id_cliente() -> str:
    global _cliente_seq
    _cliente_seq += 1
    return f"C-GUI-{_cliente_seq:04d}"


def _siguiente_id_reserva() -> str:
    global _reserva_seq
    _reserva_seq += 1
    return f"R-GUI-{_reserva_seq:04d}"


def _fabricar_servicio(tipo: str) -> Servicio:
    """Instancias coherentes con la simulación de main.py (tarifas de ejemplo)."""
    if tipo == "asesoria":
        return Asesoria("A-GUI", 100.0, "senior")
    if tipo == "equipo":
        return AlquilerEquipo("E-GUI", 50.0, "Laptop", 20.0)
    return ReservaSala("S-GUI", 80.0, 10)


def _mensaje_error(exc: BaseException) -> str:
    if isinstance(exc, SoftwareFJError):
        return exc.mensaje
    return str(exc)


def iniciar_app() -> None:
    ventana = tk.Tk()
    aplicar_estilo_oscuro_ttk(ventana)
    ventana.title("Software FJ — Gestión")
    ventana.geometry("820x520")
    ventana.configure(bg=BG)

    sidebar = tk.Frame(ventana, bg=SIDEBAR, width=200)
    sidebar.pack(side="left", fill="y")

    contenido = tk.Frame(ventana, bg=BG)
    contenido.pack(side="right", expand=True, fill="both")

    tk.Label(
        sidebar,
        text="MENÚ",
        bg=SIDEBAR,
        fg=FG,
        font=("Arial", 14, "bold"),
    ).pack(pady=20)

    boton_sidebar(sidebar, "Clientes", lambda: vista_clientes(contenido)).pack(fill="x")
    boton_sidebar(sidebar, "Reservas", lambda: vista_reservas(contenido)).pack(fill="x")
    boton_sidebar(sidebar, "Servicios", lambda: vista_servicios(contenido)).pack(fill="x")

    ventana.mainloop()


def vista_clientes(frame: tk.Frame) -> None:
    limpiar_frame(frame)

    tk.Label(
        frame,
        text="Gestión de clientes",
        bg=BG,
        fg=FG,
        font=("Arial", 16, "bold"),
    ).pack(pady=20)

    card = tk.Frame(frame, bg=CARD, padx=20, pady=20)
    card.pack(pady=10)

    _ent_kw = dict(width=40, bg=INPUT_BG, fg=FG, insertbackground=FG, relief="flat", highlightthickness=1)
    _ent_kw["highlightbackground"] = "#444444"
    _ent_kw["highlightcolor"] = ACCENT

    tk.Label(card, text="Nombre completo", bg=CARD, fg=FG).grid(row=0, column=0, sticky="w", pady=2)
    entrada_nombre = tk.Entry(card, **_ent_kw)
    entrada_nombre.grid(row=0, column=1, padx=8, pady=2)

    tk.Label(card, text="Correo", bg=CARD, fg=FG).grid(row=1, column=0, sticky="w", pady=2)
    entrada_correo = tk.Entry(card, **_ent_kw)
    entrada_correo.grid(row=1, column=1, padx=8, pady=2)

    tk.Label(card, text="Teléfono", bg=CARD, fg=FG).grid(row=2, column=0, sticky="w", pady=2)
    entrada_telefono = tk.Entry(card, **_ent_kw)
    entrada_telefono.grid(row=2, column=1, padx=8, pady=2)

    lista = tk.Listbox(frame, width=72, height=10, bg="#2a2a2a", fg=FG, selectbackground=ACCENT)
    lista.pack(pady=10, padx=12, fill="x")

    def actualizar_lista() -> None:
        lista.delete(0, tk.END)
        for c in clientes_guardados:
            lista.insert(tk.END, f"{c.identificador} | {c.resumen()} | tel {c.telefono}")

    def guardar() -> None:
        try:
            nuevo = Cliente(
                _siguiente_id_cliente(),
                entrada_nombre.get(),
                entrada_correo.get(),
                entrada_telefono.get(),
            )
            clientes_guardados.append(nuevo)
            registrar_evento(f"GUI: cliente registrado {nuevo.identificador}", "INFO")
            messagebox.showinfo("Éxito", f"Cliente guardado: {nuevo.identificador}")
            entrada_nombre.delete(0, tk.END)
            entrada_correo.delete(0, tk.END)
            entrada_telefono.delete(0, tk.END)
            entrada_nombre.focus_set()
            actualizar_lista()
        except SoftwareFJError as err:
            registrar_excepcion("GUI: validación de cliente", err)
            messagebox.showerror("Validación", _mensaje_error(err))
        except Exception as err:
            registrar_excepcion("GUI: error inesperado al crear cliente", err)
            messagebox.showerror("Error", str(err))

    tk.Button(frame, text="Guardar cliente", bg=ACCENT, fg="white", command=guardar).pack(pady=10)
    actualizar_lista()


def vista_reservas(frame: tk.Frame) -> None:
    limpiar_frame(frame)

    tk.Label(
        frame,
        text="Gestión de reservas",
        bg=BG,
        fg=FG,
        font=("Arial", 16, "bold"),
    ).pack(pady=20)

    card = tk.Frame(frame, bg=CARD, padx=20, pady=20)
    card.pack(pady=10)

    tk.Label(card, text="Cliente", bg=CARD, fg=FG).grid(row=0, column=0, sticky="w")
    cliente_var = tk.StringVar(value="")
    combo_cliente = combobox_oscuro(card, cliente_var, (), width=48)
    combo_cliente.grid(row=0, column=1, sticky="ew", padx=(8, 0))

    tk.Label(card, text="Duración (horas)", bg=CARD, fg=FG).grid(row=1, column=0, sticky="w", pady=(8, 0))
    entrada_horas = tk.Entry(
        card,
        width=12,
        bg=INPUT_BG,
        fg=FG,
        insertbackground=FG,
        relief="flat",
        highlightthickness=1,
        highlightbackground="#444444",
        highlightcolor=ACCENT,
    )
    entrada_horas.grid(row=1, column=1, sticky="w", pady=(8, 0), padx=(8, 0))

    tk.Label(card, text="Tipo de servicio", bg=CARD, fg=FG).grid(row=2, column=0, sticky="w", pady=(8, 0))
    servicio_var = tk.StringVar(value=_ETIQUETAS_SERVICIO[0])
    combo_servicio = combobox_oscuro(card, servicio_var, _ETIQUETAS_SERVICIO, width=32)
    combo_servicio.grid(row=2, column=1, sticky="w", pady=(8, 0), padx=(8, 0))

    lista_reservas = tk.Listbox(frame, width=78, height=10, bg="#2a2a2a", fg=FG, selectbackground=ACCENT)
    lista_reservas.pack(pady=10, padx=12, fill="x")

    def refrescar_combo_clientes() -> None:
        vals = [f"{c.identificador} | {c.nombre_completo}" for c in clientes_guardados]
        combo_cliente["values"] = vals
        if vals:
            cliente_var.set(vals[0])
        else:
            cliente_var.set("")

    def actualizar_lista() -> None:
        lista_reservas.delete(0, tk.END)
        for r in reservas_guardadas:
            lista_reservas.insert(tk.END, r.resumen())

    def guardar() -> None:
        try:
            if not clientes_guardados:
                messagebox.showwarning("Clientes", "Registre al menos un cliente en el menú Clientes.")
                return
            cid = _id_cliente_desde_combo(cliente_var.get())
            cliente = next((c for c in clientes_guardados if c.identificador == cid), None)
            if cliente is None:
                messagebox.showerror("Cliente", "Seleccione un cliente válido.")
                return
            horas = float(entrada_horas.get().replace(",", "."))
            codigo = _codigo_servicio_desde_etiqueta(servicio_var.get())
            servicio = _fabricar_servicio(codigo)
            nueva = Reserva(_siguiente_id_reserva(), cliente, servicio, horas)
            reservas_guardadas.append(nueva)
            registrar_evento(f"GUI: reserva creada {nueva.identificador} (pendiente)", "INFO")
            messagebox.showinfo("Éxito", f"Reserva creada: {nueva.identificador}\nEstado: pendiente de confirmación.")
            entrada_horas.delete(0, tk.END)
            actualizar_lista()
        except ValueError:
            messagebox.showerror("Duración", "Indique un número válido de horas.")
        except SoftwareFJError as err:
            registrar_excepcion("GUI: error de dominio al crear reserva", err)
            messagebox.showerror("Reserva", _mensaje_error(err))
        except Exception as err:
            registrar_excepcion("GUI: error inesperado al crear reserva", err)
            messagebox.showerror("Error", str(err))

    def procesar_seleccionada() -> None:
        """Confirma la reserva seleccionada usando Reserva.confirmar / lógica del core."""
        try:
            sel = lista_reservas.curselection()
            if not sel:
                messagebox.showwarning("Reserva", "Seleccione una reserva en la lista.")
                return
            r = reservas_guardadas[sel[0]]
            costo = r.confirmar()
            registrar_evento(f"GUI: reserva confirmada {r.identificador}, costo={costo}", "INFO")
            messagebox.showinfo("Confirmada", f"Costo calculado: {costo}\n{r.resumen()}")
            actualizar_lista()
        except SoftwareFJError as err:
            registrar_excepcion("GUI: no se pudo confirmar reserva", err)
            messagebox.showerror("Confirmación", _mensaje_error(err))
        except Exception as err:
            registrar_excepcion("GUI: error inesperado al confirmar", err)
            messagebox.showerror("Error", str(err))

    def cancelar() -> None:
        try:
            seleccion = lista_reservas.curselection()
            if not seleccion:
                messagebox.showwarning("Reserva", "Seleccione una reserva.")
                return
            index = seleccion[0]
            reserva = reservas_guardadas[index]
            reserva.cancelar("Cancelación desde GUI")
            reservas_guardadas.pop(index)
            registrar_evento(f"GUI: reserva eliminada de la sesión {reserva.identificador}", "INFO")
            messagebox.showinfo("Cancelado", f"Reserva {reserva.identificador} cancelada y quitada de la lista.")
            actualizar_lista()
        except SoftwareFJError as err:
            registrar_excepcion("GUI: cancelar reserva", err)
            messagebox.showerror("Cancelar", _mensaje_error(err))
        except Exception as err:
            registrar_excepcion("GUI: error inesperado al cancelar", err)
            messagebox.showerror("Error", str(err))

    tk.Button(frame, text="Crear reserva (pendiente)", bg=ACCENT, fg="white", command=guardar).pack(pady=6)
    tk.Button(frame, text="Confirmar seleccionada", bg="#1565C0", fg="white", command=procesar_seleccionada).pack(
        pady=4
    )
    tk.Button(frame, text="Cancelar y quitar de la lista", bg="#c62828", fg="white", command=cancelar).pack(pady=4)

    card.columnconfigure(1, weight=1)
    refrescar_combo_clientes()
    actualizar_lista()


def vista_servicios(frame: tk.Frame) -> None:
    limpiar_frame(frame)

    tk.Label(frame, text="Servicios", bg=BG, fg=FG, font=("Arial", 16, "bold")).pack(pady=20)

    card = tk.Frame(frame, bg=CARD, padx=20, pady=20)
    card.pack(pady=10)

    tk.Label(card, text="Tipo", bg=CARD, fg=FG).grid(row=0, column=0, pady=5, sticky="w")
    tipo_var = tk.StringVar(value=_ETIQUETAS_SERVICIO[0])
    combobox_oscuro(card, tipo_var, _ETIQUETAS_SERVICIO, width=32).grid(row=0, column=1, sticky="w", padx=(8, 0))

    tk.Label(card, text="Nivel (asesoría)", bg=CARD, fg=FG).grid(row=1, column=0, pady=5, sticky="w")
    nivel_var = tk.StringVar(value=_NIVELES_ASESORIA[2])
    combobox_oscuro(card, nivel_var, _NIVELES_ASESORIA, width=14).grid(row=1, column=1, sticky="w", padx=(8, 0))

    _eh = dict(bg=INPUT_BG, fg=FG, insertbackground=FG, relief="flat", highlightthickness=1)
    _eh["highlightbackground"] = "#444444"
    _eh["highlightcolor"] = ACCENT

    tk.Label(card, text="Horas", bg=CARD, fg=FG).grid(row=2, column=0, pady=5, sticky="w")
    entrada_horas = tk.Entry(card, width=10, **_eh)
    entrada_horas.grid(row=2, column=1, sticky="w", padx=(8, 0))

    tk.Label(card, text="IVA % (opcional)", bg=CARD, fg=FG).grid(row=3, column=0, pady=5, sticky="w")
    entrada_iva = tk.Entry(card, width=10, **_eh)
    entrada_iva.grid(row=3, column=1, sticky="w", padx=(8, 0))

    tk.Label(card, text="Descuento % (opcional)", bg=CARD, fg=FG).grid(row=4, column=0, pady=5, sticky="w")
    entrada_desc = tk.Entry(card, width=10, **_eh)
    entrada_desc.grid(row=4, column=1, sticky="w", padx=(8, 0))

    texto_desc = tk.Text(frame, height=4, width=72, bg="#2a2a2a", fg=FG, wrap="word")
    texto_desc.pack(pady=12, padx=12, fill="x")

    def servicio_por_tipo(etiqueta_tipo: str) -> Servicio:
        codigo = _codigo_servicio_desde_etiqueta(etiqueta_tipo)
        if codigo == "asesoria":
            return Asesoria("A-GUI", 100.0, _nivel_asesoria_desde_etiqueta(nivel_var.get()))
        if codigo == "equipo":
            return AlquilerEquipo("E-GUI", 50.0, "Laptop", 20.0)
        return ReservaSala("S-GUI", 80.0, 10)

    def calcular() -> None:
        try:
            horas = float(entrada_horas.get().replace(",", "."))
            servicio = servicio_por_tipo(tipo_var.get())
            iva_txt = entrada_iva.get().strip()
            desc_txt = entrada_desc.get().strip()
            if iva_txt or desc_txt:
                iva = float(iva_txt.replace(",", ".")) if iva_txt else None
                desc = float(desc_txt.replace(",", ".")) if desc_txt else None
                total = servicio.calcular_costo_avanzado(horas, iva, desc)
            else:
                total = servicio.calcular_costo(horas)
            texto_desc.delete("1.0", tk.END)
            texto_desc.insert(tk.END, servicio.describir_servicio())
            registrar_evento(
                f"GUI: cotización {_codigo_servicio_desde_etiqueta(tipo_var.get())} horas={horas} total={total}",
                "INFO",
            )
            messagebox.showinfo("Costo", f"Total: {total}\n\n{servicio.describir_servicio()}")
        except ValueError:
            messagebox.showerror("Datos", "Use números válidos en horas, IVA o descuento.")
        except SoftwareFJError as err:
            registrar_excepcion("GUI: cálculo de servicio", err)
            messagebox.showerror("Servicio", _mensaje_error(err))
        except Exception as err:
            registrar_excepcion("GUI: error inesperado en servicio", err)
            messagebox.showerror("Error", str(err))

    tk.Button(frame, text="Calcular costo", bg=ACCENT, fg="white", relief="flat", command=calcular).pack(pady=15)
