import customtkinter as ctk
from utils.database import cargar_ajustes

class DashboardFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        datos = cargar_ajustes()
        v, s, d, h_ini, al_i, al_d, d_slot = datos[:7]

        ctk.CTkLabel(self, text="📊 DASHBOARD", font=("Arial", 24, "bold")).pack(pady=10, fill="x")

        # Contenedor principal para las dos columnas
        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=10, pady=10)
        main_container.grid_columnconfigure(0, weight=1)
        main_container.grid_columnconfigure(1, weight=1)

        # --- Columna Izquierda: Configuración ---
        settings_frame = ctk.CTkFrame(main_container)
        settings_frame.grid(row=0, column=0, padx=10, pady=0, sticky="nsew")
        ctk.CTkLabel(settings_frame, text="Configuración", font=("Arial", 16, "bold")).pack(pady=10)

        self.crear_readonly_input(settings_frame, "Precio Ticket (€):", f"{v:.2f}")
        self.crear_readonly_input(settings_frame, "Slots Diarios:", str(s))
        self.crear_readonly_input(settings_frame, "Días Semana:", str(d))
        self.crear_readonly_input(settings_frame, "Duración Slot (min):", str(d_slot))

        # --- Columna Izquierda: Jornada ---
        ctk.CTkFrame(settings_frame, height=20, fg_color="transparent").pack() # Separador
        settings_frame.grid(row=0, column=0, padx=10, pady=0, sticky="nsew")
        ctk.CTkLabel(settings_frame, text="Jornada", font=("Arial", 16, "bold")).pack(pady=10)

        self.crear_readonly_input(settings_frame, "Hora Inicio Jornada:", h_ini)
        self.crear_readonly_input(settings_frame, "Inicio Almuerzo:", al_i)
        self.crear_readonly_input(settings_frame, "Duración Almuerzo (min):", str(al_d))

        # --- Columna Derecha: Proyección ---
        projection_frame = ctk.CTkFrame(main_container)
        projection_frame.grid(row=0, column=1, padx=10, pady=0, sticky="nsew")
        ctk.CTkLabel(projection_frame, text="Proyección Financiera", font=("Arial", 16, "bold")).pack(pady=10)
        
        diario, semanal, mensual = v * s, v * s * d, v * s * d * 4
        self.crear_readonly_input(projection_frame, "💰 Proyección Diaria:", f"{diario:.2f} €")
        self.crear_readonly_input(projection_frame, "📅 Proyección Semanal:", f"{semanal:.2f} €")
        self.crear_readonly_input(projection_frame, "🚀 Proyección Mensual:", f"{mensual:.2f} €")

    def crear_readonly_input(self, master, txt, val):
        f = ctk.CTkFrame(master, fg_color="transparent")
        f.pack(pady=5)
        ctk.CTkLabel(f, text=txt, width=180, anchor="w").pack(side="left")
        e = ctk.CTkEntry(f)
        e.insert(0, val)
        e.configure(state="disabled")
        e.pack(side="left")