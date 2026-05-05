# -*- coding: utf-8 -*-
"""Paquete de utilidades: excepciones personalizadas y registro en archivo."""

from .excepciones import (
    CalculoInconsistenteError,
    DatosFaltantesError,
    OperacionNoPermitidaError,
    ReservaError,
    ServicioNoDisponibleError,
    SoftwareFJError,
    ValidacionError,
)
from .logger import registrar_evento, registrar_excepcion

__all__ = [
    "CalculoInconsistenteError",
    "DatosFaltantesError",
    "OperacionNoPermitidaError",
    "ReservaError",
    "ServicioNoDisponibleError",
    "SoftwareFJError",
    "ValidacionError",
    "registrar_evento",
    "registrar_excepcion",
]
