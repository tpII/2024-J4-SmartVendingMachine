import zmq
from decouple import config
import threading


class ZMQConnection:
    def __init__(self):
        """
        Inicializa la conexión ZMQ utilizando las variables de entorno definidas.
        """

        # Configuración para recepción de mensajes
        # Almacén de mensajes recibidos
        self.received_messages = []

        # Hilo para escuchar mensajes
        self.listener_thread = None
        

    def send_message(self, message):
        context = zmq.Context()
        socket = context.socket(zmq.REQ)  # Socket REQ para enviar mensajes y recibir respuesta
        socket.connect(f"tcp://127.0.0.1:5555")
        """
        Envía un mensaje a través del socket de envío.
        :param message: Mensaje a enviar (string o bytes).
        :return: Respuesta recibida (si aplica).
        """
        try:
            print(f"Enviando mensaje al cliente: {message}")
            socket.send_string(message)  # Enviar mensaje al cliente

            # Esperar respuesta del cliente
            response = socket.recv_string()
            self.received_messages.append(response)
            print(f"Respuesta del cliente: {response}")
            return response
        except Exception as e:
            print(f"Error al comunicarse con el cliente: {e}")
            return None
        finally:
            socket.close()
            context.term()

    

    def _listen_for_messages(self, m):
        """
        Método interno para recibir mensajes continuamente.
        """
        while True:
            try:
                message = self.recv_string(flags=zmq.NOBLOCK)
                print(f"Mensaje recibido: {message}")
                self.received_messages.append(message)
            except zmq.Again:
                # No hay mensajes disponibles, continuar
                continue

    def get_received_messages(self):
        """
        Devuelve los mensajes recibidos hasta el momento.
        """
        return self.received_messages

    def close_connection(self):
        """
        Cierra ambos sockets y el contexto ZMQ.
        """
        self.send_socket.close()
        self.receive_socket.close()
        self.context.term()
        print("Conexión ZMQ cerrada.")
