# Análisis de algoritmos en el contexto de la bibliometría

## Alcance y preprocesamiento
Se procesan los abstracts de los 20 PDF suministrados. No se utilizan los títulos,
autores, palabras clave ni el cuerpo del artículo para calcular frecuencias.
Los encabezados Abstract se reconocen también con letras espaciadas. La lectura
conserva bloques para separar columnas laterales y evitar incorporar la introducción.
Se exporta el texto utilizado en resultados/abstracts_extraidos.txt para auditoría.
Si falta un abstract o un PDF no puede leerse, se registra el estado y la ejecución
se detiene sin publicar un ranking parcial como si correspondiera al corpus completo.
La extracción es una heurística adaptada y comprobada para este corpus: otros diseños
editoriales requieren revisar los textos exportados; no se incluye OCR.

Se aplica normalización Unicode NFKC antes de tokenizar (incluidas ligaduras),
se unen cortes de palabra por salto de línea y guiones blandos, se convierten las
palabras a minúsculas y se eliminan números, puntuación, stopwords y términos
menores de tres letras, excepto AI (normalizado a ai), por su relevancia temática.
AIED y GenAI se cuentan como términos distintos de AI.
No se aplica stemming ni lematización. Estas son decisiones
de preprocesamiento documentadas: el enunciado no especifica una lista de stopwords.
Se cuenta manualmente la frecuencia global en un diccionario y se convierte a
una lista de tuplas (término, frecuencia). Los empates conservan su orden inicial;
el orden de lectura de los archivos se fija por nombre para que sea reproducible.

## Fundamentación teórica
Los algoritmos no comparan pares de términos para determinar su posición.
Utilizan las frecuencias enteras no negativas como índices, dígitos o intervalos.
Por eso no se aplica la cota inferior de los ordenamientos por comparación.
Sea n la cantidad de términos distintos, K la frecuencia máxima, b el número
de buckets y d la cantidad de dígitos decimales de K.

### Counting Sort
Busca K, cuenta ocurrencias en K+1 posiciones, calcula posiciones descendentes
y distribuye cada elemento de forma estable. Tiempo Θ(n+K+1), espacio Θ(n+K+1).
Es lineal en n cuando K=O(n). Un K muy grande hace costoso el arreglo auxiliar.

### Radix Sort
Procesa de unidades a dígitos más significativos con Counting Sort estable de
base 10 descendente. Cada pasada cuesta Θ(n+10); hay d pasadas para K>0.
Tiempo O(n+d(n+10)), espacio O(n+10). Con d acotado se obtiene O(n).
Para K=0 conserva la copia de entrada. La estabilidad de cada pasada es necesaria
para conservar el orden construido por los dígitos anteriores.

### Bucket Sort
Usa b=floor(sqrt(n)) intervalos, distribuye por frecuencia y recorre los buckets
de mayor a menor. Cada bucket se ordena con Radix Sort, no con comparación.
La raíz manual cuesta O(sqrt(n)); distribución y concatenación cuestan O(n+b).
Si n_i es el tamaño del bucket i y d_i sus dígitos máximos, el tiempo es
O(n+b+sum(d_i*(n_i+10))) sobre buckets que necesitan ordenarse.
Como sum(n_i)=n y b<=n, una cota general es O(d*n+n), y el espacio auxiliar O(n+b).
Con frecuencias de un número acotado de dígitos es O(n). No se atribuye a esta
variante el análisis de Bucket Sort con Insertion Sort: utiliza otro algoritmo
interno y no necesita suponer una distribución uniforme para esa cota.

## Medición empírica
Los tres algoritmos reciben el mismo contenido de entrada. Se realizan tres
calentamientos y 30 repeticiones por algoritmo con perf_counter_ns(); se reportan
milisegundos. La copia de entrada se prepara antes de iniciar el cronómetro.
La lectura de PDF, limpieza, validación, escritura y gráficas quedan fuera de la
medición. La asignación de las estructuras internas del algoritmo sí se incluye.
Las cifras dependen del equipo y de su carga; son mediciones observadas, no
constantes universales ni una prueba de complejidad asintótica.

| Algoritmo | Repeticiones | Promedio ms | Mínimo ms | Máximo ms |
|---|---:|---:|---:|---:|
| Counting Sort | 30 | 0.175437 | 0.157500 | 0.451100 |
| Radix Sort | 30 | 0.423510 | 0.405500 | 0.485400 |
| Bucket Sort | 30 | 0.429013 | 0.408500 | 0.504000 |

## Validación y resultados
Se obtuvieron 989 términos distintos. Los tres rankings completos coinciden,
incluidos los empates. Esta tabla muestra el término y su frecuencia por algoritmo.

| Posición | Counting Sort | Radix Sort | Bucket Sort |
|---|---|---|---|
| 1 | ai (86) | ai (86) | ai (86) |
| 2 | education (57) | education (57) | education (57) |
| 3 | research (46) | research (46) | research (46) |
| 4 | learning (40) | learning (40) | learning (40) |
| 5 | aied (38) | aied (38) | aied (38) |
| 6 | review (36) | review (36) | review (36) |
| 7 | educational (33) | educational (33) | educational (33) |
| 8 | assessment (32) | assessment (32) | assessment (32) |
| 9 | intelligence (23) | intelligence (23) | intelligence (23) |
| 10 | artificial (22) | artificial (22) | artificial (22) |
| 11 | studies (21) | studies (21) | studies (21) |
| 12 | higher (16) | higher (16) | higher (16) |
| 13 | literature (15) | literature (15) | literature (15) |
| 14 | technologies (15) | technologies (15) | technologies (15) |
| 15 | systematic (15) | systematic (15) | systematic (15) |

También se generan las gráficas top15_terminos.png y tiempos_algoritmos.png.
Las seis pruebas automatizadas verifican estabilidad y preservación de la entrada
frente a una referencia independiente en casos aleatorios, encabezados espaciados,
separación de columnas, normalización y agregación del corpus completo.
El uso de sorted en las pruebas es exclusivamente una referencia de comprobación;
los tres algoritmos del programa construyen manualmente el ranking.

## Conclusiones
Counting Sort tuvo el menor promedio en esta ejecución. El rango pequeño de
frecuencias favorece su arreglo de conteo. Radix realiza varias pasadas y Bucket
añade distribución y gestión de listas, por lo que su mayor coste constante puede
superar sus ventajas para este tamaño. Una sola lista no permite confirmar tasas
de crecimiento: para ello se necesitarían entradas de tamaños y rangos variados.
El ranking depende del preprocesamiento; no identifica automáticamente sinónimos
ni agrupa singular/plural. ai fue el término más frecuente (86 apariciones),
seguido de education (57).
