from publication.significance_tests.significance_tests_setups import get_final_tests_significance_tests_config


def get_final_combinations_plotting_config():
    analysed_combinations, base_combination, samples, measures, results_dir, summary_dir, seeds, significance_results_path = get_final_tests_significance_tests_config()

    seed = str(seeds[0])
    plotTitle = 'PF for Uster sample achieved by final combinations in run with seed ' + seed
    sample = 'Uster'
    combinations = analysed_combinations + [base_combination]
    dataSourceDir = results_dir
    resultsDestinationDir = summary_dir

    return plotTitle, sample, combinations, seed, dataSourceDir, resultsDestinationDir


def get_initial_crossovers_plotting_config():
    _, _, _, _, _, _, seeds, _ = get_final_tests_significance_tests_config()

    seed = str(seeds[0])
    sample = 'Uster'
    plotTitle = 'PF for ' + sample + ' sample achieved by crossovers in initial run with seed ' + seed
    combinations = [
        [
            'moead;spg;rbm_rcm_brm_bcpm_wri;ac;brm',
            'moead;spg;rbm_rcm_brm_bcpm_wri;spc;brm',
            'moead;spg;rbm_rcm_brm_bcpm_wri;ppc;brm',
            'moead;spg;rbm_rcm_brm_bcpm_wri;ppc_fuo;brm'
        ],
        [
            'nsgaii;spg;rbm_rcm_brm_bcpm_wri;ac;brm',
            'nsgaii;spg;rbm_rcm_brm_bcpm_wri;spc;brm',
            'nsgaii;spg;rbm_rcm_brm_bcpm_wri;ppc;brm',
            'nsgaii;spg;rbm_rcm_brm_bcpm_wri;ppc_fuo;brm'
        ],
        [
            'moead;spg;rbm_rcm_brm_bcpm_wri;ac;brm',
            'nsgaii;spg;rbm_rcm_brm_bcpm_wri;ac;brm'
        ]
    ]
    dataSourceDir = [
        'tests_results\\100000_100\\moead_nt_combined',
        'tests_results\\100000_100\\nsgaii_nt_combined',
        'tests_results\\100000_100\\1736640671_baseline'
    ]
    resultsDestinationDir = 'summaries_results\\FS_InitialTests_19-01-2025'

    return plotTitle, sample, combinations, seed, dataSourceDir, resultsDestinationDir
