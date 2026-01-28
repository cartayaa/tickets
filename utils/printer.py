from datetime import datetime
import sqlite3
from escpos.printer import Network # O usa Usb si es por cable

def imprimir_ticket_real(id_slot, hora, fecha_obj):
    # --- CONFIGURACIÓN DE LA IMPRESORA ---
    # Cambia la IP por la de tu impresora. Si es USB usa: Usb(0x04b8, 0x0202)
    IP_IMPRESORA = "192.168.1.100" 
    
    try:
        # 1. ABRIR Y ENVIAR A IMPRESORA (Auto-cierre con 'with')
        with Network(IP_IMPRESORA) as p:
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

    except Exception as e:
        print(f" [!] Error en el proceso de impresión/DB: {e}")
    finally:
        # 3. ACTUALIZAR BASE DE DATOS
        # Solo actualizamos si la impresión no dio error
        conn = sqlite3.connect("gestion_slots.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE agenda SET estado = 1 WHERE id = ?", (id_slot,))
        conn.commit()
        conn.close()
        print(" [OK] Base de datos actualizada: Estado Ocupado (1)")

# Ejemplo de uso:
# imprimir_ticket_real(5, "10:30", datetime.now())

