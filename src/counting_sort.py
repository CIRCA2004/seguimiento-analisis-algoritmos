def counting_sort(datos: list[tuple[str, int]]) -> list[tuple[str, int]]:
    """
    Ordena de mayor a menor según la frecuencia usando Counting Sort.

    Cada elemento de datos tiene la forma:
        (palabra, frecuencia)

    El algoritmo es estable: si dos términos tienen la misma frecuencia,
    conserva el orden en el que aparecían en la lista original.
    """
    n = len(datos)

    if n <= 1:
        return datos.copy()

    frecuencia_maxima = datos[0][1]

    # Busca la frecuencia máxima sin usar max().
    for i in range(1, n):
        if datos[i][1] > frecuencia_maxima:
            frecuencia_maxima = datos[i][1]

    conteo = [0] * (frecuencia_maxima + 1)

    # Cuenta cuántos términos tienen cada frecuencia.
    for palabra, frecuencia in datos:
        conteo[frecuencia] += 1

    # posiciones[f] indica dónde debe comenzar el grupo de frecuencia f
    # en el resultado ordenado de mayor a menor.
    posiciones = [0] * (frecuencia_maxima + 1)
    acumulado = 0

    for frecuencia in range(frecuencia_maxima, -1, -1):
        posiciones[frecuencia] = acumulado
        acumulado += conteo[frecuencia]

    resultado = [None] * n

    # Se recorre de izquierda a derecha para mantener estabilidad.
    for elemento in datos:
        frecuencia = elemento[1]
        posicion = posiciones[frecuencia]
        resultado[posicion] = elemento
        posiciones[frecuencia] += 1

    return resultado
