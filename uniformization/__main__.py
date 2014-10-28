import qecc as q 
import numpy as np
from operations import *
from uniformization import *

def one_shot():
    pauli_string = raw_input("Please enter an initial Pauli (e.g. XXYZ): ")
    pauli = q.Pauli(pauli_string)
    pauli, circuit = uniformization(pauli)
    print "\nResultant pauli is " 
    print pauli
    print "\n Applied circuit was "
    print_circuit(circuit, pauli.nq)

def distribution():
    pauli_string = raw_input("Please enter an initial Pauli (e.g. XXYZ): ")
    trials = raw_input("Please enter the number of circuits to generate: ")
    pauli = q.Pauli(pauli_string)
    
    circuit_file = open("circuit_file.txt", 'w')
    pauli_file = open("pauli_file.txt", 'w')
     

    paulis = []
    pauli_counts = []
    circuits = []
    circuit_counts = []

    for i in range(0, int(trials)):
        pauli, circuit = uniformization(pauli)

        if circuit not in circuits:
            circuits.append(circuit)
            circuit_counts.append(1)
        else:
            circuit_counts[circuits.index(circuit)] += 1

        if pauli.op not in paulis:
            paulis.append(pauli.op)
            pauli_counts.append(1)
        else:
            pauli_counts[paulis.index(pauli.op)] += 1

    for i in range(0, len(circuits)):
        print_circuit_to_file(circuits[i], pauli.nq, circuit_file)
        circuit_file.write('Count: ' + str(circuit_counts[i]) + '\n\n')
                                 
    circuit_file.write("Total number of different circuits: " + str(len(circuits)) + '\n')

    for i in range(0, len(paulis)):
        pauli_file.write(paulis[i] + "\t" + str(pauli_counts[i] * 1.0 / sum(pauli_counts)))
        pauli_file.write('\n')

distribution()
