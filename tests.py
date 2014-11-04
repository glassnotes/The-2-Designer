"""
    The 2 Designer - a code for generate random unitary matrices
    from approximate unitary 2-designs.

    Copyright (C) 2014 Olivia Di Matteo

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""


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
