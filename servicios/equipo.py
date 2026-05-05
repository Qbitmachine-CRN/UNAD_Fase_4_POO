# -*- coding: utf-8 -*-
"""
Servicio especializado: alquiler de equipos tecnológicos.
"""

from __future__ import annotations

from .base_servicio import Servicio
from utils.excepciones import ServicioNoDisponibleError, ValidacionError


class AlquilerEquipo(Servicio):
    """Alquiler por horas con seguro fijo opcional modelado como constante."""

    def __init__(
        self,
        codigo_interno: str,
        tarifa_base_hora: float,
        tipo_equipo: str,
        costo_seguro_fijo: float = 0.0,
        disponible: bool = True,
    ) -> None:
        if not tipo_equipo or not tipo_equipo.strip():
            raise ValidacionError("Debe indicarse el tipo de equipo.", "tipo_equipo")
        super().__init__(codigo_interno, tarifa_base_hora, disponible)
        self._tipo_equipo = tipo_equipo.strip()
        if costo_seguro_fijo < 0:
            raise ValidacionError("El seguro no puede ser negativo.", "costo_seguro_fijo")
        self._costo_seguro_fijo = float(costo_seguro_fijo)

    @property
    def tipo_equipo(self) -> str:
        """Tipo de equipo alquilado."""
        return self._tipo_equipo

    def calcular_costo(self, horas: float, **kwargs) -> float:
        """Tarifa por hora más seguro fijo por contrato."""
        if not self.disponible:
            raise ServicioNoDisponibleError("El equipo no está disponible.", self.nombre_publico())
        if horas <= 0:
            raise ValidacionError("Las horas deben ser positivas.", "horas")
        return round(self.tarifa_base_hora * horas + self._costo_seguro_fijo, 2)

    def describir_servicio(self) -> str:
        return (
            f"Alquiler de {self._tipo_equipo} ({self.codigo_interno}), "
            f"tarifa {self.tarifa_base_hora}/h, seguro fijo {self._costo_seguro_fijo}."
        )

    def validar_parametros(self, horas: float, **kwargs) -> None:
        if not self.disponible:
            raise ServicioNoDisponibleError("Equipo en mantenimiento.", self.nombre_publico())
        if horas <= 0 or horas > 168:
            raise ValidacionError("El alquiler admite entre 0 y 168 horas (1 semana).", "horas")

    def nombre_publico(self) -> str:
        return "Alquiler de equipo"
