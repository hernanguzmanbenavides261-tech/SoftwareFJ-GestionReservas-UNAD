"""
Gestor central de Software FJ.
Administra listas internas de clientes, servicios y reservas con manejo avanzado de excepciones.
"""
from typing import List, Optional
from models import Cliente, Servicio, Reserva
from exceptions import SoftwareFJError, DatoInvalidoError, OperacionNoPermitidaError
from logger_config import configurar_logger


class GestorSoftwareFJ:
    def __init__(self):
        self.__clientes: List[Cliente] = []
        self.__servicios: List[Servicio] = []
        self.__reservas: List[Reserva] = []
        self.logger = configurar_logger()

    def registrar_cliente(self, id_c: str, nombre: str, correo: str, telefono: str) -> Optional[Cliente]:
        try:
            if any(c.id_entidad == id_c for c in self.__clientes):
                raise OperacionNoPermitidaError(f"Ya existe un cliente registrado con ID '{id_c}'.")
            nuevo_cliente = Cliente(id_c, nombre, correo, telefono)
        except SoftwareFJError as e:
            self.logger.error(f"[FALLO REGISTRO CLIENTE] {e}", exc_info=True)
            return None
        else:
            self.__clientes.append(nuevo_cliente)
            self.logger.info(f"[OK] {nuevo_cliente.obtener_resumen()}")
            return nuevo_cliente
        finally:
            self.logger.debug(f"Finalizó intento de registro para cliente ID={id_c}.")

    def registrar_servicio(self, servicio: Servicio) -> bool:
        try:
            if not isinstance(servicio, Servicio):
                raise DatoInvalidoError("El objeto proporcionado no hereda de Servicio.")
            if any(s.id_entidad == servicio.id_entidad for s in self.__servicios):
                raise OperacionNoPermitidaError(f"Servicio duplicado con ID '{servicio.id_entidad}'.")
        except SoftwareFJError as e:
            self.logger.error(f"[FALLO REGISTRO SERVICIO] {e}", exc_info=True)
            return False
        else:
            self.__servicios.append(servicio)
            self.logger.info(f"[OK] Servicio agregado: {servicio.obtener_resumen()}")
            return True
        finally:
            self.logger.debug("Verificación de inventario de servicios completada.")

    def buscar_cliente(self, id_c: str) -> Cliente:
        for c in self.__clientes:
            if c.id_entidad == id_c:
                return c
        raise DatoInvalidoError(f"No se encontró cliente con ID '{id_c}'.")

    def buscar_servicio(self, id_s: str) -> Servicio:
        for s in self.__servicios:
            if s.id_entidad == id_s:
                return s
        raise DatoInvalidoError(f"No se encontró servicio con ID '{id_s}'.")

    def crear_y_confirmar_reserva(
        self,
        id_r: str,
        id_cliente: str,
        id_servicio: str,
        duracion_horas: float,
        descuento_pct: float = 0.0,
        recargo_fijo: Optional[float] = None
    ) -> Optional[Reserva]:
        try:
            try:
                cliente = self.buscar_cliente(id_cliente)
                servicio = self.buscar_servicio(id_servicio)
            except DatoInvalidoError as err_busqueda:
                # Encadenamiento explícito de excepciones (raise ... from)
                raise OperacionNoPermitidaError(
                    f"Imposible iniciar reserva '{id_r}' por referencias inexistentes."
                ) from err_busqueda

            reserva = Reserva(id_r, cliente, servicio, duracion_horas)
            reserva.confirmar(descuento_pct=descuento_pct, recargo_fijo=recargo_fijo)

        except SoftwareFJError as e:
            causa = f" | Causa original: {e.__cause__}" if e.__cause__ else ""
            self.logger.error(f"[FALLO RESERVA {id_r}] {e}{causa}", exc_info=True)
            return None
        else:
            self.__reservas.append(reserva)
            self.logger.info(f"[OK] {reserva.obtener_resumen()}")
            return reserva
        finally:
            self.logger.debug(f"Cierre de transacción en memoria para reserva '{id_r}'.")

    def procesar_reserva(self, id_r: str) -> None:
        try:
            reserva = next((r for r in self.__reservas if r.id_entidad == id_r), None)
            if not reserva:
                raise DatoInvalidoError(f"Reserva '{id_r}' no existe en el sistema.")
            resultado = reserva.procesar()
        except SoftwareFJError as e:
            self.logger.error(f"[FALLO PROCESAMIENTO] {e}", exc_info=True)
        else:
            self.logger.info(f"[OK] {resultado}")

    def cancelar_reserva(self, id_r: str) -> None:
        try:
            reserva = next((r for r in self.__reservas if r.id_entidad == id_r), None)
            if not reserva:
                raise DatoInvalidoError(f"Reserva '{id_r}' no existe en el sistema.")
            reserva.cancelar()
        except SoftwareFJError as e:
            self.logger.error(f"[FALLO CANCELACIÓN] {e}", exc_info=True)
        else:
            self.logger.info(f"[OK] Reserva '{id_r}' cancelada y recurso liberado.")