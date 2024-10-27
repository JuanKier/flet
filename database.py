import sqlite3

# Función para conectar a la base de datos
def connect():
    return sqlite3.connect("appointments.db")

# Función para crear tablas
def create_tables():
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT NOT NULL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS services (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price REAL NOT NULL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS appointments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER,
                date TEXT NOT NULL,
                time TEXT NOT NULL,
                service_id INTEGER,  -- Relaciona con la tabla services
                status TEXT NOT NULL DEFAULT 'Pendiente',
                is_deleted BOOLEAN DEFAULT FALSE,  -- Nueva columna para marcar como eliminada
                FOREIGN KEY (customer_id) REFERENCES customers (id),
                FOREIGN KEY (service_id) REFERENCES services (id)
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS service_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER,
                service_id INTEGER,
                appointment_date TEXT,
                appointment_time TEXT,
                FOREIGN KEY (customer_id) REFERENCES customers (id),
                FOREIGN KEY (service_id) REFERENCES services (id)
            )
        ''')
        conn.commit()

# Función para insertar en el historial de servicios
def insert_service_history(customer_id, service_id, appointment_date, appointment_time):
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO service_history (customer_id, service_id, appointment_date, appointment_time)
            VALUES (?, ?, ?, ?)
        ''', (customer_id, service_id, appointment_date, appointment_time))
        conn.commit()

# Función para verificar la estructura de la tabla appointments
def check_table_structure():
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute('PRAGMA table_info(appointments);')
        columns = cursor.fetchall()
        for column in columns:
            print(column)

# Función para insertar un nuevo servicio
def insert_service(name, price):
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO services (name, price) VALUES (?, ?)", (name, price))
        conn.commit()

# Función para eliminar un servicio por su ID
def delete_service(service_id):
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM services WHERE id = ?", (service_id,))
        conn.commit()

# Función para actualizar un servicio
def update_service(service_id, name, price):
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE services SET name = ?, price = ? WHERE id = ?", (name, price, service_id))
        conn.commit()

# Función para obtener todos los servicios
def get_all_services():
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM services')
        return cursor.fetchall()

# Función para obtener el precio de un servicio
def get_service_price(service_name):
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT price FROM services WHERE name = ?', (service_name,))
        result = cursor.fetchone()
        return result[0] if result else None

# Función para insertar una cita
def insert_appointment(customer_id, date, time, service_id, status):
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO appointments (customer_id, date, time, service_id, status) VALUES (?, ?, ?, ?, ?)',
                       (customer_id, date, time, service_id, status))
        conn.commit()

# Función para obtener todas las citas
def get_all_appointments():
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute(''' 
            SELECT a.id, c.name, c.phone, a.date, a.time, s.name, a.status 
            FROM appointments a 
            JOIN customers c ON a.customer_id = c.id 
            JOIN services s ON a.service_id = s.id 
            WHERE a.is_deleted = FALSE  -- Solo cargar citas no eliminadas
        ''')
        return cursor.fetchall()

# Función para actualizar una cita
def update_appointment(appointment_id, customer_id, date, time, service_id, status):
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE appointments
            SET customer_id = ?, date = ?, time = ?, service_id = ?, status = ?
            WHERE id = ?
        ''', (customer_id, date, time, service_id, status, appointment_id))
        conn.commit()

# Función para eliminar una cita (marcar como eliminada)
def delete_appointment(appointment_id):
    with connect() as conn:
        cursor = conn.cursor()
        # Marcar la cita como eliminada en lugar de eliminarla completamente
        cursor.execute('UPDATE appointments SET is_deleted = 1 WHERE id = ?', (appointment_id,))
        conn.commit()

# Función para limpiar citas (marcar como eliminadas)
def clear_appointments(date):
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute('UPDATE appointments SET is_deleted = TRUE WHERE date = ?', (date,))
        conn.commit()

# Función para insertar en el historial de servicios
def insert_service_history(customer_id, service_id, appointment_date, appointment_time):
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO service_history (customer_id, service_id, appointment_date, appointment_time)
            VALUES (?, ?, ?, ?)
        ''', (customer_id, service_id, appointment_date, appointment_time))
        conn.commit()

# Función para obtener el historial de servicios de un cliente
def get_service_history(customer_id):
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT s.name, sh.appointment_date, sh.appointment_time
            FROM service_history sh
            JOIN services s ON sh.service_id = s.id
            WHERE sh.customer_id = ?
        ''', (customer_id,))
        return cursor.fetchall()

# Función para eliminar un cliente por su ID
def delete_customer(customer_id):
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM customers WHERE id = ?", (customer_id,))
        conn.commit()

# Función para obtener todos los clientes
def get_all_customers():
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM customers')
        return cursor.fetchall()
    
# Función para encontrar un cliente por nombre y teléfono
def find_customer(name, phone):
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM customers WHERE name = ? AND phone = ?', (name, phone))
        return cursor.fetchone()
    
def insert_or_update_customer(name, phone, customer_id=None):
    with connect() as conn:
        cursor = conn.cursor()
        if customer_id is not None:
            cursor.execute("UPDATE customers SET name = ?, phone = ? WHERE id = ?", (name, phone, customer_id))  # No se puede editar el teléfono
        else:
            cursor.execute("INSERT INTO customers (name, phone) VALUES (?, ?)", (name, phone))
        conn.commit()

def get_customer_phone(name):
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT phone FROM customers WHERE name = ?", (name,))
        result = cursor.fetchone()
        return result[0] if result else None
    
def find_customer_by_name(name):
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM customers WHERE name = ?', (name,))
        return cursor.fetchone()

def find_customer_by_id(customer_id):
    # Conectar a la base de datos y buscar el cliente por ID
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM customers WHERE id=?", (customer_id,))
        return cursor.fetchone()
    
def clear_service_history(customer_id):
    # Implementa la lógica para eliminar el historial del cliente
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM service_history WHERE customer_id = ?", (customer_id,))
        return cursor.fetchone()