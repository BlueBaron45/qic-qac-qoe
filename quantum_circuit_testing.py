from qiskit import QuantumCircuit
import matplotlib.pyplot as plt
from qiskit.visualization import plot_histogramё
from qiskit.providers.jobstatus import JobStatus
import time

#default circuit used for testing and debug purposes
def generate_default_circuit():
    circuit = QuantumCircuit(2, 2)  # 2 qubits, 2 bits
    circuit.h(0)
    circuit.cx(0, 1)

    circuit.measure([0, 1], [0, 1])
    return circuit


#test a circuit and later visualize it with a histogram, used for testing purposes
def test_circuit(simulator, shots: int = 100, exclude_low_probability_values: bool = True, low_probability_threshold: float = 0.05, circuit = generate_default_circuit()):
    # Submit the job for execution
    print(circuit)
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