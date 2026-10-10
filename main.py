# NOTE: 'backend' is pre-created as a global variable

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.compiler import transpile
import matplotlib.pyplot as plt
from qiskit.visualization import plot_histogram

# Create a basic Bell State
circuit = QuantumCircuit(2, 2)  # 2 qubits, 2 bits
circuit.h(0)
circuit.cx(0, 1)

# Measure qubits 0 and 1 into bits 0 and 1 respectively
circuit.measure([0, 1], [0, 1])
# NOTE: circuit.measure_all() or circuit.measure_active() would do the same here

# Display circuit, same as print(circuit.draw(output="text"))
print(circuit)



from qiskit.providers.jobstatus import JobStatus
import time


def main(shots: int = 100, excludeLowProbabilityValues: bool = True, lowProbabilityThreshold: float = 0.05):
    # Submit the job for execution
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
    main()