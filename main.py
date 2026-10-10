from qqq_game_backend import simple_ttt_game
from quantum_circuit_testing import test_circuit
from quantum_evaluators import simple_paramitrized_evaluator


#main method
if __name__ == "__main__":
    simple_ttt_game()
    test_circuit(circuit = simple_paramitrized_evaluator(0.8))