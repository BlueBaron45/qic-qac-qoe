# NOTE: 'backend' is pre-created as a global variable
from numpy.f2py.auxfuncs import throw_error
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.compiler import transpile
import matplotlib.pyplot as plt
from qiskit.visualization import plot_histogram
from qiskit.providers.jobstatus import JobStatus
import time

def generate_default_circuit():
    circuit = QuantumCircuit(2, 2)  # 2 qubits, 2 bits
    circuit.h(0)
    circuit.cx(0, 1)

    circuit.measure([0, 1], [0, 1])
    return circuit

def runCircuit(shots: int = 100, excludeLowProbabilityValues: bool = True, lowProbabilityThreshold: float = 0.05, circuit = generate_default_circuit()):
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



if __name__ == "__main__":
    runCircuit()