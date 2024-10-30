from gpiozero import Servo
from time import sleep

# Ajustes conservadores para el TowerPro MicroServo 9g
servo = Servo(14, min_pulse_width=0.001, max_pulse_width=0.002)

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

# Mover el servo entre las posiciones
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
