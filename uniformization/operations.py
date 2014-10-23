import qecc as q 
import numpy as np

# Defining Cliffords R = SH and R^2
R = q.Clifford(['Z'], ['Y'])
R2 = q.Clifford(['Y'], ['X'])


def c1_p1_twirl(pauli, q):
    """
        C1/P1 twirl qubit q of the Pauli
    """
    # Choose a random integer between 0 and 2 
    exponent = np.random.random_integers(0, 2)
    if exponent == 1:
        return R.on(pauli, q), exponent
    elif exponent == 2:
        return R2.on(pauli, q), exponent
    else:
        return pauli, exponent
    

def conjugate_by_random_xor(pauli, ctrl, targ, p):
    """
        Conjugate the target qubit by a CNOT with probability p.
    """
    do_xor = np.random.rand(1, 1) # Generate a single random float
    
    if do_xor[0] <= p:
        xor = q.cnot(pauli.nq, ctrl, targ)
        return xor.conjugate_pauli(pauli), True
    else:
        return pauli, False
    

def print_circuit(circuit, num_qubits):
    """
        Print a circuit in a pretty way!
    """
    # Transpose the circuit
    circuit_t = [ [circuit[d][q] for d in range(0, len(circuit))]  for q in range(0,num_qubits)]

    for line in circuit_t:
        print "\t".join(line).expandtabs(4)

