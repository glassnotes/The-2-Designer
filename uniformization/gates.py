import numpy as np
from math import sqrt

# Hadamard gate
H = np.array([ [1/sqrt(2), 1/sqrt(2)], 
			   [1/sqrt(2), -1/sqrt(2)] ])

# S (phase) gate
S = np.array([ [1, 0], 
			   [0, 1j] ])

# R gate, used in C1/P1 twirling
R = np.dot(S, H)

# One qubit Paulis
X = np.array([ [0, 1],
			   [1, 0] ])

Y = np.array([ [0, -1j],
			   [1j, 0] ])

Z = np.array([ [1, 0],
			   [0, -1] ])

# 2 qubit gates
SWAP = np.array([ [1, 0, 0, 0],
				  [0, 0, 1, 0],
				  [0, 1, 0, 0],
				  [0, 0, 0, 1] ])

CNOT = np.array([ [1, 0, 0, 0],
				  [0, 1, 0, 0],
				  [0, 0, 0, 1],
				  [0, 0, 1, 0] ])

CNOT_REV = np.array([ [1, 0, 0, 0],
				  	  [0, 0, 0, 1],
				  	  [0, 0, 1, 0],
				  	  [0, 1, 0, 0] ])
