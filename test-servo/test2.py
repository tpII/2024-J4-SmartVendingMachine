from gpiozero import Servo
from time import sleep

# Ajustes conservadores para el TowerPro MicroServo 9g
servo = Servo(14, min_pulse_width=0.001, max_pulse_width=0.002)

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

# Mover el servo entre las posiciones
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
