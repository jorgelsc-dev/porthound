import threading
import sqlite3
import time

memory_db = sqlite3.connect(":memory:", check_same_thread=False)
memory_cursor = memory_db.cursor()

memory_cursor.execute('''
    CREATE TABLE IF NOT EXISTS worker_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        host TEXT,
        port INTEGER,
        created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')
memory_db.commit()

class WorkerThread(threading.Thread):
    def __init__(self):
        super().__init__(daemon=True)
        self.running = True
        self.condition = threading.Condition()
    
    def run(self):
        while self.running:
            try:
                print("Ejecutando tarea...")
                host = "192.168.1.1"
                port = 80
                with memory_db:
                    memory_cursor.execute("INSERT INTO worker_data (host, port) VALUES (?, ?)", (host, port))
                with self.condition:
                    self.condition.wait(4)  # Espera 4 segundos
            except Exception as e:
                print(f"Error interno: {e}, pero el hilo sigue ejecutándose.")
    
    def stop(self):
        self.running = False
        with self.condition:
            self.condition.notify_all()



if __name__ == '__main__':
    print('Hello')
    worker_thread = WorkerThread()
    worker_thread.start()
    try:
        while True:
            with worker_thread.condition:
                worker_thread.condition.wait(1)
    except KeyboardInterrupt:
        print("Deteniendo el programa...")
        worker_thread.stop()
        worker_thread.join()
        memory_db.close()