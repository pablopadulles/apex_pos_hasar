import serial

STX = b'\x02'
ETX = b'\x03'
ESC = b'\x1B'
FS = b'\x1C'

def calcular_bcc(data: bytes) -> bytes:
    """Calcula el BCC: suma de todos los bytes en 2 bytes binarios, representado en 4 caracteres hexadecimales."""
    suma = sum(data)
    bcc = f"{suma & 0xFFFF:04X}".encode('ascii')  # suma de 2 bytes
    return bcc

def armar_paquete_fiscal(sn=0x20, id_cmd=b'I', campos=[]):
    cuerpo = ESC + id_cmd + FS + FS.join(c.encode('cp437') for c in campos)
    paquete = bytes([sn]) + cuerpo
    completo = STX + paquete + ETX
    bcc = calcular_bcc(completo)
    return completo + bcc

# Parámetros de ejemplo para abrir un comprobante tipo “Tique”
campos = [
    'T',  # Tipo de comprobante: Tique
    '', '', '', '',  # Cliente sin datos
    '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
]

paquete = armar_paquete_fiscal(campos=campos)

# Enviar por puerto
with serial.Serial('/dev/ttyACM0', baudrate=115200, timeout=1) as ser:
    print("Enviando paquete:", paquete)
    ser.write(paquete)
    respuesta = ser.read(512)
    print("Respuesta:", respuesta)
