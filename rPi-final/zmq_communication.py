import zmq

def setup_communication():
    context = zmq.Context()

    sender = context.socket(zmq.PUSH)
    sender.connect("tcp://192.168.1.47:5556")

    receiver = context.socket(zmq.PULL)
    receiver.bind("tcp://*:5555")

    print("Sockets configurados para la comunicación.")
    return {"sender": sender, "receiver": receiver}


def send_message(sender, message):
    sender.send_string(message)
    print(f"Mensaje enviado: {message}")


def receive_message(receiver):
    try:
        message = receiver.recv_string(flags=zmq.NOBLOCK)
        return message
    except zmq.Again:
        return "loop"
