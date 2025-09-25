# Problema 4: Programación dinámica

## Análisis del porblema

#### Definición:

Encontrar la secuencia contigua con la suma máxima en un array desordenado.

#### Ecuación de recurencia:

La solución óptima para el porblema se basa en la siguiente ecuación de recurrencia: 
    $S[i] = max(S[i-1] + A[i], A[i])$

**Explicación y Fundamentación**

Para resolver este problema con porgramación dinámica, se definió un subproblema: encontrar la suma máxima de una subsección contigua que termina en el índice $i$. Esta suma se llama $S[i]$. 

Para calcular $S[i]$, se debe tomar una decisión para el elemento $A[i]$:
    
- **Opción 1**: Ignorar todas las subsecciones anteriores y considerar que la subsección máxima que termina en $i$ es simplemente el elemento $A[i]$ por sí solo. Esto ocurre si la suma de la subsección que terminaba en $i-1$ era negativa, lo que significa que extenderla solo empeoraría el resultado.

- **Opción 2**: Extender la subsección óptima que terminaba en el índice $i-1$ al sumarle el elmento $A[i]$. Esta opción es viable si la suma $S[i-1]$ era positiva, ya que contribuirá a un valor más alto.

La ecucación de recurrencia planteada elige la mejor de estas 2 opciones. La solución general para todo el array es el valor  máximo para todo el array $S$. El caso base es $S[0] = A[0]$, ya que la suma máxima que termina en el primer índice es por definición, el primer elemento.

#### Justificación: Principios de la programación dinámica

El algoritmo diseñado usando programación dinámica para encontrar la subsección de máxima suma cumple con los 2 requisitos fundamentales para esta técnica: la **Subestructura Óptima** y los **Subproblemas superpuestos**.

- **Subestructura Óptima:** La solución óptima al porblema principal (suma máxima en todo el array) se construye a partir de las soluciones óptimas de sus subproblemas. En este caso, la solución final es el valor máximo entre todas las sumas máximas de subsecciones que terminan en cada posición del array. La ecuación de recurrencia definida, $S[i] = max(S[i-1] + A[i], A[i])$, garantiza que para cada índice $i$, se encuentra la suma máxima óptima que termina en esa posición, tomando como base la solución óptima del subproblema anterior.

- **Subproblemas Superpuestos:** Este principio se cumple porque, al resolver el problema de forma iterativa, el cálculo de la suma máxima que termina en la posición $i$ requiere la suma máxima que termina en la posición $i-1$. A medida que se avanza a través del array, se resuelve una serie de subproblemas interdependientes. Almacenar los resultados de cada subproblema ($S[i]$) en un array permite reutilizar esos valores en siguiente paso, evitando recálculos innecesarios que sí ocurrían en un enfoque recursivo. Esta reutilización de resultados intermedios es lo que hace que el algoritmo de programación dinámica sea mucho más eficiente que un enfoque de fuerza bruta o backtracking.

#### Siguimiento del algoritmo

Para demostrar el funcionamiento del algoritmo, se hará un ejemplo de seguimiento usando el siguiente arreglo $A=[3, -5, 7, 1, -8, 3, -7, 5]$.

Para este ejemplo, se seguirán los pasos del algoritmo para calcular el array de sumas óptimas, $S$, y al mismo tiempo se rastrearán las variables para la suma máxima global y sus índices.

- **suma_actual:** La suma máxima de la subsección que termina en la posición actual.
- **suma_maxima:** La suma máxima encotrada hasta el momento.
- **inicio:** El índice de inicio de la subsección con la suma máxima total.
- **fin:** El índice de fin de la subsección con la suma máxima total.
- **inicio_temp:** Un índice auxiliar para rastrear el inicio de la subsección actual.

| i | A[i] | suma_anterior | suma_actual = max(suma_anterior + A[i], A[i]) | suma_maxima | inicio | fin | inicio_temp |
|:---:|:------:|:---------------:|:-------------:|:--------------:|:--------:|:-----:|:-----------:|
| - | - | - | - | $-\infty$ | - | - | 0 |
| 0 | 3 | - | $3 = max(-∞ + 3, 3)$ | 3 | 0 | 0 | 0 |
| 1 | -5 | 3 | $-2 = max(3 + (-5), -5)$ | 3 | 0 | 0 | 0 |
| 2 | 7 | 3 | $7 = max(-2 + 7, 7)$ | 7 | 2 | 2 | 2 |
| 3 | 1 | 7 | $8 = max(7 + 1, 1)$ | 8 | 2 | 3 | 2 |
| 4 | -8 | 8 | $0 = max(8 + (-8), -8)$ | 8 | 2 | 3 | 2 |
| 5 | 3 | 0 | $3 = max(0 + 3, 3)$ | 8 | 2 | 3 | 5 |
| 6 | -7 | 3 | $-4 = max(3 + (-7), -7)$ | 8 | 2 | 3 | 5 |
| 7 | 5 | -4 | $5 = max(-4 + 5, 5)$ | 8 | 2 | 3 | 7 |

Al finalizar el recorrido, la **suma_maxima** es 8, con los índices de inicio y fin de 2 y 3, respectivamente. La subsección con la suma máxima es $A[2...3]$, que corresponde a los elementos $[7, 1]$.

#### Pseudocódigo

```python
def maxsubsetsum(A) :
    n = len(A)
    if n == 0:
        return (0, -1, -1)

    suma_maxima = A[0]
    inicio = 0
    fin = 0
    suma_actual = A[0]
    inicio_temp = 0

    for i in range(1, n):
        if suma_actual + A[i] > A[i]:
            suma_actual += A[i]
        else:
            suma_actual = A[i]
            inicio_temp = i

        if suma_actual > suma_maxima:
            suma_maxima = suma_actual
            inicio = inicio_temp
            fin = i

    return (suma_maxima, inicio, fin)

```
