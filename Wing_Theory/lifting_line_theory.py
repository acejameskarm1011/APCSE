import numpy as np


def solve_fourier_coefficients(N, C_lAlpha, cTheta, b, alphaTheta, alphaZeroLiftTheta):
    """
    This function solves for the fourier coefficients that solve the LLT equation

    Parameters
    ---------
    N : int
        The number of fourier coefficients being solved for

    C_lAlpha : int/float
        The airfoil lift coefficient per change in angle of attack [1/rad]

    b : int/float
        Wingspan of the wing [ft]

    cTheta : func
        The chord of the wing as a function of theta [ft]
    
    alphaTheta :  func
        The current angle of attack as a function theta [deg]

    alphaZeroLiftTheta : func
        The current angle of attack of zero lift as a function theta [deg]

    returns
    -------
    A_n : np.ndarray
        The total array of fourier coefficients
    theta : np.ndarray
        The array of thetas being calculated over
    """
    theta = np.linspace(0, np.pi, N+2)[1:-1]

    matrix = []
    RHS = cTheta(theta)/(4*b)*C_lAlpha*(alphaTheta(theta)-alphaZeroLiftTheta(theta))/180*np.pi
    for n in range(1,N+1):
        matrix.append((np.sin(n*theta)+cTheta(theta)/(4*b)*C_lAlpha*n*np.sin(n*theta)/np.sin(theta)).tolist())
    matrix = np.array(matrix).T

    A_n = np.linalg.inv(matrix) @ RHS
    return A_n, theta