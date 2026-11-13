# reserva.py

import logging
from entidades import EntidadBase, Cliente
from servicios import Servicio, AlquilerEquipos, AsesoriaEspecializada
from excepciones import (
    ReservaError, 
    ReservaDuplicadaError, 
    ServicioNoDisponibleError, 
    ServicioError
)

class Reserva(EntidadBase):
    """Clase Reserva que integra cliente, servicio, duración y estado."""
    
    contador_id = 1

    def __init__(self, cliente: Cliente, servicio: Servicio, horas: int, **kwargs):
        id_reserva = f"RES-{Reserva.contador_id:03d}"
        Reserva.contador_id += 1
        super().__init__(id_reserva)
        
        self.cliente = cliente
        self.servicio = servicio
        self.horas = horas
        self.estado = "Creada"  # Estados: Creada, Confirmada, Cancelada
        self.costo_total = 0.0
        
        try:
            if not self.servicio.disponible:
                raise ServicioNoDisponibleError(f"El servicio {self.servicio.identificador} no se encuentra disponible actualmente.")
            
            if isinstance(self.servicio, AlquilerEquipos):
                desc = kwargs.get('descuento', 0.0)
                self.costo_total = self.servicio.calcular_costo(self.horas, descuento=desc)
            elif isinstance(self.servicio, AsesoriaEspecializada):
                comp = kwargs.get('complejidad', 1)
                self.costo_total = self.servicio.calcular_costo(self.horas, nivel_complejidad=comp)
            else:
                self.costo_total = self.servicio.calcular_costo(self.horas)
                
        except ServicioError as e:
            raise ReservaError(f"Fallo al inicializar la reserva {self.identificador}") from e

    def confirmar(self):
        try:
            if self.estado == "Confirmada":
                raise ReservaDuplicadaError(f"La reserva {self.identificador} ya se encuentra confirmada.")
            if self.estado == "Cancelada":
                raise ReservaError("No se puede confirmar una reserva que ha sido cancelada.")
            self.estado = "Confirmada"
            logging.info(f"Reserva {self.identificador} confirmada exitosamente.")
        except Exception as e:
            logging.error(f"Error al confirmar reserva {self.identificador}: {e}")
            raise

    def cancelar(self):
        try:
            if self.estado == "Cancelada":
                raise ReservaError(f"La reserva {self.identificador} ya estaba cancelada.")
            self.estado = "Cancelada"
            logging.info(f"Reserva {self.identificador} cancelada correctamente.")
        except Exception as e:
            logging.error(f"Error al cancelar reserva {self.identificador}: {e}")
            raise

    def obtener_detalle(self) -> str:
        return (f"Reserva [{self.identificador}] | Cliente: {self.cliente.nombre} | "
                f"Servicio: {self.servicio.nombre_servicio} | Horas: {self.horas} | "
                f"Costo Total: ${self.costo_total:.2f} | Estado: {self.estado}")