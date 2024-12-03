from gpiozero import Servo
from time import sleep

# Calibrar los valores de ancho de pulso (1 ms y 2 ms, según el servo)
# min_pulse_width y max_pulse_width son fracciones de 1 segundo
servo = Servo(14, min_pulse_width=0.0005, max_pulse_width=0.0025)

# Mover el servo a la posicion mnima (0 grados aproximadamente)
print("Posicion mnima")
servo.min()
sleep(2)

# Mover el servo a la posicion media (90 grados aproximadamente)
print("Posicion media")
servo.mid()
sleep(2)

# Mover el servo a la posicion mxima (180 grados aproximadamente)
print("Posicion mxima")
servo.max()
sleep(2)

# Hacer que el servo vaya de una posicion a otra lentamente
while True:
    print("Moviendo a mnimo")
    servo.min()
    sleep(1)
    print("Moviendo a medio")
    servo.mid()
    sleep(1)
    print("Moviendo a mximo")
    servo.max()
    sleep(1)
