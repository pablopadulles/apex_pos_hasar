import serial
import json

ser = serial.Serial('/dev/ttyACM0', baudrate=115200, timeout=1)

# Enviar ENQ
print("Enviando ENQ...")
ser.write(b'\x05')
ack = ser.read(1)
print("Respuesta ENQ:", ack)

if ack == b'\x06':
    # Crear JSON válido
    comando = {
        "AbrirDocumento": {
            "CodigoComprobante": "TiqueFacturaB"
        }
    }
    json_bytes = json.dumps(comando).encode('utf-8')
    ser.write(json_bytes.encode('utf-8'))
    ser.flush()
    respuesta = ser.readline().decode('utf-8').strip()
    print(f"Respuesta: {respuesta}")
    print(f"Respuesta cruda: {respuesta!r}")

    

ser.close()
