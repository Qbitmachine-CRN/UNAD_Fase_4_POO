import tkinter as tk
from tkinter import messagebox
from gui.componentes import boton_sidebar, limpiar_frame
from servicios.asesoria import Asesoria
from servicios.equipo import AlquilerEquipo
from servicios.sala import ReservaSala
from utils.logger import registrar_evento, registrar_excepcion

#COLORES PARA USAR
BG = "#121212"
SIDEBAR = "#1f1f1f"
CARD = "#1e1e1e"
FG = "#ffffff"
ACCENT = "#4CAF50"

reservas_guardadas = []
clientes_guardados = []

#IMPORTS FALTANTES
try:
    from core.cliente import Cliente
    from core.reserva import Reserva
except:
    #Clases Temporales
    class Cliente:
        def __init__(self, nombre):
            if nombre == "":
                raise ValueError("Nombre vacío")
            self.nombre = nombre

    class Reserva:
        def __init__(self, cliente, fecha):
            if fecha == "":
                raise ValueError("Fecha vacía")
            self.cliente = cliente
            self.fecha = fecha

#APP PRINCIPAL
def iniciar_app():
    ventana = tk.Tk()
    ventana.title("Sistema de Gestión")
    ventana.geometry("800x500")
    ventana.configure(bg=BG)

    #BarraLateral
    sidebar = tk.Frame(ventana, bg=SIDEBAR, width=200)
    sidebar.pack(side="left", fill="y")

    #Contenido
    contenido = tk.Frame(ventana, bg=BG)
    contenido.pack(side="right", expand=True, fill="both")

    tk.Label(
        sidebar,
        text="MENÚ",
        bg=SIDEBAR,
        fg=FG,
        font=("Arial", 14, "bold")
    ).pack(pady=20)

    boton_sidebar(sidebar, "Clientes", lambda: vista_clientes(contenido)).pack(fill="x")
    boton_sidebar(sidebar, "Reservas", lambda: vista_reservas(contenido)).pack(fill="x")
    boton_sidebar(sidebar, "Servicios", lambda: vista_servicios(contenido)).pack(fill="x")

    ventana.mainloop()


#VISTA DE CLIENTES
def vista_clientes(frame):
    limpiar_frame(frame)

    tk.Label(frame, text="Gestión de Clientes", bg=BG, fg=FG,
             font=("Arial", 16, "bold")).pack(pady=20)

    card = tk.Frame(frame, bg=CARD, padx=20, pady=20)
    card.pack(pady=10)

    # CAMPOS
    tk.Label(card, text="Nombre", bg=CARD, fg=FG).grid(row=0, column=0)
    entrada_nombre = tk.Entry(card)
    entrada_nombre.grid(row=0, column=1)

    tk.Label(card, text="Correo", bg=CARD, fg=FG).grid(row=1, column=0)
    entrada_correo = tk.Entry(card)
    entrada_correo.grid(row=1, column=1)

    tk.Label(card, text="Teléfono", bg=CARD, fg=FG).grid(row=2, column=0)
    entrada_telefono = tk.Entry(card)
    entrada_telefono.grid(row=2, column=1)

    lista = tk.Listbox(frame, width=50)
    lista.pack(pady=10)

    def actualizar_lista():
        lista.delete(0, tk.END)
        for c in clientes_guardados:
            lista.insert(tk.END, f"{c['nombre']} | {c['correo']} | {c['telefono']}")

    def guardar():
        try:
            cliente = {
                "nombre": entrada_nombre.get(),
                "correo": entrada_correo.get(),
                "telefono": entrada_telefono.get()
            }

            if not cliente["nombre"]:
                raise Exception("Nombre obligatorio")

            clientes_guardados.append(cliente)

            registrar_evento(f"Cliente creado: {cliente}")
            messagebox.showinfo("Éxito", "Cliente guardado")

            actualizar_lista()

        except Exception as e:
            registrar_excepcion("Error cliente", e)
            messagebox.showerror("Error", str(e))

    tk.Button(frame, text="Guardar Cliente",
              bg=ACCENT, fg="white", command=guardar).pack(pady=10)

    actualizar_lista()

