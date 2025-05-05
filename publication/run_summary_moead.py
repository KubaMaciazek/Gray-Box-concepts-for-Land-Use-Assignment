import os

from publication.general_test.tests_configs import get_general_tests_config
from publication.summary.summarize_hvs import summarize_hvs

# TESTS_RESULTS = 'tests_results\\100000_100'
SUMMARIES_PATH = 'summaries_results'


def run_summary(summary_path,  reference_tests, analyzed_tests):
    (n_pop, NFFE, cxpb, mutpb, w1, w2, seeds, sample_municipalities, list_initializations, list_mutations,
     list_crossovers, list_repairs, nr_of_tests, test_nr, starting_time, test_stamp) = get_general_tests_config()
    algorithm = "moead"

    for sample in sample_municipalities:
        for test in analyzed_tests:
            test_path = os.path.join(TESTS_RESULTS, test, sample)

            # 1) Calculate HV summary
            summarize_hvs(summary_path, test_path, sample, test)

            # 2) Calculate IGD summary
            # 2.1) Calculate TPFs
            # 2.2) Calculate IGDs by run
            # 2.3) Calculate IGDs summary


# ---------------------- CALCULATE SUMMARY ----------------------


# if __name__ == '__main__':
#     reference_tests = [
#         '1724932224_nsgaii_nt_wr',
#         '1725000833_nsgaii_nt_nr_2055_end'
#     ]
#     analyzed_tests = [
#         '1724932224_nsgaii_nt_wr',
#         '1725000833_nsgaii_nt_nr_2055_end'
#     ]
#
#     summary_name = 'summary_1'
#     summary_path = os.path.join(SUMMARIES_PATH, summary_name)
#
#     run_summary(summary_path, reference_tests, analyzed_tests)


# if __name__ == '__main__':
#     reference_tests = [
#     ]
#     analyzed_tests = [
#         'moead_nt_combined'
#     ]
#
#     summary_name = 'summary_3_moead_nt_combined_1_missing'
#     summary_path = os.path.join(SUMMARIES_PATH, summary_name)
#
#     run_summary(summary_path, reference_tests, analyzed_tests)
#
#
# # ############## MOEAD-tunned summary ################

TESTS_RESULTS = 'tests_results\\100000_n_pop'
if __name__ == '__main__':
    reference_tests = [
    ]
    analyzed_tests = [
        # '1731336743_moead_tuned'
        '1731336743_moead_tuned_0505'
    ]

    # summary_name = 'summary_1731336743_moead_tuned'
    summary_name = 'summary_1731336743_moead_tuned_0505'
    summary_path = os.path.join(SUMMARIES_PATH, summary_name)

    run_summary(summary_path, reference_tests, analyzed_tests)