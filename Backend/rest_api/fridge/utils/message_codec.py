import json 

class MessageCodec:
    def __init__(self, delimiter="/"):
        self.delimiter = delimiter

    def decode(self, message):
        """
        Decodifica un mensaje en formato 'session-id-1/coca-cola-0/lays-0/oreo-0'
        a un diccionario JSON.
        """
        try:
            # Separar por el delimitador
            parts = message.split(self.delimiter)
            # Crear el diccionario
            data = {}
            for part in parts:
                key, value = part.rsplit("-", 1)
                data[key] = int(value)
            return data
        except (ValueError, IndexError) as e:
            raise ValueError("Formato de mensaje inválido") from e

    def encode(self, data):
        """
        Codifica un diccionario JSON a un mensaje en formato 'session-id-1/coca-cola-0/lays-0/oreo-0'.
        """
        try:
            # Crear el mensaje concatenando las claves y valores
            parts = [f"{key}-{value}" for key, value in data.items()]
            return self.delimiter.join(parts)
        except AttributeError as e:
            raise ValueError("El input debe ser un diccionario válido") from e


# Ejemplo de uso
# if __name__ == "__main__":
#     codec = MessageCodec()
    
#     # Decodificar
#     message = "session-id-1/coca-cola-0/lays-0/oreo-0"
#     decoded = codec.decode(message)
#     print("Decodificado:", decoded)
    
#     # Codificar
#     data = {"session-id": 1, "coca-cola": 1, "lays": 0, "oreo": 0}
#     encoded = codec.encode(data)
#     print("Codificado:", encoded)