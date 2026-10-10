# simulates a simple ttt game without any player input
import numpy

from quantum_evaluators import *

def simple_ttt_game(simulator, grid_size:int):
    evaluator = simple_evaulator()
    result = simulator.run(evaluator, shots=grid_size * grid_size, memory=True).result()
    # Get measurement counts
    counts = result.get_memory()

    # Get individual measurement results
    results = result.get_memory()

    return [int(bit) for bit in results]


def set_up_rng_circuit(max_value: int) -> QuantumCircuit:
    circuit = QuantumCircuit(2)
    if max_value < 1:
        raise ValueError("max_value must be at least 1")
    count = max(1, (max_value - 1).bit_length())
    # Number of basis states available with count qubits
    state_count = 1 << count
    # Uniform amplitudes for values 0 through max_value - 1
    state = ([1 / numpy.sqrt(max_value)] * max_value + [0] * (state_count - max_value))
    qc = QuantumCircuit(count, count)
    qubit_list = list(range(count))
    qc.initialize(state, qubit_list)
    qc.measure(qubit_list, qubit_list)
    return qc

def generate_values_from_rng_circuit(number_of_values, max_value, simulator):
    result = simulator.run(set_up_rng_circuit(max_value), shots=number_of_values, memory=True).result()
    counts = result.get_memory()

    # Get individual measurement results
    results = result.get_memory()

    return [int(bit) for bit in results]