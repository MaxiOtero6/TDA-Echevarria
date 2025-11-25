import time
import random
import matplotlib.pyplot as plt
import numpy as np

def next_fit(objetos, capacidad=1.0):
    if not objetos:
        return []

    recipientes = []
    recipiente_actual = []
    espacio_libre = capacidad

    for objeto in objetos:
        if objeto <= espacio_libre:
            recipiente_actual.append(objeto)
            espacio_libre -= objeto
        else:
            recipientes.append(recipiente_actual)
            recipiente_actual = [objeto]
            espacio_libre = capacidad - objeto

    if recipiente_actual:
        recipientes.append(recipiente_actual)

    return recipientes

"""Calcula métricas de la solución obtenida"""
def calcular_metricas(recipientes, capacidad=1.0):
    if not recipientes:
        return {"num_recipientes": 0, "utilización_promedio": 0, "desperdicio_total": 0}
    
    utilizaciones = [sum(recipiente) for recipiente in recipientes]
    desperdicio_total = len(recipientes) * capacidad - sum(utilizaciones)

    return {
        "num_recipientes": len(recipientes),
        "utilización_promedio": sum(utilizaciones) / len(recipientes),
        "desperdicio_total": desperdicio_total,
        "eficiencia": sum(utilizaciones) / (len(recipientes) * capacidad)
    }

"""Calcula la cota inferior teórica (suma toal / capacidad)"""
def cota_inferior_teorica(objetos, capacidad=1.0):
    import math
    suma_total = sum(objetos)
    return math.ceil(suma_total / capacidad)

"""Genera diferentes tipos de datasets para pruebas"""
def generar_casos_prueba():
    casos = {
        "basico": [0.6, 0.3, 0.7, 0.2, 0.1],
        "intems_grandes": [0.9, 0.8, 0.95, 0.85, 0.7],
        "intems_pequenos": [0.1, 0.2, 0.15, 0.05, 0.3],
        "peor_caso": [0.51, 0.51, 0.51, 0.51, 0.51], # Cada item necesita un recipiente nuevo
        "mixto": [0.4, 0.6, 0.2, 0.8, 0.1, 0.9, 0.3, 0.7],
        "aleatorio": [round(random.uniform(0.01, 0.99), 2) for _ in range(20)]
    }

    return casos

"""Ejecuta las pruebas y muestra los resultados"""
def ejecutar_pruebas(nombre_caso, objetos):
    inicio = time.time()
    recipientes = next_fit(objetos)
    tiempo_ejecucion = time.time() - inicio

    metricas = calcular_metricas(recipientes)
    cota_inferior = cota_inferior_teorica(objetos)
    factor_aproximacion = metricas["num_recipientes"] / cota_inferior if cota_inferior > 0 else 0

    return {
        "caso": nombre_caso,
        "objetos": objetos,
        "recipientes": recipientes,
        "tiempo_ms": tiempo_ejecucion * 1000,
        "metricas": metricas,
        "cota_inferior": cota_inferior,
        "factor_aproximacion": factor_aproximacion
    }

"""Genera el archivo de resultados"""
def generar_archivo_resultados(nombre_archivo="resultados.txt"):
    casos = generar_casos_prueba()

    with open(nombre_archivo, "w") as f:
        f.write("=== ALGORITMO DE APROXIMACIÓN - BIN PACKING PROBLEM ===\n")
        f.write("Garantía de aproximación: 2-OPT\n\n")

        for nombre, objetos in casos.items():
            resultado = ejecutar_pruebas(nombre, objetos)
            f.write(f"--- {nombre.upper()} ---\n")

            if nombre == "aleatorio":
                objetos_str = "[" + ", ".join(f"{obj:.2f}" for obj in resultado['objetos']) + "]"
                f.write(f"Items: {objetos_str}\n")
            else:
                f.write(f"Items: {resultado['objetos']}\n")
                
            f.write(f"Recipientes utilizados: {resultado['metricas']['num_recipientes']}\n")
            f.write(f"Cota inferior teórica: {resultado['cota_inferior']}\n")
            f.write(f"Factor de aproximación: {resultado['factor_aproximacion']:.2f}\n")
            f.write(f"Eficiencia: {resultado['metricas']['eficiencia']:.2%}\n")
            f.write(f"Desperdicio total: {resultado['metricas']['desperdicio_total']:.2f}\n")
            f.write(f"Tiempo de ejecución: {resultado['tiempo_ms']:.4f}ms\n\n")
            
            if len(resultado['recipientes']) <= 10:
                f.write("Asignación por recipiente:\n")
                for i, recipiente in enumerate(resultado['recipientes']):
                    suma_recipiente = sum(recipiente)
                    f.write(f"  R{i+1}: {recipiente} (suma: {suma_recipiente:.2f})\n")
                f.write("\n")

        f.write("=== ANÁLISIS DE COMPLEJIDAD ===\n")
        f.write("Temporal: O(n) - Procesa cada item exactamente una vez\n")
        f.write("Espacial: O(n) - En el peor caso, cada item necesita su propio recipiente\n\n")
        
        f.write("=== GARANTÍA TEÓRICA ===\n")
        f.write("Para cualquier instancia I: NextFit(I) ≤ 2 * OPT(I)\n")
        f.write("El algoritmo nunca utiliza más del doble de recipientes que la solución óptima.\n")

