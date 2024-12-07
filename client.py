import zmq

def run_client(backend_ip="127.0.0.1", backend_port=5555, send_port=5556, switch_message="iniciar"):
    """
    Cliente ZeroMQ en modo REP que escucha mensajes. 
    Cuando recibe un mensaje específico, cambia al modo de envío y envía un mensaje predeterminado.

    :param backend_ip: Dirección IP del backend.
    :param backend_port: Puerto del backend para recibir mensajes (modo REP).
    :param send_port: Puerto del backend para enviar mensajes (modo PUSH).
    :param switch_message: Mensaje que activa el cambio al modo de envío.
    """
    context = zmq.Context()
    socket = context.socket(zmq.REP)  # Socket REP para escuchar mensajes
    socket.bind(f"tcp://{backend_ip}:{backend_port}")

    print(f"Cliente ZeroMQ escuchando en tcp://{backend_ip}:{backend_port}...")

    try:
        while True:
            # Espera un mensaje del backend
            message = socket.recv_string()
            print(f"Mensaje recibido del backend: {message}")

            # Procesar el mensaje recibido
            if message == switch_message:
                print("Mensaje de activación recibido. Cambiando al modo de envío.")
                socket.send_string(f"ACK: {message}")  # Enviar respuesta antes de salir
                break  # Salir del bucle para cambiar al modo de envío
            else:
                response = f"ACK: {message}"
                socket.send_string(response)
                print(f"Respuesta enviada al backend: {response}")

        # Cambiar al modo de envío y enviar mensaje predeterminado
        send_test_message(context, backend_ip, send_port)

    except KeyboardInterrupt:
        print("\nCliente detenido manualmente.")
    except Exception as e:
        print(f"Error en el cliente: {e}")
    finally:
        socket.close()
        context.term()
        print("Conexión ZeroMQ cerrada.")

def send_test_message(context, backend_ip="127.0.0.1", backend_port=5556):
    """
    Envía un mensaje predeterminado al backend después de cambiar al modo de envío.

    :param context: Contexto ZeroMQ compartido.
    :param backend_ip: Dirección IP del backend.
    :param backend_port: Puerto del backend (PUSH).
    """
    socket = context.socket(zmq.PUSH)  # Cambia a PUSH para enviar mensajes
    socket.connect(f"tcp://{backend_ip}:{backend_port}")
    print(f"Modo de envío activado. Conectado a tcp://{backend_ip}:{backend_port}...")

    try:
        # Mensaje predeterminado
        message = "TEST"
        print(f"Enviando mensaje predeterminado: {message}")
        socket.send_string(message)
        print("Mensaje enviado exitosamente.")
    except Exception as e:
        print(f"Error al enviar mensaje: {e}")
    finally:
        socket.close()

if __name__ == "__main__":
    run_client()
