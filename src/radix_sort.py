def counting_por_digito(
    datos: list[tuple[str, int]],
    divisor: int,
) -> list[tuple[str, int]]:
    """
    Counting Sort estable para un solo dígito decimal.
    Ordena ese dígito de 9 a 0 para construir un Radix Sort descendente.
    """
    conteo = [0] * 10

    for elemento in datos:
        frecuencia = elemento[1]
        digito = (frecuencia // divisor) % 10
        conteo[digito] += 1

    posiciones = [0] * 10
    acumulado = 0

    for digito in range(9, -1, -1):
        posiciones[digito] = acumulado
        acumulado += conteo[digito]

    resultado = [None] * len(datos)

    for elemento in datos:
        frecuencia = elemento[1]
        digito = (frecuencia // divisor) % 10
        posicion = posiciones[digito]
        resultado[posicion] = elemento
        posiciones[digito] += 1

    return resultado


def radix_sort(datos: list[tuple[str, int]]) -> list[tuple[str, int]]:
    """Ordena de mayor a menor por frecuencia usando Radix Sort LSD."""
    n = len(datos)

    if n <= 1:
        return datos.copy()

    frecuencia_maxima = datos[0][1]

    for i in range(1, n):
        if datos[i][1] > frecuencia_maxima:
            frecuencia_maxima = datos[i][1]

    resultado = datos.copy()
    divisor = 1

    while frecuencia_maxima // divisor > 0:
        resultado = counting_por_digito(resultado, divisor)
        divisor *= 10

    return resultado
