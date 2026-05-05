# -*- coding: utf-8 -*-
"""
Configuración de registro de eventos y errores en archivo de texto.

Centraliza la escritura en log_eventos.txt con marca de tiempo.
"""

from __future__ import annotations

import os
from datetime import datetime
from threading import Lock


# Bloqueo para escrituras concurrentes seguras desde GUI y simulación.
_lock_escritura: Lock = Lock()


def _ruta_log() -> str:
    """Resuelve la ruta absoluta del archivo de log junto al proyecto."""
    # Directorio del paquete utils.
    aqui = os.path.dirname(os.path.abspath(__file__))
    # Sube un nivel a la raíz del proyecto SoftwareFJ_Project.
    raiz = os.path.dirname(aqui)
    # Nombre del archivo de eventos según la especificación de la tarea.
    return os.path.join(raiz, "log_eventos.txt")


def registrar_evento(mensaje: str, nivel: str = "INFO") -> None:
    """
    Escribe una línea en el archivo de log con fecha, hora y nivel.

    Args:
        mensaje: Texto descriptivo del evento o error.
        nivel: Etiqueta de severidad (INFO, WARNING, ERROR, etc.).
    """
    # Marca temporal ISO local para trazabilidad.
    ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Formato de línea única y fácil de filtrar.
    linea = f"[{ahora}] [{nivel.upper()}] {mensaje}\n"
    # Protege la escritura ante accesos simultáneos.
    with _lock_escritura:
        # Abre en modo append con codificación UTF-8.
        with open(_ruta_log(), "a", encoding="utf-8") as archivo:
            # Escribe la línea al final del archivo.
            archivo.write(linea)


def registrar_excepcion(mensaje_contexto: str, exc: BaseException) -> None:
    """
    Registra una excepción con su tipo y mensaje en el log.

    Args:
        mensaje_contexto: Dónde ocurrió el fallo.
        exc: Instancia de excepción capturada.
    """
    # Construye texto con tipo y args de la excepción.
    texto = f"{mensaje_contexto} | {type(exc).__name__}: {exc}"
    # Usa nivel ERROR para distinguir de eventos informativos.
    registrar_evento(texto, "ERROR")
