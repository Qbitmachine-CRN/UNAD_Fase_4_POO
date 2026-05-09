# -*- coding: utf-8 -*-
"""
Clase abstracta base para entidades del dominio Software FJ.
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class EntidadBase(ABC):
    """Representa una entidad genérica con identificador y metadatos mínimos."""

    def __init__(self, identificador: str) -> None:
        # Identificador único legible (no es persistencia en BD).
        self._identificador = identificador

    @property
    def identificador(self) -> str:
        """Expone de solo lectura el identificador interno."""
        return self._identificador

    @abstractmethod
    def resumen(self) -> str:
        """Devuelve una descripción breve de la entidad para listados."""
        raise NotImplementedError

    def __repr__(self) -> str:
        """Representación técnica útil para depuración."""
        return f"{self.__class__.__name__}(id={self._identificador!r})"
