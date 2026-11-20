"""
Punto de entrada principal de Software FJ.
Simula 12 operaciones (válidas e inválidas) demostrando estabilidad ante errores.
"""
from manager import GestorSoftwareFJ
from models import ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from exceptions import SoftwareFJError


def ejecutar_simulacion():
    sistema = GestorSoftwareFJ()
    print("\n=== INICIANDO SIMULACIÓN DE SOFTWARE FJ ===\n")

    # 1. Registro válido de clientes
    sistema.registrar_cliente("CLI-01", "Laura Martínez", "laura.m@empresa.com", "3104567890")
    sistema.registrar_cliente("CLI-02", "Carlos Gómez", "cgomez@tech.co", "3209876543")

    # 2. Registro inválido de cliente (correo mal formado y teléfono corto -> capturado)
    sistema.registrar_cliente("CLI-03", "Ana Ruiz", "correo_sin_arroba.com", "123")

    # 3. Registro inválido de cliente duplicado
    sistema.registrar_cliente("CLI-01", "Laura Duplicada", "otra@empresa.com", "3001112233")

    # 4. Creación válida de los 3 tipos de servicios especializados (Polimorfismo)
    sala_juntas = ReservaSala("SRV-01", "Sala Innovación A", 80000, capacidad=12, tiene_proyector=True)
    laptop_dev = AlquilerEquipo("SRV-02", "Workstation Dell XPS", 25000, serial="DL-998877", deposito_seguridad=50000)
    asesoria_cloud = AsesoriaEspecializada("SRV-03", "Arquitectura AWS", 120000, especialidad="Cloud Computing", nivel_senior=True)

    sistema.registrar_servicio(sala_juntas)
    sistema.registrar_servicio(laptop_dev)
    sistema.registrar_servicio(asesoria_cloud)

    # 5. Creación inválida de servicio (tarifa negativa -> capturada antes de registrar)
    try:
        servicio_malo = ReservaSala("SRV-04", "Sala Fantasma", -50000, capacidad=5)
        sistema.registrar_servicio(servicio_malo)
    except SoftwareFJError as e:
        sistema.logger.error(f"[FALLO CREACIÓN SERVICIO] {e}", exc_info=True)

    # 6. Reserva exitosa de Sala con descuento del 10% (Sobrecarga de cálculo)
    sistema.crear_y_confirmar_reserva("RES-01", "CLI-01", "SRV-01", duracion_horas=4, descuento_pct=0.10)

    # 7. Intento fallido de reserva sobre la misma Sala que ya quedó ocupada (ServicioNoDisponibleError)
    sistema.crear_y_confirmar_reserva("RES-02", "CLI-02", "SRV-01", duracion_horas=2)

    # 8. Intento fallido de alquiler de equipo por menos de 2 horas (Regla polimórfica de AlquilerEquipo)
    sistema.crear_y_confirmar_reserva("RES-03", "CLI-02", "SRV-02", duracion_horas=1)

    # 9. Reserva exitosa de Asesoría Senior con recargo por urgencia
    sistema.crear_y_confirmar_reserva("RES-04", "CLI-02", "SRV-03", duracion_horas=5, recargo_fijo=40000)

    # 10. Reserva fallida con cliente inexistente (Prueba encadenamiento raise ... from)
    sistema.crear_y_confirmar_reserva("RES-05", "CLI-999", "SRV-02", duracion_horas=3)

    # 11. Procesamiento exitoso de reserva y luego intento ilegal de cancelarla
    sistema.procesar_reserva("RES-01")
    sistema.cancelar_reserva("RES-01")  # Debe fallar porque ya está PROCESADA

    # 12. Cancelación válida de RES-04 y reserva válida de equipo
    sistema.cancelar_reserva("RES-04")
    sistema.crear_y_confirmar_reserva("RES-06", "CLI-01", "SRV-02", duracion_horas=3)

    print("\n=== SIMULACIÓN FINALIZADA SIN INTERRUPCIONES ===")
    print("Revise el archivo 'sistema_fj.log' para auditar el detalle técnico de eventos y excepciones.\n")


if __name__ == "__main__":
    ejecutar_simulacion()