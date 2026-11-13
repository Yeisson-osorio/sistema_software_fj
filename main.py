# main.py

import logging
from excepciones import ClienteInvalidoError, ServicioError, ReservaError
from entidades import Cliente
from servicios import ReservaSala, AlquilerEquipos, AsesoriaEspecializada
from reserva import Reserva

# Configuración de logs
LOG_FILENAME = "sistema_software_fj.log"
logging.basicConfig(
    filename=LOG_FILENAME,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)

def ejecutar_simulacion():
    print("=== INICIO DE LA SIMULACIÓN DE 10 OPERACIONES (SOFTWARE FJ) ===\n")
    
    clientes_registrados = []
    servicios_registrados = []
    reservas_registradas = []

    # Batería de las 10 operaciones requeridas
    operaciones = [
        lambda: registrar_cliente(clientes_registrados, "12345678", "Ana María Gómez", "ana.gomez@mail.com", "3101234567"),
        lambda: registrar_cliente(clientes_registrados, "1234AB", "Carlos Pérez", "carlos@mail.com", "3209876543"),
        lambda: registrar_servicio(servicios_registrados, ReservaSala("SAL-01", 50.0, 20, True)),
        lambda: registrar_servicio(servicios_registrados, AlquilerEquipos("EQ-01", 30.0, "Dell Latitude", True)),
        lambda: registrar_servicio(servicios_registrados, AsesoriaEspecializada("ASE-01", -100.0, "Software Architecture", True)),
        lambda: registrar_servicio(servicios_registrados, ReservaSala("SAL-02", 70.0, 50, False)),
        lambda: crear_reserva(clientes_registrados[0], servicios_registrados[0], 4, reservas_registradas),
        lambda: crear_reserva(clientes_registrados[0], servicios_registrados[2], 2, reservas_registradas), # Intentando usar SAL-02 (no disponible)
        lambda: crear_reserva(clientes_registrados[0], servicios_registrados[1], 5, reservas_registradas, descuento=0.15),
        lambda: probar_operacion_invalida()
    ]

    for i, op in enumerate(operaciones, start=1):
        print(f"--- Operación #{i} ---")
        try:
            op()
        except Exception as e:
            print(f"[CONTROLADO] Excepción capturada en Operación #{i}: {e}")
            logging.warning(f"Operación #{i} generó excepción controlada: {e}")
        print()

    print("=== FIN DE LA SIMULACIÓN ===")
    print(f"Total clientes en memoria: {len(clientes_registrados)}")
    print(f"Total servicios activos: {len(servicios_registrados)}")
    print(f"Total reservas registradas: {len(reservas_registradas)}")
    print(f"Los eventos y errores detallados han sido guardados en '{LOG_FILENAME}'.")


def registrar_cliente(lista_clientes, cedula, nombre, correo, telefono):
    try:
        print(f"Intentando registrar cliente: {nombre}...")
        cliente = Cliente(cedula, nombre, correo, telefono)
    except ClienteInvalidoError as ce:
        logging.error(f"Error de validación en cliente: {ce}")
        raise
    else:
        lista_clientes.append(cliente)
        print(f"¡Éxito! Cliente registrado: {cliente.obtener_detalle()}")
        logging.info(f"Cliente registrado con éxito: {cedula}")
    finally:
        print("-> Proceso de validación de cliente finalizado.\n")


def registrar_servicio(lista_servicios, servicio):
    try:
        print(f"Registrando servicio: {servicio.identificador} ({servicio.nombre_servicio})...")
        if servicio.costo_base < 0:
            raise ServicioError("El costo base no puede ser menor a cero.")
    except ServicioError as se:
        logging.error(f"Error registrando servicio: {se}")
        print(f"Error controlado de servicio: {se}")
        raise
    else:
        lista_servicios.append(servicio)
        print(f"¡Éxito! Servicio registrado: {servicio.obtener_detalle()}")
        logging.info(f"Servicio registrado: {servicio.identificador}")
    finally:
        print("-> Proceso de registro de servicio concluido.\n")


def crear_reserva(cliente, servicio, horas, lista_reservas, **kwargs):
    try:
        print(f"Creando reserva para {cliente.nombre} en servicio {servicio.identificador}...")
        reserva = Reserva(cliente, servicio, horas, **kwargs)
        reserva.confirmar()
    except (ReservaError, ServicioError) as ex:
        logging.error(f"Fallo en la creación/confirmación de reserva: {ex}")
        print(f"Error en reserva: {ex}")
        raise
    else:
        lista_reservas.append(reserva)
        print(f"¡Éxito! {reserva.obtener_detalle()}")
        logging.info(f"Reserva creada y confirmada: {reserva.identificador}")
    finally:
        print("-> Intento de reserva procesado.\n")


def probar_operacion_invalida():
    try:
        print("Simulando operación con datos inconsistentes (ej. cálculo con horas negativas)...")
        equipo = AlquilerEquipos("EQ-ERR", 20.0, "Test", True)
        equipo.calcular_costo(-5)
    except Exception as e:
        logging.error(f"Operación inválida detectada y manejada: {e}")
        raise RuntimeError("Fallo intencional controlado en operación de cálculo.") from e


if __name__ == "__main__":
    ejecutar_simulacion()