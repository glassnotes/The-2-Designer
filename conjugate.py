import numpy as np
from math import sqrt

# Hadamard gate
H = np.array([ [1/sqrt(2), 1/sqrt(2)], [1/sqrt(2), -1/sqrt(2)] ])

# S (phase) gate
S = np.array([ [1, 0], [0, 1j] ])

def conjugate(register, gate, k, num_qubits):
	"""
		Conjugate the kth qubit in the register by the specificied 1-qubit gate 
		Will be used to conjugate a single qubit by H or S, generally.
	"""
	if k == 1: # If we're conjugating the first qubit, need to explicitly initialize the gate
		U = gate 
	else: # Otherwise, it's the identity
		U = np.eye(2);

	for i in range(2, num_qubits + 1): # Expand out the rest
		if i == k: # Apply our specified gate
			U = np.kron(U, gate)
		else: # Identities everywhere else
			U = np.kron(U, np.eye(2))

	return np.dot(np.dot(U, register), (np.asmatrix(U)).getH()) # Return the register conjugated by U
	
	
def conjugate_random_xor(register, num_qubits):
	"""
		Conjugate the first qubit by a random XOR. For each or the qubits from
		k = 2...num_qubits, a CNOT gate targeting qubit 1 is implement with probability 3/4.
	"""
	random_floats = np.random.rand(1, num_qubits - 1)	# Generate num_qubits - 1 random floats
	cnot_choices = [i < 0.75 for i in random_floats] # Should we do the CNOTs?

	U = np.eye(2) # Build the matrix that will hold continuous result
	for i in range(0, num_qubits - 1):
		U = np.kron(U, np.eye(2))

	for i in range(1, len(cnot_choices) + 1):
		if i: # If true, we need to multiply through this CNOT
			next_cnot = generate_cnot(i, 1, num_qubits) # So generate it
			U = np.dot(next_cnot, U) # And multiply U on the left 

	return np.dot(np.dot(U, register), (np.asmatrix(U)).getH()) # Return the register conjugated by CNOTs


def generate_cnot(control, target, num_qubits):
	""" 
		Build the matrix for the CNOT gate between control and target qubit.
	"""
	return np.eye(2)
	

conjugate_random_xor("1", 9)

