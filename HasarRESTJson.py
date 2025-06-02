from descuento import Descuento
from item import ItemFactura
from tributo import Tributo
from pago import Pago

import requests
import base64
import json

TIPODEIMPUESTOINTERNO = {'IIVariableKIVA': 'IIVariableKIVA',
                         'IIVariablePorcentual': 'IIVariablePorcentual',
                         'IIFijoKIVA': 'IIFijoKIVA',
                         'IIFijoMonto': 'IIFijoMonto'}

CONDICIONIVA = {'NoGravado': 'NoGravado',
                'Gravado': 'Gravado',
                'Exento': 'Exento'}

FORMASDEPAGO = {
    'Cambio': 'Cambio',
    'CartaDeCreditoDocumentario': 'CartaDeCreditoDocumentario',
    'CartaDeCreditoSimple': 'CartaDeCreditoSimple',
    'Cheque': 'Cheque',
    'ChequeCancelatorios': 'ChequeCancelatorios',
    'CreditoDocumentario': 'CreditoDocumentario',
    'CuentaCorriente': 'CuentaCorriente',
    'Deposito': 'Deposito',
    'Efectivo': 'Efectivo',
    'EndosoDeCheque': 'EndosoDeCheque',
    'FacturaDeCredito': 'FacturaDeCredito',
    'GarantiaBancaria': 'GarantiaBancaria',
    'Giro': 'Giro',
    'LetraDeCambio': 'LetraDeCambio',
    'MedioDePagoDeComercioExterior': 'MedioDePagoDeComercioExterior',
    'OrdenDePagoDocumentaria': 'OrdenDePagoDocumentaria',
    'OrdenDePagoSimple': 'OrdenDePagoSimple',
    'PagoContraReembolso': 'PagoContraReembolso',
    'RemesaDocumentaria': 'RemesaDocumentaria',
    'RemesaSimple': 'RemesaSimple',
    'TarjetaDeCredito': 'TarjetaDeCredito',
    'TarjetaDeDebito': 'TarjetaDeDebito',
    'Ticket': 'Ticket',
    'TransferenciaBancaria': 'TransferenciaBancaria',
    'TransferenciaNoBancaria': 'TransferenciaNoBancaria',
    'OtrosMediosPago': 'OtrosMediosPago'
}

# Constantes para tipos de documentos fiscales (Hasar 2G)
CODIGOCOMPROBANTE = {
    "NoDocumento": "NoDocumento",
    "ReciboA": "ReciboA",
    "ReciboB": "ReciboB",
    "ReciboC": "ReciboC",
    "ReciboM": "ReciboM",
    "InformeDiarioDeCierre": "InformeDiarioDeCierre",
    "TiqueFacturaA": "TiqueFacturaA",
    "TiqueFacturaB": "TiqueFacturaB",
    "Tique": "Tique",
    "RemitoR": "RemitoR",
    "TiqueNotaCredito": "TiqueNotaCredito",
    "TiqueFacturaC": "TiqueFacturaC",
    "TiqueNotaCreditoA": "TiqueNotaCreditoA",  # Nota: ¿Es correcto "Tique" o "Tique"?
    "TiqueNotaCreditoB": "TiqueNotaCreditoB",
    "TiqueNotaCreditoC": "TiqueNotaCreditoC",
    "TiqueNotaDebitoA": "TiqueNotaDebitoA",
    "TiqueNotaDebitoB": "TiqueNotaDebitoB",
    "TiqueNotaDebitoC": "TiqueNotaDebitoC",
    "TiqueFacturaM": "TiqueFacturaM",
    "TiqueNotaCreditoM": "TiqueNotaCreditoM",
    "TiqueNotaDebitoM": "TiqueNotaDebitoM",
    "RemitoX": "RemitoX",
    "ReciboX": "ReciboX",
    "PresupuestoX": "PresupuestoX",
    "InformeDeAuditoria": "InformeDeAuditoria",
    "ComprobanteDonacion": "ComprobanteDonacion",
    "Generico": "Generico",
    "MensajeCF": "MensajeCF",
    "EstadisticaDeVentaHorariaYPorRubro": "EstadisticaDeVentaHorariaYPorRubro",
    "DetalleDeVentas": "DetalleDeVentas",
    "CambioIVA": "CambioIVA",
    "CambioFechaHora": "CambioFechaHora",
    "CambioCategorizacionIVA": "CambioCategorizacionIVA",
    "CambioInscripcionIngBrutos": "CambioInscripcionIngBrutos",
    "PruebaPerifericos": "PruebaPerifericos"
}



