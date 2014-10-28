import qecc as q 
import numpy as np
from operations import *
from uniformization import *
from math import log

def one_shot():
    pauli_string = raw_input("Please enter an initial Pauli (e.g. XXYZ): ")
    pauli = q.Pauli(pauli_string)
    new_pauli, circuit = uniformization(pauli)
    while new_pauli == None:
        print "Execution was bad, trying again."
        new_pauli, circuit = uniformization(pauli)
    print "\nResultant pauli is " 
    print new_pauli
    print "\n Applied circuit was "
    print_circuit(circuit, pauli.nq)

def distribution():
    pauli_string = raw_input("Please enter an initial Pauli (e.g. XXYZ): ")
    trials = raw_input("Please enter the number of circuits to generate: ")
    epsilon = float(raw_input("Enter a value for epsilon: "))
    pauli = q.Pauli(pauli_string)
    
    circuit_file = open("circuit_file" + "_" + pauli.op + "_" + trials + "_" + str(epsilon) + ".out", 'w')
    pauli_file = open("pauli_file" + "_" + pauli.op + "_" + trials + "_" + str(epsilon) + ".out", 'w')
     
    paulis = []
    pauli_counts = []
    circuits = []
    circuit_counts = []

    for i in range(0, int(trials)):
	next_circuit = []
	new_pauli = pauli
	for j in range(0, int(log(1/epsilon))):
	    new_pauli, circuit = uniformization(new_pauli)
	    next_circuit.extend(circuit)

        if circuit == None:
            continue

        if next_circuit not in circuits:
            circuits.append(next_circuit)
            circuit_counts.append(1)
        else:
            circuit_counts[circuits.index(next_circuit)] += 1

        if new_pauli.op not in paulis:
            paulis.append(new_pauli.op)
            pauli_counts.append(1)
        else:
            pauli_counts[paulis.index(new_pauli.op)] += 1

    for i in range(0, len(circuits)):
        print_circuit_to_file(circuits[i], pauli.nq, circuit_file)
        circuit_file.write('Count: ' + str(circuit_counts[i]) + '\n\n')
                                 
    circuit_file.write("Total number of different circuits: " + str(len(circuits)) + '\n')

    for i in range(0, len(paulis)):
        pauli_file.write(paulis[i] + "\t" + str(pauli_counts[i] * 1.0 / sum(pauli_counts)))
        if paulis[i][1:] == 'I' * (pauli.nq - 1):
            pauli_file.write('  **')
        pauli_file.write('\n')

distribution()
#one_shot()
