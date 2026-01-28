import customtkinter as ctk
from utils.database import inicializar_db, cargar_ajustes
from views import LogoFrame, DashboardFrame, AgendaFrame, DisponibilidadFrame, AjustesFrame

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Tickets con Almuerzo")
        self.geometry("950x650")
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.sidebar = ctk.CTkFrame(self, width=200)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        ctk.CTkFrame(self.sidebar, height=20, fg_color="transparent").pack()

        btns = [("Inicio", LogoFrame),                
                ("Dashboard", DashboardFrame), 
                ("Tickets", AgendaFrame), 
                ("Disponibilidad", DisponibilidadFrame), 
                ("Ajustes", AjustesFrame)] 
        
        for name, frame in btns:
            # Botones del menú lateral con color #5D1089
            cmd = lambda f=frame: self.show_frame(f)
            
            if name == "Ajustes":
                cmd = self.verificar_acceso_ajustes
                
            ctk.CTkButton(self.sidebar, text=name, fg_color="#2B7AE3", hover_color="#1A2EAB", command=cmd).pack(padx=10, pady=5, fill="x")
        
        # Selector de modo claro/oscuro en el menú
        self.crear_selector_tema()

        self.container = None
        self.show_frame(LogoFrame)

    def show_frame(self, frame_class):
        if self.container: self.container.destroy()
        self.container = frame_class(self)
        self.container.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

    def crear_selector_tema(self):
        ctk.CTkLabel(self.sidebar, text="Apariencia", anchor="center").pack(padx=10, pady=(20, 0), fill="x")
        mode_menu = ctk.CTkOptionMenu(self.sidebar, values=["Claro", "Oscuro", "Sistema"],
                                      command=self.change_appearance_mode_event,
                                      fg_color="#2B7AE3", button_color="#2B7AE3", button_hover_color="#2B7AE3")
        mode_menu.pack(padx=10, pady=5, fill="x")

        # Establecer valor por defecto
        mode_map_inv = {"light": "Claro", "dark": "Oscuro", "system": "Sistema"}
        current_mode = ctk.get_appearance_mode().lower()
        mode_menu.set(mode_map_inv.get(current_mode, "Sistema"))

    def change_appearance_mode_event(self, new_appearance_mode: str):
        mode_map = {"Claro": "Light", "Oscuro": "Dark", "Sistema": "System"}
        ctk.set_appearance_mode(mode_map.get(new_appearance_mode, "System"))

    def verificar_acceso_ajustes(self):
        dialog = ctk.CTkInputDialog(text="Ingrese Contraseña de Administrador:", title="Seguridad")
        pwd_ingresada = dialog.get_input()
        
        if pwd_ingresada:
            datos = cargar_ajustes()
            # print(f"Datos cargados: {datos}")
            pwd_real = datos[7]
            if pwd_ingresada == pwd_real:
                self.show_frame(AjustesFrame)
            else:
                print("Acceso denegado: Contraseña incorrecta")
                # Opcional: Podrías mostrar un mensaje de error visual si lo deseas

if __name__ == "__main__":
    inicializar_db()
    app = App()
    app.mainloop()