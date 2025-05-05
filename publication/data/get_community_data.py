from publication.data.community_data import COMMUNITY_DATA

community_data = COMMUNITY_DATA


def get_community_min_tel_possible(community):
    return get_community_data(community, "min_tel")


def get_community_min_sq_loss_possible(community):
    return get_community_data(community, "min_sq_loss_possible")


def get_community_min_sq_loss_possible_percentage(community):
    return get_community_data(community, "min_sq_loss_possible_percentage")


def get_community_regional_sq(community):
    return get_community_data(community, "regional_sq")


def get_community_max_tel_possible(community):
    return get_community_data(community, "max_tel_possible")


def get_community_max_sq_loss_possible(community):
    return get_community_data(community, "max_sq_loss_possible")


def get_community_data(community, field):
    """
    Retrieve specific field value for a given community.

    Parameters:
        community (str): The name of the community.
        field (str): The field to retrieve (e.g., 'regional_sq', 'min_tel').

    Returns:
        The value of the specified field for the given community.
    """
    if community in community_data and field in community_data[community]:
        return community_data[community][field]
    else:
        return None


def get_all_community_data(community):
    """
    Retrieve all fields and their values for a given community.

    Parameters:
        community (str): The name of the community.

    Returns:
        A dictionary containing all fields and their values for the given community.
    """
    if community in community_data:
        return community_data[community]
    else:
        return None


# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

data_gemeinden_zuerich_KUBA_PATH = "data/data_gemeinden_zuerich/"

all_communities_plus_FPUV = ["Uster", "Dübendorf", "Meilen", "Hedingen","Volketswil", "Bassersdorf","Oberglatt","Pfäffikon", "Bülach", "Nürensdorf", "Fehraltorf", "Rümlang", "Wetzikon (ZH)", "four_muni_FPUV", "canton_zuerich"]
N_for_all_samples = [212, 205, 128, 30, 213, 82, 120, 105, 201, 62, 56, 103, 136, 586, 15061]

seeds3 = [924767851, 2562755179, 963402710]
seeds20 = [1939165643, 1595794013, 3133665394, 3181000657, 2194989013, 3238441240, 3534643812, 2220046226, 673201361, 451147359, 2869651061, 1567599280, 2396077065, 3766233533, 3634474126, 2033958569, 2097258941, 867154026, 2331360844, 2490353467]


def get_areal_and_sq_rasters_paths(community):
    sq_path = ""
    areal_path = ""

    if community == "canton_zuerich":
        areal_path = data_gemeinden_zuerich_KUBA_PATH + community + "/areal_zuerich"
        sq_path = data_gemeinden_zuerich_KUBA_PATH + community + "/sq"
    else:
        areal_path = data_gemeinden_zuerich_KUBA_PATH + community + "/areal_4_09.tif"
        sq_path = data_gemeinden_zuerich_KUBA_PATH + community + "/sq.tif"

    return areal_path, sq_path


def get_all_community_names_and_ns():
    return all_communities_plus_FPUV, N_for_all_samples


def get_3_20_seeds():
    return seeds3, seeds20


def get_community_ref_point(community):
    return [get_community_max_sq_loss_possible(community), get_community_max_tel_possible(community)]


def get_community_ideal_point(community):
    return [get_community_min_sq_loss_possible(community), get_community_min_tel_possible(community)]
