from . import conjugate

from .gates import X, Y, Z

import numpy as np

def test_conjugate_X():
	rho = np.zeros((8, 8))
	rho[0, 0] = 1

	rho0 = conjugate.conjugate_qubit(rho, X, 0, 3)
	rho1 = conjugate.conjugate_qubit(rho, X, 1, 3)
	rho2 = conjugate.conjugate_qubit(rho, X, 2, 3)

	assert rho0[4, 4] == 1
	assert rho1[2, 2] == 1
	assert rho2[1, 1] == 1

	assert np.sum(rho0) == 1
	assert np.sum(rho1) == 1
	assert np.sum(rho2) == 1
