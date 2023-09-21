'''
este archivo contiene las funciones que se preocupan de la encriptacion y codificacion del mensaje,
entre cliente y servidor
'''


def desplazar_bytes_derecha(byte_list: bytearray, offset: int) -> bytearray:
    '''
    mueve los bytes de un array a la derecha, segun la cantidad de offset,
    los bytes que llegan al final se mueven al inicio del array
    '''
    for _ in range(offset):
        byte_list = bytearray([byte_list[-1]]) + byte_list[:len(byte_list) - 1]
    return byte_list


def desplazar_bytes_izquierda(byte_list: bytearray, offset: int) -> bytearray:
    '''
    mueve los bytes de un array a la izquierda, segun la cantidad de offset,
    los bytes que llegan al inicio se mueven al final del array
    '''
    for _ in range(offset):
        byte_list = byte_list[1:] + bytearray([byte_list[0]])
    return byte_list


def intercambiar_byte(byte_list: bytearray, target: int) -> bytearray:
    '''
    cambia el byte en el indice 0 por el del indice target y vice versa,
    sirve para encriptar tanto como para desencriptar
    '''
    try:
        new_start = bytearray([byte_list[target]])
        new_target = bytearray([byte_list[0]])
        start_to_target = byte_list[1:target]
        target_to_finish = byte_list[target + 1:]
        return new_start + start_to_target + new_target + target_to_finish
    except IndexError:
        return byte_list


def encriptar_bytes(byte_sequence: bytes, n_ponderador: int) -> bytes:
    '''
    encripta los bytes
    '''
    byte_list = bytearray(byte_sequence)
    desplazado = desplazar_bytes_derecha(byte_list, n_ponderador)
    intercambiado = intercambiar_byte(desplazado, n_ponderador)
    return bytes(intercambiado)


def desencriptar_bytes(byte_sequence: bytes, n_ponderador: int) -> bytes:
    '''
    desencripta los bytes
    '''
    byte_list = bytearray(byte_sequence)
    desintercambio = intercambiar_byte(byte_list, n_ponderador)
    desplazado = desplazar_bytes_izquierda(desintercambio, n_ponderador)
    return bytes(desplazado)


def chunkificador(message: bytearray) -> list:
    '''
    divide un bytearray en chunks de 128 bytes, rellena con bytes
    '''
    chunks = []
    for i in range(0, len(message), 128):
        chunk = message[i:i + 128]
        if len(chunk) != 128:
            diff = 128 - len(chunk)
            fill = bytearray(diff)
            chunk += fill
        chunks.append(chunk)
    return chunks


def codificar(byte_sequence: bytearray) -> bytearray:
    '''
    codifica el mensaje segun lo pedido en el enunciado
    '''
    length_section = bytearray(int.to_bytes(len(byte_sequence), 4, 'little'))
    chunks = chunkificador(byte_sequence)
    final = length_section
    for i in range(len(chunks)):
        spot = int.to_bytes(i, 4, 'big')
        chunk = chunks[i]
        final += spot + chunk
    return final


def decodificar(byte_sequence: bytearray):
    '''
    decodifica el mensaje segun lo pedido por el enunciado
    '''
    length = int.from_bytes(byte_sequence[:4], 'little')
    final_message = byte_sequence[4:]
    decoded = bytearray()
    for i in range(0, len(final_message), 132):
        chunk = final_message[i:i + 132]
        int.from_bytes(chunk[:4], 'big')
        decoded += chunk[4:]
    return decoded[:length]


def procesar_mensaje(byte_sequence: bytearray, n_pond: int) -> bytearray:
    '''
    lleva a cabo todo el procesamiento del mensaje para encriptarlo y codificarlo
    '''
    encriptado = encriptar_bytes(byte_sequence, n_pond)
    codificado = codificar(encriptado)
    return codificado


def recuperar_mensaje(byte_sequence: bytearray, n_pond: int) -> bytearray:
    '''
    deshace la codificacion y encriptacion del mensaje, retornando el mensaje original
    '''
    decodificado = decodificar(byte_sequence)
    desencriptado = desencriptar_bytes(decodificado, n_pond)
    return desencriptado


def encriptar(msg: bytearray, ID) -> bytearray:
    return encriptar_bytes(msg, ID)


def desencriptar(msg: bytearray, ID):
    return desencriptar_bytes(msg, ID)


if __name__ == "__main__":
    # Testear encriptar
    N = 1
    msg_original = bytearray(b'\x01\x02\x03\x04\x05\x06\x07\x08\x09\x00\x01\x02\x03\x04\x05')
    msg_esperado = bytearray(b'\x01\x05\x02\x03\x04\x05\x06\x07\x08\x09\x00\x01\x02\x03\x04')

    msg_encriptado = encriptar(msg_original, N)
    if msg_encriptado != msg_esperado:
        print("[ERROR] Mensaje escriptado erroneamente")
    else:
        print("[SUCCESSFUL] Mensaje escriptado correctamente")

    # Testear desencriptar
    msg_desencriptado = desencriptar(msg_esperado, N)
    if msg_desencriptado != msg_original:
        print("[ERROR] Mensaje descencriptado erroneamente")
    else:
        print("[SUCCESSFUL] Mensaje descencriptado correctamente")
