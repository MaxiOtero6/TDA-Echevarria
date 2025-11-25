import time
import random
import matplotlib.pyplot as plt
import numpy as np
import os, gc, statistics

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
def generar_casos_prueba(seed=None):
    rng = random.Random(seed) if seed is not None else random
    casos = {
        "basico": [0.6, 0.3, 0.7, 0.2, 0.1],
        "items_grandes": [0.9, 0.8, 0.95, 0.85, 0.7],
        "items_pequenos": [0.1, 0.2, 0.15, 0.05, 0.3],
        "peor_caso": [0.51, 0.51, 0.51, 0.51, 0.51], # Cada item necesita un recipiente nuevo
        "mixto": [0.4, 0.6, 0.2, 0.8, 0.1, 0.9, 0.3, 0.7],
        "aleatorio": [round(rng.uniform(0.01, 0.99), 2) for _ in range(20)]
    }

    return casos

"""Ejecuta las pruebas y muestra los resultados"""
def ejecutar_pruebas(nombre_caso, objetos, repeticiones=30, warmups=3):
    # inicio = time.time()
    # recipientes = next_fit(objetos)
    # tiempo_ejecucion = time.time() - inicio

    for _ in range(warmups):
        next_fit(objetos)
    muestras = [medir_corrida(lambda: next_fit(objetos)) for _ in range(repeticiones)]
    muestras.sort()
    k = max(1, repeticiones // 10)
    trimmed = muestras[k:-k] if len(muestras) > 2 * k else muestras
    tiempo_ms = statistics.mean(trimmed)
    
    recipientes = next_fit(objetos)
    metricas = calcular_metricas(recipientes)
    cota_inferior = cota_inferior_teorica(objetos)
    factor_aproximacion = metricas["num_recipientes"] / cota_inferior if cota_inferior > 0 else 0

    return {
        "caso": nombre_caso,
        "objetos": objetos,
        "recipientes": recipientes,
        "tiempo_ms": tiempo_ms,
        "metricas": metricas,
        "cota_inferior": cota_inferior,
        "factor_aproximacion": factor_aproximacion
    }

"""Guarda métricas de los casos"""
def guardar_resultados_casos(seed=42, nombre="casos.csv", repeticiones=30, warmups=3):
    casos = generar_casos_prueba(seed=seed)
    with open(nombre, "w") as f:
        f.write("caso,n,usados,lb,factor,eficiencia,desperdicio,tiempo_ms\n")
        for nombre_caso, objetos in casos.items():
            res = ejecutar_pruebas(nombre_caso, objetos, repeticiones=repeticiones, warmups=warmups)
            met = res["metricas"]
            f.write(f"{nombre_caso},{len(objetos)},{met['num_recipientes']},{res['cota_inferior']},"
                    f"{res['factor_aproximacion']:.6f},{met['eficiencia']:.6f},{met['desperdicio_total']:.6f},"
                    f"{res['tiempo_ms']:.6f}\n")

"""Genera el archivo de resultados"""
def generar_archivo_resultados(nombre_archivo="resultados.txt", seed=42):
    casos = generar_casos_prueba(seed=seed)

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
def experimentos_escalabilidad(repeticiones=40, warmups=3, seed=None):
    rng = random.Random(seed) if seed is not None else None
    tamanios = [50, 100, 200, 500, 1000, 2000, 5000]
    resultados = []

    print("=== MEDICIÓN DE TIEMPOS DE EJECUCIÓN ===")
    print("n\ttrim_mean(ms)\tmedian(ms)\tσ_trim(ms)\tfactor")
    print("-" * 60)
    
    for n in tamanios:
        datos = generar_dataset(n, rng=rng)
        stats = medir(next_fit, datos, warmups=warmups, repeticiones=repeticiones)
        recipientes = next_fit(datos)
        cota = cota_inferior_teorica(datos)
        factor = len(recipientes) / cota if cota else 0
        print(f"{n}\t{stats['trimmed_mean']:.4f}\t{stats['median']:.4f}\t{stats['trimmed_stdev']:.4f}\t{factor:.3f}")
        resultados.append((n, stats, factor))

    return resultados    
    
"""Mide una corrida única con reducción de ruido"""
def medir_corrida(func):
    gc.disable()
    t0 = time.perf_counter_ns()
    func()
    t1 = time.perf_counter_ns()
    gc.enable()
    return (t1 - t0) / 1e6 # ms

"""Genera benchmark con warmups, repeticiones y trimmed mean"""
def medir(next_fit_func, datos, warmups=3, repeticiones=40, trim_ratio=0.1):
    for _ in range(warmups):
        next_fit_func(datos)
    
    muestras = [medir_corrida(lambda: next_fit_func(datos)) for _ in range(repeticiones)]
    muestras.sort()

    k = max(1, int(repeticiones * trim_ratio))
    trimmed = muestras[k: -k] if len(muestras) > 2 * k else muestras

    return {
        "mean": statistics.mean(trimmed),
        "median": statistics.median(trimmed),
        "stdev": statistics.stdev(trimmed) if len(trimmed) > 1 else 0.0,
        "trimmed_mean": statistics.mean(trimmed),
        "trimmed_stdev": statistics.stdev(trimmed) if len(trimmed) > 1 else 0.0,
        "min": muestras[0],
        "max": muestras[-1],
        "samples": muestras
    }

"""Genera datasets separados (sin medir)"""
def generar_dataset(n, rng=None):
    r = rng if rng is not None else random
    return [round(r.uniform(0.1, 0.9), 2) for _ in range(n)]

def guardar_resultados_escalabilidad(resultados, nombre="escalabilidad.csv"):
    with open(nombre, "w") as f:
        f.write("n,trim_mean_ms,trim_stdev_ms,factor\n")
        for n, stats, factor in resultados:
            f.write(f"{n},{stats['trimmed_mean']:.6f},{stats['trimmed_stdev']:.6f},{factor:.6f}\n")

"""Genera gráfico de tiempos de ejecución vs tamaño del dataset"""
def generar_grafico_tiempos(repeticiones=40, warmups=3, seed=None):
    resultados = experimentos_escalabilidad(repeticiones=repeticiones, warmups=warmups, seed=seed)
    tamanios = [r[0] for r in resultados]
    tiempos = [r[1]['trimmed_mean'] for r in resultados]
    factores = [r[2] for r in resultados]

    x = np.array(tamanios, dtype=float)
    y = np.array(tiempos, dtype=float)
    a, b = np.polyfit(x, y, 1)
    pendiente_normalizada = a / (y[-1] / x[-1])

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    fig.suptitle('Análisis Experimental - Algoritmo Next Fit', fontsize=16, fontweight='bold')

    # Gráfico 1: Tiempo vs Tamaño
    ax1.plot(tamanios, tiempos, 'b-o', linewidth=2, markersize=6, label='Tiempo medido')
    linea_teorica = a * x + b
    ax1.plot(tamanios, linea_teorica, 'r--', label='O(n) Teórico')
    ax1.set_xlabel('n')
    ax1.set_ylabel('Tiempo (ms)')
    ax1.set_title('Tiempo de Ejecución vs tamaño')
    ax1.grid(alpha=0.3)
    ax1.legend()

    # Gráfico 2: Factor de Aproximación vs Tamaño
    # colors = ['#4a90e2', '#5ba3f5', '#6cb6ff', '#7dc9ff', '#8edcff', '#9fefff', '#b0f2ff']

    # bars = ax2.bar(tamanios, factores, color=colors, alpha=0.85, edgecolor='navy', linewidth=1.1, label='Factor medido')

    # factor_min = min(factores) - 0.02
    # factor_max = max(factores) + 0.02
    # ax2.set_ylim(factor_min, factor_max)

    # if factor_max >= 2.0:
    #     ax2.axhline(y=2.0, color='r', linestyle='--', linewidth=2.5, alpha=0.9, label='Límite teórico (2.0)')
    # if factor_min <= 1.0:
    #     ax2.axhline(y=1.0, color='green', linestyle=':', linewidth=2, alpha=0.8, label='Óptimo (1.0)')

    # ax2.set_xticks(range(len(tamanios)))
    # ax2.set_xticklabels([str(n) for n in tamanios])

    idx = list(range(len(tamanios)))
    cmap = plt.get_cmap('Blues')
    colors = [cmap(i / (len(tamanios) - 1)) for i in idx]

    ax2.set_title('Factor vs tamaño')
    bars = ax2.bar(idx, factores, width=0.6, color=colors, edgecolor='navy', linewidth=1.0)

    ax2.set_xticks(idx)
    ax2.set_xticklabels([str(n) for n in tamanios])
    ax2.set_xlabel('n')
    ax2.set_ylabel('Factor de aproximación')

    ymin = min(factores) - 0.02
    ymax = max(factores) + 0.02
    ax2.set_ylim(ymin, ymax)
    ax2.grid(alpha=0.35, axis='y')

    # Líneas de referencia
    ax2.axhline(1.0, color='green', linestyle=':', linewidth=1.8, alpha=0.8, label='Óptimo (1.0)')
    ax2.axhline(2.0, color='red', linestyle='--', linewidth=2.0, alpha=0.8, label='Cota teórica (2.0)')

    for bar, f in zip(bars, factores):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height()+0.003,
                 f'{f:.3f}', ha='center', va='bottom', fontsize=9)

    prom = sum(factores)/len(factores)
    ax2.text(0.98, 0.02,
             f'Promedio: {prom:.3f}\nRango: {min(factores):.3f}-{max(factores):.3f}',
             transform=ax2.transAxes, ha='right', va='bottom',
             bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.9))

    ax2.legend(loc='upper left')

    # bars = ax2.bar(tamanios, factores, width=0.75, color='#6cb6ff', edgecolor='navy', linewidth=1.3)
    # ax2.set_xlabel('n')
    # ax2.set_ylabel('Factor de aproximación')
    # ax2.set_title('Factor vs tamaño')
    # ax2.set_xticks(tamanios)
    # ax2.set_xticklabels([str(n) for n in tamanios], rotation=0)
    # ymin = min(factores) - 0.02; ymax = max(factores) + 0.02
    # ax2.set_ylim(ymin, ymax)
    # ax2.grid(alpha=0.35, axis='y')

    # for bar, f in zip(bars, factores):
    #     ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height()+0.003, f'{f:.3f}', ha='center', va='bottom', fontsize=9)

    # promedio = sum(factores)/len(factores)
    # ax2.text(0.98, 0.02,
    #         f'Promedio: {promedio:.3f}\nRango: {min(factores):.3f}-{max(factores):.3f}',
    #         transform=ax2.transAxes,
    #         ha='right', va='bottom',
    #         bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.9))
    # rango_min, rango_max = min(factores), max(factores)
    # variacion = rango_max - rango_min

    # stats_text = f'Promedio: {promedio:.3f}\n'
    # stats_text += f'Rango: {rango_min:.3f} - {rango_max:.3f}\n'
    # stats_text += f'Variación: ±{variacion/2:.3f}\n'
    # stats_text += f'Desv. del óptimo: ~{(promedio - 1)*100:.1f}%'

    # ax2.text(0.98, 0.02, stats_text, transform=ax2.transAxes, fontsize=9,
    #         verticalalignment='bottom', horizontalalignment='right',
    #         bbox=dict(boxstyle='round,pad=0.4', facecolor='lightyellow',
    #         alpha=0.9, edgecolor='orange'))

    plt.tight_layout()
    plt.savefig('tiempos_ejecucion_next_fit.png', dpi=300, bbox_inches='tight')
    print("Gráfico guardado como 'tiempos_ejecucion_next_fit.png'")
    plt.close()

    guardar_resultados_escalabilidad(resultados)

    return tamanios, tiempos, factores, pendiente_normalizada

