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

if __name__ == "__main__":
    run_receptor()
