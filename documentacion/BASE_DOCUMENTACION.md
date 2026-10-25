# Análisis de algoritmos en el contexto de la bibliometría

## 1. Introducción

El proyecto procesa un corpus de 20 artículos científicos relacionados con inteligencia artificial generativa. El análisis se realiza principalmente sobre el abstract de cada artículo. A partir de estos textos se extraen los términos, se eliminan palabras que no aportan al análisis y se calcula la frecuencia total de cada término dentro del corpus.

Posteriormente se aplican tres algoritmos de ordenamiento no basados en comparaciones directas: Counting Sort, Radix Sort y Bucket Sort. El objetivo es obtener un ranking de términos por frecuencia, analizar teóricamente el comportamiento de los algoritmos y comparar sus tiempos reales de ejecución.

## 2. Preprocesamiento del corpus

El preprocesamiento implementado sigue los siguientes pasos:

1. Lectura de cada archivo PDF.
2. Identificación de la sección Abstract.
3. Conversión de las palabras a minúsculas.
4. Eliminación de signos de puntuación y números.
5. Separación del texto en términos.
6. Eliminación de palabras vacías frecuentes en inglés.
7. Eliminación de términos con menos de tres caracteres.
8. Conteo de la frecuencia de cada término.
9. Acumulación de las frecuencias de los 20 artículos.

No se aplican técnicas de stemming ni lematización, ya que no están indicadas explícitamente en el requerimiento.

## 3. Estructura de los datos

Después del preprocesamiento se utiliza inicialmente un diccionario con la forma:

`termino -> frecuencia`

Para ejecutar los algoritmos de ordenamiento, los datos se convierten a una lista de tuplas:

`(termino, frecuencia)`

La frecuencia es la clave numérica utilizada por los tres algoritmos.

## 4. Counting Sort

### 4.1 Idea general

Counting Sort utiliza un arreglo auxiliar para contar cuántos términos poseen cada posible valor de frecuencia. Después calcula la posición inicial correspondiente a cada frecuencia y construye una nueva lista ordenada de mayor a menor.

La implementación es estable: si dos palabras presentan la misma frecuencia, conservan el orden en el que estaban antes del ordenamiento.

### 4.2 Complejidad asintótica

Sea `n` la cantidad de términos distintos y `k` la frecuencia máxima observada.

- Se recorre la lista de términos: O(n).
- Se recorre el arreglo de conteo: O(k).
- Se construye el resultado: O(n).

Por lo tanto:

`O(n + k)`

> El T(n) exacto se completará usando el conteo de instrucciones de la versión final del código y el criterio utilizado por el profesor en clase.

## 5. Radix Sort

### 5.1 Idea general

Radix Sort procesa las frecuencias dígito por dígito, comenzando por las unidades. Para ordenar cada dígito se utiliza una versión estable de Counting Sort con base decimal.

### 5.2 Complejidad asintótica

Sea `d` la cantidad de dígitos de la frecuencia máxima. Cada pasada cuesta O(n + 10), por lo que:

`O(d(n + 10))`

Como la base decimal es constante:

`O(dn)`

Cuando `d` se considera acotado, el comportamiento puede expresarse como O(n).

> El T(n) exacto se completará a partir del código definitivo siguiendo el procedimiento usado por el profesor.

## 6. Bucket Sort

### 6.1 Idea general

Bucket Sort distribuye los términos en varios intervalos según su frecuencia. Los buckets de frecuencias mayores se procesan primero para obtener un ranking descendente. Cada bucket se ordena internamente con Radix Sort, evitando depender de un algoritmo de comparación directa.

### 6.2 Complejidad asintótica

La distribución inicial de los elementos requiere O(n). En condiciones de distribución adecuada, el trabajo realizado dentro de los buckets se mantiene cercano a lineal, por lo que el comportamiento esperado es O(n + k) o cercano a O(n), dependiendo de la distribución y de la forma en que se definan los buckets.

## 7. Medición empírica

Los tiempos se miden con `time.perf_counter_ns()`. Cada algoritmo se ejecuta varias veces y se registra:

- tiempo promedio,
- tiempo mínimo,
- tiempo máximo.

Las mediciones se convierten a milisegundos.

Los valores definitivos deben copiarse del archivo `resultados/tiempos.csv` después de ejecutar el programa sobre los 20 artículos suministrados por el docente.

## 8. Validación de resultados

Los tres algoritmos reciben exactamente la misma lista inicial. Al finalizar se compara elemento por elemento el resultado de Counting Sort con Radix Sort y Bucket Sort.

Además, el programa genera el archivo `top15_por_algoritmo.csv`, donde se presentan los 15 términos más frecuentes obtenidos por cada algoritmo, y el gráfico `top15_terminos.png`.

## 9. Resultados

Esta sección se completa una vez se disponga de los 20 artículos y se ejecute el programa.

### 9.1 Tiempos reales

| Algoritmo | Repeticiones | Promedio (ms) | Mínimo (ms) | Máximo (ms) |
|---|---:|---:|---:|---:|
| Counting Sort | Pendiente | Pendiente | Pendiente | Pendiente |
| Radix Sort | Pendiente | Pendiente | Pendiente | Pendiente |
| Bucket Sort | Pendiente | Pendiente | Pendiente | Pendiente |

### 9.2 Quince términos más frecuentes

Pendiente de ejecutar el corpus suministrado por el profesor.

## 10. Conclusiones

Las conclusiones finales deben realizarse después de obtener las mediciones empíricas. Se comparará el comportamiento observado con las complejidades teóricas de cada algoritmo y se explicarán las diferencias encontradas para el tamaño y distribución específicos del corpus utilizado.
