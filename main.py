import qiskit_aer

from graphic_interface import grid
import pyglet

from qqq_game_backend import simple_ttt_game
from quantum_circuit_testing import test_circuit
from quantum_evaluators import simple_pair_entangled_evaluator
from terminal_interface.terminal_main import game_run

#toto nejde do qollab
from qiskit_aer import AerSimulator

#main method
if __name__ == "__main__":
    simulator = AerSimulator()
    game_run(simulator)
    test_circuit(simulator=simulator, circuit=simple_pair_entangled_evaluator(False))
    
