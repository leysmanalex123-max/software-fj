"""Excepciones personalizadas del sistema Software FJ.

Todas heredan de SoftwareFJError, de modo que el gestor pueda capturar
cualquier error propio del dominio con un solo ``except`` y, ademas,
distinguir cada caso cuando lo necesite.
"""


class SoftwareFJError(Exception):
    """Excepcion base de la aplicacion."""

    # Codigo que identifica el tipo de error en los logs (cada hija lo redefine).
    codigo_defecto = "SFJ-000"

    def __init__(self, mensaje, codigo=None):
        # Se pasa el mensaje a la clase padre para que Exception lo conserve.
        super().__init__(mensaje)
        # Se guarda el mensaje para poder leerlo despues sin formato.
        self.mensaje = mensaje
        # Si no se indica un codigo, se usa el de la clase.
        self.codigo = codigo or self.codigo_defecto

    def __str__(self):
        # Formato uniforme para consola y logs: [CODIGO] mensaje.
        return f"[{self.codigo}] {self.mensaje}"


class ClienteInvalidoError(SoftwareFJError):
    """Datos del cliente invalidos (nombre, documento, correo, telefono)."""

    codigo_defecto = "SFJ-100"


class ServicioInvalidoError(SoftwareFJError):
    """Datos del servicio invalidos (tarifa, tipo, atributos propios)."""

    codigo_defecto = "SFJ-200"


class ServicioNoDisponibleError(SoftwareFJError):
    """Se intenta usar un servicio deshabilitado."""

    codigo_defecto = "SFJ-210"


class ParametroFaltanteError(SoftwareFJError):
    """Falta un parametro obligatorio."""

    codigo_defecto = "SFJ-300"


class ParametroInvalidoError(SoftwareFJError):
    """Un parametro existe pero su valor o tipo no es aceptable."""

    codigo_defecto = "SFJ-310"


class ReservaInvalidaError(SoftwareFJError):
    """La reserva no se puede crear o confirmar con los datos dados."""

    codigo_defecto = "SFJ-400"


class OperacionNoPermitidaError(SoftwareFJError):
    """La operacion no es valida para el estado actual del objeto."""

    codigo_defecto = "SFJ-410"


class CalculoInconsistenteError(SoftwareFJError):
    """El calculo de costos produjo o recibio valores incoherentes."""

    codigo_defecto = "SFJ-500"


class EntidadNoEncontradaError(SoftwareFJError):
    """No existe una entidad con el identificador indicado."""

    codigo_defecto = "SFJ-600"


# ---------------------------------------------------------------------------
# PRUEBA DEL PASO 2: se ejecuta con  python -m sistema.excepciones
# (este bloque solo corre cuando se ejecuta el archivo directamente)
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # Caso 1: se lanza una excepcion propia y se captura con su clase especifica.
    try:
        raise ClienteInvalidoError("El correo no tiene formato valido.")
    except ClienteInvalidoError as error:
        print("Caso 1 capturado:", error)

    # Caso 2: todas las excepciones del sistema se pueden capturar con la clase base.
    try:
        raise ServicioNoDisponibleError("La sala esta deshabilitada.")
    except SoftwareFJError as error:
        print("Caso 2 capturado por la clase base:", error, "| codigo:", error.codigo)

    # Caso 3: encadenamiento (raise ... from): se conserva la causa original.
    try:
        try:
            int("abc")  # esto lanza un ValueError
        except ValueError as causa:
            raise ParametroInvalidoError("La duracion debe ser un numero.") from causa
    except SoftwareFJError as error:
        print("Caso 3 capturado:", error, "| causa original:", repr(error.__cause__))