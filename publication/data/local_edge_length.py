
import numpy as np

from publication.data.get_areal_raster import get_areal_raster
from publication.common.sq_vis import plot_lulc_map


def get_lel(lulc_raster):
    '''
    :param lulc_raster: Int matrix of values 0-4 representing land use land cover
    :return: matrix with number of different type adjecent cells. Different/comparison: Urban VS NonUrban
    '''

    # 1) Create urban mask
    urban_mask = np.zeros_like(lulc_raster, dtype=int)
    urban_mask[lulc_raster == 1] = 1
    # plot_lulc_map(urban_mask, 'urban_mask')

    # 2) Compute horizontal and vertical transition matrix - transition between urban vs non-urban
    horziontal_transition = np.array(urban_mask[:,1:] != urban_mask[:,:-1]).astype(int)
    vertical_transition = np.array(urban_mask[1:,:] != urban_mask[:-1,:]).astype(int)

    # 3) Add zero'es rows and columns, to indicate that the space beyond given area does not differ from the border
    ht_height, ht_width = horziontal_transition.shape
    ht_bordered = np.zeros((ht_height, ht_width + 2))
    ht_bordered[0:ht_height, 1:ht_width + 1] = horziontal_transition

    vt_height, vt_width = vertical_transition.shape
    vt_bordered = np.zeros((vt_height + 2, vt_width))
    vt_bordered[1:vt_height + 1, 0:vt_width] = vertical_transition

    # 4) Compute Local Edge Length - number of different (urban vs nonurban) adjecent cells
    h_sum = ht_bordered[:,1:] + ht_bordered[:,:-1]
    v_sum = vt_bordered[1:,:] + vt_bordered[:-1,:]
    lel = h_sum + v_sum

    return lel


def get_agri_lel(lulc_raster):
    lel = get_lel(lulc_raster)

    # 5) Get lel for agri cells
    agri_mask = np.zeros_like(lulc_raster, dtype=int)
    agri_mask[lulc_raster == 2] = 1

    return lel*agri_mask


def get_agri_lel_probabilities_6a_strict(lulc_raster):
    agri_lel = get_agri_lel(lulc_raster)
    return agri_lel / 4


def get_agri_lel_probabilities_6c_wide(lulc_raster):
    agri_lel = get_agri_lel(lulc_raster)
    return (agri_lel + 1) / 5


def test():
    # areal_file = "data/data_gemeinden_zuerich/Uster/areal_4_09.tif"
    # areal_raster = get_areal_raster(areal_file)

    areal_raster = np.array([
        [2, 1, 1, 1, 3, 3],
        [2, 2, 2, 2, 3, 3],
        [1, 1, 3, 3, 1, 1],
        [4, 4, 4, 1, 4, 2]
    ])

    probabilities = get_agri_lel_probabilities_6a_strict(areal_raster)
    # probabilities = get_agri_lel_probabilities_6c_wide(areal_raster)
    print(probabilities)


# Test
# test()

    # ToDo:
    #  I. Policz macierz TEL, która dla każdego pola agri będzie mówiła z iloma polami urban sąsiaduje.
    #  Potem z tego prawdopowobieństwo -> Więcej sąsiadów urban, większa szansa zamiany.
    #  .
    #   1) Stwórz maske urban vs reszta, 1 dla urban, 0 dla reszty
    #   2) Tworzymy macierz P1, porównując rzędami,  potem P2, porównując kolumnami macierze maski jak przy liczeniu tel
    #   -> uzyskamy macierz mówiącą po kolei czy x11 różni się od x12, x12 od x13, itd... (i tak samo x11 od x21)
    #   3) dodajemy border 0, mówiący o tym że granica nie różni się od tego co poza obszarem badania
    #   4) Liczymy macierz S, gdzie S_ij, to liczba pól innych niż AREAL_ij, a z nim sąsiadujących.
    #   I w zasadzie to chyba mogą być 3 sumy macierzy. Osobno zsumowane skrawki P1 i P2,
    #   krojone podobnie jak dla porównania, a potem poprostu ich suma.
    #   Uzyskana macierz mówi, w zaleznosci od pola, z iloma nie urban polami sasiaduje pole urban,
    #   lub z iloma polami urban sasiaduje pole nie urban.
    #   5) Nas interesuje to drugie, dlatego robimy iloczym macierzy S z maską agri.
    #   Uzyskana macierz SA będzie macierzą liczb od 0 do 4.
    #   Liczba większa od 0 mówi o tym że jest to pole agri, a jego wartość wskazuje na to z iloma urban sąsiaduje.
    #   6) Aby mieć z tego prawdopodobieństwo pod losowanie pól pod względem zwiększania kompaktowości to musimy:
    #       a) podzielić macierz przez 4: wtedy nie wyberamy pól nie sasiaujących z urban,
    #           a na pewno wybieramy te które są otoczone urban.
    #       b) podzielić macierz przez 5: nie wyberamy pól nie sasiaujących z urban,
    #           nie ma pewności że wybieramy te otoczone.
    #           -> To chyba bez sensu, czemu ich nie wybierać. Sama losowość odpowiada za zróżnicowanie.
    #       c) dodać 1 do każdego pola, podzielić przez 5: to sprawia że na pewno wybierzemy pola otoczone,
    #           i z 20% szansą wybierzemy pola które wgl nie sąsaidują z urban.
    #           ?czy to ma sens? zwiększa zróżnicowanie, ale całkowicie stoi w sprzecznosci z zastosowaniem wiedzy
    #           dziedzinowej. Ale w sumie, w zależnosci od mutacji, bez tego może nie byc możliwości eksplorowania
    #           nowych obszarów, tzn tworzenia skupisk oddzielonych od dotychczas istniejących.
    #   Chyba 6b bez sensu, ale 6a i 6c brzmią równie sensownie. Oba uzasadnione
    #   .
    #   7) Losować pola na podstawie tej macierzy, na bierząco ją aktualizując w zależności od wylosowanych pól.
    #   .
    #   UWAGA) Taka macierz, w połączoniu z analogiczną macierzą, ale stworzoną na podstawie maski z urban w punkcie 5,
    #   można by wyborzystać w mutacji, która by mutowała tylko (6a) pola agri i urban styczne z tymi drugimi (mutacja
    #   brzegowa) z mniejszym/większym prawdopodobieństwem w zależności od wpływu na TEL.
    #   Można by również dopuścić mutowanie losowych pól, nie będą cych na granicy urban/agri (6c).
    #   Tylko żeby zoptymalizować taką mutację, trzeba by raczej raz te macierze policzyć i przypisać do indywiduów,
    #   a potem aktualizować na bierząco przy crossach i mutacjach.