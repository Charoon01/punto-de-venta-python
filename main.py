import PySimpleGUI as sg
from database import Database
from datetime import datetime
import os

# Configurar tema
sg.theme('DarkBlue3')
sg.set_options(font=('Arial', 11))

class PuntoDeVenta:
    def __init__(self):
        self.db = Database()
        self.carrito = []
        self.numero_factura = self.generar_numero_factura()
    
    def generar_numero_factura(self):
        """Generar número de factura único"""
        return datetime.now().strftime('%Y%m%d%H%M%S')
    
    def crear_ventana_principal(self):
        """Crear ventana principal"""
        layout = [
            [sg.Text('SISTEMA DE PUNTO DE VENTA', font=('Arial', 16, 'bold'), justification='center')],
            [sg.HorizontalSeparator()],
            [
                [sg.Button('NUEVA VENTA', size=(15, 2), button_color=('white', 'green'))],
                [sg.Button('GESTIÓN DE PRODUCTOS', size=(15, 2), button_color=('white', 'blue'))],
                [sg.Button('HISTORIAL DE INVENTARIO', size=(15, 2), button_color=('white', 'orange'))],
                [sg.Button('REPORTES', size=(15, 2), button_color=('white', 'purple'))],
                [sg.Button('SALIR', size=(15, 2), button_color=('white', 'red'))]
            ]
        ]
        
        return sg.Window('Punto de Venta - Sistema POS', layout, finalize=True, size=(400, 400))
    
    def crear_ventana_nueva_venta(self):
        """Crear ventana para nueva venta"""
        productos = self.db.obtener_productos()
        
        lista_productos = [[p[0], p[1], p[3], p[4]] for p in productos]
        
        layout = [
            [sg.Text('NUEVA VENTA', font=('Arial', 14, 'bold'))],
            [sg.HorizontalSeparator()],
            
            [sg.Text('Cliente:'), sg.InputText(key='-CLIENTE-', size=(30,))],
            
            [sg.Text('Seleccionar Producto:')],
            [sg.Table(
                values=lista_productos,
                headings=['ID', 'Nombre', 'Precio', 'Stock'],
                max_col_widths=[5, 20, 10, 8],
                size=(45, 6),
                key='-TABLA_PRODUCTOS-',
                select_mode=sg.TABLE_SELECT_MODE_SINGLE_ROW
            )],
            
            [sg.Text('Cantidad:'), sg.InputText(key='-CANTIDAD-', size=(10,))],
            [sg.Button('Agregar al Carrito', size=(20,)), sg.Button('Limpiar Carrito', size=(20,))],
            
            [sg.Text('CARRITO DE COMPRAS', font=('Arial', 11, 'bold'))],
            [sg.Table(
                values=[],
                headings=['Producto', 'Cantidad', 'Precio Unit.', 'Subtotal'],
                max_col_widths=[15, 10, 12, 12],
                size=(45, 8),
                key='-CARRITO-'
            )],
            
            [sg.Text('Total: $'), sg.Text('0.00', key='-TOTAL-', font=('Arial', 12, 'bold'))],
            
            [sg.Button('Procesar Venta', size=(20,), button_color=('white', 'green')), 
             sg.Button('Cancelar', size=(20,), button_color=('white', 'red'))]
        ]
        
        return sg.Window('Nueva Venta', layout, finalize=True)
    
    def crear_ventana_gestion_productos(self):
        """Crear ventana de gestión de productos"""
        productos = self.db.obtener_productos()
        lista_productos = [[p[0], p[1], p[2], p[3], p[4], p[5]] for p in productos]
        
        layout = [
            [sg.Text('GESTIÓN DE PRODUCTOS', font=('Arial', 14, 'bold'))],
            [sg.HorizontalSeparator()],
            
            [sg.Button('Agregar Producto', size=(15,)), 
             sg.Button('Editar Producto', size=(15,)), 
             sg.Button('Eliminar Producto', size=(15,)),
             sg.Button('Volver', size=(15,))],
            
            [sg.Table(
                values=lista_productos,
                headings=['ID', 'Nombre', 'Descripción', 'Precio', 'Cantidad', 'Código Barras'],
                max_col_widths=[5, 15, 20, 10, 10, 15],
                size=(100, 15),
                key='-TABLA_PRODUCTOS-',
                select_mode=sg.TABLE_SELECT_MODE_SINGLE_ROW
            )]
        ]
        
        return sg.Window('Gestión de Productos', layout, finalize=True)
    
    def crear_ventana_agregar_producto(self):
        """Crear ventana para agregar producto"""
        layout = [
            [sg.Text('AGREGAR NUEVO PRODUCTO', font=('Arial', 14, 'bold'))],
            [sg.HorizontalSeparator()],
            
            [sg.Text('Nombre:', size=(15,)), sg.InputText(key='-NOMBRE-', size=(30,))],
            [sg.Text('Descripción:', size=(15,)), sg.Multiline(key='-DESCRIPCION-', size=(30, 4))],
            [sg.Text('Precio:', size=(15,)), sg.InputText(key='-PRECIO-', size=(15,))],
            [sg.Text('Cantidad:', size=(15,)), sg.InputText(key='-CANTIDAD-', size=(15,))],
            [sg.Text('Código Barras:', size=(15,)), sg.InputText(key='-CODIGO-', size=(30,))],
            
            [sg.Button('Guardar', size=(15,), button_color=('white', 'green')), 
             sg.Button('Cancelar', size=(15,), button_color=('white', 'red'))]
        ]
        
        return sg.Window('Agregar Producto', layout, finalize=True)
    
    def crear_ventana_historial_inventario(self):
        """Crear ventana de historial de inventario"""
        movimientos = self.db.obtener_movimientos()
        
        layout = [
            [sg.Text('HISTORIAL DE MOVIMIENTOS DE INVENTARIO', font=('Arial', 14, 'bold'))],
            [sg.HorizontalSeparator()],
            
            [sg.Button('Registrar Entrada', size=(15,), button_color=('white', 'green')), 
             sg.Button('Registrar Salida', size=(15,), button_color=('white', 'orange')),
             sg.Button('Volver', size=(15,))],
            
            [sg.Table(
                values=movimientos,
                headings=['ID', 'Producto', 'Tipo', 'Cantidad', 'Precio Unit.', 'Fecha', 'Descripción'],
                max_col_widths=[5, 15, 8, 10, 12, 20, 25],
                size=(120, 15),
                key='-TABLA_MOVIMIENTOS-'
            )]
        ]
        
        return sg.Window('Historial de Inventario', layout, finalize=True)
    
    def crear_ventana_reportes(self):
        """Crear ventana de reportes"""
        layout = [
            [sg.Text('REPORTES', font=('Arial', 14, 'bold'))],
            [sg.HorizontalSeparator()],
            
            [sg.Button('Reporte de Inventario', size=(20,), button_color=('white', 'blue')), 
             sg.Button('Reporte de Ventas', size=(20,), button_color=('white', 'green')),
             sg.Button('Reporte de Movimientos', size=(20,), button_color=('white', 'orange')),
             sg.Button('Volver', size=(20,), button_color=('white', 'red'))]
        ]
        
        return sg.Window('Reportes', layout, finalize=True)
    
    def crear_ventana_reporte_inventario(self):
        """Crear ventana de reporte de inventario"""
        datos = self.db.obtener_reporte_inventario()
        
        layout = [
            [sg.Text('REPORTE DE INVENTARIO', font=('Arial', 14, 'bold'))],
            [sg.HorizontalSeparator()],
            
            [sg.Table(
                values=datos,
                headings=['ID', 'Producto', 'Cantidad', 'Precio Unitario', 'Valor Total'],
                max_col_widths=[5, 20, 10, 15, 15],
                size=(80, 15),
                key='-TABLA_REPORTE-'
            )],
            
            [sg.Button('Exportar a PDF', size=(15,)), sg.Button('Volver', size=(15,))]
        ]
        
        return sg.Window('Reporte de Inventario', layout, finalize=True)
    
    def crear_ventana_reporte_ventas(self):
        """Crear ventana de reporte de ventas"""
        datos = self.db.obtener_reporte_ventas()
        
        layout = [
            [sg.Text('REPORTE DE VENTAS', font=('Arial', 14, 'bold'))],
            [sg.HorizontalSeparator()],
            
            [sg.Text('Desde:'), sg.InputText(key='-FECHA_INICIO-', size=(15,)), 
             sg.Text('Hasta:'), sg.InputText(key='-FECHA_FIN-', size=(15,)),
             sg.Button('Filtrar', size=(10,))],
            
            [sg.Table(
                values=datos,
                headings=['Factura', 'Fecha', 'Cliente', 'Total'],
                max_col_widths=[15, 20, 20, 15],
                size=(80, 15),
                key='-TABLA_REPORTE-'
            )],
            
            [sg.Button('Exportar a PDF', size=(15,)), sg.Button('Volver', size=(15,))]
        ]
        
        return sg.Window('Reporte de Ventas', layout, finalize=True)
    
    def mostrar_mensaje(self, titulo, mensaje):
        """Mostrar ventana de mensaje"""
        sg.popup(mensaje, title=titulo)
    
    def run(self):
        """Ejecutar aplicación"""
        ventana_principal = self.crear_ventana_principal()
        
        while True:
            event, values = ventana_principal.read()
            
            if event == sg.WINDOW_CLOSED or event == 'SALIR':
                break
            
            elif event == 'NUEVA VENTA':
                ventana_principal.hide()
                self.manejar_nueva_venta()
                ventana_principal.un_hide()
            
            elif event == 'GESTIÓN DE PRODUCTOS':
                ventana_principal.hide()
                self.manejar_gestion_productos()
                ventana_principal.un_hide()
            
            elif event == 'HISTORIAL DE INVENTARIO':
                ventana_principal.hide()
                self.manejar_historial_inventario()
                ventana_principal.un_hide()
            
            elif event == 'REPORTES':
                ventana_principal.hide()
                self.manejar_reportes()
                ventana_principal.un_hide()
        
        ventana_principal.close()
        self.db.close()
    
    def manejar_nueva_venta(self):
        """Manejar interfaz de nueva venta"""
        ventana = self.crear_ventana_nueva_venta()
        carrito = []
        
        while True:
            event, values = ventana.read()
            
            if event == sg.WINDOW_CLOSED or event == 'Cancelar':
                break
            
            elif event == 'Agregar al Carrito':
                if not values['-TABLA_PRODUCTOS-']:
                    self.mostrar_mensaje('Error', 'Seleccione un producto')
                    continue
                
                try:
                    cantidad = int(values['-CANTIDAD-'])
                    if cantidad <= 0:
                        self.mostrar_mensaje('Error', 'La cantidad debe ser mayor a 0')
                        continue
                    
                    idx = values['-TABLA_PRODUCTOS-'][0]
                    productos = self.db.obtener_productos()
                    producto = productos[idx]
                    
                    if cantidad > producto[4]:
                        self.mostrar_mensaje('Error', 'No hay suficiente stock')
                        continue
                    
                    item = {
                        'producto_id': producto[0],
                        'nombre': producto[1],
                        'cantidad': cantidad,
                        'precio_unitario': producto[3],
                        'subtotal': cantidad * producto[3]
                    }
                    
                    carrito.append(item)
                    
                    # Actualizar vista del carrito
                    carrito_data = [[item['nombre'], item['cantidad'], item['precio_unitario'], item['subtotal']] for item in carrito]
                    ventana['-CARRITO-'].update(carrito_data)
                    
                    # Actualizar total
                    total = sum(item['subtotal'] for item in carrito)
                    ventana['-TOTAL-'].update(f'{total:.2f}')
                    
                    ventana['-CANTIDAD-'].update('')
                
                except ValueError:
                    self.mostrar_mensaje('Error', 'Ingrese una cantidad válida')
            
            elif event == 'Limpiar Carrito':
                carrito = []
                ventana['-CARRITO-'].update([])
                ventana['-TOTAL-'].update('0.00')
            
            elif event == 'Procesar Venta':
                if not carrito:
                    self.mostrar_mensaje('Error', 'El carrito está vacío')
                    continue
                
                cliente = values['-CLIENTE-'] or 'Cliente General'
                
                detalles = [{
                    'producto_id': item['producto_id'],
                    'cantidad': item['cantidad'],
                    'precio_unitario': item['precio_unitario']
                } for item in carrito]
                
                numero_factura = self.generar_numero_factura()
                exito, mensaje = self.db.crear_venta(numero_factura, cliente, detalles)
                
                if exito:
                    total = sum(item['subtotal'] for item in carrito)
                    self.mostrar_mensaje('Éxito', f'Venta realizada\nFactura: {numero_factura}\nTotal: ${total:.2f}')
                    break
                else:
                    self.mostrar_mensaje('Error', mensaje)
        
        ventana.close()
    
    def manejar_gestion_productos(self):
        """Manejar interfaz de gestión de productos"""
        while True:
            ventana = self.crear_ventana_gestion_productos()
            event, values = ventana.read()
            
            if event == sg.WINDOW_CLOSED or event == 'Volver':
                ventana.close()
                break
            
            elif event == 'Agregar Producto':
                ventana.hide()
                self.manejar_agregar_producto()
                ventana.un_hide()
            
            elif event == 'Eliminar Producto':
                if not values['-TABLA_PRODUCTOS-']:
                    self.mostrar_mensaje('Error', 'Seleccione un producto')
                    ventana.close()
                    continue
                
                idx = values['-TABLA_PRODUCTOS-'][0]
                productos = self.db.obtener_productos()
                producto_id = productos[idx][0]
                
                exito, mensaje = self.db.eliminar_producto(producto_id)
                self.mostrar_mensaje('Resultado', mensaje)
                ventana.close()
                continue
            
            ventana.close()
    
    def manejar_agregar_producto(self):
        """Manejar agregar producto"""
        ventana = self.crear_ventana_agregar_producto()
        
        while True:
            event, values = ventana.read()
            
            if event == sg.WINDOW_CLOSED or event == 'Cancelar':
                break
            
            elif event == 'Guardar':
                try:
                    nombre = values['-NOMBRE-']
                    descripcion = values['-DESCRIPCION-']
                    precio = float(values['-PRECIO-'])
                    cantidad = int(values['-CANTIDAD-'])
                    codigo = values['-CODIGO-']
                    
                    if not nombre:
                        self.mostrar_mensaje('Error', 'El nombre es requerido')
                        continue
                    
                    if precio < 0 or cantidad < 0:
                        self.mostrar_mensaje('Error', 'Precio y cantidad no pueden ser negativos')
                        continue
                    
                    exito, mensaje = self.db.agregar_producto(nombre, descripcion, precio, cantidad, codigo)
                    self.mostrar_mensaje('Resultado', mensaje)
                    
                    if exito:
                        break
                
                except ValueError:
                    self.mostrar_mensaje('Error', 'Ingrese valores válidos para precio y cantidad')
        
        ventana.close()
    
    def manejar_historial_inventario(self):
        """Manejar historial de inventario"""
        while True:
            ventana = self.crear_ventana_historial_inventario()
            event, values = ventana.read()
            
            if event == sg.WINDOW_CLOSED or event == 'Volver':
                ventana.close()
                break
            
            elif event == 'Registrar Entrada' or event == 'Registrar Salida':
                ventana.hide()
                self.manejar_movimiento_inventario(event == 'Registrar Entrada')
                ventana.un_hide()
            
            ventana.close()
    
    def manejar_movimiento_inventario(self, es_entrada):
        """Manejar movimiento de inventario"""
        productos = self.db.obtener_productos()
        lista_productos = [[p[0], p[1]] for p in productos]
        
        tipo = "Entrada" if es_entrada else "Salida"
        
        layout = [
            [sg.Text(f'REGISTRAR {tipo.upper()} DE INVENTARIO', font=('Arial', 14, 'bold'))],
            [sg.HorizontalSeparator()],
            
            [sg.Text('Seleccionar Producto:')],
            [sg.Table(
                values=lista_productos,
                headings=['ID', 'Nombre'],
                max_col_widths=[5, 30],
                size=(40, 8),
                key='-TABLA_PRODUCTOS-',
                select_mode=sg.TABLE_SELECT_MODE_SINGLE_ROW
            )],
            
            [sg.Text('Cantidad:'), sg.InputText(key='-CANTIDAD-', size=(15,))],
            [sg.Text('Precio Unitario:'), sg.InputText(key='-PRECIO-', size=(15,))],
            [sg.Text('Descripción:'), sg.InputText(key='-DESCRIPCION-', size=(30,))],
            
            [sg.Button('Guardar', size=(15,), button_color=('white', 'green')), 
             sg.Button('Cancelar', size=(15,), button_color=('white', 'red'))]
        ]
        
        ventana = sg.Window(f'Registrar {tipo}', layout, finalize=True)
        
        while True:
            event, values = ventana.read()
            
            if event == sg.WINDOW_CLOSED or event == 'Cancelar':
                break
            
            elif event == 'Guardar':
                if not values['-TABLA_PRODUCTOS-']:
                    self.mostrar_mensaje('Error', 'Seleccione un producto')
                    continue
                
                try:
                    idx = values['-TABLA_PRODUCTOS-'][0]
                    producto_id = productos[idx][0]
                    cantidad = int(values['-CANTIDAD-'])
                    precio = float(values['-PRECIO-']) if values['-PRECIO-'] else 0
                    descripcion = values['-DESCRIPCION-']
                    
                    tipo_movimiento = 'ENTRADA' if es_entrada else 'SALIDA'
                    exito, mensaje = self.db.registrar_movimiento(
                        producto_id, tipo_movimiento, cantidad, precio, descripcion
                    )
                    
                    # Actualizar cantidad del producto
                    producto = self.db.obtener_producto(producto_id)
                    nueva_cantidad = producto[4] + cantidad if es_entrada else producto[4] - cantidad
                    
                    if nueva_cantidad < 0:
                        self.mostrar_mensaje('Error', 'No hay suficiente stock')
                        continue
                    
                    self.db.actualizar_producto(producto_id, producto[1], producto[2], producto[3], nueva_cantidad)
                    
                    self.mostrar_mensaje('Éxito', mensaje)
                    break
                
                except ValueError:
                    self.mostrar_mensaje('Error', 'Ingrese valores válidos')
        
        ventana.close()
    
    def manejar_reportes(self):
        """Manejar reportes"""
        while True:
            ventana = self.crear_ventana_reportes()
            event, values = ventana.read()
            
            if event == sg.WINDOW_CLOSED or event == 'Volver':
                ventana.close()
                break
            
            elif event == 'Reporte de Inventario':
                ventana.hide()
                self.mostrar_reporte_inventario()
                ventana.un_hide()
            
            elif event == 'Reporte de Ventas':
                ventana.hide()
                self.mostrar_reporte_ventas()
                ventana.un_hide()
            
            elif event == 'Reporte de Movimientos':
                ventana.hide()
                self.mostrar_reporte_movimientos()
                ventana.un_hide()
            
            ventana.close()
    
    def mostrar_reporte_inventario(self):
        """Mostrar reporte de inventario"""
        ventana = self.crear_ventana_reporte_inventario()
        
        while True:
            event, values = ventana.read()
            
            if event == sg.WINDOW_CLOSED or event == 'Volver':
                break
            
            elif event == 'Exportar a PDF':
                self.mostrar_mensaje('Información', 'Función de exportación en desarrollo')
        
        ventana.close()
    
    def mostrar_reporte_ventas(self):
        """Mostrar reporte de ventas"""
        ventana = self.crear_ventana_reporte_ventas()
        
        while True:
            event, values = ventana.read()
            
            if event == sg.WINDOW_CLOSED or event == 'Volver':
                break
            
            elif event == 'Filtrar':
                fecha_inicio = values['-FECHA_INICIO-']
                fecha_fin = values['-FECHA_FIN-']
                datos = self.db.obtener_reporte_ventas(fecha_inicio, fecha_fin)
                ventana['-TABLA_REPORTE-'].update(datos)
            
            elif event == 'Exportar a PDF':
                self.mostrar_mensaje('Información', 'Función de exportación en desarrollo')
        
        ventana.close()
    
    def mostrar_reporte_movimientos(self):
        """Mostrar reporte de movimientos"""
        datos = self.db.obtener_reporte_movimientos()
        
        layout = [
            [sg.Text('REPORTE DE MOVIMIENTOS DE INVENTARIO', font=('Arial', 14, 'bold'))],
            [sg.HorizontalSeparator()],
            
            [sg.Table(
                values=datos,
                headings=['ID', 'Producto', 'Tipo', 'Cantidad', 'Precio Unit.', 'Fecha', 'Descripción'],
                max_col_widths=[5, 15, 8, 10, 12, 20, 25],
                size=(120, 15),
                key='-TABLA_REPORTE-'
            )],
            
            [sg.Button('Volver', size=(15,))]
        ]
        
        ventana = sg.Window('Reporte de Movimientos', layout, finalize=True)
        
        while True:
            event, values = ventana.read()
            
            if event == sg.WINDOW_CLOSED or event == 'Volver':
                break
        
        ventana.close()

if __name__ == '__main__':
    app = PuntoDeVenta()
    app.run()