from time import sleep
import servo_control

try:
    # Configuración inicial
    servo_control.setup(pin=14)  # Cambia el pin si es necesario

    # Comandos para el servo
    servo_control.open_door()  # Abre la puerta
    sleep(2)                   # Espera 2 segundos
    servo_control.close_door() # Cierra la puerta

finally:
    # Limpieza de recursos
    servo_control.cleanup()