"""Ejecuta experimentos con datasets de diferentes tamaños para medir tiempos"""
def experimentos_escalabilidad():
    tamanios = [50, 100, 200, 500, 1000, 2000, 5000]
    tiempos_promedio = []
    factores_aproximacion = []

    print("=== MEDICIÓN DE TIEMPOS DE EJECUCIÓN ===")
    print("Tamaño\tTiempo(ms)\tFactor Aprox.")
    print("-" * 40)

    for n in tamanios:
        tiempos_corrida = []
        factores_corrida = []

        for _ in range(10):
            objetos = [round(random.uniform(0.1, 0.9), 2) for _ in range(n)]
            inicio = time.perf_counter()
            recipientes = next_fit(objetos)
            tiempo = (time.perf_counter() - inicio)

            metricas = calcular_metricas(recipientes)
            cota_inferior = cota_inferior_teorica(objetos)
            factor_aprox = metricas["num_recipientes"] / cota_inferior

            tiempos_corrida.append(tiempo * 1000)
            factores_corrida.append(factor_aprox)

        tiempo_promedio = sum(tiempos_corrida) / len(tiempos_corrida)
        factor_promedio = sum(factores_corrida) / len(factores_corrida)

        tiempos_promedio.append(tiempo_promedio)
        factores_aproximacion.append(factor_promedio)

        print(f"{n}\t{tiempo_promedio:.4f}\t\t{factor_promedio:.2f}")
    
    return tamanios, tiempos_promedio, factores_aproximacion

"""Genera gráfico de tiempos de ejecución vs tamaño del dataset"""
def generar_grafico_tiempos():
    tamanios, tiempos, factores = experimentos_escalabilidad()

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    fig.suptitle('Análisis Experimental - Algoritmo Next Fit', fontsize=16, fontweight='bold')

    # Gráfico 1: Tiempo vs Tamaño
    ax1.plot(tamanios, tiempos, 'b-o', linewidth=2, markersize=6, label='Tiempo medido')
    ax1.set_xlabel('Tamaño del dataset (n)')
    ax1.set_ylabel('Tiempo promedio (ms)')
    ax1.set_title('Tiempo de Ejecución vs Tamaño')
    ax1.grid(True, alpha=0.3)

    coef_lineal = tiempos[-1] / tamanios[-1]
    linea_teorica = [coef_lineal * n for n in tamanios]
    ax1.plot(tamanios, linea_teorica, 'r--', alpha=0.7, label='O(n) Teórico')
    ax1.legend()

    # Gráfico 2: Factor de Aproximación vs Tamaño
    colors = ['#4a90e2', '#5ba3f5', '#6cb6ff', '#7dc9ff', '#8edcff', '#9fefff', '#b0f2ff']

    bars = ax2.bar(range(len(tamanios)), factores, color=colors, alpha=0.8, edgecolor='navy', linewidth=1.5, label='Factor medido')

    factor_min = min(factores) - 0.02
    factor_max = max(factores) + 0.02
    ax2.set_ylim(factor_min, factor_max)

    if factor_max >= 2.0:
        ax2.axhline(y=2.0, color='r', linestyle='--', linewidth=2.5, alpha=0.9, label='Límite teórico (2.0)')
    if factor_min <= 1.0:
        ax2.axhline(y=1.0, color='green', linestyle=':', linewidth=2, alpha=0.8, label='Óptimo (1.0)')

    ax2.set_xlabel('Tamaño del dataset (n)')
    ax2.set_ylabel('Factor de aproximación')
    ax2.set_title('Factor de aproximación vs Tamaño')
    ax2.set_xticks(range(len(tamanios)))
    ax2.set_xticklabels([f'{t}' for t in tamanios])

    ax2.grid(True, alpha=0.4, axis='y', linewidth=0.5)
    if factor_max >= 2.0 or factor_min <= 1.0:
        ax2.legend(loc='upper left')
    else:
        ax2.legend(loc='upper left')

    for bar, factor in zip(bars, factores):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/ 2, height + 0.003, f'{factor:.3f}', ha='center', va='bottom', fontweight='bold', fontsize=9, color='navy')

    promedio = sum(factores)/len(factores)
    rango_min, rango_max = min(factores), max(factores)
    variacion = rango_max - rango_min

    stats_text = f'Promedio: {promedio:.3f}\n'
    stats_text += f'Rango: {rango_min:.3f} - {rango_max:.3f}\n'
    stats_text += f'Variación: ±{variacion/2:.3f}\n'
    stats_text += f'Desv. del óptimo: ~{(promedio - 1)*100:.1f}%'

    ax2.text(0.98, 0.02, stats_text, transform=ax2.transAxes, fontsize=9,
            verticalalignment='bottom', horizontalalignment='right',
            bbox=dict(boxstyle='round,pad=0.4', facecolor='lightyellow',
            alpha=0.9, edgecolor='orange'))

    plt.tight_layout()
    plt.savefig('tiempos_ejecucion_next_fit.png', dpi=300, bbox_inches='tight')
    print("Gráfico guardado como 'tiempos_ejecucion_next_fit.png'")
    plt.close()

    return tamanios, tiempos, factores

