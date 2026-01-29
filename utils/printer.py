import customtkinter as ctk
from datetime import datetime
import sqlite3
from escpos.printer import Network
from escpos.exceptions import Error
from escpos.exceptions import TextError
from utils.Alert import show_ctk_alert

def imprimir_ticket_real(id_slot, hora, fecha_obj):
    # --- CONFIGURACIÓN DE LA IMPRESORA ---
    # Cambia la IP por la de tu impresora. Si es USB usa: Usb(0x04b8, 0x0202)
    IP_IMPRESORA = "192.168.1.100" 
    PORT=9100
    TIMEOUT=3 # Segundos
    
    try:
        # 1. ABRIR Y ENVIAR A IMPRESORA (Auto-cierre con 'with')
        with Network(IP_IMPRESORA, PORT, TIMEOUT) as p:
            # Inicializar y Centrar
            p.set(align='center')
            p.text("--- TICKET DE TURNO ---\n\n")
            
            # Contenido del ticket
            p.set(align='left')
            p.text(f"HORA:  {hora}\n")
            p.text(f"FECHA: {fecha_obj.strftime('%d/%m/%Y')}\n\n")
            
            p.set(align='center')
            p.text("Gracias por su visita.\n\n")
            
            # 2. CORTAR PAPEL (Cierre implícito al salir del 'with')
            p.cut()
            print(f" [OK] Ticket impreso para el slot {id_slot}")

        # 3. ACTUALIZAR BASE DE DATOS
        # Solo actualizamos si la impresión no dio error
        conn = sqlite3.connect("gestion_slots.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE agenda SET estado = 1 WHERE id = ?", (id_slot,))
        conn.commit()
        conn.close()

    except Error as e:
        show_ctk_alert(f"Error de Impresora", f"Error: Impresora no encontrada. Verifique la conexión y la IP {e}")
    except TextError as e:
        show_ctk_alert(f"Error de Impresora", f"Error al imprimir caracteres en la impresora {e}")        
    except TimeoutError as e:
        show_ctk_alert(f"Error de Impresora", f"No se pudo conectar con la Epson {e}")
    except Exception as e:
        show_ctk_alert(f"Error de Impresora", f"Error en la impresión {e}")
    finally:
        if p.is_online():
            p.close()

