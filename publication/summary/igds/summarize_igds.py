import os

import numpy as np

from publication.summary.igds.get_sample_igd_file import get_sample_igd_file

# STATS_PATH = 'summaries_results\\Final_Summary_19-11-2024'
# STATS_PATH = 'summaries_results\\Final_Summary_12-01-2025'
# IGDS_STATS_PATH = os.path.join(STATS_PATH, 'igds_summary')


def summarize_igds(sample, summary_path):
    IGDS_STATS_PATH = os.path.join(summary_path, 'igds_summary')

    os.makedirs(IGDS_STATS_PATH, exist_ok=True)
    final_path = os.path.join(IGDS_STATS_PATH, sample + '.txt')

    sample_igd_file_path = get_sample_igd_file(sample, summary_path)

    with open(sample_igd_file_path, 'r') as file:
        with open(final_path, 'w') as output:
            output.write(
                # Standard combinations
                # 'filename' + ';' + 'alg;init;mut;cross;repair' + ';' + 'min_igd' + ';' + 'avg_igd' + ';' + 'median_igd' + ';' + 'max_igd' + ';' + 'std_igd' + '\n')
                # final combinations
                'filename' + ';' + 'alg;init;mut;cross;repair;n_pop;cxpb;mutpb' + ';' + 'min_igd' + ';' + 'avg_igd' + ';' + 'median_igd' + ';' + 'max_igd' + ';' + 'std_igd' + '\n')

            for line in file:
                combination_results = line.strip().split(';')

                # For combinations withount npop, crosspb i mutpb
                # combination = ';'.join(combination_results[:6])
                # igds = combination_results[6:]
                # For final combinations
                combination = ';'.join(combination_results[:9])
                igds = combination_results[9:]

                igds = [float(igd) for igd in igds]

                avg_igd = np.average(igds)
                median_igd = np.median(igds)
                min_igd = np.min(igds)
                max_igd = np.max(igds)
                std_igd = np.std(igds)

                output.write(combination + ';' + str(min_igd) + ';' + str(avg_igd) + ';' + str(median_igd) + ';' + str(
                    max_igd) + ';' + str(std_igd) + '\n')