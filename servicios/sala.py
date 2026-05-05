# -*- coding: utf-8 -*-
"""
Servicio especializado: reserva de salas de reunión o capacitación.
"""

from __future__ import annotations

from .base_servicio import Servicio
from utils.excepciones import ServicioNoDisponibleError, ValidacionError


class ReservaSala(Servicio):
    """Alquiler de sala con capacidad máxima y recargo por hora extra."""

    def __init__(
        self,
        codigo_interno: str,
        tarifa_base_hora: float,
        capacidad_personas: int,
        disponible: bool = True,
    ) -> None:
        # Validación de capacidad al construir.
        if capacidad_personas < 1:
            raise ValidacionError("La capacidad debe ser al menos 1 persona.", "capacidad_personas")
        super().__init__(codigo_interno, tarifa_base_hora, disponible)
        self._capacidad_personas = int(capacidad_personas)

    @property
    def capacidad_personas(self) -> int:
        """Aforo máximo de la sala."""
        return self._capacidad_personas

    def calcular_costo(self, horas: float, **kwargs) -> float:
        """Costo = tarifa * horas; horas > 8 aplican 10% recargo."""
        if not self.disponible:
            raise ServicioNoDisponibleError("La sala no está disponible.", self.nombre_publico())
        if horas <= 0:
            raise ValidacionError("Las horas deben ser positivas.", "horas")
        total = self.tarifa_base_hora * horas
        if horas > 8:
            total *= 1.10
        return round(total, 2)

    def describir_servicio(self) -> str:
        """Descripción orientada al cliente."""
        return (
            f"Sala código {self.codigo_interno}, capacidad {self._capacidad_personas} personas, "
            f"tarifa {self.tarifa_base_hora} / hora."
        )

    def validar_parametros(self, horas: float, **kwargs) -> None:
        """Exige disponibilidad y rango de horas."""
        if not self.disponible:
            raise ServicioNoDisponibleError("Sala fuera de servicio.", self.nombre_publico())
        if horas <= 0 or horas > 24:
            raise ValidacionError("Duración de sala entre 0 y 24 horas.", "horas")

    def nombre_publico(self) -> str:
        """Nombre amigable."""
        return "Reserva de sala"
