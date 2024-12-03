import zmq
import time

context = zmq.Context()

# Socket para enviar mensajes a Dispositivo B
sender = context.socket(zmq.PUSH)
sender.connect("tcp://192.168.1.115:5555")  # Reemplaza <ip_dispositivo_B> con la IP del dispositivo B

# Socket para recibir mensajes de Dispositivo B
receiver = context.socket(zmq.PULL)
receiver.bind("tcp://*:5556")

while True:
    # Enviar mensaje a Dispositivo B
    message_to_send = input("Dispositivo A - Ingresa el mensaje a enviar (o escribe 'salir' para terminar): ")
    if message_to_send.lower() == 'salir':
        print("Finalizando Dispositivo A.")
        break
    sender.send_string(message_to_send)
    print("Dispositivo A envio:", message_to_send)

    # Intentar recibir mensaje de Dispositivo B (de manera no bloqueante)
    try:
        message_received = receiver.recv_string(flags=zmq.NOBLOCK)
        print("Dispositivo A recibio:", message_received)
    except zmq.Again:
        pass  # No hay mensajes nuevos, continuar el loop

    time.sleep(1)  # Pausa de 1 segundo antes de la proxima iteracion
