# Software FJ – Sistema Integral de Gestión

## Descripción
Aplicación de consola desarrollada en Python mediante programación orientada a objetos.
Permite registrar clientes, administrar servicios y crear, confirmar, cancelar y procesar
reservas. No utiliza bases de datos: la información se mantiene en listas y objetos durante
la ejecución. Los eventos y errores se registran en `logs/software_fj.log`.

## Requisitos
- Python 3.10 o superior.
- No requiere instalar librerías externas.

## Ejecución
Desde la carpeta del proyecto, abrir una terminal y ejecutar:

```bash
python main.py
```

En Windows también puede funcionar:

```bash
py main.py
```

## Estructura
- `entidades.py`: clase abstracta Entidad.
- `clientes.py`: clase Cliente y validaciones.
- `servicios.py`: clase abstracta Servicio y tres servicios derivados.
- `reservas.py`: administración del ciclo de vida de las reservas.
- `excepciones.py`: excepciones personalizadas.
- `logger_config.py`: configuración del registro de eventos y errores.
- `main.py`: menú de demostración y 13 operaciones de prueba.
- `logs/`: archivo generado automáticamente al ejecutar el sistema.

## Principios de POO aplicados
- Abstracción: Entidad y Servicio son clases abstractas.
- Herencia: Cliente y los servicios especializados heredan de sus clases base.
- Encapsulamiento: atributos protegidos/privados y propiedades con validación.
- Polimorfismo: cada servicio implementa sus propias descripciones y cálculos.
- Sobrecarga flexible: `calcular_costo` admite impuesto y descuento opcionales,
  además de la duración obligatoria, usando argumentos predeterminados de Python.

## Manejo de excepciones
Se implementan excepciones personalizadas, bloques `try/except/else/finally`,
registro con `logging` y encadenamiento mediante `raise ... from error`.

## Almacenamiento
Los clientes, servicios y reservas se conservan en listas durante la ejecución.
No se usa ningún motor de base de datos. El archivo de log almacena únicamente
eventos y errores, no funciona como base de datos.
