import quaec as q 
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
        big_r = (eye_q(q - 1) & R & eye_q())
        return big_r.conjugate_pauli(pauli)  
    elif exponent == 2:
        big_r2 = (eye_q(q - 1) & R2 & eye_q())
        return big_r2.conjugate_pauli(pauli)
    else:
        return pauli 
    

def conjugate_by_random_xor(pauli, ctrl, targ, p):
    """
        Conjugate the target qubit by a CNOT with probability p.
    """
    do_xor = np.random.rand(1, 1) # Generate a single random float
    
    if do_xor[0] <= p:
        xor = q.cnot(pauli.nq, ctrl, targ)
        return xor.conjugate_pauli(pauli) 
    else:
        return pauli
    


def uniformization(pauli):
    """
        Apply one round of the uniformization procedure from the 
        Dankert/Emerson/Cleve/Livine paper.
    """
    # 1) C1/P1 twirl all qubits

    # 2) Conjugate the first qubit by a random XOR
    for i in range(1, pauli.np):
        pauli = conjuagte_by_random_xor(pauli, i, 0, 0.75)

    # 3) H-conjugate the first qubit, C1/P1 twirl the rest

    # 4) Conjugate the first qubit by a random XOR
    for i in range(1, pauli.np):
        pauli = conjuagte_by_random_xor(pauli, i, 0, 0.75)

    # 5) H-conjugate the first qubit, C1/P1 twirl the rest

    # 6) With probability 1/2, S-conjugate the first qubit
    

    # 7) Conjugate the first qubit by a random XOR
    for i in range(1, pauli.np):
        pauli = conjuagte_by_random_xor(pauli, i, 0, 0.75)
    
    # 8) C1/P1 twirl the first qubit