class HasarRESTJson:
    def __init__(self, ip_impresora, usuario="", clave="9999"):
        self.ip_impresora = ip_impresora
        self.usuario = usuario
        self.clave = clave
        self.auth_token = base64.b64encode(f"{usuario}:{clave}".encode()).decode()
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Basic {self.auth_token}"
        }

    def estadoComandos(self):
        url = f"http://{self.ip_impresora}/comandos.json"
        body = {
            "Estado": {}
        }
        response = requests.get(url, headers=self.headers, data=json.dumps(body))
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error al consultar el estado: {response.status_code} - {response.text}")
        
    def cerrarJornadaFiscal(self, reporte="Z"):
        url = f"http://{self.ip_impresora}/fiscal.json"
        body = {
            "CerrarJornadaFiscal": {
                "Reporte": "Reporte"+reporte.capitalize()
            }
        }
        response = requests.post(url, headers=self.headers, data=json.dumps(body))
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error al cerrar la jornada fiscal: {response.status_code} - {response.text}")

    def consultarEstado(self):
        url = f"http://{self.ip_impresora}/fiscal.json"
        body = {
            "consultarEstado": {}
        }
        response = requests.get(url, headers=self.headers, data=json.dumps(body))
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error al consultar el estado: {response.status_code} - {response.text}")
        
    def abrirDocumento(self, codigo):
        """abre un documento fiscal

        Args:
            codigo (str): CODIGOCOMPROBANTE un string que representa el tipo de comprobante a abrir
            (Ejemplo: CODIGOCOMPROBANTE['ReciboA'])

        Raises:
            Exception: Exception si la respuesta no es 200

        Returns:
            json: {
                    "AbrirDocumento":
                    {
                        "Estado":
                        {
                            "Impresora" : [ ],
                            "Fiscal" : [ ]
                        },
                        "NumeroComprobante" : "00000004",
                        "IndiceAuditoria" : "1"
                    }
                }
        """
        url = f"http://{self.ip_impresora}/fiscal.json"
        body = {
            "AbrirDocumento": {
                "CodigoComprobante": codigo
            }
        }
        response = requests.post(url, headers=self.headers, data=json.dumps(body))
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error al abrir el documento: {response.status_code} - {response.text}")
        
    def imprimirItem(self, item: ItemFactura):
        url = f"http://{self.ip_impresora}/fiscal.json"
        body = item.to_dict()
        response = requests.post(url, headers=self.headers, data=json.dumps(body))

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error al imprimir el ítem: {response.status_code} - {response.text}")

    def imprimirDescuentoItem(self, descuento: Descuento):
        url = f"http://{self.ip_impresora}/fiscal.json"
        body = descuento.to_dict()
        response = requests.post(url, headers=self.headers, data=json.dumps(body))
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error al imprimir el descuento: {response.status_code} - {response.text}")

    def imprimirOtrosTributos(self, tributo: Tributo):
        url = f"http://{self.ip_impresora}/fiscal.json"
        body = tributo.to_dict()
        response = requests.post(url, headers=self.headers, data=json.dumps(body))
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error al imprimir el tributo: {response.status_code} - {response.text}")

    def imprimirPago(self, pago: Pago):
        url = f"http://{self.ip_impresora}/fiscal.json"
        body = pago.to_api_dict()
        response = requests.post(url, headers=self.headers, data=json.dumps(body))
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error al imprimir el pago: {response.status_code} - {response.text}")

    def cerrarDocumento(self, copias:int=1):
        url = f"http://{self.ip_impresora}/fiscal.json"
        body = {
            "CerrarDocumento": {
                "Copias": copias
            }
        }
        response = requests.post(url, headers=self.headers, data=json.dumps(body))
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error al cerrar el documento: {response.status_code} - {response.text}")
    

    def cancelarDocumento(self):
        url = f"http://{self.ip_impresora}/fiscal.json"
        body = {
            "Cancelar": {}
        }
        response = requests.post(url, headers=self.headers, data=json.dumps(body))
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error al cancelar el documento: {response.status_code} - {response.text}")
        
    def crearTicket(self, codigo, items:list, descuento:Descuento=None, tributo:Tributo=None, pago:Pago=None):
        try:
            res = self.abrirDocumento(codigo)
            for i in items:
                if isinstance(i, ItemFactura):
                    self.imprimirItem(i)
                else:
                    item = ItemFactura(**i)
                    self.imprimirItem(item)
            if descuento:
                self.imprimirDescuentoItem(descuento)
            if tributo:
                self.imprimirOtrosTributos(tributo)
            if pago:
                self.imprimirPago(pago)
            self.cerrarDocumento()
            return res.get('AbrirDocumento').get('NumeroComprobante')
        except Exception as e:
            print(f"Error al crear el comprobante: {e}")
            self.cancelarDocumento()
