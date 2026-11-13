# excepciones.py

class SoftwareFJError(Exception):
    """Excepción base para todos los errores del sistema Software FJ."""
    pass

class ClienteInvalidoError(SoftwareFJError):
    """Excepción lanzada cuando los datos de un cliente son inválidos."""
    pass

class ServicioError(SoftwareFJError):
    """Excepción base para errores relacionados con los servicios."""
    pass

class ServicioNoDisponibleError(ServicioError):
    """Lanzada cuando un servicio está inactivo o no disponible."""
    pass

class ReservaError(SoftwareFJError):
    """Excepción base para errores en el proceso de reservas."""
    pass

class ReservaDuplicadaError(ReservaError):
    """Lanzada cuando se intenta duplicar una reserva activa."""
    pass