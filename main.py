# -*- coding: utf-8 -*-
"""
Punto de entrada de Software FJ: simulación en consola y opción de GUI Tkinter.

Ejecutar desde la carpeta del proyecto:
    python main.py          -> abre la interfaz gráfica
    python main.py sim      -> solo simulación por consola (10+ operaciones)
"""

from __future__ import annotations

import sys

from core.cliente import Cliente
from core.reserva import Reserva
from servicios.asesoria import Asesoria
from servicios.equipo import AlquilerEquipo
from servicios.sala import ReservaSala
from utils.excepciones import (
    DatosFaltantesError,
    SoftwareFJError,
    ValidacionError,
)
from utils.logger import registrar_evento, registrar_excepcion


def ejecutar_simulacion() -> None:
    """
    Ejecuta al menos diez operaciones válidas e inválidas sin detener el programa.

    Demuestra try/except, try/except/else, try/except/finally y encadenamiento.
    """
    registrar_evento("=== INICIO SIMULACIÓN ACADÉMICA SOFTWARE FJ ===", "INFO")
    clientes: list[Cliente] = []
    sala = ReservaSala("SALA-SIM", 40.0, 8, disponible=True)
    equipo_ok = AlquilerEquipo("EQ-SIM", 12.0, "Notebook", costo_seguro_fijo=10.0, disponible=True)

    # Operación 1: cliente válido.
    try:
        c1 = Cliente("C-0001", "Ana María López", "ana.lopez@correo.com", "3001234567")
        clientes.append(c1)
        registrar_evento("Op1: Cliente válido registrado en memoria.", "INFO")
    except Exception as exc:
        registrar_excepcion("Op1 fallida", exc)

    # Operación 2: email inválido (captura explícita).
    try:
        Cliente("C-0002", "Pedro Ruiz", "correo-sin-arroba", "3009876543")
    except ValidacionError as err:
        registrar_excepcion("Op2: email inválido controlado", err)
    else:
        registrar_evento("Op2: no debía tener éxito", "WARNING")
    finally:
        registrar_evento("Op2: bloque finally ejecutado.", "INFO")

    # Operación 3: teléfono insuficiente usando fábrica segura (else/finally en Cliente.crear_seguro).
    c3 = Cliente.crear_seguro("C-0003", "Luis Gómez", "luis@g.com", "123")
    if c3 is None:
        registrar_evento("Op3: creación segura devolvió None por teléfono corto.", "INFO")

    # Operación 4: tipo de equipo vacío al construir servicio.
    try:
        AlquilerEquipo("EQ-BAD", 10.0, "", 0.0)
    except ValidacionError as err:
        registrar_excepcion("Op4: equipo con tipo vacío", err)

    # Operación 5: nivel de asesoría no permitido.
    try:
        Asesoria("ASE-BAD", 50.0, "ninja")
    except ValidacionError as err:
        registrar_excepcion("Op5: nivel de asesoría inválido", err)

    # Operación 6: reserva y confirmación exitosa con costo avanzado (impuesto y descuento).
    try:
        r_ok = Reserva("R-00001", clientes[0], equipo_ok, 3.0)
        costo_base = r_ok.servicio.calcular_costo(3.0)
        costo_taxes = r_ok.servicio.calcular_costo_avanzado(3.0, 19.0, 5.0)
        registrar_evento(f"Op6: costo base={costo_base}, con IVA y descuento={costo_taxes}", "INFO")
        monto = r_ok.confirmar()
        registrar_evento(f"Op6: reserva confirmada, monto facturado={monto}", "INFO")
    except Exception as exc:
        registrar_excepcion("Op6: error inesperado", exc)

    # Operación 7: sala marcada no disponible e intento de reserva.
    sala.marcar_indisponible()
    try:
        r7 = Reserva("R-00002", clientes[0], sala, 2.0)
        r7.confirmar()
    except Exception as err:
        registrar_excepcion("Op7: reserva en sala no disponible", err)
    finally:
        sala.marcar_disponible()
        registrar_evento("Op7: sala reactivada en finally.", "INFO")

    # Operación 8: duración inválida al crear Reserva.
    try:
        Reserva("R-BAD", clientes[0], equipo_ok, 0.0)
    except Exception as err:
        registrar_excepcion("Op8: duración cero", err)

    # Operación 9: encadenamiento de excepciones (raise ... from).
    try:
        try:
            int("no-es-numero")
        except ValueError as causa:
            raise DatosFaltantesError("No se pudo interpretar un número de operación.") from causa
    except DatosFaltantesError as err:
        registrar_excepcion("Op9: encadenamiento ValueError -> DatosFaltantesError", err)

    # Operación 10: confirmar dos veces la misma reserva (estado no pendiente).
    try:
        r_dup = Reserva("R-00003", clientes[0], equipo_ok, 1.0)
        r_dup.confirmar()
        r_dup.confirmar()
    except Exception as err:
        registrar_excepcion("Op10: segunda confirmación rechazada", err)

    # Operación 11: cálculo inconsistente simulado (descuento fuera de rango).
    try:
        equipo_ok.calcular_costo_avanzado(2.0, 10.0, 95.0)
    except ValidacionError as err:
        registrar_excepcion("Op11: descuento extremo rechazado", err)

    # Operación 12: try/except/else/finally leyendo el archivo de log (solo demostración).
    ruta_log = None
    try:
        from pathlib import Path

        raiz = Path(__file__).resolve().parent
        ruta_log = raiz / "log_eventos.txt"
        ultima = ruta_log.read_text(encoding="utf-8")[-200:]
    except OSError as err:
        registrar_excepcion("Op12: no se pudo leer el log", err)
    else:
        registrar_evento(f"Op12: lectura parcial del log OK ({len(ultima)} chars finales).", "INFO")
    finally:
        registrar_evento("Op12: finally tras intento de lectura del log.", "INFO")

    # Operación 13: error genérico envuelto en SoftwareFJError.
    try:
        try:
            raise RuntimeError("Fallo interno simulado")
        except RuntimeError as err:
            raise SoftwareFJError("Operación abortada por fallo interno.") from err
    except SoftwareFJError as err:
        registrar_excepcion("Op13: SoftwareFJError con causa RuntimeError", err)

    registrar_evento("=== FIN SIMULACIÓN: el sistema sigue activo ===", "INFO")


def main() -> None:
    """Arranque: simulación y/o interfaz según argumentos."""
    modo = [a.lower() for a in sys.argv[1:] if not a.startswith("-")]
    if "sim" in modo or "simulacion" in modo or "--solo-sim" in sys.argv:
        ejecutar_simulacion()
        return
    # Por defecto abre Tkinter tras registrar arranque.
    registrar_evento("Inicio aplicación con interfaz gráfica", "INFO")
    try:
        from gui import iniciar_app

        iniciar_app()
    except Exception as exc:
        registrar_excepcion("Fallo crítico al iniciar la GUI", exc)
        raise


if __name__ == "__main__":
    main()
