import os

from publication.statistics.load_results import load_results


def get_sample_combinations_hvs(base_combination, analysed_combinations, sample, results_path, seeds):
    sample_combinations_hvs = {}
    # joined_combinations = [base_combination] + analysed_combinations
    joined_combinations = analysed_combinations

    combination_length = len(base_combination.split(';')) - 1
    print('combination_length: ' + str(combination_length))

    for combination in joined_combinations:
        hvs = []
        for seed in seeds:
            seedfile = os.path.join(results_path, sample, ';'.join((combination.split(';'))[1:combination_length+1]), str(seed) + '.txt')
            print('seedfile: ' + seedfile)
            seedfile_results = load_results(seedfile)
            hvs.append(seedfile_results['hvs'][-1])

        print('hvs len: ' + str(len(hvs)))
        sample_combinations_hvs[combination] = hvs

    return sample_combinations_hvs
