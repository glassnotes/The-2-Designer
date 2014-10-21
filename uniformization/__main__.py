import numpy as np
import sys
from twirl import *
from conjugate import *
import gates

def uniformization(register, circuit, num_qubits):
	# 1) C1/P1 twirl qubit k for all k in {1, ..., n}
	register, circuit = c1p1_twirl_all(register, circuit, num_qubits)

	#print "After step 1"
	#print register 

	# 2) Conjugate the first qubit by a random XOR
	register, circuit = conjugate_one_by_random_xor(register, circuit, num_qubits)

	#print "After step 2"
	#print register 

	# 3) H conjugate the first qubit and C1/P1 twirl the rest
	register = conjugate_qubit(register, gates.H, 0, num_qubits)
	circuit.append(['H'])
	register, circuit = c1p1_twirl_2tok(register, circuit, num_qubits)

	#print "After step 3"
	#print register 

	# 4) Conjugate the first qubit by a random XOR
	register, circuit = conjugate_one_by_random_xor(register, circuit, num_qubits)

	#print "After step 4"
	#print register 

	# 5) H conjugate the first qubit and C1/P1 twirl the rest
	register = conjugate_qubit(register, gates.H, 0, num_qubits)
	circuit.append(['H'])
	register, circuit = c1p1_twirl_2tok(register, circuit, num_qubits)

	#print "After step 5"
	#print register 

	# 6) With probability 1/2, S-conjugate the first qubit
	s_conj = np.random.rand()
	if s_conj <= 0.5:
		register = conjugate_qubit(register, gates.S, 0, num_qubits)
		circuit.append(['S'] + ['I'] * (num_qubits - 1))

	#print "After step 6"
	#print register 

	# 7) Conjugate the first qubit by a random XOR
	register, circuit = conjugate_one_by_random_xor(register, circuit, num_qubits)

	#print "After step 7"
	#print register 

	# 8) C1/P1 twirl the first qubit
	register, exponent = c1p1_twirl(register, 0, num_qubits)
	if exponent == 1:
		circuit.append(['R'] + ['I'] * (num_qubits - 1))
	elif exponent == 2:
		circuit.append(['R2'] + ['I'] * (num_qubits - 1))


	#print "After step 8"
	#print register 
	
	return register, circuit


def print_circuit(circuit, num_qubits):
	"""
		Print a circuit in a pretty way!
	"""
	# Transpose the circuit
	circuit_t = [ [circuit[d][q] for d in range(0, len(circuit))]  for q in range(0,num_qubits)]	
	
	for line in circuit_t:
		print "\t".join(line).expandtabs(4)


def print_circuit(circuit, num_qubits, out_file):
	"""
		Print a circuit in a pretty way!
	"""
	# Transpose the circuit
	circuit_t = [ [circuit[d][q] for d in range(0, len(circuit))]  for q in range(0,num_qubits)]	
	
	for line in circuit_t:
		out_file.write("\t".join(line).expandtabs(4))
		out_file.write('\n')



num_qubits = int(raw_input('Please enter the number of qubits: '))
epsilon = float(raw_input('Please enter a value for epsilon: '))

# Choose a Pauli to work with
pauli_register = choose_random_pauli(num_qubits)

#print "Initial Pauli register is "
#print pauli_register

circuits = []
counts = [] 

for i in range(0, int(1/epsilon)):
	circuit = []
	final, circuit = uniformization(pauli_register, circuit, num_qubits)
	if circuit in circuits:
		counts[circuits.index(circuit)] += 1	
	else:
		circuits.append(circuit)
		counts.append(1)

#for i in range(0, len(circuits)):	
#	print_circuit(circuits[i], num_qubits)
#	print "Count: " + str(counts[i])
#	print

print "Total number of circuits: " + str(len(counts))

circuit_file = open('2qubit_output_noI.txt', 'a')
prob_file = open('2qubit_probabilities_noI.txt', 'a')

for circuit in circuits:
	circuit_file.write(str(circuits.index(circuit)) + ".\n")
	print_circuit(circuit, num_qubits, circuit_file)	
	circuit_file.write('\n')
	
distribution = [i*1.0 / len(counts) for i in counts]

for i in range(0, len(distribution)):
	prob_file.write(str(i) + ', ' + str(distribution[i]) + '\n')

circuit_file.close()
prob_file.close()

