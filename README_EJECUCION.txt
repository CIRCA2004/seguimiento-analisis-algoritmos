SEGUIMIENTO - ANÁLISIS DE ALGORITMOS

1. Instalar Python 3.

2. Abrir una terminal en la carpeta del proyecto.

3. Instalar las dependencias:
   pip install -r requirements.txt

4. Copiar los 20 artículos PDF entregados por el profesor dentro de:
   corpus/

5. Ejecutar:
   python src/main.py

6. Los resultados se crean automáticamente en:
   resultados/

Archivos generados:
- frecuencias_ordenadas.csv
- tiempos.csv
- top15_por_algoritmo.csv
- estado_articulos.csv
- top15_terminos.png
- tiempos_algoritmos.png

IMPORTANTE:
- Counting Sort, Radix Sort y Bucket Sort están implementados manualmente.
- No se usa sort() ni sorted() para resolver el ranking.
- El procesamiento del ranking se realiza sobre el abstract de cada artículo.
