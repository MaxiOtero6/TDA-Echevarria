"""Benchmark utilities for AA - Next Fit
- medir_corrida: single run timing with GC noise reduction.
- medir: warmups + repetitions + trimmed mean; supports --min_seconds to target ≥ T per n.
- experimentos_escalabilidad: loops sizes [50..5000], computes factor vs. theoretical lower bound.
- generar_grafico_tiempos: saves PNG (3 panels) + CSVs (escalabilidad, residuos).

Canonical usage:
  python -m TP2.AA.algo --mode graficos --reps 0 --warmups 10 --minsec 1.0 --trim 0.20 --suffix _1s

Outputs:
  escalabilidad{suffix}.csv, residuos{suffix}.csv, tiempos_ejecucion_next_fit{suffix}.png
"""
import time, gc, statistics, random
import numpy as np
import matplotlib.pyplot as plt
from algoritmo import next_fit, cota_inferior_teorica, generar_dataset

"""Mide una corrida única con reducción de ruido"""
def medir_corrida(func):
    gc.disable()
    t0 = time.perf_counter_ns()
    func()
    t1 = time.perf_counter_ns()
    gc.enable()
    return (t1 - t0) / 1e6 # ms

"""Genera benchmark con warmups, repeticiones y trimmed mean"""
def medir(next_fit_func, datos, warmups=3, repeticiones=40, trim_ratio=0.1, min_seconds=0.0):
    for _ in range(warmups):
        next_fit_func(datos)

    if min_seconds > 0:
        est = statistics.mean(medir_corrida(lambda: next_fit_func(datos)) for _ in range(5))
        repeticiones = max(repeticiones, int((min_seconds * 1000) / max(est, 1e-6)))
        repeticiones = min(repeticiones, 200_000)

    
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
        "samples": muestras,
        "reps": repeticiones
    }

"""Ejecuta experimentos con datasets de diferentes tamaños para medir tiempos"""
def experimentos_escalabilidad(repeticiones=40, warmups=3, seed=None, trim_ratio=0.1, min_seconds=0.0):
    rng = random.Random(seed) if seed is not None else None
    tamanios = [50, 100, 200, 500, 1000, 2000, 5000]
    resultados = []

    print("=== MEDICIÓN DE TIEMPOS DE EJECUCIÓN ===")
    hdr = "n\ttrim_mean(ms)\tmedian(ms)\tσ_trim(ms)\tfactor\treps"
    print(hdr); print("-" * len(hdr.expandtabs()))
    # print("-" * 60)
    
    for n in tamanios:
        datos = generar_dataset(n, rng=rng)
        stats = medir(next_fit, datos, warmups=warmups, repeticiones=repeticiones, trim_ratio=trim_ratio, min_seconds=min_seconds)
        recipientes = next_fit(datos)
        cota = cota_inferior_teorica(datos)
        factor = len(recipientes) / cota if cota else 0
        print(f"{n}\t{stats['trimmed_mean']:.4f}\t{stats['median']:.4f}\t{stats['trimmed_stdev']:.4f}\t{factor:.3f}\t{stats['reps']}")
        resultados.append((n, stats, factor))

    return resultados

"""Guarda CSV de escalabilidad (tiempos y factores)"""
def guardar_resultados_escalabilidad(resultados, nombre="escalabilidad.csv"):
    with open(nombre, "w") as f:
        f.write("n,trim_mean_ms,trim_stdev_ms,factor\n")
        for n, stats, factor in resultados:
            f.write(f"{n},{stats['trimmed_mean']:.6f},{stats['trimmed_stdev']:.6f},{factor:.6f}\n")

"""Guarda residuos de la regresión lineal"""
def guardar_residuos(tamanios, tiempos, a, b, out_suffix=""):
    import math
    pred = a * np.array(tamanios) + b
    resid = np.array(tiempos) - pred
    std = float(np.std(resid, ddof=1)) if len(resid) > 1 else 0.0
    with open(f"residuos{out_suffix}.csv", "w") as f:
        f.write("n,tiempo_ms,pred_ms,resid_ms,z\n")
        for n, t, p, r in zip(tamanios, tiempos, pred, resid):
            z = (r / std) if std > 0 else 0.0
            f.write(f"{n},{t:.6f},{float(p):.6f},{float(r):.6f},{z:.3f}\n")
    orden = np.argsort(-np.abs(resid / std)) if std > 0 else []
    if len(orden) > 0:
        print("Top outliers por |z|:", [(tamanios[i], float(resid[i]/std)) for i in orden[:2]])

