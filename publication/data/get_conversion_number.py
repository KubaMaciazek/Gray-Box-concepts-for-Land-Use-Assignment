import warnings


def get_conversion_number(sample_name):
    """
    Return number of cells to be converted from agricultural to urban
    :param sample_name: sample name
    :return: number of new urban areas to be allocated for given sample name
    """
    int_quantity = 0

    if sample_name == "Uster":
        int_quantity = 212

    elif sample_name == "Dübendorf":
        int_quantity = 205

    elif sample_name == "Meilen":
        int_quantity = 128

    elif sample_name == "Hedingen":
        int_quantity = 30

    elif sample_name == "Volketswil":
        int_quantity = 213

    elif sample_name == "Bassersdorf":
        int_quantity = 82

    elif sample_name == "Oberglatt":
        int_quantity = 120

    elif sample_name == "Pfäffikon":
        int_quantity = 105

    elif sample_name == "Bülach":
        int_quantity = 201

    elif sample_name == "Nürensdorf":
        int_quantity = 62

    elif sample_name == "Fehraltorf":
        int_quantity = 56

    elif sample_name == "Rümlang":
        int_quantity = 103

    elif sample_name == "Wetzikon (ZH)":
        int_quantity = 136

    elif sample_name == "four_muni_FPUV":
        int_quantity = 586

    elif sample_name == "canton_zuerich":
        int_quantity = 15061

    elif sample_name == "ToDo: ?SoMeOtHeR?":
        int_quantity = 12345

    else:
        warnings.warn("Unknown sample: conversion number set to 0.")

    return int_quantity

# all_communities_plus_FPUV = ["Uster", "Dübendorf", "Meilen", "Hedingen","Volketswil", "Bassersdorf","Oberglatt","Pfäffikon", "Bülach", "Nürensdorf", "Fehraltorf", "Rümlang", "Wetzikon (ZH)", "four_muni_FPUV", "canton_zuerich"] #"Wetzikon (ZH)",
# N_for_all_samples = [212, 205, 128, 30, 213, 82, 120, 105, 201, 62, 56, 103, 136, 586, 15061]
