import random

def crear_esferas():
    return [0, 1]

def intercambiar_esferas(esferas):
    return [esferas[1], esferas[0]]

def turno_victor():
    return random.randint(0, 1)

def turno_peggy(esferas_originales, esferas_actuales, es_impostor):
    if not es_impostor:
        if esferas_originales != esferas_actuales:
            return 1
        else:
            return 0
    else:
        return random.randint(0, 1)
    
def ejecutar_protocolo(k_rondas, es_impostor=False):
    esferas_base = crear_esferas()

    for _ in range(k_rondas):
        decision = turno_victor()

        if decision == 1:
            esferas_mesa = intercambiar_esferas(esferas_base)
        else:
            esferas_mesa = list(esferas_base)
        
        respuesta = turno_peggy(esferas_base, esferas_mesa, es_impostor)

        if respuesta != decision:
            return False
    
    return True

