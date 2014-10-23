import qecc as q

import numpy as np

def test_on():
    small = q.Pauli('XZ')
    medium = q.Pauli('XYZY')
    large = q.Pauli('XZZZYXY')

    R = q.Clifford(['Z'], ['Y'])
    SWAP = q.Clifford(['IX', 'XI'], ['IZ', 'ZI'])

    assert R.on(small, 0) == q.Pauli('ZZ')
    assert R.on(small, 1) == q.Pauli('XY')
    assert R.on(medium, 2) == q.Pauli('XYYY')
    assert R.on(large, 0) == q.Pauli('ZZZZYXY')
  
    assert SWAP.on(small, 0, 1) == q.Pauli('ZX')
    assert SWAP.on(medium, 0, 1) == q.Pauli('YXZY')
    assert SWAP.on(medium, 2, 3) == q.Pauli('XYYZ')
    assert SWAP.on(medium, 0, 3) == q.Pauli('YYZX')
    assert SWAP.on(medium, 1, 2) == q.Pauli('XZYY')


test_on()
