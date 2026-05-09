# -*- coding: utf-8 -*-
"""
Clase Reserva: integra cliente, servicio, duración y estado con excepciones.
"""

from __future__ import annotations

from enum import Enum, auto
from typing import TYPE_CHECKING

from .base import EntidadBase
from utils.excepciones import OperacionNoPermitidaError, ReservaError
from utils.logger import registrar_evento, registrar_excepcion

if TYPE_CHECKING:
    from .cliente import Cliente
    from servicios.base_servicio import Servicio


class EstadoReserva(Enum):
    """Estados posibles del ciclo de vida de una reserva."""

    PENDIENTE = auto()
    CONFIRMADA = auto()
    CANCELADA = auto()
    COMPLETADA = auto()


class Reserva(EntidadBase):
    """Reserva que vincula un cliente con un servicio y una duración."""

    def __init__(
        self,
        identificador: str,
        cliente: Cliente,
        servicio: Servicio,
        duracion_horas: float,
    ) -> None:
        # Delega validación de horas al procesamiento para reutilizar lógica.
        if duracion_horas <= 0:
            raise ReservaError("La duración debe ser mayor que cero.", identificador)
        super().__init__(identificador)
        self._cliente = cliente
        self._servicio = servicio
        self._duracion_horas = float(duracion_horas)
        self._estado = EstadoReserva.PENDIENTE

    @property
    def cliente(self) -> Cliente:
        """Cliente asociado (solo lectura)."""
        return self._cliente

    @property
    def servicio(self) -> Servicio:
        """Servicio contratado (solo lectura)."""
        return self._servicio

    @property
    def duracion_horas(self) -> float:
        """Duración en horas."""
        return self._duracion_horas

    @property
    def estado(self) -> EstadoReserva:
        """Estado actual de la reserva."""
        return self._estado

    def resumen(self) -> str:
        """Línea descriptiva para la GUI."""
        return (
            f"Reserva {self.identificador} | {self._cliente.resumen()} | "
            f"{self._servicio.nombre_publico()} | {self._estado.name}"
        )

    def confirmar(self) -> float:
        """
        Confirma la reserva y devuelve el costo calculado.

        Raises:
            OperacionNoPermitidaError: si el estado no permite confirmar.
            ReservaError: si el servicio rechaza la operación.
        """
        if self._estado is not EstadoReserva.PENDIENTE:
            raise OperacionNoPermitidaError(
                "Solo se pueden confirmar reservas pendientes.",
                operacion="confirmar",
            )
        try:
            # Valida parámetros del servicio antes de cobrar.
            self._servicio.validar_parametros(self._duracion_horas)
            # Calcula costo base con polimorfismo.
            costo = self._servicio.calcular_costo(self._duracion_horas)
        except Exception as exc:
            # Encadenamiento: conserva causa original.
            raise ReservaError("No se pudo confirmar la reserva por fallo del servicio.", self.identificador) from exc
        self._estado = EstadoReserva.CONFIRMADA
        registrar_evento(f"Reserva confirmada {self.identificador}, costo={costo}", "INFO")
        return costo

    def cancelar(self, motivo: str = "") -> None:
        """Cancela si el estado lo permite."""
        if self._estado in (EstadoReserva.CANCELADA, EstadoReserva.COMPLETADA):
            raise OperacionNoPermitidaError("La reserva ya está cerrada.", operacion="cancelar")
        self._estado = EstadoReserva.CANCELADA
        registrar_evento(f"Reserva cancelada {self.identificador}. Motivo: {motivo}", "INFO")

    def completar(self) -> None:
        """Marca como completada tras prestación del servicio."""
        if self._estado is not EstadoReserva.CONFIRMADA:
            raise OperacionNoPermitidaError("Solo reservas confirmadas pueden completarse.", operacion="completar")
        self._estado = EstadoReserva.COMPLETADA
        registrar_evento(f"Reserva completada {self.identificador}", "INFO")

    def procesar(self) -> dict[str, float | str]:
        """
        Procesa la reserva con bloques try/except/else/finally.

        Returns:
            Diccionario con costo y mensaje de resultado.
        """
        resultado: dict[str, float | str] = {}
        try:
            costo = self.confirmar()
        except OperacionNoPermitidaError as err:
            registrar_excepcion("procesar: operación no permitida", err)
            resultado["ok"] = 0.0
            resultado["mensaje"] = str(err)
        except ReservaError as err:
            registrar_excepcion("procesar: error de reserva", err)
            resultado["ok"] = 0.0
            resultado["mensaje"] = str(err)
        else:
            # Sin excepción al confirmar.
            resultado["ok"] = 1.0
            resultado["mensaje"] = "Confirmada"
            resultado["costo"] = costo
        finally:
            # Siempre deja constancia en log del intento de procesamiento.
            registrar_evento(f"procesar() ejecutado para reserva {self.identificador}", "INFO")
        return resultado
