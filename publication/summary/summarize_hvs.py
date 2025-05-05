import os

import numpy as np

from publication.statistics.load_results import load_results

HVS_DIR = 'hvs_summary'
# 'summaries/summary_name/hvs_summary.txt' -> testcasy w liniach'


def summarize_hvs(summary_path, test_result_sample_root_path, sample, test):
    combinations = os.listdir(test_result_sample_root_path)

    hvs_dir = os.path.join(summary_path, HVS_DIR, sample)
    os.makedirs(hvs_dir, exist_ok=True)
    final_path = os.path.join(hvs_dir, test + '.txt')

    with open(final_path, 'w') as file:
        # Standard combinations
        # file.write('alg;init;mut;cross;repair' + ';' + 'min_hv' + ';' + 'avg_hv' + ';' + 'median_hv' + ';' + 'max_hv' + ';' + 'std_hv' + '\n')
        # Final combinations
        file.write('alg;init;mut;cross;repair;n_pop;cxpb;mutpb' + ';' + 'min_hv' + ';' + 'avg_hv' + ';' + 'median_hv' + ';' + 'max_hv' + ';' + 'std_hv' + '\n')

        for combination in combinations:
            # sample combination path
            scp = os.path.join(test_result_sample_root_path, combination)
            # sample combination seeds results
            scsr = []

            for seedfile in os.listdir(scp):
                scsr.append(load_results(os.path.join(scp, seedfile)))

            fhvs = []
            for result in scsr:
                fhvs.append(result['hvs'][-1])

            avg_hv = np.average(fhvs)
            median_hv = np.median(fhvs)
            min_hv = np.min(fhvs)
            max_hv = np.max(fhvs)
            std_hv = np.std(fhvs)

            file.write(combination + ';' + str(min_hv) + ';' + str(avg_hv) + ';' + str(median_hv) + ';' + str(max_hv) + ';' + str(std_hv) + '\n')
