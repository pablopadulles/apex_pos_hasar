from HasarFiscalPrinter import HasarFiscalPrinter

printer = HasarFiscalPrinter(puerto='/dev/ttyACM0')  # Poné tu puerto

try:
    printer.prueba()  # Abre un tique simple
    printer.abrir_tique()  # Abre un tique simple
    printer.agregar_item('Coca Cola 500ml', 1, 1.00)
    printer.agregar_item('Alfajor', 2, 0.50)
    printer.cerrar_tique()  # Cierra el comprobante
finally:
    printer.cerrar()
