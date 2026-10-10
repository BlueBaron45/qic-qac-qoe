from qqq_backend import qqq_functions
from quantum_circuit_testing import test_circuit

#toto nejde do qollab
from qiskit_aer import AerSimulator

from terminal_interface.terminal_main import game_run

#main method
if __name__ == "__main__":
    simulator = AerSimulator()
    game_run(simulator)
    #test_circuit(circuit = qqq_grid.set_up_rng_circuit(7), simulator = simulator)
