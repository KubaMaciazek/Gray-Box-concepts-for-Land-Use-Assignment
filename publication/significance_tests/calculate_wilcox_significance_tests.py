from scipy.stats import ranksums

from publication.significance_tests.get_sample_combinations_hvs import get_sample_combinations_hvs
from publication.significance_tests.get_sample_combinations_igds import get_sample_combinations_igds


def calculate_wilcox_significance_tests(analysed_combinations, base_combination, samples, measures, results_dir, summary_dir, seeds, significance_results_path):
    table_headers = []
    rows = {}

    table_headers.append("combination")
    for combination in analysed_combinations:
        rows[combination] = [combination]

    for measure in measures:
        for sample in samples:
            table_headers.append(sample + '_' + measure)

            analysed_sample_combination_results = {}
            if measure == 'igd':
                analysed_sample_combination_results = get_sample_combinations_igds(base_combination, sample, summary_dir)
            else:
                analysed_sample_combination_results = get_sample_combinations_hvs(base_combination, analysed_combinations, sample, results_dir, seeds)

            base_combination_results = analysed_sample_combination_results[base_combination]

            if measure == 'igd':
                alternative = 'less'
            else:
                alternative = 'greater'

            # print('|'.join(['combination', 'base_combination', 'sample_' + measure, 'test_value', 'p_value']))
            for combination in analysed_combinations:
                curr_combination_results = analysed_sample_combination_results[combination]

                test_result = ranksums(curr_combination_results, base_combination_results, alternative)

                # print('|'.join([combination, base_combination, sample, str(test_result.statistic), str(test_result.pvalue)]))
                rows[combination].append(str(test_result.pvalue))


    headers_line = '|'.join(table_headers)
    rows_lines = []
    for line in rows.values():
        rows_lines.append('|'.join(line))

    # Print result
    print(headers_line)
    for row in rows_lines:
        print(row)

    # save result to significance_results_path

    with open(significance_results_path, 'w') as file:
        file.write(headers_line + '\n')
        for row in rows_lines:
            file.write(row + '\n')
            