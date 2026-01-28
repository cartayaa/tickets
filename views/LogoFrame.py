import customtkinter as ctk
from PIL import Image

class LogoFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="white", **kwargs)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        try:
            logo_image = ctk.CTkImage(Image.open("./images/istockphoto.jpg"), size=(600, 350))
            logo_label = ctk.CTkLabel(self, image=logo_image, text="")
            logo_label.grid(row=0, column=0, padx=20, pady=20)
        except FileNotFoundError:
            logo_label = ctk.CTkLabel(self, text="Logo no encontrado.\nAsegúrese que 'istockphoto.jpg' está en la carpeta.", font=("Arial", 16), text_color="black")
            logo_label.grid(row=0, column=0, padx=20, pady=20)