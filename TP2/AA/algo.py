"""AA - Bin Packing (Next Fit) CLI
Quick start:
    python -m TP2.AA.algo          # menú interactivo (casos/gráficos/ambos)

Canonical run (used in the report):
    python -m TP2.AA.algo --mode graficos --reps 0 --warmups 10 --minsec 1.0 --trim 0.20 --suffix _1s

Options:
    --mode {casos,graficos,ambos}  --reps N  --warmups N  --trim R  --minsec S  --suffix _tag  --seed 42

Outputs (in TP2/AA):
    resultados.txt, casos{suffix}.csv, escalabilidad{suffix}.csv, residuos{suffix}.csv,
    tiempos_ejecucion_next_fit{suffix}.png
"""
import argparse
import statistics
from algoritmo import generar_casos_prueba, next_fit, calcular_metricas, cota_inferior_teorica
from benchmark_plot import medir_corrida, generar_grafico_tiempos

"""Ejecuta las pruebas y muestra los resultados"""
def ejecutar_pruebas(nombre_caso, objetos, repeticiones=30, warmups=3):
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
            r = ejecutar_pruebas(nombre, objetos)
            f.write(f"--- {nombre.upper()} ---\n")
            objs = "[" + ", ".join(f"{o:.2f}" for o in r['objetos']) + "]"
            f.write(f"Items: {objs}\n")
            f.write(f"Recipientes utilizados: {r['metricas']['num_recipientes']}\n")
            f.write(f"Cota inferior teórica: {r['cota_inferior']}\n")
            f.write(f"Factor de aproximación: {r['factor_aproximacion']:.2f}\n")
            f.write(f"Eficiencia: {r['metricas']['eficiencia']:.2%}\n")
            f.write(f"Desperdicio total: {r['metricas']['desperdicio_total']:.2f}\n")
            f.write(f"Tiempo de ejecución: {r['tiempo_ms']:.4f}ms\n\n")
            
            if len(r['recipientes']) <= 10:
                f.write("Asignación por recipiente:\n")
                for i, rec in enumerate(r['recipientes']):
                    f.write(f"  R{i+1}: {rec} (suma: {sum(rec):.2f})\n")
                f.write("\n")

        f.write("=== ANÁLISIS DE COMPLEJIDAD ===\n")
        f.write("Temporal: O(n) - Procesa cada item exactamente una vez\n")
        f.write("Espacial: O(n) - En el peor caso, cada item necesita su propio recipiente\n\n")
        
        f.write("=== GARANTÍA TEÓRICA ===\n")
        f.write("Para cualquier instancia I: NextFit(I) ≤ 2 * OPT(I)\n")
        f.write("El algoritmo nunca utiliza más del doble de recipientes que la solución óptima.\n")

"""Genera reporte detallado de tiempos para el informe"""
def generar_reporte_tiempos():
    generar_grafico_tiempos()

    print("\n=== REPORTE DE TIEMPOS PARA INFORME ===")
    print("Complejidad teórica: O(n)")
    print("Complejidad empírica observada: Lineal")
    print("Los datos detallados se encuentran en la tabla anterior.")
    print("Gráfico generado y guardado como 'tiempos_ejecucion_next_fit.png'")

"""Parsea argumentos de línea de comandos"""
def parse_args():
    p = argparse.ArgumentParser(description="Next Fit - CLI")
    p.add_argument("--mode", choices=["1", "2", "3", "casos", "graficos", "ambos"],
                   help="1=casos, 2=gráficos, 3=ambos")
    p.add_argument("--reps", type=int, default=40)
    p.add_argument("--warmups", type=int, default=3)
    p.add_argument("--trim", type=float, default=0.10)
    p.add_argument("--minsec", type=float, default=0.0, help="tiempo mínimo por n (segundos)")
    p.add_argument("--suffix", default="")
    p.add_argument("--seed", type=int, default=42)
    return p.parse_args()

"""Punto de entrada de la CLI"""
def main():
    args = parse_args()
    seed = args.seed
    casos = generar_casos_prueba(seed=seed)

    opcion = args.mode
    if opcion is None:
        print("=== ALGORITMO NEXT FIT - MENÚ DE OPCIONES ===\n")
        print("1. Ejecutar casos de prueba básicos")
        print("2. Generar gráficos de tiempos de ejecución")
        print("3. Ambos")
        opcion = input("Seleccione una opción (1-3): ")

    if opcion in ["casos"]: opcion = '1'
    if opcion in ["graficos"]: opcion = '2'
    if opcion in ["ambos"]: opcion = '3'

    if opcion in ['1', '3']:
        print("\n=== RESULTADOS DE CASOS DE PRUEBA ===\n")

        for nombre, objetos in casos.items():
            r = ejecutar_pruebas(nombre, objetos)
            print(f"--- {nombre.upper()} ---")
            objs = "[" + ", ".join(f"{o:.2f}" for o in r['objetos']) + "]"
            print(f"Objetos: {objs}")
            print(f"Recipientes utilizados: {r['metricas']['num_recipientes']}")
            print(f"Factor de aproximación: {r['factor_aproximacion']:.2f}")
            print(f"Eficiencia: {r['metricas']['eficiencia']:.2%}")
            print(f"Tiempo: {r['tiempo_ms']:.4f}ms")
            print()

    if opcion in ['2', '3']:
        reps, warms, trim, suf = args.reps, args.warmups, args.trim, args.suffix
        minsec = args.minsec
        if args.mode is None:
            try:
                reps = int(input("Repeticiones [40]: ") or 40)
                warms = int(input("Warmups [3]: ") or 3)
                trim = float(input("Trim ratio [0.10]: ") or 0.10)
                min_in = input("Tiempo mínimo por n en s [0]: ") or "0"
                minsec = float(min_in)
                suf = input("Sufijo del PNG (ej. _60rp) []: ") or ""
            except Exception:
                pass

        print("\n=== ANÁLISIS DE TIEMPOS DE EJECUCIÓN ===")
        tamanios, tiempos, factores, pend = generar_grafico_tiempos(
            repeticiones=reps, warmups=warms, seed=42, trim_ratio=trim, out_suffix=suf, min_seconds=minsec)
        print(f"\nTiempo para n={tamanios[-1]}: {tiempos[-1]:.4f}ms")
        print(f"Factor medio: {sum(factores)/len(factores):.3f}")
        print(f"Pendiente normalizada (linealidad ≈1): {pend:.2f}")

    if opcion in ['1', '3']:
        print("Generando archivo de resultados...")
        generar_archivo_resultados(seed=42)
        guardar_resultados_casos(seed=42, nombre=f"casos{args.suffix}.csv")
        print("Archivo de resultados generado.")

if __name__ == "__main__":
    main()