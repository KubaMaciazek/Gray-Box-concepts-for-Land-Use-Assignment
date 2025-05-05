from publication.significance_tests.calculate_wicox_significance_tests_mp import calculate_wilcox_significance_tests_mp
from publication.significance_tests.calculate_wilcox_significance_tests import calculate_wilcox_significance_tests
from publication.significance_tests.significance_tests_setups import get_test_config, \
    get_final_tests_significance_tests_config, get_initial_tests_base_and_crossovers_significance_test_config


def run_significance_tests():
    # analysed_combinations, base_combination, samples, measures, results_dir, summary_dir, seeds, significance_results_path = get_final_tests_significance_tests_config()
    # calculate_wilcox_significance_tests(analysed_combinations, base_combination, samples, measures, results_dir, summary_dir, seeds, significance_results_path)

    analysed_combinations, base_combination, samples, measures, dataSourceDir, summary_dir, seeds, significance_results_path = get_initial_tests_base_and_crossovers_significance_test_config()
    calculate_wilcox_significance_tests_mp(analysed_combinations, base_combination, samples, measures, dataSourceDir, summary_dir, seeds, significance_results_path)

run_significance_tests()
