import unittest
import algo

class TestZKP(unittest.TestCase):
    
    def test_peggy_honesta(self):
        """Una Peggy honesta debe pasar siempre"""
        for _ in range(50):
            resultado = algo.ejecutar_protocolo(10, es_impostor=False)
            self.assertTrue(resultado)

    def test_intercambio(self):
        """Verifica que la función de intercambio funcione"""
        base = [0, 1]
        cambio = algo.intercambiar_esferas(base)
        self.assertEqual(cambio, [1, 0])

    def test_impostor_falla(self):
        """Un impostor debe fallar eventualmente con muchas rondas"""
        fallos = 0
        intentos = 100
        for _ in range(intentos):
            if not algo.ejecutar_protocolo(20, es_impostor=True):
                fallos += 1
        
        self.assertTrue(fallos > 0)

if __name__ == '__main__':
    unittest.main()