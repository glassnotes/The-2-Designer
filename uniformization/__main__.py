import qecc as q 
import numpy as np
from operations import *
from uniformization import *

pauli_string = raw_input("Please enter an initial Pauli (e.g. XXYZ): ")

pauli = q.Pauli(pauli_string)

pauli, circuit = uniformization(pauli)

print_circuit(circuit, pauli.nq)

