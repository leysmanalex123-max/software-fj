"""Configuración centralizada del registro de eventos y errores."""

import logging
from pathlib import Path

RUTA_LOGS = Path(__file__).resolve().parent / "logs"
RUTA_LOGS.mkdir(exist_ok=True)
ARCHIVO_LOG = RUTA_LOGS / "software_fj.log"

logger = logging.getLogger("SoftwareFJ")
logger.setLevel(logging.INFO)

if not logger.handlers:
    formato = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    archivo = logging.FileHandler(ARCHIVO_LOG, encoding="utf-8")
    archivo.setFormatter(formato)
    logger.addHandler(archivo)

    consola = logging.StreamHandler()
    consola.setFormatter(formato)
    logger.addHandler(consola)
