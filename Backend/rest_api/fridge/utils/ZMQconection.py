


#   DISCLAIMER:
#       LA FUNCION DE RECEPCION ESTA MAL, LA TERMINO ESTA NOCHE
#       AHORA NO SE QUEDA OSCIOSO ESPERANDO LOS MENSAJES SI NO QUE ES EVENT-DRIVEN
#           .Tom


import zmq
from decouple import config

class ZMQConnection:
    def __init__(self):
        """
        inicializa la conexión ZMQ utilizando las variables de entorno definidas.
        """
        self.ip = config('ZMQ_IP', default='127.0.0.1')
        self.port = config('ZMQ_PORT', default='5555')
        self.timeout = int(config('ZMQ_TIMEOUT', default='5000'))  # en milisegundos

        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)
        self.socket.connect(f"tcp://{self.ip}:{self.port}")
        self.socket.setsockopt(zmq.RCVTIMEO, self.timeout)
        print(f"Conectado a ZMQ en tcp://{self.ip}:{self.port}")

    def send_message(self, message):
        """
        envia un mensaje a través de ZMQ.

        :param message: Mensaje a enviar (string o bytes)
        :return: Respuesta recibida del servidor
        """
        try:
            self.socket.send_string(message) if isinstance(message, str) else self.socket.send(message)
            response = self.socket.recv_string()
            return response
        except zmq.error.Again:
            raise ConnectionError("No se recibió respuesta dentro del tiempo establecido.")
        except Exception as e:
            raise RuntimeError(f"Error al enviar mensaje: {e}")

    def receive_message(self):
        """
        recibe un mensaje desde el servidor ZMQ.

        :return: mensaje recibido (string)
        """
        try:
            message = self.socket.recv_string()
            return message
        except zmq.error.Again:
            raise ConnectionError("No se recibió un mensaje dentro del tiempo establecido.")
        except Exception as e:
            raise RuntimeError(f"Error al recibir mensaje: {e}")

    def close_connection(self):
        """
        cierra la conexion ZMQ.
        """
        self.socket.close()
        self.context.term()
        print("Conexión ZMQ cerrada.")

zmq_conection = ZMQConnection()