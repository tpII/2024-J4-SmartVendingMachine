def decode_message(message):
    """
    Decodifica un mensaje recibido.

    Args:
        message (str): Mensaje recibido.

    Returns:
        str: Acción decodificada ('start' o 'stop').

    Raises:
        ValueError: Si el mensaje no es válido.
    """
    message = message.strip().lower()
    if message in ["start", "stop"]:
        return message
    else:
        return "loop"
    

def encode_difference_message(difference):
    """
    Codifica la diferencia entre dos diccionarios en un mensaje formateado.

    Args:
        difference (dict): Diccionario con las diferencias calculadas.

    Returns:
        str: Mensaje codificado en el formato 'coca-cola-cantidad/lays-cantidad/oreo-cantidad'.
    """
    components = [f"{key}-{value}" for key, value in difference.items()]
    return "/".join(components)

