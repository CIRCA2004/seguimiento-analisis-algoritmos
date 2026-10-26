from bucket_sort import bucket_sort
from configuracion import CORPUS_DIR, REPETICIONES, RESULTADOS_DIR
from counting_sort import counting_sort
from graficas import grafica_tiempos, grafica_top15
from medicion import medir_algoritmo
from procesamiento import convertir_a_lista, procesar_corpus
from radix_sort import radix_sort
from salida import (
    guardar_estado_articulos,
    guardar_frecuencias,
    guardar_tiempos,
    guardar_top15,
)


def resultados_iguales(a, b) -> bool:
    if len(a) != len(b):
        return False

    for i in range(len(a)):
        if a[i] != b[i]:
            return False

    return True


def mostrar_top15(resultado: list[tuple[str, int]]) -> None:
    limite = 15

    if len(resultado) < limite:
        limite = len(resultado)

    print("\n15 términos más frecuentes")
    print("-" * 45)
    print(f'{"Pos.":<6}{"Término":<28}{"Frecuencia":>10}')
    print("-" * 45)

    for i in range(limite):
        termino, frecuencia = resultado[i]
        print(f'{i + 1:<6}{termino:<28}{frecuencia:>10}')


def main() -> None:
    RESULTADOS_DIR.mkdir(parents=True, exist_ok=True)

    if not CORPUS_DIR.exists():
        print("No existe la carpeta corpus.")
        return

    cantidad_pdf = 0
    for archivo in CORPUS_DIR.iterdir():
        if archivo.is_file() and archivo.suffix.lower() == ".pdf":
            cantidad_pdf += 1

    print(f"PDF encontrados en el corpus: {cantidad_pdf}")

    if cantidad_pdf == 0:
        print("Agrega los artículos PDF en la carpeta corpus y vuelve a ejecutar.")
        return

    if cantidad_pdf != 20:
        raise SystemExit("Se requieren exactamente 20 artículos para analizar el corpus completo.")

    frecuencias, articulos = procesar_corpus(CORPUS_DIR)
    guardar_estado_articulos(RESULTADOS_DIR / "estado_articulos.csv", articulos)
    with (RESULTADOS_DIR / "abstracts_extraidos.txt").open("w", encoding="utf-8") as archivo:
        for articulo in articulos:
            archivo.write(articulo["archivo"] + "\n" + articulo.get("abstract", "") + "\n\n")
    if any(not a["abstract_encontrado"] or not a["cantidad_terminos"] for a in articulos):
        raise SystemExit("Corpus incompleto: revisa estado_articulos.csv y abstracts_extraidos.txt.")
    datos = convertir_a_lista(frecuencias)

    if len(datos) == 0:
        print("No se encontraron términos para ordenar.")
        print("Revisa resultados/estado_articulos.csv para verificar los abstracts.")
        guardar_estado_articulos(RESULTADOS_DIR / "estado_articulos.csv", articulos)
        return

    mediciones = {
        "Counting Sort": medir_algoritmo(counting_sort, datos, REPETICIONES),
        "Radix Sort": medir_algoritmo(radix_sort, datos, REPETICIONES),
        "Bucket Sort": medir_algoritmo(bucket_sort, datos, REPETICIONES),
    }

    resultados = {}
    for nombre, medicion in mediciones.items():
        resultados[nombre] = medicion["resultado"]

    valido_counting_radix = resultados_iguales(
        resultados["Counting Sort"],
        resultados["Radix Sort"],
    )
    valido_counting_bucket = resultados_iguales(
        resultados["Counting Sort"],
        resultados["Bucket Sort"],
    )

    print(f"\nCantidad de términos diferentes: {len(datos)}")
    print(
        "Validación Counting = Radix:",
        "CORRECTA" if valido_counting_radix else "INCORRECTA",
    )
    print(
        "Validación Counting = Bucket:",
        "CORRECTA" if valido_counting_bucket else "INCORRECTA",
    )

    if not (valido_counting_radix and valido_counting_bucket):
        raise SystemExit("Los algoritmos no coinciden; no se publica el ranking.")
    mostrar_top15(resultados["Counting Sort"])

    print("\nTiempos promedio")
    print("-" * 45)
    for nombre, datos_medicion in mediciones.items():
        print(f'{nombre:<18}: {datos_medicion["promedio_ms"]:.6f} ms')

    # Archivos requeridos para la documentación del seguimiento.
    guardar_frecuencias(
        RESULTADOS_DIR / "frecuencias_ordenadas.csv",
        resultados["Counting Sort"],
    )
    guardar_tiempos(RESULTADOS_DIR / "tiempos.csv", mediciones)
    guardar_top15(RESULTADOS_DIR / "top15_por_algoritmo.csv", resultados)
    guardar_estado_articulos(RESULTADOS_DIR / "estado_articulos.csv", articulos)

    grafica_top15(
        RESULTADOS_DIR / "top15_terminos.png",
        resultados["Counting Sort"][:15],
    )
    grafica_tiempos(RESULTADOS_DIR / "tiempos_algoritmos.png", mediciones)

    print("\nResultados guardados en la carpeta resultados.")


if __name__ == "__main__":
    main()
