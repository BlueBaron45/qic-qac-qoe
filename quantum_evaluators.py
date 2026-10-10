#simple evaluator, checks a single spot with equall chances for either one
import numpy as np
import qiskit
from qiskit import QuantumCircuit

#simple evaluator that can take the wanted probability of 0 as input
def simple_evaulator() -> qiskit.QuantumCircuit:
    circuit = QuantumCircuit(1, 1)
    circuit.h(0)
    circuit.measure(0, 0)
    return circuit


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

#simple evaluator for 2 entangled qubits, the parameter changes if the output qubits are same or not
#for both cases the distribution is same (50/50)
def simple_pair_entangled_evaluator(are_same: bool = True) -> qiskit.QuantumCircuit:
    circuit = QuantumCircuit(2,2)
    circuit.h(0)
    if are_same:
        circuit.x(1)
    circuit.cx(0, 1)
    circuit.measure(0, 0)
    circuit.measure(1, 1)
    return circuit

#for all be same, count has to be more than 2
#there seems to be problems with values higher then 4
def simple_multi_entangled_evaluator(input_qubit:int):
    if input_qubit < 2:
        raise ValueError("input_qubit must be greater than 2")
    circuit = QuantumCircuit(input_qubit + 1,input_qubit + 1)
    for i in range(input_qubit):
        circuit.h(i)
    circuit.mcx(list(range(input_qubit)), input_qubit)
    circuit.measure(list(range(input_qubit + 1)), list(range(input_qubit + 1)))
    return circuit