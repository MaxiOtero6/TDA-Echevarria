import time
import random

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

def main():
    casos = generar_casos_prueba()

    print("=== ALGORITMO NEXT FIT - RESULTADOS DE PRUEBAS ===\n")

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

if __name__ == "__main__":
    main()
    print("Generando archivo de resultados...")
    generar_archivo_resultados()
    print("Archivo de resultados generado.")