import psycopg2
from psycopg2 import sql

# --- CONFIGURACIÓN ---
DB_CONFIG = {
    "host": "localhost",
    "database": "registro_civil",
    "user": "postgres",
    "password": "P0str3s24**",  # <--- ¡NO OLVIDES PONER TU CONTRASEÑA!
    "port": "5432"
}

def conectar_db():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"❌ Error fatal conectando a la base de datos: {e}")
        return None

# --- FUNCIONES DEL SISTEMA ---
# ... (Los imports y DB_CONFIG quedan igual) ...

def registrar_prestamo_web(codigo_empleado, codigo_barras_doc):
    conn = conectar_db()
    if not conn: return "Error de conexión"

    try:
        cursor = conn.cursor()
        
        # PARTE 1: Validar Usuario
        cursor.execute("SELECT id FROM usuarios WHERE codigo_empleado = %s AND activo = TRUE", (codigo_empleado,))
        usuario_data = cursor.fetchone()
        if not usuario_data:
            raise ValueError("Usuario no encontrado.")
        usuario_id = usuario_data[0]

        # PARTE 2: Validar Documento
        cursor.execute("SELECT id, estado FROM documentos WHERE codigo_barras = %s", (codigo_barras_doc,))
        doc_data = cursor.fetchone()
        if not doc_data:
            raise ValueError("Documento no existe.")
        
        doc_id, estado_actual = doc_data
        
        # Aquí está el guardián. Si el estado no cambió antes, esto te dejará pasar siempre.
        if estado_actual != 'DISPONIBLE':
            raise ValueError(f"⚠️ El documento ya está prestado (Estado: {estado_actual})")

        # PARTE 3: Crear el registro en el historial
        query_prestamo = """
            INSERT INTO prestamos (usuario_id, documento_id, fecha_limite)
            VALUES (%s, %s, CURRENT_TIMESTAMP + INTERVAL '24 hours')
        """
        cursor.execute(query_prestamo, (usuario_id, doc_id))

        # PARTE 4: CAMBIAR EL ESTADO DEL DOCUMENTO (¡ESTA ES LA CLAVE!)
        # Si esta línea falta, el libro siempre parecerá disponible.
        cursor.execute("UPDATE documentos SET estado = 'PRESTADO' WHERE id = %s", (doc_id,)) # <--- ¡OJO AQUÍ!

        conn.commit()
        return f"✅ ÉXITO: Préstamo registrado para {codigo_empleado}"

    except ValueError as ve:
        conn.rollback()
        return f"{ve}"
    except Exception as e:
        conn.rollback()
        return f"❌ Error Técnico: {e}"
    finally:
        if conn:
            cursor.close()
            conn.close()

def registrar_devolucion_web(codigo_barras_doc):
    conn = conectar_db()
    if not conn: return "Error de conexión con base de datos"

    try:
        cursor = conn.cursor()
        
        # 1. Verificar estado actual del libro
        cursor.execute("SELECT id, estado FROM documentos WHERE codigo_barras = %s", (codigo_barras_doc,))
        doc_data = cursor.fetchone()
        
        if not doc_data:
            raise ValueError("Documento no encontrado en el inventario.")
            
        doc_id, estado_actual = doc_data
        
        # Validación: No puedes devolver algo que ya está en el estante
        if estado_actual == 'DISPONIBLE':
            raise ValueError(f"⚠️ El documento ya figura como DISPONIBLE. No se requiere devolución.")

        # 2. Cerrar el préstamo en el historial (Poner fecha de devolución)
        query_cierre = """
            UPDATE prestamos 
            SET fecha_devolucion = CURRENT_TIMESTAMP 
            WHERE documento_id = %s AND fecha_devolucion IS NULL
        """
        cursor.execute(query_cierre, (doc_id,))
        
        # Validación de integridad: ¿Realmente se cerró algo?
        if cursor.rowcount == 0:
            raise ValueError("Inconsistencia: El libro dice PRESTADO, pero no encontré un registro abierto en el historial.")

        # 3. Liberar el documento en el inventario (Ponerlo DISPONIBLE)
        cursor.execute("UPDATE documentos SET estado = 'DISPONIBLE' WHERE id = %s", (doc_id,))

        conn.commit()
        return f"✅ DEVOLUCIÓN EXITOSA: El documento {codigo_barras_doc} ha sido retornado."

    except ValueError as ve:
        conn.rollback()
        return f"{ve}"
    except Exception as e:
        conn.rollback()
        return f"❌ Error Técnico: {e}"
    finally:
        if conn:
            cursor.close()
            conn.close()

def obtener_prestamos_activos():
    conn = conectar_db()
    if not conn: return []
    
    lista = []
    try:
        cursor = conn.cursor()
        # Usamos la VISTA que creamos en SQL (es más rápido y limpio)
        cursor.execute("SELECT funcionario, documento, fecha_prestamo FROM vista_prestamos_activos")
        lista = cursor.fetchall() # Nos devuelve una lista de tuplas [(Juan, Libro1, Fecha), (Maria, Libro2, Fecha)...]
    except Exception as e:
        print(f"Error al leer historial: {e}")
    finally:
        if conn: cursor.close(); conn.close()
    
    return lista

