from publication.summary.igds.get_sample_igd_file import get_sample_igd_file


def get_sample_combinations_igds(base_combination, sample, summary_path):
    sample_combinations_igds = {}
    sample_file = get_sample_igd_file(sample, summary_path)

    combination_length = len(base_combination.split(';'))
    print('combination_length: ' + str(combination_length))
    # combination_length += 1

    with open(sample_file, 'r') as file:
        for line in file:
            combination_results = line.strip().split(';')
            # combination = ';'.join(combination_results[1:combination_length])
            combination = ';'.join(combination_results[0:combination_length])
            print('combination: ' + combination)
            igds = combination_results[combination_length:]
            print('igds length: ' + str(len(igds)))
            igds = [float(igd) for igd in igds]
            sample_combinations_igds[combination] = igds

    return sample_combinations_igds
