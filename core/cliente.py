from core.base import EntidadBase

class Cliente(EntidadBase):
    """
    Representa un cliente del sistema.
    Hereda de EntidadBase e implementa validaciones básicas.
    """

    def __init__(self, nombre, documento):
        # Validaciones
        if not nombre or not nombre.strip():
            raise ValueError("El nombre no puede estar vacío")
        if not documento or not documento.strip():
            raise ValueError("El documento no puede estar vacío")

        self.__nombre = nombre.strip()
        self.__documento = documento.strip()

    # --- Getters ---
    def get_nombre(self):
        return self.__nombre

    def get_documento(self):
        return self.__documento

    # --- Setters ---
    def set_nombre(self, nuevo_nombre):
        if not nuevo_nombre or not nuevo_nombre.strip():
            raise ValueError("El nombre no puede estar vacío")
        self.__nombre = nuevo_nombre.strip()

    def set_documento(self, nuevo_documento):
        if not nuevo_documento or not nuevo_documento.strip():
            raise ValueError("El documento no puede estar vacío")
        self.__documento = nuevo_documento.strip()

    # --- Representación ---
    def __str__(self):
        return f"Cliente: {self.__nombre} - Documento: {self.__documento}"