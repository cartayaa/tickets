import customtkinter as ctk
from utils.database import get_next_working_days, get_slots_for_date, actualizar_estado_slot
from utils.printer import imprimir_ticket_real
from datetime import datetime

class AgendaFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.selected_id = None
        self.selected_hora = None
        self.selected_fecha = None

        ctk.CTkLabel(self, text="🎟️ GESTIÓN DE TICKETS", font=("Arial", 24, "bold")).pack(pady=10, fill="x")

        self.scrollable_frame = ctk.CTkScrollableFrame(self)
        self.scrollable_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Botón de Confirmar con color #2742F5
        self.btn_print = ctk.CTkButton(self,
                                       text="IMPRIMIR TICKET",
                                       state="disabled",
                                       fg_color="#2742F5",
                                       hover_color="#1A2EAB",
                                       command=self.imprimir)
        self.btn_print.pack(pady=10)

        self.actualizar_vista_slots()

    def actualizar_vista_slots(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        hoy = datetime.now().date()
        dias_a_mostrar = get_next_working_days(hoy, 3)

        if not dias_a_mostrar:
            ctk.CTkLabel(self.scrollable_frame, text="No hay días laborables configurados.").pack(pady=20)
            return

        for dia_obj in dias_a_mostrar:
            slots = get_slots_for_date(dia_obj)

            # Título para el día con la fecha
            dias_semana = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
            meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
            fecha_formateada = f"{dias_semana[dia_obj.weekday()]}, {dia_obj.day} de {meses[dia_obj.month-1]} de {dia_obj.year}"
            ctk.CTkLabel(self.scrollable_frame, text=fecha_formateada, font=("Arial", 18, "bold")).pack(pady=(20, 10), anchor="w", padx=10)

            # Frame para los slots de este día
            day_frame = ctk.CTkFrame(self.scrollable_frame)
            day_frame.pack(fill="x", padx=10, pady=5)

            # Definimos la fuente para el estado "Libre" (Negrita)
            fuente_negrita = ("Arial", 12, "bold")
            fuente_normal = ("Arial", 12)

            # Configurar grid para los botones
            num_columnas = 4
            for i in range(num_columnas):
                day_frame.grid_columnconfigure(i, weight=1)

            for i, (slot_id, hora, estado) in enumerate(slots):
                fila = i // num_columnas
                columna = i % num_columnas
                
                if estado == 0: # Libre
                    if self.selected_id == slot_id:
                        texto, color, hover, cmd, btn_estado = f"{hora}\nSeleccionado", "#555555", "#444444", self.deseleccionar, "normal"
                        t_color = "white"
                        f_config = fuente_normal
                    else:
                        # LIBRE (No seleccionado): Fondo verde, LETRA NEGRA Y NEGRITA
                        texto, color, hover, cmd, btn_estado = f"{hora}\nLibre", "#2B7AE3", "#1A2EAB", lambda id=slot_id, h=hora, d=dia_obj: self.seleccionar_slot(id, h, d), "normal"
                        t_color = "white"  # <--- Letra negra
                        f_config = fuente_negrita # <--- Negrita
                elif estado == 1: # Ocupado
                    texto, color, hover, cmd, btn_estado = f"{hora}\nOcupado", "#E74C3C", "#C0392B", lambda id=slot_id: self.cambiar_estado(id, 0), "normal"
                    t_color = "white"
                    f_config = fuente_normal
                else: # estado == 2, No laborable (No debería ocurrir si el día es laborable)
                    texto, color, hover, cmd, btn_estado = f"{hora}\nNo Disponible", "#95A5A6", "#7F8C8D", None, "disabled"
                    t_color = "white"
                    f_config = fuente_normal

                btn = ctk.CTkButton(
                    day_frame, 
                    text=texto, 
                    command=cmd, 
                    fg_color=color, 
                    hover_color=hover,
                    text_color=t_color,    # <--- Aplicamos color de texto
                    font=f_config,         # <--- Aplicamos la fuente (negrita o normal)
                    state=btn_estado,
                    height=60
                )
                btn.grid(row=fila, column=columna, padx=5, pady=5, sticky="nsew")

    def seleccionar_slot(self, slot_id, hora, fecha):
        self.selected_id = slot_id
        self.selected_hora = hora
        self.selected_fecha = fecha
        self.btn_print.configure(state="normal")
        self.actualizar_vista_slots()

    def deseleccionar(self):
        self.selected_id = None
        self.selected_hora = None
        self.selected_fecha = None
        self.btn_print.configure(state="disabled")
        self.actualizar_vista_slots()

    def cambiar_estado(self, slot_id, nuevo_estado):
        actualizar_estado_slot(slot_id, nuevo_estado)
        if self.selected_id == slot_id:
            self.deseleccionar()
        else:
            self.actualizar_vista_slots()

    def imprimir(self):
        if not self.selected_id or not self.selected_hora or not self.selected_fecha:
            return
        imprimir_ticket_real(self.selected_id, self.selected_hora, self.selected_fecha)
        self.deseleccionar()