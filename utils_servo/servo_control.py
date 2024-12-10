import RPi.GPIO as GPIO
from time import sleep

# Variable global para el PWM
pwm = None
SERVO_PIN = 14  # Pin predeterminado; puedes cambiarlo al usar setup()


def setup(pin=14):
    """
    Configura el pin GPIO y el PWM para el servomotor.
    :param pin: Pin GPIO al que está conectado el servo (default: 14).
    """
    global pwm, SERVO_PIN
    SERVO_PIN = pin
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(SERVO_PIN, GPIO.OUT)
    pwm = GPIO.PWM(SERVO_PIN, 50)  # Frecuencia estándar para servos (50 Hz)
    pwm.start(0)  # Inicia con 0% de ciclo de trabajo
    print(f"Servo configurado en el pin {SERVO_PIN} con PWM a 50Hz.")


def set_angle(angle):
    """
    Mueve el servo al ángulo especificado.
    Los servos típicos trabajan con ángulos entre 0° y 180°,
    y requieren un ciclo de trabajo (duty cycle) entre 2% y 12%.
    """
    if pwm is None:
        raise RuntimeError("Debes llamar a setup() antes de usar set_angle().")
    duty = 2 + (angle / 18)  # Conversión de ángulo a ciclo de trabajo
    print(f"Moviendo servo a {angle}° (Duty cycle: {duty:.2f}%)")
    pwm.ChangeDutyCycle(duty)
    sleep(0.5)  # Esperar para que el servo se mueva
    pwm.ChangeDutyCycle(0)  # Detener la señal para evitar micromovimientos


def open_door():
    """
    Mueve el servo a la posición de "puerta abierta" (90°).
    """
    print("Abriendo la puerta...")
    set_angle(90)


def close_door():
    """
    Mueve el servo a la posición de "puerta cerrada" (180°).
    """
    print("Cerrando la puerta...")
    set_angle(180)


def cleanup():
    """
    Limpia los recursos GPIO.
    """
    if pwm is not None:
        pwm.stop()
    GPIO.cleanup()
    print("Recursos GPIO limpiados.")
