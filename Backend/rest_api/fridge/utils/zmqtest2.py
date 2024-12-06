import zmq
from decouple import config

class ZMQConnection:
    def __init__(self):
        """
        Inicializa la conexión ZMQ utilizando las variables de entorno definidas.
        """
        self.ip = config('ZMQ_IP', default='127.0.0.1')
        self.port = config('ZMQ_PORT', default='5555')

        # Crear contexto y socket ZMQ
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)  # Patrón REQ/REP
        self.socket.connect(f"tcp://{self.ip}:{self.port}")

        # Imprimir estado de la conexión
        print(f"Conectado a ZMQ en tcp://{self.ip}:{self.port}")

    def send_message(self, message):
        """
        Envía un mensaje a través de ZMQ.

        :param message: Mensaje a enviar (string o bytes)
        :return: Respuesta recibida del servidor
        """
        try:
            # Enviar mensaje
            self.socket.send_string(message) if isinstance(message, str) else self.socket.send(message)
            # Recibir respuesta
            response = self.socket.recv_string()
            return response
        except Exception as e:
            raise RuntimeError(f"Error al enviar mensaje: {e}")

    def receive_message(self):
        """
        Queda ocioso esperando un mensaje desde el servidor ZMQ.

        :return: Mensaje recibido (string)
        """
        try:
            print("Esperando mensaje...")
            # Bloquea hasta recibir un mensaje
            message = self.socket.recv_string()
            print(f"Mensaje recibido: {message}")
            return message
        except Exception as e:
            raise RuntimeError(f"Error al recibir mensaje: {e}")

    def close_connection(self):
        """
        Cierra la conexión ZMQ.
        """
        self.socket.close()
        self.context.term()
        print("Conexión ZMQ cerrada.")


# Inicialización de la conexión ZMQ
if __name__ == "__main__":
    zmq_connection = ZMQConnection()

    try:
        # Ejemplo de enviar un mensaje
        response = zmq_connection.send_message("Hola desde el cliente")
        print(f"Respuesta recibida: {response}")

        # Ejemplo de recibir un mensaje (bloqueante)
        received_message = zmq_connection.receive_message()
        print(f"Mensaje recibido: {received_message}")

    finally:
        zmq_connection.close_connection()
