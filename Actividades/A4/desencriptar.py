from typing import List
import json
from json import JSONDecodeError
from errors import JsonError, SequenceError


def deserializar_diccionario(mensaje_codificado: bytearray) -> dict:
    try:
        diccionario = json.loads(mensaje_codificado.decode('utf-8'))
        return diccionario
    except JSONDecodeError:
        raise JsonError


def decodificar_largo(mensaje: bytearray) -> int:
    bytes_necesarios = mensaje[:4]
    numero = int.from_bytes(bytes_necesarios, 'big')
    return numero


def separar_msg_encriptado(mensaje: bytearray) -> List[bytearray]:
    m_bytes_secuencia = bytearray()
    m_reducido = bytearray()
    secuencia_codificada = bytearray()
    
    largo = decodificar_largo(mensaje)
    mensaje_sin_largo = mensaje[4:]

    m_bytes_secuencia = mensaje_sin_largo[:largo]
    mensaje_sin_secuencia = mensaje_sin_largo[largo:]

    secuencia_codificada = mensaje_sin_secuencia[-2 * largo:]
    m_reducido = mensaje_sin_secuencia[: len(mensaje_sin_secuencia) - 2*largo]

    return [m_bytes_secuencia, m_reducido, secuencia_codificada]


def decodificar_secuencia(secuencia_codificada: bytearray) -> List[int]:
    spliteado = []
    for index in range(0, len(secuencia_codificada), 2):
        spliteado.append(secuencia_codificada[index: index + 2])
    numeros = []
    for byte in spliteado:
        numeros.append(int.from_bytes(byte, 'big'))
    return numeros


def desencriptar(mensaje: bytearray) -> bytearray:
    mensaje_separado = separar_msg_encriptado(mensaje)
    secuencia = decodificar_secuencia(mensaje_separado[-1])
    for byte, indice in zip(mensaje_separado[0], secuencia):
        mensaje_separado[1].insert(indice, byte)
    return mensaje_separado[1]


if __name__ == "__main__":
    mensaje = bytearray(b'\x00\x00\x00\x04"a}a{tm": 1\x00\x01\x00\x05\x00\n\x00\x03')
    desencriptado = desencriptar(mensaje)
    diccionario = deserializar_diccionario(desencriptado)
    print(diccionario)
