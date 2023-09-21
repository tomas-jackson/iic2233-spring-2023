from typing import List
import json
from errors import JsonError, SequenceError


def serializar_diccionario(dictionary: dict) -> bytearray:
    try:
        serializacion = json.dumps(dictionary)
        return bytearray(serializacion.encode('utf-8'))
    except TypeError:
        raise JsonError


def verificar_secuencia(mensaje: bytearray, secuencia: List[int]) -> None:
    mayor_num = max(secuencia)
    unicos = True
    for entry in secuencia:
        repeat = secuencia.count(entry)
        if repeat > 1:
            unicos = False
    if len(mensaje) < mayor_num or unicos is False:
        raise SequenceError
    else:
        return None


def codificar_secuencia(secuencia: List[int]) -> bytearray:
    bytes_text = b''
    for entero in secuencia:
        bytes_text += entero.to_bytes(2, 'big')
    return bytearray(bytes_text)


def codificar_largo(largo: int) -> bytearray:
    largo_byte = largo.to_bytes(4, 'big')
    return bytearray(largo_byte)


def separar_msg(mensaje: bytearray, secuencia: List[int]) -> List[bytearray]:
    m_bytes_secuencia = bytearray()
    m_reducido = bytearray()
    for index in secuencia:
        m_bytes_secuencia.append(mensaje[index])
    anti_secuencia = [i for i in range(len(mensaje)) if i not in secuencia]
    for index in anti_secuencia:
        m_reducido.append(mensaje[index])
    return [m_bytes_secuencia, m_reducido]


def encriptar(mensaje: dict, secuencia: List[int]) -> bytearray:
    verificar_secuencia(mensaje, secuencia)

    m_bytes_secuencia, m_reducido = separar_msg(mensaje, secuencia)
    secuencia_codificada = codificar_secuencia(secuencia)

    return (
        codificar_largo(len(secuencia))
        + m_bytes_secuencia
        + m_reducido
        + secuencia_codificada
    )


if __name__ == "__main__":
    original = serializar_diccionario({"tama": 1})
    encriptado = encriptar(original, [1, 5, 10, 3])
    print(original)
    print(encriptado)
