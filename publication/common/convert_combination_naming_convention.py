def convert_combination_naming_convention(combination):
    # replace mutations
    combination = combination.replace("rbm_rcm_brm_bcpm_wri", "MutC")
    combination = combination.replace("rbm_rcm_brm_bcpm_nrii", "MutC2")

    # replace inits
    combination = combination.replace("sq_bpg_50x50_tel_bgp_strict_pr", "HALI")
    combination = combination.replace("bpg_sq_tel_pp", "HYBI")
    combination = combination.replace("sq_bpg", "SQI")
    combination = combination.replace("tel_bpg_strict", "TELI")
    combination = combination.replace("spg", "SPI")

    # replace crossovers
    combination = combination.replace("ppc_fuo", "IDRC")
    combination = combination.replace("ppc", "DRC")
    combination = combination.replace("spc", "SRC")
    combination = combination.replace("ac", "AC")

    # replace repairs
    combination = combination.replace("rrm", "RRM")
    combination = combination.replace("brm", "BRM")

    # replace alg
    combination = combination.replace("moead", "MOEAD")
    combination = combination.replace("nsgaii", "NSGAII")

    return combination
