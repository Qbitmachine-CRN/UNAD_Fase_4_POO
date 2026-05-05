# -*- coding: utf-8 -*-
"""
Módulo de excepciones personalizadas para Software FJ.

Define jerarquía de errores del dominio y mensajes coherentes para
registro en logs y presentación controlada al usuario.
"""


class SoftwareFJError(Exception):
    """Excepción base de la aplicación Software FJ."""

    def __init__(self, mensaje: str, codigo: str = "GEN-000") -> None:
        # Guarda el mensaje legible para el usuario o el log.
        self.mensaje = mensaje
        # Código interno para clasificar el tipo de fallo.
        self.codigo = codigo
        # Invoca el constructor de Exception con el mismo mensaje.
        super().__init__(mensaje)


class ValidacionError(SoftwareFJError):
    """Se lanza cuando los datos no cumplen reglas de validación."""

    def __init__(self, mensaje: str, campo: str | None = None) -> None:
        # Identifica opcionalmente el campo que falló la validación.
        self.campo = campo
        # Prefijo de código para errores de validación.
        codigo = "VAL-001"
        # Propaga el mensaje y el código a la clase base.
        super().__init__(mensaje, codigo)


class DatosFaltantesError(SoftwareFJError):
    """Se lanza cuando faltan parámetros obligatorios en una operación."""

    def __init__(self, mensaje: str, parametros: tuple[str, ...] = ()) -> None:
        # Lista de nombres de parámetros ausentes para diagnóstico.
        self.parametros = parametros
        # Código para datos incompletos.
        super().__init__(mensaje, "DAT-002")


class ServicioNoDisponibleError(SoftwareFJError):
    """Indica que el servicio solicitado no puede ofrecerse en ese momento."""

    def __init__(self, mensaje: str, nombre_servicio: str = "") -> None:
        # Nombre del servicio no disponible.
        self.nombre_servicio = nombre_servicio
        # Código de indisponibilidad.
        super().__init__(mensaje, "SRV-003")


class ReservaError(SoftwareFJError):
    """Errores específicos del ciclo de vida de una reserva."""

    def __init__(self, mensaje: str, id_reserva: str | None = None) -> None:
        # Identificador de la reserva afectada si existe.
        self.id_reserva = id_reserva
        # Código de error de reservas.
        super().__init__(mensaje, "RSV-004")


class CalculoInconsistenteError(SoftwareFJError):
    """Cálculos de costo o totales que no son coherentes."""

    def __init__(self, mensaje: str, detalle: str = "") -> None:
        # Texto adicional con valores intermedios si aplica.
        self.detalle = detalle
        # Código de inconsistencia numérica.
        super().__init__(mensaje, "CAL-005")


class OperacionNoPermitidaError(SoftwareFJError):
    """Operación solicitada no permitida en el estado actual."""

    def __init__(self, mensaje: str, operacion: str = "") -> None:
        # Nombre de la operación rechazada.
        self.operacion = operacion
        # Código de operación prohibida.
        super().__init__(mensaje, "OPN-006")
