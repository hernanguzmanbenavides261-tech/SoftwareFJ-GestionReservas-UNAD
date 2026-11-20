"""
Módulo de excepciones personalizadas para el sistema de Software FJ.
Permite capturar y encadenar errores específicos de negocio y validación.
"""

class SoftwareFJError(Exception):
    """Excepción base para todos los errores controlados del sistema."""
    pass


class DatoInvalidoError(SoftwareFJError):
    """Se lanza cuando un parámetro tiene formato, tipo o valor incorrecto."""
    pass


class ParametroFaltanteError(SoftwareFJError):
    """Se lanza cuando falta un dato obligatorio para crear una entidad."""
    pass


class ServicioNoDisponibleError(SoftwareFJError):
    """Se lanza cuando el servicio solicitado está inactivo o sin cupo."""
    pass


class OperacionNoPermitidaError(SoftwareFJError):
    """Se lanza al intentar cambiar estados inválidos (ej. cancelar algo ya cancelado)."""
    pass


class CalculoInconsistenteError(SoftwareFJError):
    """Se lanza cuando los costos, impuestos o descuentos arrojan valores ilógicos."""
    pass