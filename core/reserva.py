from datetime import datetime
from core.base import EntidadBase
from core.cliente import Cliente

class Reserva(EntidadBase):
    """
    Representa una reserva hecha por un cliente.
    Hereda de EntidadBase e implementa validaciones básicas.
    """

    FORMATO_FECHA = "%Y-%m-%d"

    def __init__(self, cliente, fecha, tipo_servicio):
        # Validaciones
        if not isinstance(cliente, Cliente):
            raise ValueError("El parámetro 'cliente' debe ser un objeto Cliente")
        if not fecha or not fecha.strip():
            raise ValueError("La fecha no puede estar vacía")
        if not tipo_servicio or not tipo_servicio.strip():
            raise ValueError("El tipo de servicio no puede estar vacío")

        # Validar formato de fecha
        try:
            datetime.strptime(fecha.strip(), self.FORMATO_FECHA)
        except ValueError:
            raise ValueError(f"La fecha debe tener el formato {self.FORMATO_FECHA} (ej: 2025-12-31)")

        self.__cliente = cliente
        self.__fecha = fecha.strip()
        self.__tipo_servicio = tipo_servicio.strip()

    # --- Getters ---
    def get_cliente(self):
        return self.__cliente

    def get_fecha(self):
        return self.__fecha

    def get_tipo_servicio(self):
        return self.__tipo_servicio

    # --- Setters ---
    def set_fecha(self, nueva_fecha):
        if not nueva_fecha or not nueva_fecha.strip():
            raise ValueError("La fecha no puede estar vacía")
        try:
            datetime.strptime(nueva_fecha.strip(), self.FORMATO_FECHA)
        except ValueError:
            raise ValueError(f"La fecha debe tener el formato {self.FORMATO_FECHA} (ej: 2025-12-31)")
        self.__fecha = nueva_fecha.strip()

    def set_tipo_servicio(self, nuevo_tipo):
        if not nuevo_tipo or not nuevo_tipo.strip():
            raise ValueError("El tipo de servicio no puede estar vacío")
        self.__tipo_servicio = nuevo_tipo.strip()

    # --- Representación ---
    def __str__(self):
        return (f"Reserva de {self.__cliente.get_nombre()} "
                f"para el {self.__fecha} - Servicio: {self.__tipo_servicio}")
