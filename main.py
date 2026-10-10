import qiskit
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
import matplotlib.pyplot as plt
from qiskit.visualization import plot_histogram
from qiskit.providers.jobstatus import JobStatus
import time
import numpy as np
from numpy import pi

#default circuit used for testing and debug purpouses
def generate_default_circuit():
    circuit = QuantumCircuit(2, 2)  # 2 qubits, 2 bits
    circuit.h(0)
    circuit.cx(0, 1)

    circuit.measure([0, 1], [0, 1])
    return circuit

#test a circuit and later visualize it with a histogram, used for testing purpouses
def test_circuit(shots: int = 100, exclude_low_probability_values: bool = True, low_probability_threshold: float = 0.05, circuit = generate_default_circuit()):
    # Submit the job for execution
    print(circuit)
    simulator = AerSimulator()
    job = simulator.run(circuit, shots=shots)

    # Poll for status till the job is done
    while True:
        status = job.status()
        print(f"Job status is {status}")
        match status:
            case JobStatus.DONE:
                break
            case JobStatus.ERROR:
                raise Exception(job.result())
        time.sleep(10)

    # Get measurement counts
    counts = job.result().get_counts()

    if exclude_low_probability_values:
        shots_threshold = shots * low_probability_threshold
        counts = {
            bits: cnt
            for bits, cnt in counts.items()
            if cnt > shots_threshold
        }

    print(f"Counts for {shots} shots: {counts}")
    # Display the result distribution
    plot_histogram(counts, title=f"Bell State Distribution ({shots} shots)")
    plt.show()

#simple evaluator, checks a single spot with equall chances for either one
def simple_evaulator() -> qiskit.QuantumCircuit:
    circuit = QuantumCircuit(1, 1)
    circuit.h(0)
    circuit.measure(0, 0)
    return circuit

#simple evaluator that can take the wanted probability of 0 as input
#value has to be between 0 and 1
#some values are not recommended to use here, such as: 0, 1, 0.5 (for this one just use simple_evaluator function)
def simple_paramitrized_evaluator(chance_for_0: float = 0.5) -> qiskit.QuantumCircuit:
    if not (0 <= chance_for_0 <= 1):
        raise ValueError("x must be between 0 and 1 for valid quantum probabilities.")
    theta = 2 * np.arccos(np.sqrt(chance_for_0))
    circuit = QuantumCircuit(1, 1)
    circuit.ry(theta, 0)
    circuit.measure(0, 0)
    return circuit


# simulates a simple ttt game without any player input
def simple_ttt_game():
    evaluator = simple_paramitrized_evaluator(chance_for_0 = 0.5)
    simulator = AerSimulator()
    result = simulator.run(evaluator, shots=9).result()
    # Get measurement counts
    counts = result.get_counts()

    # Convert counts into an array of individual results
    results = []
    for bit, count in counts.items():
        results.extend([int(bit)] * count)

    print(f"Game result: {results}")

#main method
if __name__ == "__main__":
    #test_circuit()
    #test_circuit(circuit = simple_evaulator())
    #simple_ttt_game()
    test_circuit(circuit = simple_paramitrized_evaluator(0.9))