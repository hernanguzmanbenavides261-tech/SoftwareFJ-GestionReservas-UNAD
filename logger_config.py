"""
Módulo encargado de configurar el sistema de logs en archivo plano.
Registra tanto eventos exitosos como excepciones capturadas con su traza.
"""
import logging

def configurar_logger(nombre_archivo: str = "sistema_fj.log") -> logging.Logger:
    logger = logging.getLogger("SoftwareFJ")
    logger.setLevel(logging.DEBUG)

    # Evitar duplicar handlers si se importa varias veces
    if not logger.handlers:
        formato = logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(module)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        # Handler para archivo (persistencia de logs)
        file_handler = logging.FileHandler(nombre_archivo, encoding="utf-8")
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formato)

        # Handler para consola (visualización en tiempo real)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formato)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger