import numpy as np
import scipy
from deap.benchmarks.tools import igd


def deap_igd(A, Z):
    return igd(A, Z)


def my_igd(aproksymacja, tpf):
    distances = scipy.spatial.distance.cdist(aproksymacja, tpf)
    return np.average(np.min(distances, axis=0))


    # def igd(A, Z):
    #     """Inverse generational distance.
    #     """
    #     if not scipy_imported:
    #         raise ImportError("idg requires scipy module")
    #     distances = scipy.spatial.distance.cdist(A, Z)
    #     return numpy.average(numpy.min(distances, axis=0))


# %%%%%%%%%%%%%%%%%%%%


# [(20.250753, 168.0), (12.0, 248.0), (12.046914, 244.0), (12.824691, 224.0),
def test_my_igd():
    apf = [(0, 0)]
    tpf = [(0, 0), (0, 1), (0, 1), (0, -1)]

    print(my_igd(apf, tpf)) # poprawna
    print(my_igd(tpf, apf)) # NIE poprawna


# test_my_igd()