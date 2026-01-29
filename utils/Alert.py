import customtkinter as ctk

def show_ctk_alert(titulo, mensaje):
    alert = ctk.CTkToplevel()
    alert.title(titulo)
    alert.geometry("300x100")
    alert.attributes("-topmost", True)
    alert.resizable(False, False) # Bloquea el cambio de tamaño en X e Y

    # Texto
    label = ctk.CTkLabel(alert, text=mensaje, pady=20)
    label.pack()
    
    # Botón único
    btn = ctk.CTkButton(alert, text="OK", command=alert.destroy)
    btn.pack(pady=10)
    
    # Esto hace que la app espere a que cierres el aviso (como el InputDialog)
    alert.grab_set()