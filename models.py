"""
Módulo principal de dominio orientado a objetos.
Implementa abstracción, herencia, encapsulación, polimorfismo y sobrecarga simulada.
"""
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional
from exceptions import (
    DatoInvalidoError,
    ParametroFaltanteError,
    ServicioNoDisponibleError,
    OperacionNoPermitidaError,
    CalculoInconsistenteError,
)


class EntidadBase(ABC):
    """Clase abstracta raíz que representa cualquier entidad del sistema."""

    def __init__(self, id_entidad: str):
        if not id_entidad or not str(id_entidad).strip():
            raise ParametroFaltanteError("El ID de la entidad es obligatorio.")
        self.__id_entidad = str(id_entidad).strip()
        self.__fecha_creacion = datetime.now()

    @property
    def id_entidad(self) -> str:
        return self.__id_entidad

    @property
    def fecha_creacion(self) -> datetime:
        return self.__fecha_creacion

    @abstractmethod
    def obtener_resumen(self) -> str:
        """Método abstracto que obliga a las subclases a describirse."""
        pass


class Cliente(EntidadBase):
    """Representa un cliente de Software FJ con encapsulación estricta."""

    def __init__(self, id_cliente: str, nombre: str, correo: str, telefono: str):
        super().__init__(id_cliente)
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono

    @property
    def nombre(self) -> str:
        return self.__nombre

    @nombre.setter
    def nombre(self, valor: str):
        if not valor or len(valor.strip()) < 3:
            raise DatoInvalidoError(f"Nombre de cliente inválido: '{valor}'. Mínimo 3 caracteres.")
        self.__nombre = valor.strip()

    @property
    def correo(self) -> str:
        return self.__correo

    @correo.setter
    def correo(self, valor: str):
        if not valor or "@" not in valor or "." not in valor.split("@")[-1]:
            raise DatoInvalidoError(f"Correo electrónico inválido: '{valor}'.")
        self.__correo = valor.strip().lower()

    @property
    def telefono(self) -> str:
        return self.__telefono

    @telefono.setter
    def telefono(self, valor: str):
        limpio = str(valor).strip()
        if not limpio.isdigit() or len(limpio) < 7:
            raise DatoInvalidoError(f"Teléfono inválido: '{valor}'. Debe tener al menos 7 dígitos.")
        self.__telefono = limpio

    def obtener_resumen(self) -> str:
        return f"Cliente [{self.id_entidad}] {self.nombre} | Email: {self.correo} | Tel: {self.telefono}"


class Servicio(EntidadBase, ABC):
    """Clase abstracta base para los servicios ofrecidos por Software FJ."""

    def __init__(self, id_servicio: str, nombre: str, tarifa_base: float, disponible: bool = True):
        super().__init__(id_servicio)
        if not nombre or not nombre.strip():
            raise ParametroFaltanteError("El nombre del servicio no puede estar vacío.")
        if tarifa_base <= 0:
            raise DatoInvalidoError(f"La tarifa base debe ser mayor a 0. Recibido: {tarifa_base}")

        self.__nombre = nombre.strip()
        self.__tarifa_base = float(tarifa_base)
        self.__disponible = bool(disponible)

    @property
    def nombre(self) -> str:
        return self.__nombre

    @property
    def tarifa_base(self) -> float:
        return self.__tarifa_base

    @property
    def disponible(self) -> bool:
        return self.__disponible

    @disponible.setter
    def disponible(self, estado: bool):
        self.__disponible = bool(estado)

    @abstractmethod
    def validar_parametros_uso(self, duracion_horas: float) -> None:
        """Valida reglas específicas de cada tipo de servicio."""
        pass

    @abstractmethod
    def calcular_costo_base(self, duracion_horas: float) -> float:
        """Cálculo polimórfico del costo antes de impuestos/descuentos."""
        pass

    def calcular_costo_total(
        self,
        duracion_horas: float,
        impuesto_pct: float = 0.19,
        descuento_pct: float = 0.0,
        recargo_fijo: Optional[float] = None
    ) -> float:
        """
        Método con sobrecarga funcional mediante parámetros opcionales:
        Permite calcular costo estándar, con descuento, exento de IVA o con recargo extra.
        """
        if not (0 <= impuesto_pct <= 1):
            raise CalculoInconsistenteError(f"Porcentaje de impuesto fuera de rango: {impuesto_pct}")
        if not (0 <= descuento_pct < 1):
            raise CalculoInconsistenteError(f"Porcentaje de descuento inválido: {descuento_pct}")

        subtotal = self.calcular_costo_base(duracion_horas)
        if recargo_fijo is not None:
            if recargo_fijo < 0:
                raise CalculoInconsistenteError("El recargo fijo no puede ser negativo.")
            subtotal += recargo_fijo

        subtotal_con_desc = subtotal * (1 - descuento_pct)
        total = subtotal_con_desc * (1 + impuesto_pct)

        if total <= 0:
            raise CalculoInconsistenteError("El costo total calculado no puede ser menor o igual a cero.")
        return round(total, 2)


