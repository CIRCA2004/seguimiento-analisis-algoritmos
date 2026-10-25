import csv
from pathlib import Path


def guardar_frecuencias(ruta: Path, datos: list[tuple[str, int]]) -> None:
    with open(ruta, "w", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(["termino", "frecuencia"])

        for termino, frecuencia in datos:
            escritor.writerow([termino, frecuencia])


def guardar_tiempos(ruta: Path, tiempos: dict) -> None:
    with open(ruta, "w", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow([
            "algoritmo",
            "repeticiones",
            "promedio_ms",
            "minimo_ms",
            "maximo_ms",
        ])

        for nombre, datos in tiempos.items():
            escritor.writerow([
                nombre,
                datos["repeticiones"],
                f'{datos["promedio_ms"]:.6f}',
                f'{datos["minimo_ms"]:.6f}',
                f'{datos["maximo_ms"]:.6f}',
            ])


def guardar_top15(ruta: Path, resultados: dict) -> None:
    with open(ruta, "w", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow([
            "posicion",
            "counting_termino", "counting_frecuencia",
            "radix_termino", "radix_frecuencia",
            "bucket_termino", "bucket_frecuencia",
        ])

        for i in range(15):
            fila = [i + 1]

            for nombre in ["Counting Sort", "Radix Sort", "Bucket Sort"]:
                resultado = resultados[nombre]

                if i < len(resultado):
                    fila.append(resultado[i][0])
                    fila.append(resultado[i][1])
                else:
                    fila.append("")
                    fila.append("")

            escritor.writerow(fila)


def guardar_estado_articulos(ruta: Path, articulos: list[dict]) -> None:
    with open(ruta, "w", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(["archivo", "abstract_encontrado", "cantidad_terminos"])

        for articulo in articulos:
            escritor.writerow([
                articulo["archivo"],
                articulo["abstract_encontrado"],
                articulo["cantidad_terminos"],
            ])
