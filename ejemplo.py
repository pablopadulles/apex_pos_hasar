from HasarRESTJson import HasarRESTJson, CODIGOCOMPROBANTE, CONDICIONIVA
from item import ItemFactura
from descuento import Descuento
from tributo import Tributo
from pago import Pago

printer = HasarRESTJson(ip_impresora='192.168.1.101')
# estado = printer.consultar_estado()
estado = printer.consultarEstado()

print(estado)

item0 = ItemFactura('descripcion1', 3.0, 0.50, CONDICIONIVA['Gravado'], 'codigo')
item1 = ItemFactura('descripcion2', 1.0, 1.00, CONDICIONIVA['Gravado'], 'codigo')
item2 = ItemFactura('descripcion3', 1.0, 1.00, CONDICIONIVA['Gravado'], 'codigo')

descuento = Descuento(
    descripcion="Super oferta semanal",
    monto=1.00,
)

pago = Pago(
    descripcion="Efectivo",
    monto=5.00,
    codigo_forma_pago="Efectivo"
)

printer.crearTicket(codigo=CODIGOCOMPROBANTE['TiqueFacturaB'], items=[item0, item1, item2], descuento=descuento, pago=pago)

