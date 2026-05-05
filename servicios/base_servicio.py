# -*- coding: utf-8 -*-
"""
Clase abstracta Servicio: contrato para costos, descripción y validación.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import overload

from utils.excepciones import CalculoInconsistenteError, ValidacionError


class Servicio(ABC):
    """Servicio ofrecido por Software FJ con polimorfismo en cálculo de costos."""

    def __init__(self, codigo_interno: str, tarifa_base_hora: float, disponible: bool = True) -> None:
        # Código corto para inventarios en memoria.
        self._codigo_interno = codigo_interno
        # Precio por hora antes de impuestos o descuentos.
        if tarifa_base_hora < 0:
            raise ValidacionError("La tarifa base no puede ser negativa.", "tarifa_base_hora")
        self._tarifa_base_hora = float(tarifa_base_hora)
        # Bandera de disponibilidad comercial.
        self._disponible = bool(disponible)

    @property
    def codigo_interno(self) -> str:
        """Código del servicio."""
        return self._codigo_interno

    @property
    def tarifa_base_hora(self) -> float:
        """Tarifa por hora."""
        return self._tarifa_base_hora

    @property
    def disponible(self) -> bool:
        """Indica si el servicio se puede contratar."""
        return self._disponible

    def marcar_indisponible(self) -> None:
        """Desactiva temporalmente el servicio."""
        self._disponible = False

    def marcar_disponible(self) -> None:
        """Reactiva el servicio."""
        self._disponible = True

    @abstractmethod
    def calcular_costo(self, horas: float, *args, **kwargs) -> float:
        """Calcula el costo total según reglas de la subclase."""
        raise NotImplementedError

    @overload
    def calcular_costo_avanzado(self, horas: float) -> float: ...

    @overload
    def calcular_costo_avanzado(self, horas: float, impuesto_porcentaje: float) -> float: ...

    @overload
    def calcular_costo_avanzado(
        self, horas: float, impuesto_porcentaje: float, descuento_porcentaje: float
    ) -> float: ...

    def calcular_costo_avanzado(
        self,
        horas: float,
        impuesto_porcentaje: float | None = None,
        descuento_porcentaje: float | None = None,
    ) -> float:
        """
        Sobrecarga simulada: costo con impuesto opcional y descuento opcional.

        Orden de aplicación: subtotal -> descuento -> impuesto sobre el neto.
        """
        # Costo específico de la subclase sin recargos.
        subtotal = self.calcular_costo(horas)
        if subtotal < 0:
            raise CalculoInconsistenteError("Subtotal negativo no permitido.", detalle=str(subtotal))
        neto = subtotal
        if descuento_porcentaje is not None:
            if not 0 <= descuento_porcentaje <= 90:
                raise ValidacionError("Descuento debe estar entre 0 y 90%.", "descuento_porcentaje")
            neto = subtotal * (1 - descuento_porcentaje / 100.0)
        if impuesto_porcentaje is not None:
            if impuesto_porcentaje < 0:
                raise ValidacionError("Impuesto no puede ser negativo.", "impuesto_porcentaje")
            neto = neto * (1 + impuesto_porcentaje / 100.0)
        return round(neto, 2)

    @abstractmethod
    def describir_servicio(self) -> str:
        """Texto comercial del servicio."""
        raise NotImplementedError

    @abstractmethod
    def validar_parametros(self, horas: float, **kwargs) -> None:
        """Valida horas y parámetros específicos antes de reservar."""
        raise NotImplementedError

    def nombre_publico(self) -> str:
        """Nombre para mostrar; puede sobrescribirse."""
        return self.__class__.__name__
