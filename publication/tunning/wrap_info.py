import os

# ######################    NSGAII   ##################################################
# source_dir = '../tests_results/nsgaii_tunning/1727466533_nt_0901/Uster'
# destination_path = 'tunned_parameters_dictionary_nsgaii.txt'

# ######################    MOEAD   ##################################################
# # source_dir = '../tests_results/moead_tunning/1729266974_mt_0901/Uster'
# # destination_path = 'tunned_parameters_dictionary_moead.txt'
# source_dir = '../tests_results/moead_tunning/1731599275_mt_0505/Uster'
# destination_path = 'tunned_parameters_dictionary_moead_0505.txt'
source_dir = '../tests_results/nsgaii_tunning/1731746812_nt_0505/Uster'
destination_path = 'tunned_parameters_dictionary_nsgaii_0505.txt'


def wrap_info():
    files = [f for f in os.listdir(source_dir) if os.path.isfile(os.path.join(source_dir, f))]

    with open(destination_path, 'w') as dest_file:
        for file_name in files:
            combination, _ = os.path.splitext(file_name)
            file_path = os.path.join(source_dir, file_name)
            with open(file_path, 'r') as file:
                lines = [line.strip() for line in file.readlines()]
                n_pop = (int(lines[0]) + 5) // 10 * 10
                cxpb = round(float(lines[1]), 1)
                mutpb = round(float(lines[2]), 1)

                dest_file.write(f"{combination};{n_pop};{cxpb};{mutpb}\n")


wrap_info()
