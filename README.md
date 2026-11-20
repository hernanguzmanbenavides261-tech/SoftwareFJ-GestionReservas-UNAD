# Sistema Integral de Gestión de Clientes, Servicios y Reservas - Software FJ

Proyecto desarrollado para el componente práctico (Fase 4) del curso **Programación (213023)** de la **Universidad Nacional Abierta y a Distancia (UNAD)**, programa de Ingeniería de Sistemas.

## Descripción
Aplicación modular en Python basada en Programación Orientada a Objetos (POO) sin uso de bases de datos. Gestiona clientes, servicios especializados y reservas en memoria mediante listas internas, implementando manejo avanzado de excepciones y registro persistente de eventos y errores en archivo plano (`sistema_fj.log`).

## Arquitectura del Proyecto
* `exceptions.py`: Jerarquía de excepciones personalizadas (`SoftwareFJError`, `DatoInvalidoError`, `ParametroFaltanteError`, `ServicioNoDisponibleError`, `OperacionNoPermitidaError`, `CalculoInconsistenteError`).
* `logger_config.py`: Configuración de `logging` hacia consola y archivo `sistema_fj.log`.
* `models.py`: Clases abstractas (`EntidadBase`, `Servicio`), encapsulación estricta (`Cliente`), polimorfismo en tres servicios especializados (`ReservaSala`, `AlquilerEquipo`, `AsesoriaEspecializada`), sobrecarga funcional en cálculo de costos y gestión de estados en `Reserva`.
* `manager.py`: Controlador en memoria con bloques `try/except`, `try/except/else`, `try/except/finally` y encadenamiento explícito de excepciones (`raise ... from`).
* `main.py`: Simulación de 12 escenarios (operaciones exitosas y fallidas) que verifican la continuidad operativa del sistema ante errores.

## Ejecución
```bash
python main.py