import sys
import random
import unittest
from pathlib import Path
from collections import Counter
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from counting_sort import counting_sort
from radix_sort import radix_sort
from bucket_sort import bucket_sort
from procesamiento import extraer_abstract, tokenizar_abstract, procesar_corpus
from medicion import medir_algoritmo

class Pruebas(unittest.TestCase):
    def test_algoritmos_contra_referencia(self):
        rng = random.Random(2026)
        casos = [[], [("a", 0)], [("a", 10), ("b", 2), ("c", 10)]]
        casos += [[(str(i), rng.randrange(1000)) for i in range(n)] for n in range(2, 150)]
        for datos in casos:
            esperado = sorted(datos, key=lambda par: par[1], reverse=True)
            for algoritmo in (counting_sort, radix_sort, bucket_sort):
                original = datos.copy()
                self.assertEqual(algoritmo(datos), esperado)
                self.assertEqual(datos, original)

    def test_abstract_espaciado_y_columna_lateral(self):
        texto = "Title\n\nA B S T R A C T\n\nKeywords: education\nAI\n\nThis review mentions keywords, and introduction methods.\n\n1. Introduction\nBody"
        self.assertEqual(extraer_abstract(texto), "This review mentions keywords, and introduction methods.")
        self.assertEqual(extraer_abstract("The abstract is discussed in the body."), "")
        self.assertEqual(extraer_abstract("Abstract: Summary.\n\nBody without heading."), "Summary.")

    def test_normalizacion(self):
        self.assertEqual(tokenizar_abstract("Artiﬁcial edu-\ncation tech\xad\nnology the AI"), ["artificial", "education", "technology"])

    def test_corpus_completo(self):
        frecuencias, articulos = procesar_corpus(Path(__file__).resolve().parents[1] / "corpus")
        self.assertEqual(len(articulos), 20)
        contador = Counter()
        for articulo in articulos:
            self.assertTrue(articulo["abstract_encontrado"])
            self.assertGreater(len(articulo["abstract"]), 800)
            self.assertLess(len(articulo["abstract"]), 2500)
            contador.update(tokenizar_abstract(articulo["abstract"]))
        self.assertEqual(frecuencias, dict(contador))
        self.assertEqual(frecuencias["education"], 57)

    def test_repeticiones_invalidas(self):
        with self.assertRaises(ValueError):
            medir_algoritmo(counting_sort, [], 0)

if __name__ == "__main__":
    unittest.main()
