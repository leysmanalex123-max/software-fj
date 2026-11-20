"""Excepciones personalizadas del sistema Software FJ."""


class SoftwareFJError(Exception):
    """Excepción base de la aplicación."""
    codigo_defecto = "SFJ-000"

    def __init__(self, mensaje="Se produjo un error en Software FJ"):
        super().__init__(mensaje)


class ValidacionError(SoftwareFJError):
    codigo_defecto = "SFJ-001"


class ClienteNoEncontradoError(SoftwareFJError):
    codigo_defecto = "SFJ-002"


class ServicioNoDisponibleError(SoftwareFJError):
    codigo_defecto = "SFJ-003"


class ReservaError(SoftwareFJError):
    codigo_defecto = "SFJ-004"


class EstadoReservaError(ReservaError):
    codigo_defecto = "SFJ-005"


class ParametroFaltanteError(SoftwareFJError):
    codigo_defecto = "SFJ-006"
