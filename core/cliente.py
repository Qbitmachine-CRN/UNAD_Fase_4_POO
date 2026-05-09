# -*- coding: utf-8 -*-
"""
Clase Cliente con validaciones y encapsulación de datos personales.
"""

from __future__ import annotations

import re

from .base import EntidadBase
from utils.excepciones import ValidacionError
from utils.logger import registrar_evento


# Patrón simple de correo electrónico para validación básica.
_PATRON_EMAIL = re.compile(r"^[\w.+-]+@[\w-]+\.[\w.-]+$")


class Cliente(EntidadBase):
    """Cliente de Software FJ con datos personales protegidos por propiedades."""

    def __init__(
        self,
        identificador: str,
        nombre_completo: str,
        email: str,
        telefono: str,
    ) -> None:
        # Valida antes de asignar para mantener invariantes.
        self._validar_nombre(nombre_completo)
        self._validar_email(email)
        self._validar_telefono(telefono)
        # Inicializa la porción abstracta con el id del cliente.
        super().__init__(identificador)
        # Atributos privados encapsulados.
        self._nombre_completo = nombre_completo.strip()
        self._email = email.strip().lower()
        self._telefono = telefono.strip()

    @staticmethod
    def _validar_nombre(valor: str) -> None:
        """Comprueba longitud y caracteres mínimos del nombre."""
        if not valor or not valor.strip():
            raise ValidacionError("El nombre no puede estar vacío.", "nombre_completo")
        if len(valor.strip()) < 3:
            raise ValidacionError("El nombre debe tener al menos 3 caracteres.", "nombre_completo")

    @staticmethod
    def _validar_email(valor: str) -> None:
        """Comprueba formato de correo con expresión regular."""
        if not valor or not valor.strip():
            raise ValidacionError("El email es obligatorio.", "email")
        if not _PATRON_EMAIL.match(valor.strip()):
            raise ValidacionError("El formato del email no es válido.", "email")

    @staticmethod
    def _validar_telefono(valor: str) -> None:
        """Exige solo dígitos y longitud razonable."""
        limpio = "".join(ch for ch in valor if ch.isdigit())
        if len(limpio) < 7 or len(limpio) > 15:
            raise ValidacionError("El teléfono debe tener entre 7 y 15 dígitos.", "telefono")

    @property
    def nombre_completo(self) -> str:
        """Nombre del cliente visible de solo lectura."""
        return self._nombre_completo

    @nombre_completo.setter
    def nombre_completo(self, valor: str) -> None:
        """Permite actualizar el nombre con las mismas reglas de validación."""
        self._validar_nombre(valor)
        self._nombre_completo = valor.strip()

    @property
    def email(self) -> str:
        """Correo en minúsculas."""
        return self._email

    @email.setter
    def email(self, valor: str) -> None:
        """Actualiza email validado."""
        self._validar_email(valor)
        self._email = valor.strip().lower()

    @property
    def telefono(self) -> str:
        """Teléfono normalizado solo dígitos para uso interno."""
        return "".join(ch for ch in self._telefono if ch.isdigit())

    @telefono.setter
    def telefono(self, valor: str) -> None:
        """Actualiza teléfono con validación."""
        self._validar_telefono(valor)
        self._telefono = valor.strip()

    def resumen(self) -> str:
        """Texto corto para listas en la interfaz."""
        return f"{self._nombre_completo} <{self._email}>"

    @classmethod
    def crear_seguro(cls, identificador: str, nombre: str, email: str, telefono: str) -> Cliente | None:
        """
        Fábrica que no lanza: devuelve None y registra en log si falla la validación.

        Demuestra manejo controlado sin detener la aplicación.
        """
        try:
            # Intento de construcción normal.
            cliente = cls(identificador, nombre, email, telefono)
        except ValidacionError as err:
            # Registra el motivo del rechazo.
            registrar_evento(f"Cliente no creado ({identificador}): {err}", "WARNING")
            # Indica fallo al llamador sin propagar excepción.
            return None
        else:
            # Rama else de try/except: éxito sin excepción.
            registrar_evento(f"Cliente creado correctamente: {identificador}", "INFO")
            return cliente
        finally:
            # Siempre ejecutado: traza fin del intento de creación.
            registrar_evento(f"Finalizado intento de creación de cliente {identificador}", "INFO")
