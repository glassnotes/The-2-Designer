import qecc as q 
import numpy as np
from operations import *

def uniformization(pauli):
    """
        Apply one round of the uniformization procedure from the 
        Dankert/Emerson/Cleve/Livine paper to a Pauli.
        Return the transformed Pauli and the corresponding circuit we applied.
    """

    circuit = []

    ################################################
    # 1) C1/P1 twirl all qubits
    next_circuit_line = []
    for idx_qubit in range(0, pauli.nq):
        pauli, exponent = c1_p1_twirl(pauli, idx_qubit)
        if exponent == 0:
            next_circuit_line.append('I')
        elif exponent == 1:
            next_circuit_line.append('R')
        else:
            next_circuit_line.append('R2')

    if len(next_circuit_line) != 0 and next_circuit_line != ['I'] * (pauli.nq):
        circuit.append(next_circuit_line)
    next_circuit_line = []

    #print "Step 1: " , pauli
    ################################################


    ################################################
    # 2) Conjugate the first qubit by a random XOR
    for idx_qubit in range(1, pauli.nq):
        pauli, xor_applied = conjugate_by_random_xor(pauli, idx_qubit, 0, 0.75)
        if xor_applied:
            circuit.append(['X'] + ['I'] * (idx_qubit - 1) + ['C'] + ['I'] * (pauli.nq - idx_qubit - 1))

    # Check if output was good
    #if pauli.op[0] == 'I' or pauli.op[0] == 'Z':
    #    return None, None

    #print "Step 2: " , pauli

    next_circuit_line = []
    ################################################


    ################################################
    # 3) H-conjugate the first qubit, C1/P1 twirl the rest
    H = q.hadamard(pauli.nq, 0)
    next_circuit_line.append('H')

    pauli = H.conjugate_pauli(pauli)
    for idx_qubit in range(1, pauli.nq):
        pauli, exponent = c1_p1_twirl(pauli, idx_qubit)
        if exponent == 0:
            next_circuit_line.append('I')
        elif exponent == 1:
            next_circuit_line.append('R')
        else:
            next_circuit_line.append('R2')

    circuit.append(next_circuit_line)
    next_circuit_line = []

    #print "Step 3: " , pauli
    ################################################


    ################################################
    # 4) Conjugate the first qubit by a random XOR
    for idx_qubit in range(1, pauli.nq):
        pauli, xor_applied = conjugate_by_random_xor(pauli, idx_qubit, 0, 0.75)
        if xor_applied:
            circuit.append(['X'] + ['I'] * (idx_qubit - 1) + ['C'] + ['I'] * (pauli.nq - idx_qubit - 1))

    #print "Step 4: " , pauli
    ################################################


    ################################################
    # 5) H-conjugate the first qubit, C1/P1 twirl the rest
    H = q.hadamard(pauli.nq, 0)
    next_circuit_line.append('H')

    pauli = H.conjugate_pauli(pauli)
    for idx_qubit in range(1, pauli.nq):
        pauli, exponent = c1_p1_twirl(pauli, idx_qubit)
        if exponent == 0:
            next_circuit_line.append('I')
        elif exponent == 1:
            next_circuit_line.append('R')
        else:
            next_circuit_line.append('R2')

    circuit.append(next_circuit_line)
    next_circuit_line = []

    #print "Step 5: " , pauli
    ################################################


    ################################################
    # 6) With probability 1/2, S-conjugate the first qubit
    S = q.phase(pauli.nq, 0)
    do_s = np.random.rand(1, 1) # Generate a single random float
    if do_s[0] <= 0.5:
        pauli = S.conjugate_pauli(pauli)
        circuit.append(['S'] + ['I'] * (pauli.nq - 1))

    #print "Step 6: " , pauli
    ################################################
    ################################################


    ################################################
    # 7) Conjugate the first qubit by a random XOR
    for idx_qubit in range(1, pauli.nq):
        pauli, xor_applied = conjugate_by_random_xor(pauli, idx_qubit, 0, 0.75)
        if xor_applied:
            circuit.append(['X'] + ['I'] * (idx_qubit - 1) + ['C'] + ['I'] * (pauli.nq - idx_qubit - 1))

    #print "Step 7: " , pauli
    ################################################
    

    ################################################
    # 8) C1/P1 twirl the first qubit
    pauli, exponent = c1_p1_twirl(pauli, 0)
    if exponent == 0:
        next_circuit_line.append('I')
    elif exponent == 1:
        next_circuit_line.append('R')
    else:
        next_circuit_line.append('R2')

    if next_circuit_line != ['I']:
        circuit.append(next_circuit_line + ['I'] * (pauli.nq - 1))
    
    #print "Step 8: " , pauli
    ################################################

    return pauli, circuit
