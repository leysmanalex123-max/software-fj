"""Servicios abstractos y especializados de Software FJ."""

from abc import abstractmethod
from excepciones import ValidacionError, ServicioNoDisponibleError
from entidades import Entidad


class Servicio(Entidad):
    def __init__(self, identificador, nombre, tarifa_base, disponible=True):
        super().__init__(identificador)
        if not isinstance(nombre, str) or not nombre.strip():
            raise ValidacionError("El nombre del servicio es obligatorio.")
        if isinstance(tarifa_base, bool) or not isinstance(tarifa_base, (int, float)) or tarifa_base <= 0:
            raise ValidacionError("La tarifa base debe ser un número positivo.")
        self._nombre = nombre.strip()
        self._tarifa_base = float(tarifa_base)
        self._disponible = bool(disponible)

    @property
    def nombre(self):
        return self._nombre

    @property
    def tarifa_base(self):
        return self._tarifa_base

    @property
    def disponible(self):
        return self._disponible

    def verificar_disponibilidad(self):
        if not self._disponible:
            raise ServicioNoDisponibleError(
                f"El servicio '{self.nombre}' no está disponible."
            )

    def cambiar_disponibilidad(self, estado):
        if not isinstance(estado, bool):
            raise ValidacionError("La disponibilidad debe ser True o False.")
        self._disponible = estado

    def calcular_costo(self, duracion, impuesto=0.19, descuento=0.0):
        """Variante general: costo con impuesto y descuento opcionales."""
        self.verificar_disponibilidad()
        if isinstance(duracion, bool) or not isinstance(duracion, (int, float)) or duracion <= 0:
            raise ValidacionError("La duración debe ser un número positivo.")
        if not 0 <= impuesto <= 1 or not 0 <= descuento <= 1:
            raise ValidacionError("Impuesto y descuento deben estar entre 0 y 1.")

        subtotal = self._calcular_subtotal(float(duracion))
        total = subtotal * (1 - descuento) * (1 + impuesto)
        if total < 0 or total != total:
            raise ValidacionError("El cálculo del costo produjo un resultado inconsistente.")
        return round(total, 2)

    @abstractmethod
    def _calcular_subtotal(self, duracion):
        raise NotImplementedError

    @abstractmethod
    def describir(self):
        raise NotImplementedError

    @abstractmethod
    def validar_parametros(self, **parametros):
        raise NotImplementedError


class ReservaSala(Servicio):
    def _calcular_subtotal(self, duracion):
        return self.tarifa_base * duracion

    def describir(self):
        return f"Reserva de sala: {self.nombre}. Tarifa por hora: ${self.tarifa_base:,.2f}"

    def validar_parametros(self, **parametros):
        capacidad = parametros.get("capacidad")
        if capacidad is not None and (
            isinstance(capacidad, bool) or not isinstance(capacidad, int) or capacidad <= 0
        ):
            raise ValidacionError("La capacidad de la sala debe ser un entero positivo.")
        return True


class AlquilerEquipo(Servicio):
    def _calcular_subtotal(self, duracion):
        return self.tarifa_base * duracion

    def describir(self):
        return f"Alquiler de equipo: {self.nombre}. Tarifa por día: ${self.tarifa_base:,.2f}"

    def validar_parametros(self, **parametros):
        cantidad = parametros.get("cantidad", 1)
        if isinstance(cantidad, bool) or not isinstance(cantidad, int) or cantidad <= 0:
            raise ValidacionError("La cantidad de equipos debe ser un entero positivo.")
        return True


class AsesoriaEspecializada(Servicio):
    def _calcular_subtotal(self, duracion):
        return self.tarifa_base * duracion

    def describir(self):
        return f"Asesoría especializada: {self.nombre}. Tarifa por hora: ${self.tarifa_base:,.2f}"

    def validar_parametros(self, **parametros):
        tema = parametros.get("tema")
        if tema is not None and (not isinstance(tema, str) or not tema.strip()):
            raise ValidacionError("El tema de la asesoría no puede estar vacío.")
        return True