"""Genera reporte detallado de tiempos para el informe"""
def generar_reporte_tiempos():
    generar_grafico_tiempos()

    print("\n=== REPORTE DE TIEMPOS PARA INFORME ===")
    print("Complejidad teórica: O(n)")
    print("Complejidad empírica observada: Lineal")
    print("Los datos detallados se encuentran en la tabla anterior.")
    print("Gráfico generado y guardado como 'tiempos_ejecucion_next_fit.png'")

def main():
    casos = generar_casos_prueba()

    print("=== ALGORITMO NEXT FIT - MENÚ DE OPCIONES ===\n")
    print("1. Ejecutar casos de prueba básicos")
    print("2. Generar gráficos de tiempos de ejecución")
    print("3. Ambos")

    opcion = input("Seleccione una opción (1-3): ")

    if opcion in ['1', '3']:
        casos = generar_casos_prueba()
        print("\n=== RESULTADOS DE CASOS DE PRUEBA ===\n")

        for nombre, objetos in casos.items():
            resultado = ejecutar_pruebas(nombre, objetos)
            print(f"--- {nombre.upper()} ---")

            if nombre == "aleatorio":
                objetos_str = "[" + ", ".join(f"{obj:.2f}" for obj in resultado['objetos']) + "]"
                print(f"Objetos: {objetos_str}")
            else:
                print(f"Objetos: {resultado['objetos']}")
            
            print(f"Recipientes utilizados: {resultado['metricas']['num_recipientes']}")
            print(f"Factor de aproximación: {resultado['factor_aproximacion']:.2f}")
            print(f"Eficiencia: {resultado['metricas']['eficiencia']:.2%}")
            print(f"Tiempo: {resultado['tiempo_ms']:.4f}ms")
            print()
    if opcion in ['2', '3']:
        print("\n=== ANÁLISIS DE TIEMPOS DE EJECUCIÓN ===")
        tamanios, tiempos, factores = generar_grafico_tiempos()
        
        print(f"\nTiempo para n=5000: {tiempos[-1]:.4f}ms")
        
        ratios = []
        for i in range(1, len(tamanios)):
            ratio_tamaño = tamanios[i] / tamanios[i-1]
            ratio_tiempo = tiempos[i] / tiempos[i-1]
            ratios.append(ratio_tiempo / ratio_tamaño)
        
        linealidad_promedio = sum(ratios) / len(ratios)
        print(f"Coeficiente de linealidad promedio: {linealidad_promedio:.2f} (ideal: 1.0)")
        print(f"Factor de aproximación promedio: {sum(factores)/len(factores):.2f}")

        generar_reporte_tiempos()

    if opcion in ['1', '3']:
        print("Generando archivo de resultados...")
        generar_archivo_resultados()
        print("Archivo de resultados generado.")

if __name__ == "__main__":
    main()