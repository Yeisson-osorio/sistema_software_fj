# entidades.py

from abc import ABC, abstractmethod
from excepciones import ClienteInvalidoError

class EntidadBase(ABC):
    """Clase abstracta que representa entidades generales del sistema."""
    
    def __init__(self, identificador: str):
        self._identificador = identificador

    @property
    def identificador(self) -> str:
        return self._identificador

    @abstractmethod
    def obtener_detalle(self) -> str:
        pass


class Cliente(EntidadBase):
    """Clase Cliente con validaciones robustas y encapsulación."""
    
    def __init__(self, cedula: str, nombre: str, correo: str, telefono: str):
        super().__init__(cedula)
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono

    @property
    def cedula(self) -> str:
        return self._identificador

    @cedula.setter
    def cedula(self, valor: str):
        if not valor or not valor.strip():
            raise ClienteInvalidoError("La cédula no puede estar vacía.")
        if not valor.isdigit():
            raise ClienteInvalidoError(f"Cédula inválida ('{valor}'). Debe contener solo dígitos.")
        self._identificador = valor

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str):
        if not valor or len(valor.strip()) < 3:
            raise ClienteInvalidoError("El nombre del cliente debe tener al menos 3 caracteres.")
        self._nombre = valor.strip()

    @property
    def correo(self) -> str:
        return self._correo

    @correo.setter
    def correo(self, valor: str):
        if not valor or "@" not in valor or "." not in valor:
            raise ClienteInvalidoError(f"Correo electrónico inválido ('{valor}').")
        self._correo = valor.strip()

    @property
    def telefono(self) -> str:
        return self._telefono

    @telefono.setter
    def telefono(self, valor: str):
        if not valor or not valor.isdigit() or len(valor) < 7:
            raise ClienteInvalidoError(f"Teléfono inválido ('{valor}'). Debe tener al menos 7 dígitos numéricos.")
        self._telefono = valor

    def obtener_detalle(self) -> str:
        return f"Cliente [Cédula: {self.cedula}, Nombre: {self.nombre}, Correo: {self.correo}]"