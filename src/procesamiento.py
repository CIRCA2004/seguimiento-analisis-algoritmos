import re
import unicodedata
from pathlib import Path

import pymupdf as fitz

from configuracion import STOPWORDS


def extraer_texto_pdf(ruta_pdf: Path) -> str:
    """Extrae el texto completo de un archivo PDF."""
    partes = []

    with fitz.open(ruta_pdf) as documento:
        for pagina in documento:
            partes.append("\n\n".join(b[4].strip() for b in pagina.get_text("blocks") if b[6] == 0))

    return "\n".join(partes)


def extraer_abstract(texto: str) -> str:
    """
    Busca la sección Abstract y devuelve su contenido.

    La búsqueda termina cuando aparece una sección típica posterior al abstract,
    por ejemplo Keywords o Introduction. Si no se encuentra un abstract claro,
    devuelve una cadena vacía para que el problema pueda ser detectado.
    """
    texto = unicodedata.normalize("NFKC", texto.replace("\r", ""))
    # Encabezado en una línea: no confundir menciones de abstract en el cuerpo.
    inicio = re.search(r"(?im)^[ \t]*a[ \t]*b[ \t]*s[ \t]*t[ \t]*r[ \t]*a[ \t]*c[ \t]*t\b[ \t]*[:—-]?[ \t]*", texto)
    if inicio is None:
        return ""
    resto = texto[inicio.end():].lstrip()
    # Algunas revistas extraen primero la columna lateral de palabras clave.
    if re.match(r"(?i)^keywords?\b", resto):
        bloques = resto.split("\n\n", 1)
        if len(bloques) < 2:
            return ""
        resto = bloques[1].lstrip()
    fin = re.search(
        r"(?im)^[ \t]*(?:(?:1[.\s|]*)?introduction\b|"
        r"k[ \t]*e[ \t]*y[ \t]*w[ \t]*o[ \t]*r[ \t]*d[ \t]*s?\b|index[ \t]+terms?\b)",
        resto,
    )
    if fin:
        return resto[:fin.start()].strip()
    # Sin encabezado posterior se conserva solo el bloque del resumen.
    # Nunca se acepta un recorte arbitrario del cuerpo completo del artículo.
    return resto.split("\n\n", 1)[0].strip()


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
    abstract = unicodedata.normalize("NFKC", abstract)
    abstract = re.sub(r"(?<=\w)\xad\s*", "", abstract)
    abstract = re.sub(r"(?<=[a-z])-[ \t]*\n[ \t]*(?=[a-z])", "", abstract)
    abstract = abstract.replace("’", "'")
    abstract = re.sub(r"(?i)\b([a-z]+)'s\b", r"\1", abstract)
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

    archivos = [ruta for ruta in carpeta_corpus.iterdir() if ruta.is_file() and ruta.suffix.lower() == ".pdf"]

    archivos.sort(key=lambda ruta: ruta.name)  # Solo orden de lectura, no ranking.

    # El orden de lectura fija el desempate estable entre frecuencias iguales.
    for ruta_pdf in archivos:
        try:
            texto = extraer_texto_pdf(ruta_pdf)
            abstract = extraer_abstract(texto)
        except (RuntimeError, OSError, ValueError) as error:
            articulos.append({"archivo": ruta_pdf.name, "abstract_encontrado": False,
                              "cantidad_terminos": 0, "error": str(error), "abstract": ""})
            continue

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
            "abstract": abstract,
        })

    return frecuencias_totales, articulos


def convertir_a_lista(frecuencias: dict[str, int]) -> list[tuple[str, int]]:
    """Convierte {palabra: frecuencia} a [(palabra, frecuencia), ...]."""
    datos = []

    for palabra, frecuencia in frecuencias.items():
        datos.append((palabra, frecuencia))

    return datos
