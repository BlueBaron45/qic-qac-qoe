from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
import matplotlib.pyplot as plt
from qiskit.visualization import plot_histogram
from qiskit.providers.jobstatus import JobStatus
import time

#default circuit used for testing and debug purpouses
def generate_default_circuit():
    circuit = QuantumCircuit(2, 2)  # 2 qubits, 2 bits
    circuit.h(0)
    circuit.cx(0, 1)

    circuit.measure([0, 1], [0, 1])
    return circuit

#test a circuit and later visualize it with a histogram, used for testing purpouses
def test_circuit(shots: int = 100, excludeLowProbabilityValues: bool = True, lowProbabilityThreshold: float = 0.05, circuit = generate_default_circuit()):
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

    if excludeLowProbabilityValues:
        shotsThreshold = shots * lowProbabilityThreshold
        counts = {
            bits: cnt
            for bits, cnt in counts.items()
            if cnt > shotsThreshold
        }

    print(f"Counts for {shots} shots: {counts}")
    # Display the result distribution
    plot_histogram(counts, title=f"Bell State Distribution ({shots} shots)")
    plt.show()

#simple evaluator, checks a single spot with equall chances for either one
def simple_evaulator():
    circuit = QuantumCircuit(1, 1)
    circuit.h(0)
    circuit.measure(0, 0)
    return circuit

# simulates a simple ttt game without any player input
def simple_ttt_game():
    evaluator = simple_evaulator()
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
    #testCircuit()
    #testCircuit(circuit = simple_evaulator())
    simple_ttt_game()