#VISTA DE RESERVAS
def vista_reservas(frame):
    limpiar_frame(frame)

    tk.Label(frame, text="Gestión de Reservas", bg=BG, fg=FG,
             font=("Arial", 16, "bold")).pack(pady=20)

    card = tk.Frame(frame, bg=CARD, padx=20, pady=20)
    card.pack(pady=10)

    # ---------------- CLIENTES ----------------
    tk.Label(card, text="Cliente", bg=CARD, fg=FG).grid(row=0, column=0)

    nombres = [c["nombre"] for c in clientes_guardados]
    cliente_var = tk.StringVar()

    if nombres:
        cliente_var.set(nombres[0])

    tk.OptionMenu(card, cliente_var, *nombres).grid(row=0, column=1)

    # ---------------- FECHA ----------------
    tk.Label(card, text="Fecha", bg=CARD, fg=FG).grid(row=1, column=0)
    entrada_fecha = tk.Entry(card)
    entrada_fecha.grid(row=1, column=1)

    # ---------------- SERVICIO ----------------
    tk.Label(card, text="Servicio", bg=CARD, fg=FG).grid(row=2, column=0)
    servicio_var = tk.StringVar(value="asesoria")

    tk.OptionMenu(card, servicio_var, "asesoria", "equipo", "sala").grid(row=2, column=1)

    # ---------------- LISTA ----------------
    lista_reservas = tk.Listbox(frame, width=60)
    lista_reservas.pack(pady=10)

    def actualizar_lista():
        lista_reservas.delete(0, tk.END)
        for r in reservas_guardadas:
            texto = f"{r['cliente']} | {r['fecha']} | {r['servicio']}"
            lista_reservas.insert(tk.END, texto)

    # ---------------- GUARDAR ----------------
    def guardar():
        try:
            if not clientes_guardados:
                raise Exception("No hay clientes")

            reserva = {
                "cliente": cliente_var.get(),
                "fecha": entrada_fecha.get(),
                "servicio": servicio_var.get()
            }

            reservas_guardadas.append(reserva)

            registrar_evento(f"Reserva creada: {reserva}")
            messagebox.showinfo("Éxito", "Reserva creada")

            actualizar_lista()

        except Exception as e:
            registrar_excepcion("Error reserva", e)
            messagebox.showerror("Error", str(e))

    # ---------------- CANCELAR SELECCIONADA ----------------
    def cancelar():
        try:
            seleccion = lista_reservas.curselection()

            if not seleccion:
                raise Exception("Selecciona una reserva")

            index = seleccion[0]
            reserva = reservas_guardadas.pop(index)

            registrar_evento(f"Reserva cancelada: {reserva}")
            messagebox.showinfo("Cancelado", f"{reserva['cliente']} eliminado")

            actualizar_lista()

        except Exception as e:
            registrar_excepcion("Error cancelar", e)
            messagebox.showerror("Error", str(e))

    # ---------------- BOTONES ----------------
    tk.Button(frame, text="Guardar Reserva",
              bg=ACCENT, fg="white", command=guardar).pack(pady=10)

    tk.Button(frame, text="Cancelar seleccionada",
              bg="red", fg="white", command=cancelar).pack()

    actualizar_lista()
              
#VISTA DE SERVICIOS
def vista_servicios(frame):
    limpiar_frame(frame)

    tk.Label(
        frame,
        text="Servicios",
        bg=BG,
        fg=FG,
        font=("Arial", 16, "bold")
    ).pack(pady=20)

    card = tk.Frame(frame, bg=CARD, padx=20, pady=20)
    card.pack(pady=10)

    tk.Label(card, text="Tipo", bg=CARD, fg=FG).grid(row=0, column=0, pady=5)
    tipo_var = tk.StringVar(value="asesoria")

    opciones = ["asesoria", "equipo", "sala"]
    tk.OptionMenu(card, tipo_var, *opciones).grid(row=0, column=1)

    tk.Label(card, text="Horas", bg=CARD, fg=FG).grid(row=1, column=0, pady=5)
    entrada_horas = tk.Entry(card)
    entrada_horas.grid(row=1, column=1)

    def calcular():
        try:
            horas = float(entrada_horas.get())

            if tipo_var.get() == "asesoria":
                servicio = Asesoria("A1", 100, "senior")

            elif tipo_var.get() == "equipo":
                servicio = AlquilerEquipo("E1", 50, "Laptop", 20)

            else:
                servicio = ReservaSala("S1", 80, 10)

            costo = servicio.calcular_costo(horas)

            registrar_evento(f"Servicio calculado: {tipo_var.get()} - costo {costo}")
            messagebox.showinfo("Costo", f"Costo total: {costo}")

        except Exception as e:
            registrar_excepcion("Error al calcular servicio", e)
            messagebox.showerror("Error", str(e))

    tk.Button(
        frame,
        text="Calcular costo",
        bg=ACCENT,
        fg="white",
        relief="flat",
        command=calcular
    ).pack(pady=15)
