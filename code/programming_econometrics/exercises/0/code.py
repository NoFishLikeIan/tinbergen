"""
e0_elim.py
Purpose : ???
Date: 2017/7/13
@author : cbs310

The code comes from https://personal.vu.nl/c.s.bos/ppectr.html
"""


import numpy as np


def ElimElement(mC, i, j):
    """
    br = ElimElement ( mC , i , j )

    Purpose :
    Eliminate one element [i , j ] of a matrix , subtracting multiples
    of row j from row i

    Inputs :
    mC iK x iK + iY matrix
    i integer , number of row to eliminate
    j integer , number of row with pivot

    Outputs :
    mC iK x iK + iY matrix , with 0 created in location [i , j ]

    Return value :
    br boolean , True if all went well
    """
    if mC[j, j] == 0:
        return False

    # Find factor multiplying row j
    dF = mC[i, j] / mC[j, j]

    # Subtract dF times row j from row i
    mC[i, j:] = mC[i, j:] - dF * mC[j, j:]

    return True


def ElimColumn(mC, j):
    """
    br = ElimColumn ( mC , j )

    Purpose :
    Eliminate one column [: , j ] of a matrix , creating zeros below
    the pivot at [j , j ]

    Inputs :
    mC iK x iK + iY matrix
    j integer , number of row with pivot

    Outputs :
    mC iK x iK + iY matrix , with 0 created below [j , j ]

    Return value :
    br boolean , True if all went well
    """
    br = True
    iK = np.size(mC, 0)
    for i in range(j + 1, iK):
        # print (" Starting row " , i )
        br = br and ElimElement(mC, i, j)
        # print (" resulting in mC = \ n " , mC )
    return br


def ElimGauss(mC):
    """
    br = ElimGauss ( mC )

    Purpose :
    Eliminate a matrix , creating zeros at lower triangular

    Inputs :
    mC iK x iK + iY matrix

    Outputs :
    mC iK x iK + iY matrix , with 0 created below main diagonal

    Return value :
    br boolean , True if all went well
    """
    iK = np.size(mC, 0)
    br = True
    for j in range(iK):
        print(" Starting iteration ", j)

        br = br and ElimColumn(mC, j)

    print(" resulting in mC = \ n ", mC)
    return br


def main():
    # Magic numbers
    mX = [[1, 1, 3],
          [1, -1, -3],
          [1, -4, -1],
          [1, 1, -1],
          [1, 0, 2],
          [1, 1, -2],
          [1, 2, 3],
          [1, 1, -2],
          [1, -5, 1],
          [1, -3, -4]]
    vY = [4, -2, 12, -4, 5,
          -6, 1, -6, 19, 1]

    # Transform inputs to matrices of floats
    mX = np.array(mX)
    iN = np.size(vY)
    vY = np.array(vY).reshape(iN, 1)
    # Prepare A = X ’X , b = X ’y , C = [A , b ]
    mA = np.transpose(mX)@mX
    vB = np.transpose(mX)@vY
    mC = np.hstack((mA, vB))

    mC = mC.astype(float)
    print(" Initial matrix [ A | b ]: \n ", mC)
    # Eliminate the mC matrix , resulting in [ mU | vC ]
    ir = ElimGauss(mC)
    print(" ElimGauss returns ir = ", ir,
          " with mC = \n ", mC)


if __name__ == '__main__':
    main()
