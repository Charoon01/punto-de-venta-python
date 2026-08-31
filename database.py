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
        # Tabla de productos
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS productos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                descripcion TEXT,
                precio REAL NOT NULL,
                cantidad INTEGER NOT NULL,
                codigo_barras TEXT UNIQUE,
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabla de movimientos de inventario
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS movimientos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                producto_id INTEGER NOT NULL,
                tipo TEXT NOT NULL,
                cantidad INTEGER NOT NULL,
                precio_unitario REAL,
                fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                descripcion TEXT,
                FOREIGN KEY (producto_id) REFERENCES productos(id)
            )
        ''')
        
        # Tabla de ventas
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS ventas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                numero_factura TEXT UNIQUE,
                fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                total REAL NOT NULL,
                cliente TEXT,
                estado TEXT DEFAULT 'completada'
            )
        ''')
        
        # Tabla de detalles de ventas
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS detalles_ventas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                venta_id INTEGER NOT NULL,
                producto_id INTEGER NOT NULL,
                cantidad INTEGER NOT NULL,
                precio_unitario REAL NOT NULL,
                subtotal REAL NOT NULL,
                FOREIGN KEY (venta_id) REFERENCES ventas(id),
                FOREIGN KEY (producto_id) REFERENCES productos(id)
            )
        ''')
        
        self.conn.commit()
    
    def agregar_producto(self, nombre, descripcion, precio, cantidad, codigo_barras=''):
        """Agregar nuevo producto"""
        try:
            self.cursor.execute('''
                INSERT INTO productos (nombre, descripcion, precio, cantidad, codigo_barras)
                VALUES (?, ?, ?, ?, ?)
            ''', (nombre, descripcion, precio, cantidad, codigo_barras))
            self.conn.commit()
            return True, "Producto agregado exitosamente"
        except sqlite3.IntegrityError:
            return False, "El código de barras ya existe"
        except Exception as e:
            return False, str(e)
    
    def obtener_productos(self):
        """Obtener todos los productos"""
        self.cursor.execute('SELECT * FROM productos')
        return self.cursor.fetchall()
    
    def obtener_producto(self, producto_id):
        """Obtener un producto específico"""
        self.cursor.execute('SELECT * FROM productos WHERE id = ?', (producto_id,))
        return self.cursor.fetchone()
    
    def actualizar_producto(self, producto_id, nombre, descripcion, precio, cantidad):
        """Actualizar información del producto"""
        try:
            self.cursor.execute('''
                UPDATE productos 
                SET nombre = ?, descripcion = ?, precio = ?, cantidad = ?
                WHERE id = ?
            ''', (nombre, descripcion, precio, cantidad, producto_id))
            self.conn.commit()
            return True, "Producto actualizado"
        except Exception as e:
            return False, str(e)
    
    def eliminar_producto(self, producto_id):
        """Eliminar un producto"""
        try:
            self.cursor.execute('DELETE FROM productos WHERE id = ?', (producto_id,))
            self.conn.commit()
            return True, "Producto eliminado"
        except Exception as e:
            return False, str(e)
    
    def registrar_movimiento(self, producto_id, tipo, cantidad, precio_unitario=0, descripcion=''):
        """Registrar movimiento de inventario (entrada/salida)"""
        try:
            self.cursor.execute('''
                INSERT INTO movimientos (producto_id, tipo, cantidad, precio_unitario, descripcion)
                VALUES (?, ?, ?, ?, ?)
            ''', (producto_id, tipo, cantidad, precio_unitario, descripcion))
            self.conn.commit()
            return True, "Movimiento registrado"
        except Exception as e:
            return False, str(e)
    
    def obtener_movimientos(self):
        """Obtener historial de movimientos"""
        self.cursor.execute('''
            SELECT m.id, p.nombre, m.tipo, m.cantidad, m.precio_unitario, m.fecha, m.descripcion
            FROM movimientos m
            JOIN productos p ON m.producto_id = p.id
            ORDER BY m.fecha DESC
        ''')
        return self.cursor.fetchall()
    
    def crear_venta(self, numero_factura, cliente, detalles):
        """Crear una nueva venta con detalles"""
        try:
            total = sum(detalle['cantidad'] * detalle['precio_unitario'] for detalle in detalles)
            
            self.cursor.execute('''
                INSERT INTO ventas (numero_factura, cliente, total)
                VALUES (?, ?, ?)
            ''', (numero_factura, cliente, total))
            
            venta_id = self.cursor.lastrowid
            
            # Insertar detalles de venta
            for detalle in detalles:
                self.cursor.execute('''
                    INSERT INTO detalles_ventas (venta_id, producto_id, cantidad, precio_unitario, subtotal)
                    VALUES (?, ?, ?, ?, ?)
                ''', (venta_id, detalle['producto_id'], detalle['cantidad'], 
                      detalle['precio_unitario'], detalle['cantidad'] * detalle['precio_unitario']))
                
                # Actualizar cantidad de producto
                self.cursor.execute('''
                    UPDATE productos 
                    SET cantidad = cantidad - ?
                    WHERE id = ?
                ''', (detalle['cantidad'], detalle['producto_id']))
                
                # Registrar movimiento
                self.cursor.execute('''
                    INSERT INTO movimientos (producto_id, tipo, cantidad, precio_unitario, descripcion)
                    VALUES (?, 'SALIDA', ?, ?, ?)
                ''', (detalle['producto_id'], detalle['cantidad'], 
                      detalle['precio_unitario'], f"Venta #{numero_factura}"))
            
            self.conn.commit()
            return True, f"Venta creada: #{numero_factura}"
        except Exception as e:
            self.conn.rollback()
            return False, str(e)
    
    def obtener_ventas(self):
        """Obtener historial de ventas"""
        self.cursor.execute('''
            SELECT id, numero_factura, fecha, total, cliente, estado
            FROM ventas
            ORDER BY fecha DESC
        ''')
        return self.cursor.fetchall()
    
    def obtener_detalles_venta(self, venta_id):
        """Obtener detalles de una venta específica"""
        self.cursor.execute('''
            SELECT p.nombre, dv.cantidad, dv.precio_unitario, dv.subtotal
            FROM detalles_ventas dv
            JOIN productos p ON dv.producto_id = p.id
            WHERE dv.venta_id = ?
        ''', (venta_id,))
        return self.cursor.fetchall()
    
    def obtener_reporte_inventario(self):
        """Obtener reporte de inventario actual"""
        self.cursor.execute('''
            SELECT id, nombre, cantidad, precio, (cantidad * precio) as valor_total
            FROM productos
            ORDER BY nombre
        ''')
        return self.cursor.fetchall()
    
    def obtener_reporte_ventas(self, fecha_inicio=None, fecha_fin=None):
        """Obtener reporte de ventas por período"""
        if fecha_inicio and fecha_fin:
            self.cursor.execute('''
                SELECT numero_factura, fecha, cliente, total
                FROM ventas
                WHERE DATE(fecha) BETWEEN ? AND ?
                ORDER BY fecha DESC
            ''', (fecha_inicio, fecha_fin))
        else:
            self.cursor.execute('''
                SELECT numero_factura, fecha, cliente, total
                FROM ventas
                ORDER BY fecha DESC
            ''')
        return self.cursor.fetchall()
    
    def obtener_reporte_movimientos(self, fecha_inicio=None, fecha_fin=None):
        """Obtener reporte de movimientos de inventario"""
        if fecha_inicio and fecha_fin:
            self.cursor.execute('''
                SELECT m.id, p.nombre, m.tipo, m.cantidad, m.precio_unitario, m.fecha, m.descripcion
                FROM movimientos m
                JOIN productos p ON m.producto_id = p.id
                WHERE DATE(m.fecha) BETWEEN ? AND ?
                ORDER BY m.fecha DESC
            ''', (fecha_inicio, fecha_fin))
        else:
            self.cursor.execute('''
                SELECT m.id, p.nombre, m.tipo, m.cantidad, m.precio_unitario, m.fecha, m.descripcion
                FROM movimientos m
                JOIN productos p ON m.producto_id = p.id
                ORDER BY m.fecha DESC
            ''')
        return self.cursor.fetchall()
    
    def close(self):
        """Cerrar conexión con la base de datos"""
        self.conn.close()
