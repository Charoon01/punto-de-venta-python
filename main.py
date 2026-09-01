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
            [sg.Text('SISTEMA DE GESTIÓN DE MÁQUINAS', font=('Arial', 16, 'bold'), justification='center')],
            [sg.HorizontalSeparator()],
            [
                [sg.Button('NUEVA ENTREGA', size=(15, 2), button_color=('white', 'green'))],
                [sg.Button('GESTIÓN DE MÁQUINAS', size=(15, 2), button_color=('white', 'blue'))],
                [sg.Button('HISTORIAL DE INVENTARIO', size=(15, 2), button_color=('white', 'orange'))],
                [sg.Button('REPORTES', size=(15, 2), button_color=('white', 'purple'))],
                [sg.Button('SALIR', size=(15, 2), button_color=('white', 'red'))]
            ]
        ]
        
        return sg.Window('Sistema de Gestión de Máquinas', layout, finalize=True, size=(500, 500), resizable=True)
    
    def crear_ventana_nueva_entrega(self):
        """Crear ventana para nueva entrega"""
        maquinas = self.db.obtener_maquinas()
        
        lista_maquinas = [[m[0], m[1], m[3], m[4]] for m in maquinas]
        
        layout = [
            [sg.Text('NUEVA ENTREGA DE MÁQUINA', font=('Arial', 14, 'bold'))],
            [sg.HorizontalSeparator()],
            
            [sg.Text('Dueño:'), sg.InputText(key='-DUEÑO-', size=(30,))],
            [sg.Text('Localia:'), sg.InputText(key='-LOCALIA-', size=(30,))],
            
            [sg.Text('Seleccionar Máquina:')],
            [sg.Table(
                values=lista_maquinas,
                headings=['ID', 'Nombre', 'Estado', 'Stock'],
                max_col_width=20,
                size=(45, 6),
                key='-TABLA_MAQUINAS-',
                select_mode=sg.TABLE_SELECT_MODE_SINGLE_ROW
            )],
            
            [sg.Text('Cantidad:'), sg.InputText(key='-CANTIDAD-', size=(10,))],
            [sg.Text('Estado de la Máquina:'), sg.InputText(key='-ESTADO_MAQUINA-', size=(20,))],
            [sg.Button('Agregar Máquina', size=(20,)), sg.Button('Limpiar Carrito', size=(20,))],
            
            [sg.Text('MÁQUINAS A ENTREGAR', font=('Arial', 11, 'bold'))],
            [sg.Table(
                values=[],
                headings=['Máquina', 'Cantidad', 'Estado', 'Subtotal'],
                max_col_width=20,
                size=(45, 8),
                key='-CARRITO-'
            )],
            
            [sg.Text('Total: '), sg.Text('0', key='-TOTAL-', font=('Arial', 12, 'bold'))],
            
            [sg.Button('Procesar Estado de la Máquina', size=(25,), button_color=('white', 'green')), 
             sg.Button('Cancelar', size=(20,), button_color=('white', 'red'))]
        ]
        
        return sg.Window('Nueva Entrega de Máquina', layout, finalize=True, resizable=True)
    
    def crear_ventana_gestion_maquinas(self):
        """Crear ventana de gestión de máquinas"""
        maquinas = self.db.obtener_maquinas()
        lista_maquinas = [[m[0], m[1], m[2], m[3], m[4]] for m in maquinas]
        
        layout = [
            [sg.Text('GESTIÓN DE MÁQUINAS', font=('Arial', 14, 'bold'))],
            [sg.HorizontalSeparator()],
            
            [sg.Button('Agregar Máquina', size=(15,)), 
             sg.Button('Editar Máquina', size=(15,)), 
             sg.Button('Eliminar Máquina', size=(15,)),
             sg.Button('Volver', size=(15,))],
            
            [sg.Table(
                values=lista_maquinas,
                headings=['ID', 'Nombre', 'Descripción', 'Estado', 'Cantidad'],
                max_col_width=20,
                size=(100, 15),
                key='-TABLA_MAQUINAS-',
                select_mode=sg.TABLE_SELECT_MODE_SINGLE_ROW
            )]
        ]
        
        return sg.Window('Gestión de Máquinas', layout, finalize=True, resizable=True)
    
    def crear_ventana_agregar_maquina(self):
        """Crear ventana para agregar máquina"""
        layout = [
            [sg.Text('AGREGAR NUEVA MÁQUINA', font=('Arial', 14, 'bold'))],
            [sg.HorizontalSeparator()],
            
            [sg.Text('Nombre:', size=(15,)), sg.InputText(key='-NOMBRE-', size=(30,))],
            [sg.Text('Descripción:', size=(15,)), sg.Multiline(key='-DESCRIPCION-', size=(30, 4))],
            [sg.Text('Estado:', size=(15,)), sg.InputText(key='-ESTADO-', size=(30,))],
            [sg.Text('Cantidad:', size=(15,)), sg.InputText(key='-CANTIDAD-', size=(15,))],
            
            [sg.Button('Guardar', size=(15,), button_color=('white', 'green')), 
             sg.Button('Cancelar', size=(15,), button_color=('white', 'red'))]
        ]
        
        return sg.Window('Agregar Máquina', layout, finalize=True, resizable=True)
    
    def crear_ventana_historial_inventario(self):
        """Crear ventana de historial de inventario"""
        movimientos = self.db.obtener_movimientos()
        
        layout = [
            [sg.Text('HISTORIAL DE MOVIMIENTOS DE INVENTARIO', font=('Arial', 14, 'bold'))],
            [sg.HorizontalSeparator()],
            
            [sg.Button('Entrada de Stock Nuevo', size=(20,), button_color=('white', 'green')), 
             sg.Button('Mantenimiento', size=(20,), button_color=('white', 'orange')),
             sg.Button('Volver', size=(15,))],
            
            [sg.Table(
                values=movimientos,
                headings=['ID', 'Máquina', 'Tipo', 'Cantidad', 'Precio Unit.', 'Fecha', 'Descripción'],
                max_col_width=20,
                size=(120, 15),
                key='-TABLA_MOVIMIENTOS-'
            )]
        ]
        
        return sg.Window('Historial de Inventario', layout, finalize=True, resizable=True)
    
    def crear_ventana_reportes(self):
        """Crear ventana de reportes"""
        layout = [
            [sg.Text('REPORTES', font=('Arial', 14, 'bold'))],
            [sg.HorizontalSeparator()],
            
            [sg.Button('Reporte de Inventario', size=(20,), button_color=('white', 'blue')), 
             sg.Button('Reporte de Entrega de Máquinas', size=(20,), button_color=('white', 'green')),
             sg.Button('Reporte de Movimientos', size=(20,), button_color=('white', 'orange')),
             sg.Button('Volver', size=(20,), button_color=('white', 'red'))]
        ]
        
        return sg.Window('Reportes', layout, finalize=True, resizable=True)
    
    def crear_ventana_reporte_inventario(self):
        """Crear ventana de reporte de inventario"""
        datos = self.db.obtener_reporte_inventario()
        
        layout = [
            [sg.Text('REPORTE DE INVENTARIO', font=('Arial', 14, 'bold'))],
            [sg.HorizontalSeparator()],
            
            [sg.Table(
                values=datos,
                headings=['ID', 'Máquina', 'Cantidad', 'Estado', 'Total'],
                max_col_width=20,
                size=(80, 15),
                key='-TABLA_REPORTE-'
            )],
            
            [sg.Button('Exportar a PDF', size=(15,)), sg.Button('Volver', size=(15,))]
        ]
        
        return sg.Window('Reporte de Inventario', layout, finalize=True, resizable=True)
    
    def crear_ventana_reporte_entregas(self):
        """Crear ventana de reporte de entregas"""
        datos = self.db.obtener_reporte_entregas()
        
        layout = [
            [sg.Text('REPORTE DE ENTREGA DE MÁQUINAS', font=('Arial', 14, 'bold'))],
            [sg.HorizontalSeparator()],
            
            [sg.Text('Desde:'), sg.InputText(key='-FECHA_INICIO-', size=(15,)), 
             sg.Text('Hasta:'), sg.InputText(key='-FECHA_FIN-', size=(15,)),
             sg.Button('Filtrar', size=(10,))],
            
            [sg.Table(
                values=datos,
                headings=['Factura', 'Fecha', 'Dueño', 'Localia', 'Total'],
                max_col_width=20,
                size=(100, 15),
                key='-TABLA_REPORTE-'
            )],
            
            [sg.Button('Exportar a PDF', size=(15,)), sg.Button('Volver', size=(15,))]
        ]
        
        return sg.Window('Reporte de Entrega de Máquinas', layout, finalize=True, resizable=True)
    
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
            
            elif event == 'NUEVA ENTREGA':
                ventana_principal.hide()
                self.manejar_nueva_entrega()
                ventana_principal.un_hide()
            
            elif event == 'GESTIÓN DE MÁQUINAS':
                ventana_principal.hide()
                self.manejar_gestion_maquinas()
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
    
    def manejar_nueva_entrega(self):
        """Manejar interfaz de nueva entrega"""
        ventana = self.crear_ventana_nueva_entrega()
        carrito = []
        
        while True:
            event, values = ventana.read()
            
            if event == sg.WINDOW_CLOSED or event == 'Cancelar':
                break
            
            elif event == 'Agregar Máquina':
                if not values['-TABLA_MAQUINAS-']:
                    self.mostrar_mensaje('Error', 'Seleccione una máquina')
                    continue
                
                try:
                    cantidad = int(values['-CANTIDAD-'])
                    if cantidad <= 0:
                        self.mostrar_mensaje('Error', 'La cantidad debe ser mayor a 0')
                        continue
                    
                    idx = values['-TABLA_MAQUINAS-'][0]
                    maquinas = self.db.obtener_maquinas()
                    maquina = maquinas[idx]
                    
                    if cantidad > maquina[4]:
                        self.mostrar_mensaje('Error', 'No hay suficiente stock')
                        continue
                    
                    estado_maquina = values['-ESTADO_MAQUINA-']
                    
                    item = {
                        'maquina_id': maquina[0],
                        'nombre': maquina[1],
                        'cantidad': cantidad,
                        'estado_maquina': estado_maquina,
                        'subtotal': cantidad
                    }
                    
                    carrito.append(item)
                    
                    # Actualizar vista del carrito
                    carrito_data = [[item['nombre'], item['cantidad'], item['estado_maquina'], item['subtotal']] for item in carrito]
                    ventana['-CARRITO-'].update(carrito_data)
                    
                    # Actualizar total
                    total = sum(item['subtotal'] for item in carrito)
                    ventana['-TOTAL-'].update(str(total))
                    
                    ventana['-CANTIDAD-'].update('')
                    ventana['-ESTADO_MAQUINA-'].update('')
                
                except ValueError:
                    self.mostrar_mensaje('Error', 'Ingrese una cantidad válida')
            
            elif event == 'Limpiar Carrito':
                carrito = []
                ventana['-CARRITO-'].update([])
                ventana['-TOTAL-'].update('0')
            
            elif event == 'Procesar Estado de la Máquina':
                if not carrito:
                    self.mostrar_mensaje('Error', 'El carrito está vacío')
                    continue
                
                dueño = values['-DUEÑO-'] or 'Dueño General'
                localia = values['-LOCALIA-'] or 'Localia General'
                
                detalles = [{
                    'maquina_id': item['maquina_id'],
                    'cantidad': item['cantidad'],
                    'estado_maquina': item['estado_maquina']
                } for item in carrito]
                
                numero_factura = self.generar_numero_factura()
                exito, mensaje = self.db.crear_entrega(numero_factura, dueño, localia, detalles)
                
                if exito:
                    total = sum(item['subtotal'] for item in carrito)
                    self.mostrar_mensaje('Éxito', f'Entrega realizada\nFactura: {numero_factura}\nDueño: {dueño}\nLocalia: {localia}\nTotal: {total}')
                    break
                else:
                    self.mostrar_mensaje('Error', mensaje)
        
        ventana.close()
    
    def manejar_gestion_maquinas(self):
        """Manejar interfaz de gestión de máquinas"""
        while True:
            ventana = self.crear_ventana_gestion_maquinas()
            event, values = ventana.read()
            
            if event == sg.WINDOW_CLOSED or event == 'Volver':
                ventana.close()
                break
            
            elif event == 'Agregar Máquina':
                ventana.hide()
                self.manejar_agregar_maquina()
                ventana.un_hide()
            
            elif event == 'Eliminar Máquina':
                if not values['-TABLA_MAQUINAS-']:
                    self.mostrar_mensaje('Error', 'Seleccione una máquina')
                    ventana.close()
                    continue
                
                idx = values['-TABLA_MAQUINAS-'][0]
                maquinas = self.db.obtener_maquinas()
                maquina_id = maquinas[idx][0]
                
                exito, mensaje = self.db.eliminar_maquina(maquina_id)
                self.mostrar_mensaje('Resultado', mensaje)
                ventana.close()
                continue
            
            ventana.close()
    
    def manejar_agregar_maquina(self):
        """Manejar agregar máquina"""
        ventana = self.crear_ventana_agregar_maquina()
        
        while True:
            event, values = ventana.read()
            
            if event == sg.WINDOW_CLOSED or event == 'Cancelar':
                break
            
            elif event == 'Guardar':
                try:
                    nombre = values['-NOMBRE-']
                    descripcion = values['-DESCRIPCION-']
                    estado = values['-ESTADO-']
                    cantidad = int(values['-CANTIDAD-'])
                    
                    if not nombre:
                        self.mostrar_mensaje('Error', 'El nombre es requerido')
                        continue
                    
                    if cantidad < 0:
                        self.mostrar_mensaje('Error', 'La cantidad no puede ser negativa')
                        continue
                    
                    exito, mensaje = self.db.agregar_maquina(nombre, descripcion, estado, cantidad)
                    self.mostrar_mensaje('Resultado', mensaje)
                    
                    if exito:
                        break
                
                except ValueError:
                    self.mostrar_mensaje('Error', 'Ingrese valores válidos para cantidad')
        
        ventana.close()
    
    def manejar_historial_inventario(self):
        """Manejar historial de inventario"""
        while True:
            ventana = self.crear_ventana_historial_inventario()
            event, values = ventana.read()
            
            if event == sg.WINDOW_CLOSED or event == 'Volver':
                ventana.close()
                break
            
            elif event == 'Entrada de Stock Nuevo' or event == 'Mantenimiento':
                ventana.hide()
                self.manejar_movimiento_inventario(event == 'Entrada de Stock Nuevo')
                ventana.un_hide()
            
            ventana.close()
    
    def manejar_movimiento_inventario(self, es_entrada):
        """Manejar movimiento de inventario"""
        maquinas = self.db.obtener_maquinas()
        lista_maquinas = [[m[0], m[1]] for m in maquinas]
        
        tipo = "Entrada de Stock Nuevo" if es_entrada else "Mantenimiento"
        
        layout = [
            [sg.Text(f'REGISTRAR {tipo.upper()}', font=('Arial', 14, 'bold'))],
            [sg.HorizontalSeparator()],
            
            [sg.Text('Seleccionar Máquina:')],
            [sg.Table(
                values=lista_maquinas,
                headings=['ID', 'Nombre'],
                max_col_width=30,
                size=(40, 8),
                key='-TABLA_MAQUINAS-',
                select_mode=sg.TABLE_SELECT_MODE_SINGLE_ROW
            )],
            
            [sg.Text('Cantidad:'), sg.InputText(key='-CANTIDAD-', size=(15,))],
            [sg.Text('Precio Unitario:'), sg.InputText(key='-PRECIO-', size=(15,))],
            [sg.Text('Descripción:'), sg.InputText(key='-DESCRIPCION-', size=(30,))],
            
            [sg.Button('Guardar', size=(15,), button_color=('white', 'green')), 
             sg.Button('Cancelar', size=(15,), button_color=('white', 'red'))]
        ]
        
        ventana = sg.Window(f'Registrar {tipo}', layout, finalize=True, resizable=True)
        
        while True:
            event, values = ventana.read()
            
            if event == sg.WINDOW_CLOSED or event == 'Cancelar':
                break
            
            elif event == 'Guardar':
                if not values['-TABLA_MAQUINAS-']:
                    self.mostrar_mensaje('Error', 'Seleccione una máquina')
                    continue
                
                try:
                    idx = values['-TABLA_MAQUINAS-'][0]
                    maquina_id = maquinas[idx][0]
                    cantidad = int(values['-CANTIDAD-'])
                    precio = float(values['-PRECIO-']) if values['-PRECIO-'] else 0
                    descripcion = values['-DESCRIPCION-']
                    
                    tipo_movimiento = 'ENTRADA' if es_entrada else 'MANTENIMIENTO'
                    exito, mensaje = self.db.registrar_movimiento(
                        maquina_id, tipo_movimiento, cantidad, precio, descripcion
                    )
                    
                    # Actualizar cantidad de la máquina
                    maquina = self.db.obtener_maquina(maquina_id)
                    nueva_cantidad = maquina[4] + cantidad if es_entrada else maquina[4] - cantidad
                    
                    if nueva_cantidad < 0:
                        self.mostrar_mensaje('Error', 'No hay suficiente stock')
                        continue
                    
                    self.db.actualizar_maquina(maquina_id, maquina[1], maquina[2], maquina[3], nueva_cantidad)
                    
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
            
            elif event == 'Reporte de Entrega de Máquinas':
                ventana.hide()
                self.mostrar_reporte_entregas()
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
    
    def mostrar_reporte_entregas(self):
        """Mostrar reporte de entregas"""
        ventana = self.crear_ventana_reporte_entregas()
        
        while True:
            event, values = ventana.read()
            
            if event == sg.WINDOW_CLOSED or event == 'Volver':
                break
            
            elif event == 'Filtrar':
                fecha_inicio = values['-FECHA_INICIO-']
                fecha_fin = values['-FECHA_FIN-']
                datos = self.db.obtener_reporte_entregas(fecha_inicio, fecha_fin)
                ventana['-TABLA_REPORTE-'].update(datos)
            
            elif event == 'Exportar a PDF':
                self.mostrar_mensaje('Información', 'Función de exportación en desarrollo')
        
        ventana.close()
    
    def mostrar_reporte_movimientos(self):
        """Mostrar reporte de movimientos"""
        datos = self.db.obtener_reporte_movimientos()
        
        layout = [
            [sg.Text('REPORTE DE MÁQUINAS TRABAJADAS', font=('Arial', 14, 'bold'))],
            [sg.HorizontalSeparator()],
            
            [sg.Table(
                values=datos,
                headings=['ID', 'Máquina', 'Tipo', 'Cantidad', 'Precio Unit.', 'Fecha', 'Descripción'],
                max_col_width=20,
                size=(120, 15),
                key='-TABLA_REPORTE-'
            )],
            
            [sg.Button('Volver', size=(15,))]
        ]
        
        ventana = sg.Window('Reporte de Máquinas Trabajadas', layout, finalize=True, resizable=True)
        
        while True:
            event, values = ventana.read()
            
            if event == sg.WINDOW_CLOSED or event == 'Volver':
                break
        
        ventana.close()

if __name__ == '__main__':
    app = PuntoDeVenta()
    app.run()
