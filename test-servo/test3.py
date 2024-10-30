from gpiozero import Servo
from time import sleep

# Calibrar los valores de ancho de pulso (1 ms y 2 ms, según el servo)
# min_pulse_width y max_pulse_width son fracciones de 1 segundo
servo = Servo(14, min_pulse_width=0.0005, max_pulse_width=0.0025)

# Mover el servo a la posición mínima (0 grados aproximadamente)
print("Posición mínima")
servo.min()
sleep(2)

# Mover el servo a la posición media (90 grados aproximadamente)
print("Posición media")
servo.mid()
sleep(2)

# Mover el servo a la posición máxima (180 grados aproximadamente)
print("Posición máxima")
servo.max()
sleep(2)

# Hacer que el servo vaya de una posición a otra lentamente
while True:
    print("Moviendo a mínimo")
    servo.min()
    sleep(1)
    print("Moviendo a medio")
    servo.mid()
    sleep(1)
    print("Moviendo a máximo")
    servo.max()
    sleep(1)
