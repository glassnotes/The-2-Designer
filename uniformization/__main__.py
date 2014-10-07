import numpy as np
import sys
from twirl import *
from conjugate import *
import gates

def uniformization(register, num_qubits):
	# 1) C1/P1 twirl qubit k for all k in {1, ..., n}
	register = c1p1_twirl_all(register, num_qubits)

	#print "After step 1"
	#print register 

	# 2) Conjugate the first qubit by a random XOR
	register = conjugate_one_by_random_xor(register, num_qubits)

	#print "After step 2"
	#print register 

	# 3) H conjugate the first qubit and C1/P1 twirl the rest
	register = conjugate_qubit(register, gates.H, 1, num_qubits)
	register = c1p1_twirl_2tok(register, num_qubits)

	#print "After step 3"
	#print register 

	# 4) Conjugate the first qubit by a random XOR
	register = conjugate_one_by_random_xor(register, num_qubits)

	#print "After step 4"
	#print register 

	# 5) H conjugate the first qubit and C1/P1 twirl the rest
	register = conjugate_qubit(register, gates.H, 1, num_qubits)
	register = c1p1_twirl_2tok(register, num_qubits)

	#print "After step 5"
	#print register 

	# 6) With probability 1/2, S-conjugate the first qubit
	s_conj = np.random.rand()
	if s_conj <= 0.5:
		register = conjugate_qubit(register, gates.S, 1, num_qubits)

	#print "After step 6"
	#print register 

	# 7) Conjugate the first qubit by a random XOR
	register = conjugate_one_by_random_xor(register, num_qubits)

	#print "After step 7"
	#print register 

	# 8) C1/P1 twirl the first qubit
	register = c1p1_twirl(register, 1, num_qubits)
	#print "After step 8"
	#print register 

	return register


# Start everything in state 0
num_qubits = int(raw_input('Please enter the number of qubits: '))

print "Select one of the following options: "
print "0 - start all qubits in state 0"
print "1 - start all qubits in state 1"

state_selection = int(raw_input('Your choice: '))

# ket0 = np.array([[1], [0]])
# ket1 = np.array([[0], [1]])
kets = np.eye(2)[:, np.newaxis, :]

if state_selection in xrange(2):
	initial_state = reduce(np.kron, [kets[state_selection]] * num_qubits)
else:
	raise ValueError("Given state of {}, expected 0 or 1.".format(state_selection))

# if state_selection == 0:
# 	initial_state = ket0
# 	for i in range(1, num_qubits):
# 		initial_state = np.kron(initial_state, ket0)
# elif state_selection == 1:
# 	initial_state = ket1
# 	for i in range(1, num_qubits):
# 		initial_state = np.kron(initial_state, ket1)
# else:
# 	print "Fail"
# 	sys.exit()


# Run the uniformization procedure.
initial_register = np.dot(initial_state.T, initial_state)


print "Your initial register is"
print initial_register

pauli_register = pauli_twirl_all(initial_register, num_qubits)

# Repeatedly iterate this procedure.
for i in range(0, 10):
	pauli_register = uniformization(pauli_register, num_qubits)

print 

final_register = pauli_register

print "Your final register is" 
print final_register
print
print "Checking that the matrix is unitary: "
print np.dot( final_register, np.asmatrix(final_register).getH() )


