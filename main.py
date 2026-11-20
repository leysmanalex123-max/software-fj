"""Punto de entrada. Ejecuta una demostración de más de diez operaciones."""

from clientes import Cliente
from servicios import ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from reservas import Reserva
from excepciones import SoftwareFJError
from logger_config import logger


class SistemaSoftwareFJ:
    def __init__(self):
        self.clientes = []
        self.servicios = []
        self.reservas = []

    def registrar_cliente(self, cliente):
        if any(c.identificador == cliente.identificador for c in self.clientes):
            raise ValueError("Ya existe un cliente con ese identificador.")
        self.clientes.append(cliente)
        logger.info("Cliente registrado: %s", cliente.nombre)
        return cliente

    def registrar_servicio(self, servicio):
        if any(s.identificador == servicio.identificador for s in self.servicios):
            raise ValueError("Ya existe un servicio con ese identificador.")
        self.servicios.append(servicio)
        logger.info("Servicio registrado: %s", servicio.nombre)
        return servicio

    def crear_reserva(self, reserva):
        if any(r.identificador == reserva.identificador for r in self.reservas):
            raise ValueError("Ya existe una reserva con ese identificador.")
        self.reservas.append(reserva)
        logger.info("Reserva agregada al sistema: %s", reserva.identificador)
        return reserva

    def mostrar_resumen(self):
        print("\n========== RESUMEN SOFTWARE FJ ==========")
        print(f"Clientes registrados: {len(self.clientes)}")
        print(f"Servicios registrados: {len(self.servicios)}")
        print(f"Reservas creadas: {len(self.reservas)}")
        for reserva in self.reservas:
            print(reserva.describir())
        print("=========================================\n")


def ejecutar_operacion(numero, descripcion, funcion):
    """Aísla cada prueba para que un error no detenga las siguientes."""
    print(f"\nOPERACIÓN {numero}: {descripcion}")
    try:
        resultado = funcion()
    except SoftwareFJError as error:
        logger.exception("Error controlado en operación %s: %s", numero, error)
        print(f"Error controlado: {error}")
    except (ValueError, TypeError) as error:
        logger.exception("Dato u operación inválida en operación %s.", numero)
        print(f"Operación no completada: {error}")
    except Exception as error:
        logger.exception("Error inesperado en operación %s.", numero)
        print(f"Error inesperado controlado: {error}")
    else:
        print("Resultado:", resultado if resultado is not None else "Operación exitosa.")
    finally:
        print("La aplicación continúa ejecutándose.")


def main():
    sistema = SistemaSoftwareFJ()
    print("SISTEMA INTEGRAL DE GESTIÓN - SOFTWARE FJ")
    logger.info("Inicio de la aplicación Software FJ.")

    # 1. Registro correcto de cliente.
    cliente1 = None
    def op1():
        nonlocal cliente1
        cliente1 = sistema.registrar_cliente(
            Cliente("C001", "Leysman Riaño", "leysman@email.com", "3001234567")
        )
        return cliente1.describir()
    ejecutar_operacion(1, "Registrar cliente válido", op1)

    # 2. Intento de registro con correo inválido.
    ejecutar_operacion(
        2, "Registrar cliente con correo inválido",
        lambda: Cliente("C002", "Ana Pérez", "correo-invalido", "3111234567")
    )

    # 3. Segundo cliente válido.
    cliente2 = None
    def op3():
        nonlocal cliente2
        cliente2 = sistema.registrar_cliente(
            Cliente("C003", "Carlos Gómez", "carlos@email.com", "3201234567")
        )
        return cliente2.describir()
    ejecutar_operacion(3, "Registrar otro cliente válido", op3)

    # 4, 5 y 6. Crear los tres tipos de servicio.
    sala = ReservaSala("S001", "Sala de reuniones", 50000)
    equipo = AlquilerEquipo("S002", "Computador portátil", 35000)
    asesoria = AsesoriaEspecializada("S003", "Asesoría en programación", 80000)

    ejecutar_operacion(4, "Registrar servicio de reserva de sala",
                       lambda: sistema.registrar_servicio(sala))
    ejecutar_operacion(5, "Registrar servicio de alquiler de equipos",
                       lambda: sistema.registrar_servicio(equipo))
    ejecutar_operacion(6, "Registrar servicio de asesoría",
                       lambda: sistema.registrar_servicio(asesoria))

    # 7. Crear, confirmar y procesar reserva exitosa.
    reserva1 = None
    def op7():
        nonlocal reserva1
        reserva1 = sistema.crear_reserva(
            Reserva("R001", cliente1, sala, 2, {"capacidad": 10})
        )
        reserva1.confirmar()
        return f"Total: ${reserva1.procesar(descuento=0.10):,.2f}"
    ejecutar_operacion(7, "Crear y procesar una reserva válida", op7)

    # 8. Intentar procesar una reserva que no está confirmada.
    def op8():
        reserva = sistema.crear_reserva(
            Reserva("R002", cliente2, equipo, 1, {"cantidad": 1})
        )
        return reserva.procesar()
    ejecutar_operacion(8, "Procesar una reserva sin confirmarla", op8)

    # 9. Intentar crear una reserva con duración inválida.
    ejecutar_operacion(
        9, "Crear reserva con duración negativa",
        lambda: Reserva("R003", cliente1, asesoria, -2)
    )

    # 10. Servicio no disponible.
    servicio_no_disponible = ReservaSala("S004", "Sala ocupada", 60000, False)
    def op10():
        sistema.registrar_servicio(servicio_no_disponible)
        reserva = sistema.crear_reserva(
            Reserva("R004", cliente1, servicio_no_disponible, 1)
        )
        reserva.confirmar()
    ejecutar_operacion(10, "Intentar reservar un servicio no disponible", op10)

    # 11. Cancelar una reserva pendiente.
    def op11():
        reserva = sistema.crear_reserva(
            Reserva("R005", cliente2, asesoria, 1, {"tema": "Python"})
        )
        reserva.cancelar()
        return reserva.estado
    ejecutar_operacion(11, "Cancelar una reserva pendiente", op11)

    # 12. Validar cálculo con parámetros incorrectos.
    ejecutar_operacion(
        12, "Calcular costo con impuesto inválido",
        lambda: sala.calcular_costo(2, impuesto=1.5)
    )

    # 13. Mostrar descripción polimórfica de servicios.
    ejecutar_operacion(
        13, "Consultar descripciones de los servicios",
        lambda: [servicio.describir() for servicio in sistema.servicios]
    )

    sistema.mostrar_resumen()
    logger.info("Finalización de la demostración Software FJ.")


if __name__ == "__main__":
    try:
        main()
    except Exception:
        logger.exception("Error crítico no previsto en el programa principal.")
        print("Se presentó un error crítico. Consulta el archivo de logs.")
    finally:
        print("Ejecución finalizada. Revisa logs/software_fj.log para ver los eventos.")
