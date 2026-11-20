"""Administración de clientes y validación de sus datos."""

import re
from entidades import Entidad
from excepciones import ValidacionError


class Cliente(Entidad):
    def __init__(self, identificador, nombre, correo, telefono):
        super().__init__(identificador)
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        if not isinstance(valor, str) or len(valor.strip()) < 3:
            raise ValidacionError("El nombre debe tener al menos 3 caracteres.")
        self._nombre = valor.strip().title()

    @property
    def correo(self):
        return self._correo

    @correo.setter
    def correo(self, valor):
        if not isinstance(valor, str) or not re.fullmatch(
            r"[^@\s]+@[^@\s]+\.[^@\s]+", valor.strip()
        ):
            raise ValidacionError("El correo electrónico no tiene un formato válido.")
        self._correo = valor.strip().lower()

    @property
    def telefono(self):
        return self._telefono

    @telefono.setter
    def telefono(self, valor):
        limpio = re.sub(r"\s+", "", str(valor))
        if not re.fullmatch(r"\+?\d{7,15}", limpio):
            raise ValidacionError("El teléfono debe contener entre 7 y 15 dígitos.")
        self._telefono = limpio

    def describir(self):
        return (
            f"Cliente {self.identificador}: {self.nombre} | "
            f"{self.correo} | {self.telefono}"
        )
