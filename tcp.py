import socket
import threading
import sqlite3
import base64

def init_db():
    """Inicializa la base de datos y crea la tabla si no existe"""
    conn = sqlite3.connect('tcp_scans.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS scan_tcp (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data_base64 TEXT UNIQUE
        )
    ''')
    conn.commit()
    conn.close()

def handle_packet(data, addr):
    """Maneja los paquetes y guarda en base de datos"""
    print(f"\nPaquete recibido desde {addr[0]}:{addr[1]}")
    print("Contenido (bytes):", data)
    
    try:
        print("Contenido (texto):", data.decode('utf-8', errors='replace'))
    except Exception as e:
        print("Error al decodificar:", e)
    
    # Convertir a base64
    data_b64 = base64.b64encode(data).decode('utf-8')
    
    # Guardar en base de datos
    conn = sqlite3.connect('tcp_scans.db')
    try:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO scan_tcp (data_base64) VALUES (?)', (data_b64,))
        conn.commit()
    except sqlite3.IntegrityError:
        print("Dato duplicado, no se guardará")
    except Exception as e:
        print("Error en la base de datos:", e)
    finally:
        conn.close()

def tcp_server():
    """Inicia el servidor TCP en el puerto 80"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        sock.bind(('', 80))
        sock.listen(5)  # Permitir hasta 5 conexiones simultáneas
    except PermissionError:
        print("Error: Necesitas permisos de administrador para usar el puerto 80")
        return
    
    print("Escuchando en el puerto 80 (TCP)...")
    
    while True:
        client_socket, addr = sock.accept()  # Aceptar una conexión
        print(f"Conexión establecida con {addr[0]}:{addr[1]}")
        
        # Leer los datos de la conexión
        data = client_socket.recv(1024)  # Puedes aumentar el tamaño del buffer según sea necesario
        if data:
            thread = threading.Thread(target=handle_packet, args=(data, addr))
            thread.start()
        
        client_socket.close()  # Cerrar la conexión después de manejarla

if __name__ == "__main__":
    init_db()  # Inicializar base de datos al inicio
    tcp_server()
