import zmq
import threading

def start_zmq_server(ip="127.0.0.1", port_push=5555, port_pull=5556):
    """
    Inicia un servidor ZMQ que escucha mensajes en un socket PUSH y envía mensajes en un socket PULL.

    :param ip: Dirección IP del servidor (por defecto, 127.0.0.1).
    :param port_push: Puerto para el socket PULL que recibe mensajes del cliente.
    :param port_pull: Puerto para el socket PUSH que envía mensajes al cliente.
    """
    print(f"[INFO] Iniciando servidor ZMQ en {ip}...")

    # Crear contexto de ZMQ
    context = zmq.Context()

    # Configurar socket PULL para recibir mensajes
    pull_socket = context.socket(zmq.PULL)
    pull_socket.bind(f"tcp://{ip}:{port_push}")
    print(f"[INFO] Socket PULL escuchando en tcp://{ip}:{port_push}")

    # Configurar socket PUSH para enviar mensajes
    push_socket = context.socket(zmq.PUSH)
    push_socket.bind(f"tcp://{ip}:{port_pull}")
    print(f"[INFO] Socket PUSH escuchando en tcp://{ip}:{port_pull}")

    # Bandera para controlar la ejecución del servidor
    running = True

    def receive_messages():
        """Hilo que escucha y procesa mensajes recibidos en el socket PULL."""
        print("[INFO] Hilo de recepción de mensajes iniciado.")
        while running:
            try:
                message = pull_socket.recv_string(flags=0)  # Bloquea hasta recibir un mensaje
                print(f"[INFO] Mensaje recibido: {message}")
            except zmq.ZMQError as e:
                print(f"[ERROR] Error al recibir mensaje: {e}")

    # Iniciar hilo para recibir mensajes
    receive_thread = threading.Thread(target=receive_messages, daemon=True)
    receive_thread.start()

    print("[INFO] Servidor listo para enviar mensajes.")
    try:
        while running:
            # Permitir al usuario enviar mensajes manualmente desde el servidor
            message = input("Ingrese un mensaje para enviar ('exit' para salir): ")
            if message.lower() == "exit":
                running = False
                break
            try:
                push_socket.send_string(message)
                print(f"[INFO] Mensaje enviado: {message}")
            except zmq.ZMQError as e:
                print(f"[ERROR] Error al enviar mensaje: {e}")
    except KeyboardInterrupt:
        print("[INFO] Servidor detenido manualmente.")
    finally:
        # Cerrar sockets y contexto
        print("[INFO] Cerrando servidor ZMQ...")
        receive_thread.join(timeout=1)
        pull_socket.close()
        push_socket.close()
        context.term()
        print("[INFO] Servidor ZMQ cerrado correctamente.")

if __name__ == "__main__":
    start_zmq_server()