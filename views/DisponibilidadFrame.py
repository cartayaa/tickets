import customtkinter as ctk
from utils.database import get_slots_for_date
from datetime import datetime

class DisponibilidadFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        ctk.CTkLabel(self, text="🕒 DISPONIBILIDAD DE HOY", font=("Arial", 24, "bold")).pack(pady=10, fill="x")

        slots = get_slots_for_date(datetime.now().date())
        
        if not slots:
            ctk.CTkLabel(self, text="No hay slots configurados para hoy.", font=("Arial", 16)).pack(pady=20)
            return

        # Caso especial: Día no laborable
        if slots and all(slot[2] == 2 for slot in slots):
            frame = ctk.CTkFrame(self)
            frame.pack(pady=20, padx=20, fill="x", expand=True)
            ctk.CTkLabel(frame, text="🚫", font=("Arial", 48)).pack(pady=(20,0))
            ctk.CTkLabel(frame, text="Hoy es un día no laborable.", font=("Arial", 18)).pack(pady=(0, 20))
            return

        total_slots = len(slots)
        slots_libres = len([s for s in slots if s[2] == 0])
        slots_ocupados = len([s for s in slots if s[2] == 1])
        
        progreso = slots_ocupados / total_slots if total_slots > 0 else 0

        # Frame para la barra de progreso
        progress_frame = ctk.CTkFrame(self)
        progress_frame.pack(pady=20, padx=20, fill="x")
        ctk.CTkLabel(progress_frame, text=f"Ocupación: {slots_ocupados} de {total_slots}", font=("Arial", 16)).pack(pady=(10, 5))
        progressbar = ctk.CTkProgressBar(progress_frame, height=20)
        progressbar.pack(fill="x", padx=20, pady=(0, 20))
        progressbar.set(progreso)

        # Frame para los contadores
        counters_frame = ctk.CTkFrame(self, fg_color="transparent")
        counters_frame.pack(pady=10, padx=20, fill="x")
        counters_frame.grid_columnconfigure((0, 1), weight=1)
        ctk.CTkLabel(counters_frame, text=f"✅ Libres: {slots_libres}", font=("Arial", 18, "bold"), text_color="#2ECC71").grid(row=0, column=0)
        ctk.CTkLabel(counters_frame, text=f"❌ Ocupados: {slots_ocupados}", font=("Arial", 18, "bold"), text_color="#E74C3C").grid(row=0, column=1)

        # Frame con scroll para los slots
        slots_container = ctk.CTkScrollableFrame(self, fg_color="transparent")
        slots_container.pack(pady=10, padx=20, fill="both", expand=True)
        
        ctk.CTkLabel(slots_container, text="Horarios disponibles:", font=("Arial", 14, "bold")).pack(anchor="w", pady=(10, 5))
        
        # Crear una grid para los slots
        slots_grid_frame = ctk.CTkFrame(slots_container, fg_color="transparent")
        slots_grid_frame.pack(fill="both", expand=True)
        
        slots_por_fila = 4
        for idx, slot in enumerate(slots):
            slot_id, hora, estado = slot
            row = idx // slots_por_fila
            col = idx % slots_por_fila
            
            # Determinar color según estado
            if estado == 0:  # Libre
                color = "#2ECC71"
                estado_texto = "Libre"
            elif estado == 1:  # Ocupado
                color = "#E74C3C"
                estado_texto = "Ocupado"
            else:  # No laborable o desconocido
                color = "#95A5A6"
                estado_texto = "N/A"
            
            slot_frame = ctk.CTkFrame(slots_grid_frame, fg_color=color, corner_radius=8)
            slot_frame.grid(row=row, column=col, padx=5, pady=5, sticky="ew")
            
            ctk.CTkLabel(slot_frame, text=hora, font=("Arial", 14, "bold"), text_color="white").pack(pady=8)
            ctk.CTkLabel(slot_frame, text=estado_texto, font=("Arial", 11), text_color="white").pack(pady=(0, 8))
        
        # Configurar pesos de columnas
        for i in range(slots_por_fila):
            slots_grid_frame.grid_columnconfigure(i, weight=1)