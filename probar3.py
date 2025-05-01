import socket
import json

IMPRESORA_IP = '192.168.1.101'
IMPRESORA_PUERTO = 8082  # Verificá este dato en la config de red de la impresora

def enviar_json_a_impresora(json_data):
    mensaje = json.dumps(json_data).encode('utf-8')
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((IMPRESORA_IP, IMPRESORA_PUERTO))
        s.sendall(mensaje)
        respuesta = s.recv(4096)
        print("Respuesta:", respuesta.decode())

# Paso 1: Abrir documento (comprobante tipo ticket)
abrir_documento = {
    "comando": "A",  # Comando para abrir un comprobante (confirmalo en la documentación JSON)
    "tipo": "T",     # Tique
    "id": 1
}
enviar_json_a_impresora(abrir_documento)

# Paso 2: Agregar ítem
agregar_item = {
    "comando": "B",  # Comando para agregar ítem
    "descripcion": "Producto de prueba",
    "cantidad": 1.0,
    "precio": 100.0,
    "iva": 21.0,
    "id": 2
}
enviar_json_a_impresora(agregar_item)

# Paso 3: Cerrar documento
cerrar_documento = {
    "comando": "C",  # Comando para cerrar comprobante
    "id": 3
}
enviar_json_a_impresora(cerrar_documento)
