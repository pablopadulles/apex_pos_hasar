import serial
import time

class HasarFiscalPrinter:
    def __init__(self, puerto='COM3', baudrate=9600):
        self.ser = serial.Serial(
            port=puerto,
            baudrate=baudrate,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            timeout=1
        )
    
    def cerrar(self):
        if self.ser.is_open:
            self.ser.close()
    
    def enviar_comando(self, comando_str):
        """Envía un comando formateado a la impresora."""
        paquete = self.armar_paquete(comando_str)
        print(f"Enviando: {paquete}")
        self.ser.write(paquete)
        time.sleep(0.5)
        respuesta = self.ser.read_all()
        print(f"Respuesta: {respuesta}")
        return respuesta

    def armar_paquete(self, comando_str):
        """Arma el paquete con STX, comando, ETX y BCC."""
        STX = b'\x02'
        ETX = b'\x03'
        datos = comando_str.encode('latin1')  # La impresora espera codificación latin1
        cuerpo = STX + datos + ETX
        bcc = self.calcular_bcc(cuerpo)
        return cuerpo + bytes([bcc])

    def calcular_bcc(self, datos):
        """Calcula el BCC como XOR de todos los bytes."""
        bcc = 0
        for b in datos:
            bcc ^= b
        return bcc

    def abrir_tique(self, tipo_factura=83):  # 83 = TIQUE
        """Abre un tique (por defecto un TIQUE)."""
        comando = f'\x30{tipo_factura}|'
        return self.enviar_comando(comando)

    def agregar_item(self, descripcion, cantidad, precio_unitario, iva=21.00):
        """
        Agrega un ítem al comprobante.

        - descripcion: texto
        - cantidad: cantidad vendida (ej: 1.0)
        - precio_unitario: precio antes de IVA
        - iva: porcentaje de IVA (default 21%)
        """
        # Armo el comando "Agregar ítem"
        comando = f'\x32{descripcion}|{cantidad:.3f}|{precio_unitario:.2f}|M|{iva:.2f}|0.00'
        return self.enviar_comando(comando)

    def cerrar_tique(self):
        """Cierra el tique."""
        comando = '\x38'  # Comando de cierre de comprobante
        return self.enviar_comando(comando)


    def prueba(self):
        """Ejemplo de prueba para enviar un comando simple."""
        # Comando de prueba para identificar la impresora
        # Esto es solo un ejemplo, deberías reemplazarlo por el comando real
        # que quieras enviar a la impresora.
        STX = '\x02'
        ETX = '\x03'

        comando = 'I0'  # Comando para identificar impresora
        mensaje = f"{STX}{comando}{ETX}"

        self.ser.write(mensaje.encode('ascii'))
        self.ser.flush()
        respuesta = self.ser.read_all().decode('ascii', errors='ignore')
        print(f"Respuesta cruda: {respuesta!r}")