"""Genera reporte detallado de tiempos para el informe"""
def generar_reporte_tiempos():
    generar_grafico_tiempos()

    print("\n=== REPORTE DE TIEMPOS PARA INFORME ===")
    print("Complejidad teórica: O(n)")
    print("Complejidad empírica observada: Lineal")
    print("Los datos detallados se encuentran en la tabla anterior.")
    print("Gráfico generado y guardado como 'tiempos_ejecucion_next_fit.png'")

def main():
    casos = generar_casos_prueba(seed=42)

    print("=== ALGORITMO NEXT FIT - MENÚ DE OPCIONES ===\n")
    print("1. Ejecutar casos de prueba básicos")
    print("2. Generar gráficos de tiempos de ejecución")
    print("3. Ambos")

    opcion = input("Seleccione una opción (1-3): ")

    if opcion in ['1', '3']:
        print("\n=== RESULTADOS DE CASOS DE PRUEBA ===\n")

        for nombre, objetos in casos.items():
            resultado = ejecutar_pruebas(nombre, objetos)
            print(f"--- {nombre.upper()} ---")

            # if nombre == "aleatorio":
            objs = "[" + ", ".join(f"{obj:.2f}" for obj in resultado['objetos']) + "]"
            print(f"Objetos: {objs}")
            # else:
            #     print(f"Objetos: {resultado['objetos']}")
            
            print(f"Recipientes utilizados: {resultado['metricas']['num_recipientes']}")
            print(f"Factor de aproximación: {resultado['factor_aproximacion']:.2f}")
            print(f"Eficiencia: {resultado['metricas']['eficiencia']:.2%}")
            print(f"Tiempo: {resultado['tiempo_ms']:.4f}ms")
            print()

    if opcion in ['2', '3']:
        print("\n=== ANÁLISIS DE TIEMPOS DE EJECUCIÓN ===")
        tamanios, tiempos, factores, pend_norm = generar_grafico_tiempos(seed=42)
        print(f"\nTiempo para n=5000: {tiempos[-1]:.4f}ms")
        print(f"Factor medio: {sum(factores)/len(factores):.3f}")
        print(f"Pendiente normalizada (linealidad ≈1): {pend_norm:.2f}")
        
        # # ratios = []
        # # for i in range(1, len(tamanios)):
        # #     ratio_tamaño = tamanios[i] / tamanios[i-1]
        # #     ratio_tiempo = tiempos[i] / tiempos[i-1]
        # #     ratios.append(ratio_tiempo / ratio_tamaño)
        
        # # linealidad_promedio = sum(ratios) / len(ratios)
        # print(f"Coeficiente de linealidad promedio: {linealidad_promedio:.2f} (ideal: 1.0)")
        # print(f"Factor de aproximación promedio: {sum(factores)/len(factores):.2f}")

        # generar_reporte_tiempos()

    if opcion in ['1', '3']:
        print("Generando archivo de resultados...")
        generar_archivo_resultados(seed=42)
        guardar_resultados_casos(seed=42)
        print("Archivo de resultados generado.")

if __name__ == "__main__":
    main()