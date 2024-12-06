import zmq

def run_receptor():
    """
    Simula la Raspberry Pi escuchando mensajes del backend.
    """
    context = zmq.Context()
    socket = context.socket(zmq.REP)  # REQ/REP pattern
    socket.bind("tcp://*:5555")  # Cambia el puerto si es necesario

    print("Receptor ZeroMQ escuchando en tcp://*:5555...")

    while True:
        try:
            # Recibe mensaje del backend
            message = socket.recv_string()
            print(type(message))
            print(f"Mensaje recibido: {message}")
            
            # Envía una respuesta al backend
            socket.send_string("respuesta")
        except Exception as e:
            print(f"Error en el receptor: {e}")
            socket.send_string({"status": "error", "message": str(e)})

def send_message_to_receptor(message, receptor_ip="192.168.1.170", receptor_port=5555):
    """
    Envía un mensaje al receptor ZeroMQ y espera una respuesta.

    :param message: Mensaje a enviar (string).
    :param receptor_ip: Dirección IP del receptor (por defecto: localhost).
    :param receptor_port: Puerto del receptor (por defecto: 5555).
    :return: Respuesta recibida del receptor.
    """
    context = zmq.Context()
    socket = context.socket(zmq.REQ)  # Patrón REQ/REP
    socket.connect(f"tcp://{receptor_ip}:{receptor_port}")

    try:
        print(f"Enviando mensaje al receptor: {message}")
        socket.send_string(message)  # Enviar mensaje al receptor

        # Esperar respuesta
        response = socket.recv_string()
        print(f"Respuesta recibida: {response}")
        return response
    except Exception as e:
        print(f"Error al enviar mensaje: {e}")
        return None
    finally:
        socket.close()
        context.term()

if __name__ == "__main__":
    run_receptor()
    send_message_to_receptor('hola')
    send_message_to_receptor('hola123')

