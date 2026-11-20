"""
Interfaz Gráfica (Tkinter) para el Sistema Integral de Software FJ.
Permite operar clientes, servicios, reservas, ejecutar la simulación y auditar logs.
"""
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from manager import GestorSoftwareFJ
from models import ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from exceptions import SoftwareFJError


class InterfazSoftwareFJ:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Software FJ - Gestión Integral de Clientes, Servicios y Reservas (UNAD)")
        self.root.geometry("880x620")
        self.sistema = GestorSoftwareFJ()

        # Notebook (pestañas)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        self.tab_clientes = ttk.Frame(self.notebook)
        self.tab_servicios = ttk.Frame(self.notebook)
        self.tab_reservas = ttk.Frame(self.notebook)
        self.tab_logs = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_clientes, text="1. Clientes")
        self.notebook.add(self.tab_servicios, text="2. Servicios")
        self.notebook.add(self.tab_reservas, text="3. Reservas y Simulación")
        self.notebook.add(self.tab_logs, text="4. Auditoría (sistema_fj.log)")

        self._construir_tab_clientes()
        self._construir_tab_servicios()
        self._construir_tab_reservas()
        self._construir_tab_logs()

    # ---------------- PESTAÑA CLIENTES ----------------
    def _construir_tab_clientes(self):
        frame = ttk.LabelFrame(self.tab_clientes, text="Registrar Nuevo Cliente", padding=15)
        frame.pack(fill="x", padx=15, pady=15)

        ttk.Label(frame, text="ID Cliente (ej. CLI-10):").grid(row=0, column=0, sticky="w", pady=5)
        self.ent_cli_id = ttk.Entry(frame, width=35)
        self.ent_cli_id.grid(row=0, column=1, pady=5, padx=10)

        ttk.Label(frame, text="Nombre Completo:").grid(row=1, column=0, sticky="w", pady=5)
        self.ent_cli_nombre = ttk.Entry(frame, width=35)
        self.ent_cli_nombre.grid(row=1, column=1, pady=5, padx=10)

        ttk.Label(frame, text="Correo Electrónico:").grid(row=2, column=0, sticky="w", pady=5)
        self.ent_cli_correo = ttk.Entry(frame, width=35)
        self.ent_cli_correo.grid(row=2, column=1, pady=5, padx=10)

        ttk.Label(frame, text="Teléfono (mín. 7 dígitos):").grid(row=3, column=0, sticky="w", pady=5)
        self.ent_cli_tel = ttk.Entry(frame, width=35)
        self.ent_cli_tel.grid(row=3, column=1, pady=5, padx=10)

        ttk.Button(frame, text="Registrar Cliente", command=self._accion_registrar_cliente).grid(
            row=4, column=0, columnspan=2, pady=12
        )

    def _accion_registrar_cliente(self):
        cliente = self.sistema.registrar_cliente(
            self.ent_cli_id.get(),
            self.ent_cli_nombre.get(),
            self.ent_cli_correo.get(),
            self.ent_cli_tel.get(),
        )
        self._actualizar_vista_logs()
        if cliente:
            messagebox.showinfo("Éxito", f"Registrado:\n{cliente.obtener_resumen()}")
            self.ent_cli_id.delete(0, tk.END)
            self.ent_cli_nombre.delete(0, tk.END)
            self.ent_cli_correo.delete(0, tk.END)
            self.ent_cli_tel.delete(0, tk.END)
        else:
            messagebox.showerror("Error Controlado", "No se pudo registrar el cliente. Revisa el detalle en la pestaña de Auditoría/Logs.")

    # ---------------- PESTAÑA SERVICIOS ----------------
    def _construir_tab_servicios(self):
        frame = ttk.LabelFrame(self.tab_servicios, text="Crear Servicio Especializado", padding=15)
        frame.pack(fill="x", padx=15, pady=15)

        ttk.Label(frame, text="Tipo de Servicio:").grid(row=0, column=0, sticky="w", pady=5)
        self.cmb_srv_tipo = ttk.Combobox(
            frame, values=["ReservaSala", "AlquilerEquipo", "AsesoriaEspecializada"], state="readonly", width=32
        )
        self.cmb_srv_tipo.current(0)
        self.cmb_srv_tipo.grid(row=0, column=1, pady=5, padx=10)

        ttk.Label(frame, text="ID Servicio (ej. SRV-10):").grid(row=1, column=0, sticky="w", pady=5)
        self.ent_srv_id = ttk.Entry(frame, width=35)
        self.ent_srv_id.grid(row=1, column=1, pady=5, padx=10)

        ttk.Label(frame, text="Nombre del Servicio:").grid(row=2, column=0, sticky="w", pady=5)
        self.ent_srv_nombre = ttk.Entry(frame, width=35)
        self.ent_srv_nombre.grid(row=2, column=1, pady=5, padx=10)

        ttk.Label(frame, text="Tarifa Base por Hora ($):").grid(row=3, column=0, sticky="w", pady=5)
        self.ent_srv_tarifa = ttk.Entry(frame, width=35)
        self.ent_srv_tarifa.grid(row=3, column=1, pady=5, padx=10)

        ttk.Label(frame, text="Atributo Extra (Capacidad / Serial / Área):").grid(row=4, column=0, sticky="w", pady=5)
        self.ent_srv_extra = ttk.Entry(frame, width=35)
        self.ent_srv_extra.insert(0, "10")
        self.ent_srv_extra.grid(row=4, column=1, pady=5, padx=10)

        ttk.Button(frame, text="Guardar Servicio", command=self._accion_registrar_servicio).grid(
            row=5, column=0, columnspan=2, pady=12
        )

    def _accion_registrar_servicio(self):
        tipo = self.cmb_srv_tipo.get()
        try:
            tarifa = float(self.ent_srv_tarifa.get())
            id_s = self.ent_srv_id.get()
            nombre = self.ent_srv_nombre.get()
            extra = self.ent_srv_extra.get()

            if tipo == "ReservaSala":
                srv = ReservaSala(id_s, nombre, tarifa, capacidad=int(extra), tiene_proyector=True)
            elif tipo == "AlquilerEquipo":
                srv = AlquilerEquipo(id_s, nombre, tarifa, serial=extra, deposito_seguridad=30000)
            else:
                srv = AsesoriaEspecializada(id_s, nombre, tarifa, especialidad=extra, nivel_senior=True)

            if self.sistema.registrar_servicio(srv):
                self._actualizar_vista_logs()
                messagebox.showinfo("Éxito", f"Servicio creado:\n{srv.obtener_resumen()}")
            else:
                self._actualizar_vista_logs()
                messagebox.showerror("Error Controlado", "Servicio duplicado o inválido. Revisa los logs.")
        except (ValueError, SoftwareFJError) as e:
            self.sistema.logger.error(f"[FALLO GUI SERVICIO] {e}", exc_info=True)
            self._actualizar_vista_logs()
            messagebox.showerror("Error de Validación", f"Datos inválidos: {e}")

    # ---------------- PESTAÑA RESERVAS Y SIMULACIÓN ----------------
    def _construir_tab_reservas(self):
        frame = ttk.LabelFrame(self.tab_reservas, text="Crear y Confirmar Reserva", padding=15)
        frame.pack(fill="x", padx=15, pady=10)

        ttk.Label(frame, text="ID Reserva (ej. RES-10):").grid(row=0, column=0, sticky="w", pady=4)
        self.ent_res_id = ttk.Entry(frame, width=30)
        self.ent_res_id.grid(row=0, column=1, pady=4, padx=10)

        ttk.Label(frame, text="ID Cliente:").grid(row=1, column=0, sticky="w", pady=4)
        self.ent_res_cli = ttk.Entry(frame, width=30)
        self.ent_res_cli.grid(row=1, column=1, pady=4, padx=10)

        ttk.Label(frame, text="ID Servicio:").grid(row=2, column=0, sticky="w", pady=4)
        self.ent_res_srv = ttk.Entry(frame, width=30)
        self.ent_res_srv.grid(row=2, column=1, pady=4, padx=10)

        ttk.Label(frame, text="Duración (Horas):").grid(row=3, column=0, sticky="w", pady=4)
        self.ent_res_horas = ttk.Entry(frame, width=30)
        self.ent_res_horas.grid(row=3, column=1, pady=4, padx=10)

        ttk.Label(frame, text="Descuento (0.0 a 0.5):").grid(row=4, column=0, sticky="w", pady=4)
        self.ent_res_desc = ttk.Entry(frame, width=30)
        self.ent_res_desc.insert(0, "0.0")
        self.ent_res_desc.grid(row=4, column=1, pady=4, padx=10)

        ttk.Button(frame, text="Confirmar Reserva", command=self._accion_crear_reserva).grid(
            row=5, column=0, columnspan=2, pady=10
        )

        # Botón para ejecutar la simulación automática de las 12 operaciones del Anexo 3
        frame_sim = ttk.LabelFrame(self.tab_reservas, text="Pruebas Automáticas (Anexo 3 - 12 Escenarios)", padding=15)
        frame_sim.pack(fill="x", padx=15, pady=10)
        ttk.Button(
            frame_sim,
            text="Ejecutar Simulación Completa (Éxitos y Excepciones Controladas)",
            command=self._ejecutar_simulacion_gui,
        ).pack(pady=5)

    def _accion_crear_reserva(self):
        try:
            horas = float(self.ent_res_horas.get())
            desc = float(self.ent_res_desc.get())
            reserva = self.sistema.crear_y_confirmar_reserva(
                self.ent_res_id.get(),
                self.ent_res_cli.get(),
                self.ent_res_srv.get(),
                duracion_horas=horas,
                descuento_pct=desc,
            )
            self._actualizar_vista_logs()
            if reserva:
                messagebox.showinfo("Reserva Confirmada", reserva.obtener_resumen())
            else:
                messagebox.showerror("Reserva Fallida", "La operación fue rechazada y registrada en el log.")
        except ValueError as e:
            self.sistema.logger.error(f"[FALLO GUI RESERVA] {e}", exc_info=True)
            self._actualizar_vista_logs()
            messagebox.showerror("Error Numérico", "Horas y descuento deben ser valores numéricos.")

    def _ejecutar_simulacion_gui(self):
        from main import ejecutar_simulacion
        ejecutar_simulacion()
        self._actualizar_vista_logs()
        self.notebook.select(self.tab_logs)
        messagebox.showinfo("Simulación Completada", "Se ejecutaron los 12 escenarios sin interrupciones. Revisa el registro en pantalla.")

    # ---------------- PESTAÑA LOGS ----------------
    def _construir_tab_logs(self):
        ttk.Button(self.tab_logs, text="Recargar Archivo sistema_fj.log", command=self._actualizar_vista_logs).pack(
            pady=8
        )
        self.txt_logs = scrolledtext.ScrolledText(self.tab_logs, width=100, height=28, font=("Consolas", 9))
        self.txt_logs.pack(fill="both", expand=True, padx=10, pady=5)
        self._actualizar_vista_logs()

    def _actualizar_vista_logs(self):
        self.txt_logs.delete("1.0", tk.END)
        try:
            with open("sistema_fj.log", "r", encoding="utf-8") as f:
                self.txt_logs.insert(tk.END, f.read())
            self.txt_logs.see(tk.END)
        except FileNotFoundError:
            self.txt_logs.insert(tk.END, "Aún no se ha generado el archivo sistema_fj.log.")


if __name__ == "__main__":
    ventana = tk.Tk()
    app = InterfazSoftwareFJ(ventana)
    ventana.mainloop()