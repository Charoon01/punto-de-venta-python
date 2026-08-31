import sqlite3
from datetime import datetime

class Database:
    def __init__(self, db_name='pos_database.db'):
        self.db_name = db_name
        self.connect()
        self.create_tables()
    
    def connect(self):
        """Conectar a la base de datos"""
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
    
    def create_tables(self):
        """Crear las tablas necesarias"""
        # Tabla de máquinas
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS maquinas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                descripcion TEXT,
                estado TEXT NOT NULL,
                cantidad INTEGER NOT NULL,
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabla de movimientos de inventario
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS movimientos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                maquina_id INTEGER NOT NULL,
                tipo TEXT NOT NULL,
                cantidad INTEGER NOT NULL,
                precio_unitario REAL,
                fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                descripcion TEXT,
                FOREIGN KEY (maquina_id) REFERENCES maquinas(id)
            )
        ''')
        
        # Tabla de entregas de máquinas
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS entregas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                numero_factura TEXT UNIQUE,
                fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                total REAL NOT NULL,
                dueño TEXT,
                localia TEXT,
                estado_entrega TEXT DEFAULT 'completada'
            )
        ''')
        
        # Tabla de detalles de entregas
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS detalles_entregas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                entrega_id INTEGER NOT NULL,
                maquina_id INTEGER NOT NULL,
                cantidad INTEGER NOT NULL,
                estado_maquina TEXT NOT NULL,
                subtotal REAL NOT NULL,
                FOREIGN KEY (entrega_id) REFERENCES entregas(id),
                FOREIGN KEY (maquina_id) REFERENCES maquinas(id)
            )
        ''')
        
        self.conn.commit()
    
    def agregar_maquina(self, nombre, descripcion, estado, cantidad):
        """Agregar nueva máquina"""
        try:
            self.cursor.execute('''
                INSERT INTO maquinas (nombre, descripcion, estado, cantidad)
                VALUES (?, ?, ?, ?)
            ''', (nombre, descripcion, estado, cantidad))
            self.conn.commit()
            return True, "Máquina agregada exitosamente"
        except Exception as e:
            return False, str(e)
    
    def obtener_maquinas(self):
        """Obtener todas las máquinas"""
        self.cursor.execute('SELECT * FROM maquinas')
        return self.cursor.fetchall()
    
    def obtener_maquina(self, maquina_id):
        """Obtener una máquina específica"""
        self.cursor.execute('SELECT * FROM maquinas WHERE id = ?', (maquina_id,))
        return self.cursor.fetchone()
    
    def actualizar_maquina(self, maquina_id, nombre, descripcion, estado, cantidad):
        """Actualizar información de la máquina"""
        try:
            self.cursor.execute('''
                UPDATE maquinas 
                SET nombre = ?, descripcion = ?, estado = ?, cantidad = ?
                WHERE id = ?
            ''', (nombre, descripcion, estado, cantidad, maquina_id))
            self.conn.commit()
            return True, "Máquina actualizada"
        except Exception as e:
            return False, str(e)
    
    def eliminar_maquina(self, maquina_id):
        """Eliminar una máquina"""
        try:
            self.cursor.execute('DELETE FROM maquinas WHERE id = ?', (maquina_id,))
            self.conn.commit()
            return True, "Máquina eliminada"
        except Exception as e:
            return False, str(e)
    
    def registrar_movimiento(self, maquina_id, tipo, cantidad, precio_unitario=0, descripcion=''):
        """Registrar movimiento de inventario (entrada/mantenimiento)"""
        try:
            self.cursor.execute('''
                INSERT INTO movimientos (maquina_id, tipo, cantidad, precio_unitario, descripcion)
                VALUES (?, ?, ?, ?, ?)
            ''', (maquina_id, tipo, cantidad, precio_unitario, descripcion))
            self.conn.commit()
            return True, "Movimiento registrado"
        except Exception as e:
            return False, str(e)
    
    def obtener_movimientos(self):
        """Obtener historial de movimientos"""
        self.cursor.execute('''
            SELECT m.id, ma.nombre, m.tipo, m.cantidad, m.precio_unitario, m.fecha, m.descripcion
            FROM movimientos m
            JOIN maquinas ma ON m.maquina_id = ma.id
            ORDER BY m.fecha DESC
        ''')
        return self.cursor.fetchall()
    
    def crear_entrega(self, numero_factura, dueño, localia, detalles):
        """Crear una nueva entrega de máquina"""
        try:
            total = sum(detalle['cantidad'] * 1 for detalle in detalles)  # Simplificado
            
            self.cursor.execute('''
                INSERT INTO entregas (numero_factura, dueño, localia, total)
                VALUES (?, ?, ?, ?)
            ''', (numero_factura, dueño, localia, total))
            
            entrega_id = self.cursor.lastrowid
            
            # Insertar detalles de entrega
            for detalle in detalles:
                self.cursor.execute('''
                    INSERT INTO detalles_entregas (entrega_id, maquina_id, cantidad, estado_maquina, subtotal)
                    VALUES (?, ?, ?, ?, ?)
                ''', (entrega_id, detalle['maquina_id'], detalle['cantidad'], 
                      detalle['estado_maquina'], detalle['cantidad']))
                
                # Actualizar cantidad de máquina
                self.cursor.execute('''
                    UPDATE maquinas 
                    SET cantidad = cantidad - ?
                    WHERE id = ?
                ''', (detalle['cantidad'], detalle['maquina_id']))
                
                # Registrar movimiento
                self.cursor.execute('''
                    INSERT INTO movimientos (maquina_id, tipo, cantidad, descripcion)
                    VALUES (?, 'ENTREGA', ?, ?)
                ''', (detalle['maquina_id'], detalle['cantidad'], f"Entrega #{numero_factura}"))
            
            self.conn.commit()
            return True, f"Entrega creada: #{numero_factura}"
        except Exception as e:
            self.conn.rollback()
            return False, str(e)
    
    def obtener_entregas(self):
        """Obtener historial de entregas"""
        self.cursor.execute('''
            SELECT id, numero_factura, fecha, total, dueño, localia, estado_entrega
            FROM entregas
            ORDER BY fecha DESC
        ''')
        return self.cursor.fetchall()
    
    def obtener_detalles_entrega(self, entrega_id):
        """Obtener detalles de una entrega específica"""
        self.cursor.execute('''
            SELECT ma.nombre, de.cantidad, de.estado_maquina, de.subtotal
            FROM detalles_entregas de
            JOIN maquinas ma ON de.maquina_id = ma.id
            WHERE de.entrega_id = ?
        ''', (entrega_id,))
        return self.cursor.fetchall()
    
    def obtener_reporte_inventario(self):
        """Obtener reporte de inventario actual"""
        self.cursor.execute('''
            SELECT id, nombre, cantidad, estado, (cantidad) as valor_total
            FROM maquinas
            ORDER BY nombre
        ''')
        return self.cursor.fetchall()
    
    def obtener_reporte_entregas(self, fecha_inicio=None, fecha_fin=None):
        """Obtener reporte de entregas de máquinas por período"""
        if fecha_inicio and fecha_fin:
            self.cursor.execute('''
                SELECT numero_factura, fecha, dueño, localia, total
                FROM entregas
                WHERE DATE(fecha) BETWEEN ? AND ?
                ORDER BY fecha DESC
            ''', (fecha_inicio, fecha_fin))
        else:
            self.cursor.execute('''
                SELECT numero_factura, fecha, dueño, localia, total
                FROM entregas
                ORDER BY fecha DESC
            ''')
        return self.cursor.fetchall()
    
    def obtener_reporte_movimientos(self, fecha_inicio=None, fecha_fin=None):
        """Obtener reporte de movimientos de inventario"""
        if fecha_inicio and fecha_fin:
            self.cursor.execute('''
                SELECT m.id, ma.nombre, m.tipo, m.cantidad, m.precio_unitario, m.fecha, m.descripcion
                FROM movimientos m
                JOIN maquinas ma ON m.maquina_id = ma.id
                WHERE DATE(m.fecha) BETWEEN ? AND ?
                ORDER BY m.fecha DESC
            ''', (fecha_inicio, fecha_fin))
        else:
            self.cursor.execute('''
                SELECT m.id, ma.nombre, m.tipo, m.cantidad, m.precio_unitario, m.fecha, m.descripcion
                FROM movimientos m
                JOIN maquinas ma ON m.maquina_id = ma.id
                ORDER BY m.fecha DESC
            ''')
        return self.cursor.fetchall()
    
    def close(self):
        """Cerrar conexión con la base de datos"""
        self.conn.close()
