import re
import unicodedata
from pathlib import Path

import fitz  # PyMuPDF

from configuracion import STOPWORDS


def extraer_texto_pdf(ruta_pdf: Path) -> str:
    """Extrae el texto completo de un archivo PDF."""
    partes = []

    with fitz.open(ruta_pdf) as documento:
        for pagina in documento:
            partes.append(pagina.get_text("text"))

    return "\n".join(partes)


def extraer_abstract(texto: str) -> str:
    """
    Busca la sección Abstract y devuelve su contenido.

    La búsqueda termina cuando aparece una sección típica posterior al abstract,
    por ejemplo Keywords o Introduction. Si no se encuentra un abstract claro,
    devuelve una cadena vacía para que el problema pueda ser detectado.
    """
    texto_normalizado = texto.replace("\r", "\n")

    patron_inicio = re.compile(r"\babstract\b\s*[:\-—]?", re.IGNORECASE)
    coincidencia = patron_inicio.search(texto_normalizado)

    if coincidencia is None:
        return ""

    inicio = coincidencia.end()
    resto = texto_normalizado[inicio:]

    # Posibles encabezados que normalmente aparecen después del abstract.
    finales = [
        r"\bkeywords?\b\s*[:\-—]?",
        r"\bkey\s+words?\b\s*[:\-—]?",
        r"\bindex\s+terms?\b\s*[:\-—]?",
        r"\b1\s*[\.\-]?\s*introduction\b",
        r"\bintroduction\b",
    ]

    posiciones = []
    for patron in finales:
        fin = re.search(patron, resto, flags=re.IGNORECASE)
        if fin is not None:
            posiciones.append(fin.start())

    if posiciones:
        fin_abstract = min(posiciones)
        return resto[:fin_abstract].strip()

    # Si no aparece un encabezado posterior, se limita el tamaño para evitar
    # procesar accidentalmente todo el artículo.
    return resto[:6000].strip()


def normalizar_palabra(palabra: str) -> str:
    """Convierte una palabra a minúscula y elimina marcas Unicode extrañas."""
    palabra = palabra.lower()
    palabra = unicodedata.normalize("NFKC", palabra)
    return palabra


def tokenizar_abstract(abstract: str) -> list[str]:
    """
    Limpia el abstract y devuelve los términos útiles.

    Criterios utilizados:
    - minúsculas,
    - solo palabras formadas por letras,
    - longitud mínima de 3 caracteres,
    - eliminación de palabras vacías en inglés.
    """
    palabras = re.findall(r"[A-Za-z]+(?:'[A-Za-z]+)?", abstract)
    terminos = []

    for palabra in palabras:
        palabra = normalizar_palabra(palabra)

        if len(palabra) < 3:
            continue
        if palabra in STOPWORDS:
            continue

        terminos.append(palabra)

    return terminos


def contar_frecuencias(terminos: list[str]) -> dict[str, int]:
    """Cuenta manualmente cuántas veces aparece cada término."""
    frecuencias = {}

    for termino in terminos:
        if termino in frecuencias:
            frecuencias[termino] += 1
        else:
            frecuencias[termino] = 1

    return frecuencias


def unir_frecuencias(destino: dict[str, int], origen: dict[str, int]) -> None:
    """Suma al diccionario destino las frecuencias de otro artículo."""
    for termino, frecuencia in origen.items():
        if termino in destino:
            destino[termino] += frecuencia
        else:
            destino[termino] = frecuencia


def procesar_corpus(carpeta_corpus: Path) -> tuple[dict[str, int], list[dict]]:
    """
    Procesa todos los PDF del corpus.

    Retorna:
    1. Frecuencia total de palabras de todos los abstracts.
    2. Información básica de procesamiento por artículo.
    """
    frecuencias_totales = {}
    articulos = []

    archivos = [ruta for ruta in carpeta_corpus.iterdir() if ruta.suffix.lower() == ".pdf"]

    # No se usa sort/sorted porque el trabajo se centra en algoritmos de ordenamiento.
    # El orden físico de lectura de los PDF no afecta las frecuencias finales.
    for ruta_pdf in archivos:
        texto = extraer_texto_pdf(ruta_pdf)
        abstract = extraer_abstract(texto)

        if abstract == "":
            articulos.append({
                "archivo": ruta_pdf.name,
                "abstract_encontrado": False,
                "cantidad_terminos": 0,
            })
            continue

        terminos = tokenizar_abstract(abstract)
        frecuencias_articulo = contar_frecuencias(terminos)
        unir_frecuencias(frecuencias_totales, frecuencias_articulo)

        articulos.append({
            "archivo": ruta_pdf.name,
            "abstract_encontrado": True,
            "cantidad_terminos": len(terminos),
        })

    return frecuencias_totales, articulos


def convertir_a_lista(frecuencias: dict[str, int]) -> list[tuple[str, int]]:
    """Convierte {palabra: frecuencia} a [(palabra, frecuencia), ...]."""
    datos = []

    for palabra, frecuencia in frecuencias.items():
        datos.append((palabra, frecuencia))

    return datos
