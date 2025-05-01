import serial

# Abre el puerto serial
ser = serial.Serial('/dev/ttyACM0', baudrate=115200, timeout=1)

# Ejemplo: comando de prueba (deberías reemplazar esto por el comando Hasar real)
comando = b'\x05'  # Esto es solo un ejemplo
# comando = b'\x02@\x03'  # Esto es solo un ejemplo
ser.write(comando)

# Leer la respuesta
respuesta = ser.read(100)
print("Respuesta:", respuesta)

ser.close()