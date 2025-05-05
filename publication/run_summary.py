import os

from publication.general_test.tests_configs import get_general_tests_config
from publication.summary.calculate_igds import calculate_igds_by_run
from publication.summary.calculate_tpf import calculate_tpf_by_sample
from publication.summary.igds.summarize_igds import summarize_igds
from publication.summary.summarize_hvs import summarize_hvs


def run_summary(summary_path,  reference_tests, analyzed_tests, sample_municipalities):
    """
    Calculate summary statistics for defined tests, nsgaii and moead both
    :param summary_path:
    :param reference_tests:
    :param analyzed_tests:
    :param sample_municipalities:
    :return:
    """

    for sample in sample_municipalities:
        # # 2.1) Calculate TPFs
        calculate_tpf_by_sample(reference_tests, sample, summary_path)
        # # 2.2) Calculate IGDs by run
        calculate_igds_by_run(analyzed_tests, sample, summary_path)
        # 2.3) Calculate IGDs summary
        summarize_igds(sample, summary_path)

        for test_path in analyzed_tests:
            test = test_path.split('\\')[-1]
            test_path_sample = os.path.join(test_path, sample)

            # # 1) Calculate HV summary
            summarize_hvs(summary_path, test_path_sample, sample, test)



# ---------------------- FINAL SUMMARY ----------------------

# TESTS_RESULTS = 'tests_results\\100000_n_pop'
SUMMARIES_PATH = 'summaries_results'

if __name__ == '__main__':

    # # Basic summary: initial tests + baseline results
    # # reference: what constitutes base for creating TPFs
    # reference_tests = [
    #     'tests_results\\100000_100\\nsgaii_nt_combined',    # wyniki nietuningowanego nsgaii
    #     'tests_results\\100000_100\\moead_nt_combined',    # wyniki nietuningowanego moead
    #     'tests_results\\100000_100\\1736640671_baseline'    # wyniki baseline
    # ]
    # # analysed: results of what do I want to calculate
    # analyzed_tests = [
    #     'tests_results\\100000_100\\nsgaii_nt_combined',
    #     'tests_results\\100000_100\\moead_nt_combined',
    #     'tests_results\\100000_100\\1736640671_baseline'
    # ]
    # # name of the summary
    # summary_name = 'FS_InitialTests_19-01-2025'
    # # sample dla których liczymy TPFy i wyniki
    # sample_municipalities = ["Hedingen", "Uster", "four_muni_FPUV"]
    # # Basic end --------------------------------------------------------------------



    # # Select best / after tunning summary: initial tests + baseline + tunned results
    # # reference: what constitutes base for creating TPFs
    # reference_tests = [
    #     'tests_results\\100000_100\\nsgaii_nt_combined',
    #     'tests_results\\100000_n_pop\\1728300766_nsgaii_tuned',
    #     'tests_results\\100000_n_pop\\1728300766_nsgaii_tuned_0505',
    #
    #     'tests_results\\100000_100\\moead_nt_combined',
    #     'tests_results\\100000_n_pop\\1731336743_moead_tuned',
    #     'tests_results\\100000_n_pop\\1731336743_moead_tuned_0505',
    #
    #     'tests_results\\100000_100\\1736640671_baseline'
    # ]
    # # analysed: results of what do I want to calculate
    # # -> dalej wszystko, bo chcę porównać do orginałów na tym samym rozszerzonym tle.
    # analyzed_tests = [
    #     'tests_results\\100000_100\\nsgaii_nt_combined',
    #     'tests_results\\100000_n_pop\\1728300766_nsgaii_tuned',
    #     'tests_results\\100000_n_pop\\1728300766_nsgaii_tuned_0505',
    #
    #     'tests_results\\100000_100\\moead_nt_combined',
    #     'tests_results\\100000_n_pop\\1731336743_moead_tuned',
    #     'tests_results\\100000_n_pop\\1731336743_moead_tuned_0505',
    #
    #     'tests_results\\100000_100\\1736640671_baseline'
    # ]
    # # name of the summary
    # summary_name = 'FS_AfterTunningTests_19-01-2025'
    # # sample dla których liczymy TPFy i wyniki
    # sample_municipalities = ["Hedingen", "Uster", "four_muni_FPUV"]
    # # Select end --------------------------------------------------------------------



    # final / Best summary: initial tests + baseline + tunned + final tests results
    # reference: what constitutes base for creating TPFs
    reference_tests = [
        'tests_results\\100000_100\\nsgaii_nt_combined',
        'tests_results\\100000_n_pop\\1728300766_nsgaii_tuned',
        'tests_results\\100000_n_pop\\1728300766_nsgaii_tuned_0505',

        'tests_results\\100000_100\\moead_nt_combined',
        'tests_results\\100000_n_pop\\1731336743_moead_tuned',
        'tests_results\\100000_n_pop\\1731336743_moead_tuned_0505',

        'tests_results\\100000_100\\1736640671_baseline',

        'tests_results\\100000_n_pop\\1737136140_fianl_tests'
    ]
    # analysed: results of what do I want to calculate
    # -> nie potrzebuje przeliczać starych, bo nie chce sie do nich porownywac, tylo te mnie interesują
    analyzed_tests = [
        'tests_results\\100000_n_pop\\1737136140_fianl_tests'
    ]
    # name of the summary
    summary_name = 'FS_FinalTests_19-01-2025'
    # sample dla których liczymy TPFy i wyniki
    sample_municipalities = ["Dubendorf", "Meilen", "Volketswil", "Bassersdorf", "Oberglatt", "Pfaffikon", "Bulach", "Nurensdorf", "Fehraltorf", "Rumlang", "Wetzikon (ZH)", "Hedingen", "Uster", "four_muni_FPUV"]
    # Final end --------------------------------------------------------------------

    summary_path = os.path.join(SUMMARIES_PATH, summary_name)

    run_summary(summary_path, reference_tests, analyzed_tests, sample_municipalities)
















    # reference_tests = [
    #     'tests_results\\100000_100\\nsgaii_nt_combined',
    #     'tests_results\\100000_n_pop\\1728300766_nsgaii_tuned',
    #     'tests_results\\100000_n_pop\\1728300766_nsgaii_tuned_0505',
    #
    #     'tests_results\\100000_100\\moead_nt_combined',
    #     'tests_results\\100000_n_pop\\1731336743_moead_tuned',
    #     'tests_results\\100000_n_pop\\1731336743_moead_tuned_0505'
    # ]
    #
    # analyzed_tests = [
    #     # 'tests_results\\100000_100\\nsgaii_nt_combined',
    #     # 'tests_results\\100000_n_pop\\1728300766_nsgaii_tuned',
    #     # 'tests_results\\100000_n_pop\\1728300766_nsgaii_tuned_0505',
    #     #
    #     # 'tests_results\\100000_100\\moead_nt_combined',
    #     # 'tests_results\\100000_n_pop\\1731336743_moead_tuned',
    #     # 'tests_results\\100000_n_pop\\1731336743_moead_tuned_0505',
    #
    #     'tests_results\\100000_100\\1736640671_baseline'
    # ]
    #
    # summary_name = 'Final_Summary_12-01-2025'


