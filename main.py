from quantum_circuit_testing import test_circuit
from quantum_evaluators import simple_pair_entangled_evaluator, simple_multi_entangled_evaluator
from terminal_interface.terminal_main import game_run

#toto nejde do qollab
from qiskit_aer import AerSimulator

#main method
if __name__ == "__main__":
    simulator = AerSimulator()
    game_run(simulator)
    test_circuit(circuit=simple_multi_entangled_evaluator(5), simulator=simulator)
    
