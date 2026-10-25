from radix_sort import radix_sort


def raiz_entera(n: int) -> int:
    """Calcula una aproximación entera de sqrt(n) sin depender de math.sqrt."""
    if n <= 1:
        return 1

    raiz = 1
    while (raiz + 1) * (raiz + 1) <= n:
        raiz += 1

    return raiz


def bucket_sort(datos: list[tuple[str, int]]) -> list[tuple[str, int]]:
    """
    Ordena de mayor a menor por frecuencia usando Bucket Sort.

    Los elementos se distribuyen en intervalos de frecuencia. Cada bucket se
    ordena con Radix Sort para mantener el enfoque de algoritmos no comparativos.
    """
    n = len(datos)

    if n <= 1:
        return datos.copy()

    frecuencia_maxima = datos[0][1]

    for i in range(1, n):
        if datos[i][1] > frecuencia_maxima:
            frecuencia_maxima = datos[i][1]

    cantidad_buckets = raiz_entera(n)
    if cantidad_buckets < 1:
        cantidad_buckets = 1

    buckets = []
    for _ in range(cantidad_buckets):
        buckets.append([])

    # Distribución proporcional de 0..frecuencia_maxima entre los buckets.
    for elemento in datos:
        frecuencia = elemento[1]

        if frecuencia_maxima == 0:
            indice = 0
        else:
            indice = (frecuencia * cantidad_buckets) // (frecuencia_maxima + 1)

        if indice >= cantidad_buckets:
            indice = cantidad_buckets - 1

        buckets[indice].append(elemento)

    resultado = []

    # Se recorren los buckets de mayor a menor frecuencia.
    for indice in range(cantidad_buckets - 1, -1, -1):
        bucket_ordenado = radix_sort(buckets[indice])

        for elemento in bucket_ordenado:
            resultado.append(elemento)

    return resultado
