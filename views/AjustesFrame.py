import customtkinter as ctk
import sqlite3
from utils.database import cargar_ajustes, inicializar_db

class AjustesFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        datos = cargar_ajustes()
        v, s, d, h_ini, al_i, al_d, d_slot, pwd = datos[:8]
        lunes, martes, miercoles, jueves, viernes, sabado, domingo = datos[8:15]
        
        ctk.CTkLabel(self, text="⚙️ CONFIGURACIÓN", font=("Arial", 20, "bold")).pack(pady=20)
        
        self.entry_v = self.crear_input("Precio Ticket (€):", str(v))
        self.entry_s = self.crear_input("Slots Diarios:", str(s))
        self.entry_d = self.crear_input("Días Semana:", str(d))
        self.entry_ds = self.crear_input("Duración Slot (min):", str(d_slot))
        self.entry_hi = self.crear_input("Hora Inicio Jornada (HH:MM):", h_ini)
        
        ctk.CTkFrame(self, height=10, fg_color="transparent").pack() # Separador

        self.entry_ai = self.crear_input("Inicio Almuerzo (HH:MM):", al_i)
        self.entry_ad = self.crear_input("Duración Almuerzo (min):", str(al_d))

        ctk.CTkFrame(self, height=10, fg_color="transparent").pack() # Separador
        
        self.entry_pwd = self.crear_input("Contraseña Admin:", pwd)

        ctk.CTkFrame(self, height=10, fg_color="transparent").pack() # Separador
        
        # Sección de días laborables
        ctk.CTkLabel(self, text="Días Laborables", font=("Arial", 14, "bold")).pack(pady=10)
        
        dias_frame = ctk.CTkFrame(self, fg_color="transparent")
        dias_frame.pack(pady=5)
        
        self.dias_laborables = {}
        dias_nombres = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        dias_valores = [lunes, martes, miercoles, jueves, viernes, sabado, domingo]
        
        for i, (dia_nombre, dia_valor) in enumerate(zip(dias_nombres, dias_valores)):
            var = ctk.BooleanVar(value=bool(dia_valor))
            check = ctk.CTkCheckBox(dias_frame, text=dia_nombre, variable=var)
            if i < 4:
                check.grid(row=0, column=i, padx=5)
            else:
                check.grid(row=1, column=i-4, padx=5)
            self.dias_laborables[dia_nombre] = var

        self.label_mensual = ctk.CTkLabel(self, text="", font=("Arial", 16, "bold"), text_color="#3498db")
        self.label_mensual.pack(pady=10)

        # Botón Guardar con color #2742F5
        ctk.CTkButton(self, text="💾 GUARDAR Y REGENERAR", fg_color="#2742F5", hover_color="#1A2EAB", command=self.guardar).pack(pady=10)
        self.recalcular_en_vivo()

    def crear_input(self, txt, def_val):
        f = ctk.CTkFrame(self, fg_color="transparent")
        f.pack(pady=5)
        ctk.CTkLabel(f, text=txt, width=180).pack(side="left")
        e = ctk.CTkEntry(f)
        e.insert(0, def_val)
        e.pack(side="left")
        e.bind("<KeyRelease>", lambda event: self.recalcular_en_vivo())
        return e

    def recalcular_en_vivo(self):
        try:
            v, s, d = float(self.entry_v.get() or 0), int(self.entry_s.get() or 0), int(self.entry_d.get() or 0)
            self.label_mensual.configure(text=f"Proyección Mensual: {v*s*d*4:,.2f} €")
        except: pass

    def guardar(self):
        try:
            vals = (float(self.entry_v.get()), int(self.entry_s.get()), int(self.entry_d.get()), self.entry_hi.get(), self.entry_ai.get(), int(self.entry_ad.get()), int(self.entry_ds.get()), self.entry_pwd.get(),
                    int(self.dias_laborables["Lunes"].get()),
                    int(self.dias_laborables["Martes"].get()),
                    int(self.dias_laborables["Miércoles"].get()),
                    int(self.dias_laborables["Jueves"].get()),
                    int(self.dias_laborables["Viernes"].get()),
                    int(self.dias_laborables["Sábado"].get()),
                    int(self.dias_laborables["Domingo"].get()))
            conn = sqlite3.connect("gestion_slots.db")
            conn.cursor().execute("UPDATE ajustes SET valor_slot=?, slots_diarios=?, dias_semana=?, hora_inicio=?, inicio_almuerzo=?, duracion_almuerzo=?, duracion_slot=?, password=?, lunes=?, martes=?, miercoles=?, jueves=?, viernes=?, sabado=?, domingo=? WHERE id=1", vals)
            conn.commit()
            conn.close()
            inicializar_db(force_regenerate=True)
        except Exception as e: 
            print(f"Error al guardar: {e}")