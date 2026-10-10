# simulates a simple ttt game without any player input

from quantum_evaluators import *

def simple_ttt_game(simulator):
    evaluator = simple_evaulator()
    result = simulator.run(evaluator, shots=9).result()
    # Get measurement counts
    counts = result.get_counts()

    # Convert counts into an array of individual results
    results = []
    for bit, count in counts.items():
        results.extend([int(bit)] * count)
    return results