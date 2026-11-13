# servicios.py

from abc import ABC, abstractmethod
from entidades import EntidadBase
from excepciones import ServicioError

class Servicio(EntidadBase, ABC):
    """Clase abstracta Servicio."""
    
    def __init__(self, codigo: str, nombre_servicio: str, costo_base: float, disponible: bool = True):
        super().__init__(codigo)
        self.nombre_servicio = nombre_servicio
        self.costo_base = costo_base
        self.disponible = disponible

    @property
    def costo_base(self) -> float:
        return self._costo_base

    @costo_base.setter
    def costo_base(self, valor: float):
        if valor < 0:
            raise ServicioError("El costo base no puede ser negativo.")
        self._costo_base = float(valor)

    @abstractmethod
    def calcular_costo(self, horas: int) -> float:
        """Método polimórfico para calcular costo."""
        pass

    @abstractmethod
    def obtener_detalle(self) -> str:
        pass


class ReservaSala(Servicio):
    """Servicio especializado: Reserva de Salas."""
    
    def __init__(self, codigo: str, costo_base: float, capacidad: int, disponible: bool = True):
        super().__init__(codigo, "Reserva de Sala", costo_base, disponible)
        self.capacidad = capacidad

    def calcular_costo(self, horas: int) -> float:
        if horas <= 0:
            raise ServicioError("Las horas de reserva deben ser mayores a cero.")
        return (self.costo_base * horas) * 1.05  # 5% cargo de gestión de sala

    def obtener_detalle(self) -> str:
        return f"Sala [Código: {self.identificador}, Capacidad: {self.capacidad} personas, Costo Base/h: {self.costo_base}]"


class AlquilerEquipos(Servicio):
    """Servicio especializado: Alquiler de Equipos."""
    
    def __init__(self, codigo: str, costo_base: float, marca: str, disponible: bool = True):
        super().__init__(codigo, "Alquiler de Equipos", costo_base, disponible)
        self.marca = marca

    def calcular_costo(self, horas: int, descuento: float = 0.0) -> float:
        """Método con sobrecarga lógica (parámetro opcional de descuento)."""
        if horas <= 0:
            raise ServicioError("Las horas de alquiler deben ser mayores a cero.")
        if not (0.0 <= descuento <= 1.0):
            raise ServicioError("El porcentaje de descuento debe estar entre 0.0 y 1.0.")
        subtotal = self.costo_base * horas
        return subtotal * (1.0 - descuento)

    def obtener_detalle(self) -> str:
        return f"Equipo [Código: {self.identificador}, Marca: {self.marca}, Costo Base/h: {self.costo_base}]"


class AsesoriaEspecializada(Servicio):
    """Servicio especializado: Asesorías Especializadas."""
    
    def __init__(self, codigo: str, costo_base: float, area_experticia: str, disponible: bool = True):
        super().__init__(codigo, "Asesoría Especializada", costo_base, disponible)
        self.area_experticia = area_experticia

    def calcular_costo(self, horas: int, nivel_complejidad: int = 1) -> float:
        """Método con sobrecarga lógica basada en complejidad."""
        if horas <= 0:
            raise ServicioError("Las horas de asesoría deben ser mayores a cero.")
        multiplicador = 1.0 + (nivel_complejidad * 0.1)
        return (self.costo_base * horas) * multiplicador

    def obtener_detalle(self) -> str:
        return f"Asesoría [Código: {self.identificador}, Área: {self.area_experticia}, Costo Base/h: {self.costo_base}]"