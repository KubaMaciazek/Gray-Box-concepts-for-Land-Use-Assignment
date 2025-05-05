import numpy as np

from publication.objective_functions.tel import edge_length_urban


# [KUBA]: Zbiorcza funkcja celu, która zwraca tupla dwóch wartości:
#   - SQ - sum of qualities of soil cells choosen for urbanization:  NIE JEST TO DOMYŚLNE SQ, NIE PROCENTOWA STRATA.
#   - TEL - total edge length of urban patches
# dla każdej ze składowych funkcji celu (dwóch celów optymalizacyjnych)
def aggregated_objective_function(individual, sq_raster_normalized, areal_4kl_09):  # objective1 to all_obj["sq"]
    '''

    :param individual:
    :param sq_raster_normalized: macierz, która dla danego obszaru, zawiera informację o żyzności każdej z komórek.
        Wartości żyznosci są z przediału 0-1, ponieważ orginalne z przedziału 0-9 podzielono przez max wartość=9.
    :param areal_4kl_09:
    :return:
    '''

    individual = np.array(individual)

    # elif(name_objective1 == "sq"):
    objective1_val = sq_raster_normalized[np.array(individual == 1) & np.array(areal_4kl_09 == 2)]
    # objective1_val - macierz wartości jakości gleby tych pól, które są wybrane do urbanizacji (1 dla indyvidual)
    # a w pierwotnym planie zagospodarowania są rolne (areal_4kl_09 == 2)

    # elif(name_objective2 == "tot_edge_len"):
    objective2_val = edge_length_urban(areal_4kl_09, individual, [2, 1])
    # [ab]: https://docs.scipy.org/doc/scipy/reference/generated/scipy.ndimage.generate_binary_structure.html

    return np.sum(objective1_val), np.sum(objective2_val)
