# -*- coding: utf-8 -*-
"""
Servicio especializado: asesorías técnicas o de negocio.
"""

from __future__ import annotations

from .base_servicio import Servicio
from utils.excepciones import ServicioNoDisponibleError, ValidacionError


class Asesoria(Servicio):
    """Sesión de asesoría con nivel de seniority que multiplica la tarifa."""

    def __init__(
        self,
        codigo_interno: str,
        tarifa_base_hora: float,
        nivel: str,
        disponible: bool = True,
    ) -> None:
        niveles = ("junior", "semi", "senior")
        nivel_norm = nivel.strip().lower()
        if nivel_norm not in niveles:
            raise ValidacionError(f"Nivel debe ser uno de: {niveles}.", "nivel")
        super().__init__(codigo_interno, tarifa_base_hora, disponible)
        self._nivel = nivel_norm

    @property
    def nivel(self) -> str:
        """Nivel de consultor asignado."""
        return self._nivel

    def _multiplicador(self) -> float:
        """Factor de precio según seniority."""
        return {"junior": 1.0, "semi": 1.25, "senior": 1.6}[self._nivel]

    def calcular_costo(self, horas: float, **kwargs) -> float:
        """Precio proporcional a horas y multiplicador de nivel."""
        if not self.disponible:
            raise ServicioNoDisponibleError("No hay consultores disponibles.", self.nombre_publico())
        if horas <= 0:
            raise ValidacionError("Las horas deben ser positivas.", "horas")
        return round(self.tarifa_base_hora * horas * self._multiplicador(), 2)

    def describir_servicio(self) -> str:
        return (
            f"Asesoría {self._nivel} ({self.codigo_interno}), "
            f"tarifa base {self.tarifa_base_hora}/h x factor {self._multiplicador()}."
        )

    def validar_parametros(self, horas: float, **kwargs) -> None:
        if not self.disponible:
            raise ServicioNoDisponibleError("Asesoría no disponible.", self.nombre_publico())
        if horas <= 0 or horas > 12:
            raise ValidacionError("Las asesorías admiten máximo 12 horas por reserva.", "horas")

    def nombre_publico(self) -> str:
        return "Asesoría especializada"