"""Guarda CSV extendido (trimmed, mediana, repeticiones, factor)"""
def guardar_resultados_ext(resultados, nombre="escalabilidad_ext.csv"):
    with open(nombre, "w") as f:
        f.write("n,trim_mean_ms,median_ms,trim_stdev_ms,reps,factor\n")
        for n, stats, factor in resultados:
            f.write(f"{n},{stats['trimmed_mean']:.6f},{stats['median']:.6f},{stats['trimmed_stdev']:.6f},{stats['reps']},{factor:.6f}\n")

"""Genera gráfico de tiempos de ejecución vs tamaño del dataset"""
def generar_grafico_tiempos(repeticiones=40, warmups=3, seed=None, trim_ratio=0.1, out_suffix="", min_seconds=0.0):
    resultados = experimentos_escalabilidad(repeticiones, warmups, seed, trim_ratio, min_seconds)
    tamanios = [r[0] for r in resultados]
    tiempos = [r[1]['trimmed_mean'] for r in resultados]
    medianas = [r[1]['median'] for r in resultados]
    factores = [r[2] for r in resultados]

    x = np.array(tamanios, dtype=float)
    y = np.array(tiempos, dtype=float)
    a, b = np.polyfit(x, y, 1)
    pendiente_normalizada = a / (y[-1] / x[-1])

    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 6))
    fig.suptitle('Análisis Experimental - Algoritmo Next Fit', fontsize=16, fontweight='bold')

    # Gráfico 1: Tiempo vs Tamaño
    ax1.plot(tamanios, tiempos, 'b-o', linewidth=2, markersize=6, label='Tiempo medido')
    linea_teorica = a * x + b
    ax1.plot(tamanios, linea_teorica, 'r--', label='Ajuste lineal (O(n))')
    ax1.set_xlabel('n')
    ax1.set_ylabel('Tiempo (ms)')
    ax1.set_title('Tiempo de Ejecución vs tamaño')
    ax1.grid(alpha=0.3)
    ax1.legend()

    # Gráfico 2: Factor de Aproximación vs Tamaño
    idx = list(range(len(tamanios)))
    cmap = plt.get_cmap('Blues')
    colors = [cmap(i / (len(tamanios) - 1)) for i in idx]

    ax2.set_title('Factor vs tamaño')
    bars = ax2.bar(idx, factores, width=0.6, color=colors, edgecolor='navy', linewidth=1.0)

    ax2.set_xticks(idx)
    ax2.set_xticklabels([str(n) for n in tamanios])
    ax2.set_xlabel('n')
    ax2.set_ylabel('Factor de aproximación')

    ax2.set_ylim(min(factores) - 0.02, max(factores) + 0.02)
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

    # Gráfico 3: Mediana vs trimmed
    ax3.plot(tamanios, tiempos, 'b-o', label='Trimmed mean')
    ax3.plot(tamanios, medianas, 'g-s', label='Mediana')
    ax3.set_title('Mediana vs Trimmed')
    ax3.set_xlabel('n')
    ax3.set_ylabel('Tiempo (ms)')
    ax3.grid(alpha=0.3)
    ax3.legend()

    plt.tight_layout()
    nombre_png = f"tiempos_ejecucion_next_fit{out_suffix}.png"
    plt.savefig(nombre_png, dpi=300, bbox_inches='tight')
    print(f"Gráfico guardado como '{nombre_png}'")
    plt.close()

    guardar_resultados_escalabilidad(resultados, nombre=f"escalabilidad{out_suffix}.csv")
    guardar_residuos(tamanios, tiempos, a, b, out_suffix)

    return tamanios, tiempos, factores, pendiente_normalizada
