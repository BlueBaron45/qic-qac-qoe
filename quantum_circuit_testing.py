"""Utilities for testing and debugging quantum circuits used by the project."""

from qiskit import QuantumCircuit
import matplotlib.pyplot as plt
from qiskit.visualization import plot_histogram
from qiskit.providers.jobstatus import JobStatus
import time


# Default circuit used for testing and debug purposes.
def generate_default_circuit():
    """Return a simple Bell-state circuit to verify entanglement behavior."""
    circuit = QuantumCircuit(2, 2)  # 2 qubits, 2 bits
    circuit.h(0)
    circuit.cx(0, 1)

    circuit.measure([0, 1], [0, 1])
    return circuit


# Test a circuit and later visualize it with a histogram, used for testing purposes.
def test_circuit(simulator, shots: int = 100, exclude_low_probability_values: bool = True,
                low_probability_threshold: float = 0.05, circuit=generate_default_circuit()):
    """Submit a circuit, wait for completion, and print a measurement histogram.

    Args:
        simulator: Qiskit backend that executes the circuit.
        shots: Number of measurement shots.
        exclude_low_probability_values: If True, drop rare counts below threshold.
        low_probability_threshold: Relative fraction of shots considered too small.
        circuit: The quantum circuit to evaluate.
    """
    print(circuit)
    job = simulator.run(circuit, shots=shots)

    while True:
        status = job.status()
        print(f"Job status is {status}")
        match status:
            case JobStatus.DONE:
                break
            case JobStatus.ERROR:
                raise Exception(job.result())
        time.sleep(10)

    counts = job.result().get_counts()

    if exclude_low_probability_values:
        shots_threshold = shots * low_probability_threshold
        counts = {
            bits: cnt
            for bits, cnt in counts.items()
            if cnt > shots_threshold
        }

    print(f"Counts for {shots} shots: {counts}")
    if len(counts) > 0:
        plot_histogram(counts, title=f"Bell State Distribution ({shots} shots)")
        plt.show()
    else:
        print("No results generated with set threshold.")


def entaglement_test(simulator):
    """Run a quick Bell-state demonstration and print the measurement distribution."""
    qc = QuantumCircuit(2, 2)

    qc.h(0)
    qc.cx(0, 1)
    qc.measure([0, 1], [0, 1])

    job = simulator.run(qc, shots=1000)
    result = job.result()
    counts = result.get_counts()

    print("Measurement outcomes:", counts)