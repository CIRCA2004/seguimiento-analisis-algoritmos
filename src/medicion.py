import time


def medir_algoritmo(funcion, datos, repeticiones: int = 30) -> dict:
    """Mide el tiempo real de una función de ordenamiento en milisegundos."""
    if repeticiones < 1:
        raise ValueError("repeticiones debe ser mayor que cero")
    tiempos = []
    ultimo_resultado = None

    # Tres ejecuciones de calentamiento que no se incluyen en el promedio.
    for _ in range(3):
        funcion(datos.copy())

    for _ in range(repeticiones):
        entrada = datos.copy()
        inicio = time.perf_counter_ns()
        ultimo_resultado = funcion(entrada)
        fin = time.perf_counter_ns()

        tiempo_ms = (fin - inicio) / 1_000_000
        tiempos.append(tiempo_ms)

    suma = 0.0
    minimo = tiempos[0]
    maximo = tiempos[0]

    for tiempo in tiempos:
        suma += tiempo

        if tiempo < minimo:
            minimo = tiempo
        if tiempo > maximo:
            maximo = tiempo

    promedio = suma / len(tiempos)

    return {
        "resultado": ultimo_resultado,
        "promedio_ms": promedio,
        "minimo_ms": minimo,
        "maximo_ms": maximo,
        "repeticiones": repeticiones,
    }
