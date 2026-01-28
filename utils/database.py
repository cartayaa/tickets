import sqlite3
from datetime import datetime, timedelta

def inicializar_db(force_regenerate=False):
    conn = sqlite3.connect("gestion_slots.db")
    cursor = conn.cursor()

    # Tabla de configuración con campos de almuerzo y días laborables
    # print('Creando tabla de ajustes')
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ajustes (
            id INTEGER PRIMARY KEY,
            valor_slot REAL,
            slots_diarios INTEGER,
            dias_semana INTEGER,
            hora_inicio TEXT DEFAULT ('09:00'),
            inicio_almuerzo TEXT DEFAULT ('14:30'),
            duracion_almuerzo INTEGER default 60,
            duracion_slot INTEGER DEFAULT 35,
            password TEXT DEFAULT ('1234'),
            lunes INTEGER DEFAULT 0,
            martes INTEGER DEFAULT 0,
            miercoles INTEGER DEFAULT 0,
            jueves INTEGER DEFAULT 0,
            viernes INTEGER DEFAULT 0,
            sabado INTEGER DEFAULT 0,
            domingo INTEGER DEFAULT 0
        )
    """)

    # print('Creando tabla de agendas')
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS agenda (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            hora TEXT,
            estado INTEGER DEFAULT 0,
            fecha_actualizacion TEXT
        )
    """)

    # Valores iniciales
    cursor.execute("SELECT COUNT(*) FROM ajustes WHERE id = 1")
    if cursor.fetchone()[0] == 0:
        # print('Insertando valores iniciales en ajustes')
        cursor.execute("""
            INSERT INTO ajustes(id, 
                                valor_slot, 
                                slots_diarios, 
                                dias_semana, 
                                hora_inicio, 
                                inicio_almuerzo, 
                                duracion_almuerzo, 
                                duracion_slot, 
                                password) 
            VALUES (1, 6.0, 16, 6, '09:00', '14:00', 60, 35, '1234')
        """)
        conn.commit()


    if force_regenerate:
        cursor.execute("DELETE FROM agenda")
        conn.commit()

    conn.close()
    
    # Asegura que los slots para el día de hoy existan al iniciar
    get_slots_for_date(datetime.now().date())

def cargar_ajustes():
    conn = sqlite3.connect("gestion_slots.db")
    cursor = conn.cursor()    
    cursor.execute("SELECT valor_slot, slots_diarios, dias_semana, hora_inicio, inicio_almuerzo, duracion_almuerzo, duracion_slot, password, lunes, martes, miercoles, jueves, viernes, sabado, domingo FROM ajustes WHERE id = 1")
    datos = cursor.fetchone()
    conn.close()
    print(f"Cargar ajustes: {datos}")
    return datos

def get_slots_for_date(date_obj):
    conn = sqlite3.connect("gestion_slots.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    fecha_str = date_obj.strftime("%Y-%m-%d")

    # print(f"Obteniendo slots para la fecha: {fecha_str}")

    cursor.execute("SELECT * FROM ajustes WHERE id=1")
    ajustes = cursor.fetchone()
    if not ajustes:
        conn.close()
        return []
    
    n_slots_config = ajustes['slots_diarios']

    cursor.execute("SELECT COUNT(*) FROM agenda WHERE fecha_actualizacion = ?", (fecha_str,))
    n_slots_actuales = cursor.fetchone()[0]

    # Si no existen slots para este día, o la configuración ha cambiado, (re)generarlos.
    if n_slots_actuales != n_slots_config:
        cursor.execute("DELETE FROM agenda WHERE fecha_actualizacion = ?", (fecha_str,))
        
        dias_laborables = [ajustes['lunes'], ajustes['martes'], ajustes['miercoles'], ajustes['jueves'], ajustes['viernes'], ajustes['sabado'], ajustes['domingo']]
        dia_semana = date_obj.weekday()
        es_dia_laborable = (dias_laborables[dia_semana] or 0) == 1
        
        if es_dia_laborable:
            h_inicio, h_almuerzo, d_almuerzo, d_slot = ajustes['hora_inicio'], ajustes['inicio_almuerzo'], ajustes['duracion_almuerzo'], ajustes['duracion_slot']
            estado_slot = 0
            hora_actual = datetime.strptime(h_inicio, "%H:%M")
            inicio_alm = datetime.strptime(h_almuerzo, "%H:%M")
            fin_alm = inicio_alm + timedelta(minutes=d_almuerzo)
            
            slots_creados = 0
            while slots_creados < n_slots_config:
                if inicio_alm <= hora_actual < fin_alm:
                    hora_actual = fin_alm
                    continue
                
                hora_str = hora_actual.strftime("%H:%M")
                cursor.execute("INSERT INTO agenda (hora, estado, fecha_actualizacion) VALUES (?, ?, ?)", (hora_str, estado_slot, fecha_str))
                hora_actual += timedelta(minutes=d_slot)
                slots_creados += 1
        conn.commit()

    cursor.execute("SELECT id, hora, estado FROM agenda WHERE fecha_actualizacion = ? ORDER BY hora", (fecha_str,))
    slots = cursor.fetchall()
    conn.close()
    return [tuple(row) for row in slots]

def get_next_working_days(start_date, num_days_to_find):
    conn = sqlite3.connect("gestion_slots.db")
    cursor = conn.cursor()
    cursor.execute("SELECT lunes, martes, miercoles, jueves, viernes, sabado, domingo FROM ajustes WHERE id = 1")
    dias_laborables_flags = cursor.fetchone()
    conn.close()
    if not dias_laborables_flags: return []

    working_days, current_date, days_checked = [], start_date, 0
    while len(working_days) < num_days_to_find and days_checked < 365:
        if (dias_laborables_flags[current_date.weekday()] or 0) == 1:
            working_days.append(current_date)
        current_date += timedelta(days=1)
        days_checked += 1
    return working_days

def actualizar_estado_slot(slot_id, nuevo_estado):
    conn = sqlite3.connect("gestion_slots.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE agenda SET estado = ? WHERE id = ?", (nuevo_estado, slot_id))
    conn.commit()
    conn.close()