class ReservaSala(Servicio):
    """Servicio especializado: Reserva de salas de juntas o capacitación."""

    def __init__(self, id_servicio: str, nombre: str, tarifa_base: float, capacidad: int, tiene_proyector: bool = True):
        super().__init__(id_servicio, nombre, tarifa_base)
        if capacidad <= 0:
            raise DatoInvalidoError("La capacidad de la sala debe ser mayor a 0 personas.")
        self.__capacidad = int(capacidad)
        self.__tiene_proyector = bool(tiene_proyector)

    def validar_parametros_uso(self, duracion_horas: float) -> None:
        if duracion_horas < 1 or duracion_horas > 12:
            raise DatoInvalidoError("Las salas solo se reservan entre 1 y 12 horas por jornada.")

    def calcular_costo_base(self, duracion_horas: float) -> float:
        self.validar_parametros_uso(duracion_horas)
        extra_equipo = 15000.0 if self.__tiene_proyector else 0.0
        return (self.tarifa_base * duracion_horas) + extra_equipo

    def obtener_resumen(self) -> str:
        proy = "con proyector" if self.__tiene_proyector else "sin proyector"
        return f"Sala [{self.id_entidad}] {self.nombre} (Cap: {self.__capacidad}, {proy}) - ${self.tarifa_base:,.0f}/h"


class AlquilerEquipo(Servicio):
    """Servicio especializado: Alquiler de hardware (portátiles, servidores, proyectores)."""

    def __init__(self, id_servicio: str, nombre: str, tarifa_base: float, serial: str, deposito_seguridad: float):
        super().__init__(id_servicio, nombre, tarifa_base)
        if not serial or not serial.strip():
            raise ParametroFaltanteError("El serial del equipo es obligatorio.")
        if deposito_seguridad < 0:
            raise DatoInvalidoError("El depósito de seguridad no puede ser negativo.")
        self.__serial = serial.strip()
        self.__deposito = float(deposito_seguridad)

    def validar_parametros_uso(self, duracion_horas: float) -> None:
        if duracion_horas < 2:
            raise DatoInvalidoError("El alquiler mínimo de equipos es de 2 horas.")

    def calcular_costo_base(self, duracion_horas: float) -> float:
        self.validar_parametros_uso(duracion_horas)
        return (self.tarifa_base * duracion_horas) + self.__deposito

    def obtener_resumen(self) -> str:
        return f"Equipo [{self.id_entidad}] {self.nombre} (SN: {self.__serial}) - ${self.tarifa_base:,.0f}/h"


