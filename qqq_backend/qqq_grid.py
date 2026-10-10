# simulates a simple ttt game without any player input

from quantum_evaluators import *

def simple_ttt_game(simulator, grid_size:int):
    evaluator = simple_evaulator()
    result = simulator.run(evaluator, shots=grid_size * grid_size, memory=True).result()
    # Get measurement counts
    counts = result.get_memory()

    # Get individual measurement results
    results = result.get_memory()

    return [int(bit) for bit in results]