import numpy as np
import gates

def bsr_to_pauli(x):
    """
        Convert a bsr string into a Pauli. 
    """
    if x == "00":
        return "I"
    elif x == "01":
        return "X"
    elif x == "10":
        return "Z"
    else:
        return "Y"


def pauli_to_gate(x):
    """
        Take a Pauli character and return the corresponding gate.
    """
    if x == "I":
        return np.eye(2)
    elif x == "X":
        return gates.X
    elif x == "Z":
        return gates.Z
    else:
        return gates.Y
    

def bsr_to_gate(x):
    """
        Take a bsr string and return the corresponding gate.
    """
    if x == "00":
        return np.eye(2) 
    elif x == "01":
        return gates.X 
    elif x == "10":
        return gates.Z
    else:
        return gates.Y
    