class AsesoriaEspecializada(Servicio):
    """Servicio especializado: Consultoría en ingeniería de software, redes o cloud."""

    def __init__(self, id_servicio: str, nombre: str, tarifa_base: float, especialidad: str, nivel_senior: bool = True):
        super().__init__(id_servicio, nombre, tarifa_base)
        if not especialidad or not especialidad.strip():
            raise ParametroFaltanteError("Debe indicar el área de especialidad.")
        self.__especialidad = especialidad.strip()
        self.__nivel_senior = bool(nivel_senior)

    def validar_parametros_uso(self, duracion_horas: float) -> None:
        if duracion_horas <= 0 or duracion_horas > 40:
            raise DatoInvalidoError("La asesoría debe ser mayor a 0 y máximo 40 horas por bloque.")

    def calcular_costo_base(self, duracion_horas: float) -> float:
        self.validar_parametros_uso(duracion_horas)
        factor = 1.25 if self.__nivel_senior else 1.0
        return self.tarifa_base * duracion_horas * factor

    def obtener_resumen(self) -> str:
        nivel = "Senior" if self.__nivel_senior else "Semi-Senior"
        return f"Asesoría [{self.id_entidad}] {self.nombre} ({self.__especialidad} - {nivel}) - ${self.tarifa_base:,.0f}/h"


class Reserva(EntidadBase):
    """Integra Cliente, Servicio, duración y ciclo de vida de estados."""

    def __init__(self, id_reserva: str, cliente: Cliente, servicio: Servicio, duracion_horas: float):
        super().__init__(id_reserva)
        if not isinstance(cliente, Cliente):
            raise DatoInvalidoError("Se requiere una instancia válida de Cliente.")
        if not isinstance(servicio, Servicio):
            raise DatoInvalidoError("Se requiere una instancia válida de Servicio.")
        if not servicio.disponible:
            raise ServicioNoDisponibleError(f"El servicio '{servicio.nombre}' no está disponible actualmente.")

        servicio.validar_parametros_uso(duracion_horas)
        self.__cliente = cliente
        self.__servicio = servicio
        self.__duracion_horas = float(duracion_horas)
        self.__estado = "PENDIENTE"
        self.__costo_final = 0.0

    @property
    def estado(self) -> str:
        return self.__estado

    @property
    def costo_final(self) -> float:
        return self.__costo_final

    def confirmar(self, descuento_pct: float = 0.0, recargo_fijo: Optional[float] = None) -> float:
        if self.__estado != "PENDIENTE":
            raise OperacionNoPermitidaError(f"No se puede confirmar una reserva en estado '{self.__estado}'.")
        if not self.__servicio.disponible:
            raise ServicioNoDisponibleError(f"El servicio '{self.__servicio.nombre}' dejó de estar disponible.")

        self.__costo_final = self.__servicio.calcular_costo_total(
            duracion_horas=self.__duracion_horas,
            descuento_pct=descuento_pct,
            recargo_fijo=recargo_fijo
        )
        self.__estado = "CONFIRMADA"
        # Si es sala o equipo único, se marca ocupado
        if isinstance(self.__servicio, (ReservaSala, AlquilerEquipo)):
            self.__servicio.disponible = False
        return self.__costo_final

    def cancelar(self) -> None:
        if self.__estado == "CANCELADA":
            raise OperacionNoPermitidaError(f"La reserva {self.id_entidad} ya se encuentra cancelada.")
        if self.__estado == "PROCESADA":
            raise OperacionNoPermitidaError(f"La reserva {self.id_entidad} ya fue procesada/facturada y no puede cancelarse.")

        self.__estado = "CANCELADA"
        self.__servicio.disponible = True

    def procesar(self) -> str:
        if self.__estado != "CONFIRMADA":
            raise OperacionNoPermitidaError(
                f"Solo se pueden procesar reservas CONFIRMADAS. Estado actual: '{self.__estado}'."
            )
        self.__estado = "PROCESADA"
        self.__servicio.disponible = True
        return f"Reserva {self.id_entidad} ejecutada y facturada por ${self.__costo_final:,.2f}."

    def obtener_resumen(self) -> str:
        return (
            f"Reserva [{self.id_entidad}] | Estado: {self.__estado} | "
            f"Cliente: {self.__cliente.nombre} | Servicio: {self.__servicio.nombre} | "
            f"Horas: {self.__duracion_horas} | Total: ${self.__costo_final:,.2f}"
        )