import qecc as q 
import numpy as np
from operations import *
from uniformization import *
from math import log
from scipy.stats import entropy
import time

def one_shot():
    """
        For the initial part of the in-class demo. Takes a single Pauli and computes
        one random circuit from the eps-approximate 2-design and applies it to the Pauli.
    """

    print "\n====================================================================="
    print "Choosing a single random circuit from an epsilon-approximate 2-design"
    print "=====================================================================\n"

    pauli_string = raw_input("Please enter an initial Pauli (e.g. XXYZ): ")
    epsilon = float(raw_input("Enter a value for epsilon: "))

    pauli = q.Pauli(pauli_string)
    new_pauli = pauli
    new_circuit = []
    
    for i in range(0, int(log(1/epsilon)) + 1): 
        new_pauli, circuit = uniformization(new_pauli)
        new_circuit.extend(circuit)

    print "\nResultant pauli is " 
    print new_pauli
    print "\nApplied circuit was "
    print_circuit(new_circuit, pauli.nq)

    print "\n\n\n"


def distribution():
    print "\n====================================================================="
    print "Generate statistics for the distribution of Paulis after successive "
    print "application of circuits chosen randomly from the 2-design"
    print "=====================================================================\n"

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

        for j in range(0, int(log(1/epsilon)) + 1):
            new_pauli, circuit = uniformization(new_pauli)
            next_circuit.extend(circuit)

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

    pauli_probs = [pauli_counts[i]*1.0 / sum(pauli_counts) for i in range(0, len(paulis))]

    for i in range(0, len(paulis)):
        pauli_file.write(paulis[i] + "\t" + str(pauli_probs[i]))
        pauli_file.write('\n')

    pauli_file.write('\n'+"KL divergence is " + str( entropy(pauli_probs, [1.0/len(paulis)]*len(paulis)) ) )


def main():
    demo_type = raw_input("Select demo type:\n0. Full demo\n1. One-shot\n2. Distribution\n")

    np.random.seed(int(time.mktime(time.gmtime())))

    if demo_type == '0':
        one_shot()
        distribution()
    elif demo_type == '1':
        one_shot()
    elif demo_type == '2':
        distribution()
    else:
        print "Error, invalid input."        


if __name__ == '__main__':
    main()
