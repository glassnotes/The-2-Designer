import numpy as np
from conjugate import *
from bsr import *
import gates

def choose_random_pauli(num_qubits):
	"""
		Twirl the register with a random Pauli.
		As per Dankert et. al, this simply sends some
		density matrix p to a linear combination of
 		P_a p P_a where the P_a are Pauli matrices
	
		As a first implementation, simply choose a random Pauli.
	"""
	# Choose a Pauli between 2 and 4^num_qubits (don't choose the identity) 
	pauli_int = np.random.random_integers(1, 4**num_qubits - 1)
	bsr = bin(pauli_int) # Get binary symplectic rep
	bsr = bsr[2:]

	if len(bsr) < 2*num_qubits:
		string_pad = "0" * (2*num_qubits - len(bsr))
		bsr = string_pad + bsr

	pauli_binary = [bsr[i:i+2] for i in range(0, len(bsr), 2)]

	pauli_gates = [bsr_to_gate(x) for x in pauli_binary]
	
	pauli = pauli_gates[0]
	for next_pauli in pauli_gates[1:]:
		pauli = np.kron(pauli, next_pauli)
	
	return pauli 


def pauli_twirl_all(register, num_qubits):
	"""
		Twirl the register into a linear combination of Pauli channels.
	"""
	# Normalized linear combination of all the Pauli matrices for now
	weights = np.random.rand(1, 4**num_qubits)
	norm = np.linalg.norm(weights)
	weights = weights[0] / norm

	mapped_register = np.zeros((2**num_qubits, 2**num_qubits)) # Running matrix sum

	for i in range(0, 4**num_qubits - 1):
		bsr = bin(i)[2:] # Get binary symplectic rep

		if len(bsr) < 2*num_qubits:
			string_pad = "0" * (2*num_qubits - len(bsr))
			bsr = string_pad + bsr

		pauli_binary = [bsr[i:i+2] for i in range(0, len(bsr), 2)]

		pauli_gates = [bsr_to_gate(x) for x in pauli_binary]
	
		pauli = pauli_gates[0]
		for next_pauli in pauli_gates[1:]: # Build Pauli matrix
			pauli = np.kron(pauli, next_pauli)

		mapped_register = mapped_register +  weights[i] * conjugate_register(register, pauli)
	
	return mapped_register
		

def c1p1_twirl(register, k, num_qubits):
	"""
		Perform a C1/P1 twirl of qubit k
	"""
	# Randomly choose an integer in {0, 1, 2}
	exponent = np.random.random_integers(0, 2)

	# Conjugate the qubit 
	if exponent == 1:
		return conjugate_qubit(register, gates.R, k, num_qubits), exponent
	elif exponent == 2:
		return conjugate_qubit(register, np.dot(gates.R, gates.R), k, num_qubits), exponent
	else:
		return register, exponent


def c1p1_twirl_all(register, circuit, num_qubits):
	"""
		Perform a C1/P1 twirl on all the qubits
	"""
	exponents = []
	next_circuit_line = []
	for i in range(0, num_qubits):
		register, exponent = c1p1_twirl(register, i, num_qubits)
		exponents.append(exponent)
	for e in exponents:
		if e == 0:
			next_circuit_line.append('I')
		elif e == 1:
			next_circuit_line.append('R')
		else:
			next_circuit_line.append('R2') 
	circuit.append(next_circuit_line)
	return register, circuit


def c1p1_twirl_2tok(register, circuit, num_qubits):
	"""
		Perform a C1/P1 twirl on all the qubits except the first one
	"""
	exponents = []

	assert len(circuit[-1]) == 1 # Make sure we have filled in the circuit value for the first qubit

	for i in range(1, num_qubits):
		register, exponent = c1p1_twirl(register, i, num_qubits)
		exponents.append(exponent)
	for e in exponents:
		if e == 0:
			circuit[-1].append('I') # Append to the last line of the circuit
		elif e == 1:
			circuit[-1].append('R')
		else:
			circuit[-1].append('R2') 
	return register, circuit

