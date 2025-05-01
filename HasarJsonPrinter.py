import serial
import json
import time

class HasarJsonPrinter:
    def __init__(self, puerto='/dev/ttyUSB0', baudrate=9600):
        self.ser = serial.Serial(
            port=puerto,
            baudrate=baudrate,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            timeout=2
        )

    def cerrar(self):
        if self.ser.is_open:
            self.ser.close()

    def enviar_comando_json(self, comando_dict):
        """Envía un diccionario como JSON y espera respuesta."""
        json_str = json.dumps(comando_dict) + '\n'
        print(f"Enviando: {json_str}")
        self.ser.write(json_str.encode('utf-8'))
        self.ser.flush()
        time.sleep(0.5)
        respuesta = self.ser.readline().decode('utf-8').strip()
        print(f"Respuesta: {respuesta}")
        print(f"Respuesta cruda: {respuesta!r}")
        return json.loads(respuesta)

    def estado_impresora(self):
        """Ejemplo: consulta de estado."""
        cmd = {
            "idComando": 100,
            "params": {}
        }
        return self.enviar_comando_json(cmd)
