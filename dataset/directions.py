import numpy as np


def versor(A,B):
    """
    Compute the unitary vector
    pointing from A to B.
    """

    # Check A and B to be of type np.array
    if type(A) != np.ndarray:
        A = np.asarray(A)
    if type(B) != np.ndarray:
        B = np.asarray(B)
    # Compute the vector pointing from A to B
    vector = B - A
    module = np.sqrt(np.sum(vector**2))
    versor = vector/module
    return versor

def versor_perp_plane(A,B,C):
    """
    Compute the unitary vector
    perpendicular to the plane
    defined by the points A, B
    and C.
    """
    # Check A, B and C to be of type np.array
    if type(A) != np.ndarray:
        A = np.asarray(A)
    if type(B) != np.ndarray:
        B = np.asarray(B)
    if type(C) != np.ndarray:
        C = np.asarray(C)
    # Vector AC
    vector1 = C - A
    # Vector AB
    vector2 = B - A
    perp_vector = np.cross(vector2, vector1)
    perp_module = np.sqrt(np.sum(perp_vector**2))
    perp_versor = perp_vector/perp_module
    return perp_versor


#if "__main__":
#   X = [0,0,0]
#   Y = [0,3,0]
#   Z = [0,0,5]
#   print(versor(X,Y))
#   print(versor_perp_plane(X,Y,Z))
