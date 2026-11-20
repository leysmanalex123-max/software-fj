"""Creación, confirmación, cancelación y procesamiento de reservas."""

from entidades import Entidad
from excepciones import (
    ReservaError, EstadoReservaError, ParametroFaltanteError, ValidacionError
)
from logger_config import logger


class Reserva(Entidad):
    ESTADOS = ("PENDIENTE", "CONFIRMADA", "CANCELADA", "PROCESADA")

    def __init__(self, identificador, cliente, servicio, duracion, parametros=None):
        super().__init__(identificador)
        if cliente is None or servicio is None:
            raise ParametroFaltanteError("La reserva requiere un cliente y un servicio.")
        if isinstance(duracion, bool) or not isinstance(duracion, (int, float)) or duracion <= 0:
            raise ValidacionError("La duración de la reserva debe ser positiva.")
        self._cliente = cliente
        self._servicio = servicio
        self._duracion = float(duracion)
        self._parametros = parametros or {}
        self._estado = "PENDIENTE"
        self._costo = None
        self._servicio.validar_parametros(**self._parametros)
        logger.info("Reserva %s creada para el cliente %s.", identificador, cliente.nombre)

    @property
    def estado(self):
        return self._estado

    @property
    def costo(self):
        return self._costo

    def confirmar(self):
        if self._estado != "PENDIENTE":
            raise EstadoReservaError("Solo se puede confirmar una reserva pendiente.")
        self._servicio.verificar_disponibilidad()
        self._estado = "CONFIRMADA"
        logger.info("Reserva %s confirmada.", self.identificador)

    def cancelar(self):
        if self._estado in ("CANCELADA", "PROCESADA"):
            raise EstadoReservaError("No se puede cancelar una reserva cancelada o procesada.")
        self._estado = "CANCELADA"
        logger.info("Reserva %s cancelada.", self.identificador)

    def procesar(self, impuesto=0.19, descuento=0.0):
        if self._estado != "CONFIRMADA":
            raise EstadoReservaError("La reserva debe estar confirmada antes de procesarse.")
        try:
            self._costo = self._servicio.calcular_costo(
                self._duracion, impuesto, descuento
            )
            if self._costo <= 0:
                raise ValidacionError("El costo calculado debe ser mayor que cero.")
        except Exception as error:
            logger.exception("Error procesando la reserva %s.", self.identificador)
            raise ReservaError(
                f"No fue posible procesar la reserva {self.identificador}."
            ) from error
        else:
            self._estado = "PROCESADA"
            logger.info(
                "Reserva %s procesada. Total: $%.2f",
                self.identificador, self._costo
            )
            return self._costo
        finally:
            logger.info("Finalizó el intento de procesamiento de reserva %s.", self.identificador)

    def describir(self):
        return (
            f"Reserva {self.identificador} | Cliente: {self._cliente.nombre} | "
            f"Servicio: {self._servicio.nombre} | Duración: {self._duracion} | "
            f"Estado: {self._estado} | Costo: {self._costo}"
        )
