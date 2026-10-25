from pathlib import Path

import matplotlib.pyplot as plt


def grafica_top15(ruta: Path, top15: list[tuple[str, int]]) -> None:
    terminos = []
    frecuencias = []

    # Se invierte manualmente para que el término más frecuente quede arriba.
    for i in range(len(top15) - 1, -1, -1):
        terminos.append(top15[i][0])
        frecuencias.append(top15[i][1])

    plt.figure(figsize=(10, 7))
    plt.barh(terminos, frecuencias)
    plt.xlabel("Frecuencia")
    plt.ylabel("Término")
    plt.title("15 términos más frecuentes del corpus")
    plt.tight_layout()
    plt.savefig(ruta, dpi=200)
    plt.close()


def grafica_tiempos(ruta: Path, tiempos: dict) -> None:
    nombres = []
    promedios = []

    for nombre, datos in tiempos.items():
        nombres.append(nombre)
        promedios.append(datos["promedio_ms"])

    plt.figure(figsize=(8, 5))
    plt.bar(nombres, promedios)
    plt.ylabel("Tiempo promedio (ms)")
    plt.title("Comparación empírica de tiempos de ejecución")
    plt.tight_layout()
    plt.savefig(ruta, dpi=200)
    plt.close()