# # ---------------------- CALCULATE SUMMARY ----------------------
#
#
# # if __name__ == '__main__':
# #     reference_tests = [
# #         '1724932224_nsgaii_nt_wr',
# #         '1725000833_nsgaii_nt_nr_2055_end'
# #     ]
# #     analyzed_tests = [
# #         '1724932224_nsgaii_nt_wr',
# #         '1725000833_nsgaii_nt_nr_2055_end'
# #     ]
# #
# #     summary_name = 'summary_1'
# #     summary_path = os.path.join(SUMMARIES_PATH, summary_name)
# #
# #     run_summary(summary_path, reference_tests, analyzed_tests)
#
#
# # if __name__ == '__main__':
# #     reference_tests = [
# #     ]
# #     analyzed_tests = [
# #         '1725136347_moead_nt_wr_220_end'
# #     ]
# #
# #     summary_name = 'summary_2'
# #     summary_path = os.path.join(SUMMARIES_PATH, summary_name)
# #
# #     run_summary(summary_path, reference_tests, analyzed_tests)
# #
# #
# # # ############## NSGAII-tunned summary ################
#
# TESTS_RESULTS = 'tests_results\\100000_n_pop'
# if __name__ == '__main__':
#     reference_tests = [
#     ]
#     analyzed_tests = [
#         '1728300766_nsgaii_tuned'
#     ]
#
#     summary_name = 'summary_1728300766_nsgaii_tuned'
#     summary_path = os.path.join(SUMMARIES_PATH, summary_name)
#
#     run_summary(summary_path, reference_tests, analyzed_tests)
