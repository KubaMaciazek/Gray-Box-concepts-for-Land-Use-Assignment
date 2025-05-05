"""
    Cruicial statistisc for each sample:
        regional_sq: Sum of normalized soil quailty values from the whole area.
        min_sq_loss_possible: Minimum possible loss of soil quality (sum of normalized soil quaility values from N worst areas, N lowest values).
        min_sq_loss_possible_percentage: Min relative sq loss.
        min_tel: Estimated shortest possible edge length of all urban areas.
        max_sq_loss_possible: Maximum possible sq loss.
        max_tel_possible: Estimated longest possible TEL.
"""

COMMUNITY_DATA = {
    'Uster': {
        'regional_sq': 972.0266,
        'min_sq_loss_possible': 108.23181,
        'min_sq_loss_possible_percentage': 0.11134655,
        'min_tel': 930.0,
        'max_sq_loss_possible': 212.0,
        'max_tel_possible': 1990
    },
    'Dübendorf': {
        'regional_sq': 358.21362,
        'min_sq_loss_possible': 110.786804,
        'min_sq_loss_possible_percentage': 0.3092758,
        'min_tel': 372.0,
        'max_sq_loss_possible': 187.34195,
        'max_tel_possible': 1404
    },
    'Meilen': {
        'regional_sq': 359.40298,
        'min_sq_loss_possible': 52.440628,
        'min_sq_loss_possible_percentage': 0.14591038,
        'min_tel': 378.0,
        'max_sq_loss_possible': 119.75984,
        'max_tel_possible': 1026
    },
    'Hedingen': {
        'regional_sq': 220.02432,
        'min_sq_loss_possible': 11.88889,
        'min_sq_loss_possible_percentage': 0.054034438,
        'min_tel': 158.0,
        'max_sq_loss_possible': 30.0,
        'max_tel_possible': 316
    },
    'Volketswil': {
        'regional_sq': 448.34332,
        'min_sq_loss_possible': 139.69394,
        'min_sq_loss_possible_percentage': 0.31157807,
        'min_tel': 358.0,
        'max_sq_loss_possible': 213.0,
        'max_tel_possible': 1424
    },
    'Bassersdorf': {
        'regional_sq': 242.31628,
        'min_sq_loss_possible': 39.715317,
        'min_sq_loss_possible_percentage': 0.16389868,
        'min_tel': 258.0,
        'max_sq_loss_possible': 70.68658,
        'max_tel_possible': 696
    },
    'Oberglatt': {
        'regional_sq': 304.50116,
        'min_sq_loss_possible': 61.68215,
        'min_sq_loss_possible_percentage': 0.20256788,
        'min_tel': 280.0,
        'max_sq_loss_possible': 109.59999,
        'max_tel_possible': 894
    },
    'Pfäffikon': {
        'regional_sq': 555.91077,
        'min_sq_loss_possible': 40.913727,
        'min_sq_loss_possible_percentage': 0.073597655,
        'min_tel': 450.0,
        'max_sq_loss_possible': 102.56952,
        'max_tel_possible': 1016
    },
    'Bülach': {
        'regional_sq': 373.01068,
        'min_sq_loss_possible': 113.50087,
        'min_sq_loss_possible_percentage': 0.30428317,
        'min_tel': 420.0,
        'max_sq_loss_possible': 186.70978,
        'max_tel_possible': 1322
    },
    'Nürensdorf': {
        'regional_sq': 353.85315,
        'min_sq_loss_possible': 26.610023,
        'min_sq_loss_possible_percentage': 0.07520075,
        'min_tel': 276.0,
        'max_sq_loss_possible': 56.000008,
        'max_tel_possible': 574
    },
    'Fehraltorf': {
        'regional_sq': 373.29498,
        'min_sq_loss_possible': 23.6,
        'min_sq_loss_possible_percentage': 0.063220784,
        'min_tel': 240.0,
        'max_sq_loss_possible': 50.600002,
        'max_tel_possible': 512
    },
    'Rümlang': {
        'regional_sq': 450.87335,
        'min_sq_loss_possible': 52.369415,
        'min_sq_loss_possible_percentage': 0.11615106,
        'min_tel': 418.0,
        'max_sq_loss_possible': 95.66571,
        'max_tel_possible': 966
    },
    'Wetzikon (ZH)': {
        'regional_sq': 389.87592,
        'min_sq_loss_possible': 56.689465,
        'min_sq_loss_possible_percentage': 0.14540386,
        'min_tel': 382.0,
        'max_sq_loss_possible': 98.01162,
        'max_tel_possible': 1120
    },
    'four_muni_FPUV': {
        'regional_sq': 2151.9478,
        'min_sq_loss_possible': 254.69714,
        'min_sq_loss_possible_percentage': 0.11835656,
        'min_tel': 2228.0,
        'max_sq_loss_possible': 527.60004,
        'max_tel_possible': 4914
    },
    'canton_zuerich': {
        'regional_sq': 46358.254,
        'min_sq_loss_possible': 4985.498,
        'min_sq_loss_possible_percentage': 0.107542835,
        'min_tel': 59152.0,
        'max_sq_loss_possible': 13984.178,
        'max_tel_possible': 111662
    }
}
