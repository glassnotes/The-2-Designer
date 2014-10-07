import numpy as np
import sys
from math import sqrt
import gates

np.set_printoptions(threshold=np.nan)


def conjugate_qubit(register, gate, k, num_qubits):
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
	
	
def conjugate_register(register, gate):
	""" 
		Conjugate an entire register by the provided gate.
		This is really just here to save typing the long run.
	"""
	return np.dot( np.dot(gate, register), np.asmatrix(gate).getH() )


def conjugate_one_by_random_xor(register, num_qubits):
	"""
		Conjugate the first qubit by a random XOR. For each or the qubits from
		k = 2...num_qubits, a CNOT gate targeting qubit 1 is implement with probability 3/4.
	"""
	random_floats = np.random.rand(1, num_qubits - 1)	# Generate num_qubits - 1 random floats
	#print random_floats
	cnot_choices = [i < 0.75 for i in random_floats[0]] # Should we do the CNOTs?
	#print cnot_choices
	U = np.eye(2**num_qubits)

	for qubit in range(2, num_qubits + 1):
		if cnot_choices[qubit - 2]: # If true, we need to multiply through this CNOT (note indexing)
			#print "Applying cnot from qubit " + str(qubit) + " to qubit 1" 
			register = apply_cnot(qubit, register, num_qubits) # So generate it

	return register # Return the register conjugated by CNOTs


def apply_cnot(control, register, num_qubits):
	""" 
		Apply a CNOT between the control qubit and qubit 1.
	"""
	# Swap the qubits until we get the control qubit in position 2
	if num_qubits > 2:
		for i in range(control, 2, -1):
			#print "Swapping qubits " + str(i) + " and " + str(i - 1)
			register = swap(register, i, i - 1, num_qubits)

	# Build and apply the CNOT
	cnot = gates.CNOT_REV # CNOT from control qubit 2 to target qubit 1
	if num_qubits > 2: # We'll need to pad some identities
		for i in range(3, num_qubits + 1):
			cnot = np.kron(cnot, np.eye(2))
	register = conjugate_register(register, cnot)	

	# Swap the qubit back to it's original position
	if num_qubits > 2:
		for i in range(2, control):
			#print "Swapping qubits " + str(i) + " and " + str(i + 1)
			register = swap(register, i, i + 1, num_qubits)

	return register
	

def swap(register, q1, q2, num_qubits):
	"""
		Build a swap gate between qubits indexed by qubits q1 and q2 which are adjacent.
	"""
	if np.absolute(q2 - q1) != 1:
		print "Cannot swap two qubits which are not adjacent!" 
		sys.exit()

	if num_qubits == 2:
		return gates.SWAP
	
	if q1 == 1 or q2 == 1: # Swapping between 1 and 2	
		swap_gate = gates.SWAP # Make the swap gate
		for i in range(3, num_qubits + 1): # Identities in the rest of the places
			swap_gate = np.kron(swap_gate, np.eye(2))
		return conjugate_register(register, swap_gate)
	else:
		swap_gate = np.eye(2)
		i = 2
		while (i <= num_qubits):
			if i == q1 or i == q2: # Get to the qubits we have to swap
				swap_gate = np.kron(swap_gate, gates.SWAP)
				i = max(q1, q2) + 1 # Increment i again so we don't add in any extra identities
			else: # Add identities everywhere else
				swap_gate = np.kron(swap_gate, np.eye(2))
				i += 1
		return conjugate_register(register, swap_gate)

