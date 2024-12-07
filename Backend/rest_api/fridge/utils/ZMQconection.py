import zmq
from decouple import config
import threading


class ZMQConnection:
    def __init__(self):
        """
        Inicializa la conexión ZMQ utilizando las variables de entorno definidas.
        """
        # Configuración para envío de mensajes
        self.send_ip = config('ZMQ_SEND_IP', default='127.0.0.1')
        self.send_port = config('ZMQ_SEND_PORT', default='5555')  # Puerto para enviar

        # Configuración para recepción de mensajes
        self.receive_ip = config('ZMQ_RECEIVE_IP', default='127.0.0.1')
        self.receive_port = config('ZMQ_RECEIVE_PORT', default='5556')  # Puerto para recibir

        # Contexto ZMQ
        self.context = zmq.Context()

        # Socket para enviar mensajes (REQ o PUSH)
        self.send_socket = self.context.socket(zmq.REQ)
        self.send_socket.connect(f"tcp://{self.send_ip}:{self.send_port}")
        print(f"Socket de envío conectado a tcp://{self.send_ip}:{self.send_port}")

        # Socket para recibir mensajes (PULL)
        self.receive_socket = self.context.socket(zmq.PULL)
        self.receive_socket.bind(f"tcp://{self.receive_ip}:{self.receive_port}")
        print(f"Socket de recepción escuchando en tcp://{self.receive_ip}:{self.receive_port}")

        # Almacén de mensajes recibidos
        self.received_messages = []

        # Hilo para escuchar mensajes
        self.listener_thread = None

    def send_message(self, message):
        """
        Envía un mensaje a través del socket de envío.
        :param message: Mensaje a enviar (string o bytes).
        :return: Respuesta recibida (si aplica).
        """
        try:
            self.send_socket.send_string(message) if isinstance(message, str) else self.send_socket.send(message)
            response = self.send_socket.recv_string()
            return response
        except Exception as e:
            raise RuntimeError(f"Error al enviar mensaje: {e}")

    def start_listener(self):
        """
        Inicia un hilo separado para escuchar mensajes de forma continua.
        """
        if self.listener_thread is None:
            self.listener_thread = threading.Thread(target=self._listen_for_messages, daemon=True)
            self.listener_thread.start()

    def _listen_for_messages(self):
        """
        Método interno para recibir mensajes continuamente.
        """
        while True:
            try:
                message = self.receive_socket.recv_string(flags=zmq.NOBLOCK)
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
