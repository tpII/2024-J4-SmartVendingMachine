import zmq
import time

context = zmq.Context()

# Socket para enviar mensajes a Dispositivo A
sender = context.socket(zmq.PUSH)
sender.connect("tcp://192.168.1.38:5555")  # Reemplaza <ip_dispositivo_A> con la IP del dispositivo A

# Socket para recibir mensajes de Dispositivo A
receiver = context.socket(zmq.PULL)
receiver.bind("tcp://*:5555")

while True:
    # Enviar mensaje a Dispositivo A
    message_to_send = input("Dispositivo B - Ingresa el mensaje a enviar (o escribe 'salir' para terminar): ")
    if message_to_send.lower() == 'salir':
        print("Finalizando Dispositivo B.")
        break
    sender.send_string(message_to_send)
    print("Dispositivo B envio:", message_to_send)

    # Intentar recibir mensaje de Dispositivo A (de manera no bloqueante)
    try:
        message_received = receiver.recv_string(flags=zmq.NOBLOCK)
        print("Dispositivo B recibio:", message_received)
    except zmq.Again:
        pass  # No hay mensajes nuevos, continuar el loop

    time.sleep(1)  # Pausa de 1 segundo antes de la proxima iteracion
