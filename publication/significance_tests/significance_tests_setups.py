from publication.general_test.tests_configs import get_final_tests_config


def get_test_config():
    analysed_combinations, base_combination, samples, measures, results_dir, summary_dir, seeds, significance_results_path = get_final_tests_significance_tests_config()
    samples = [samples[0]]
    # measures = [measures[0]]

    return analysed_combinations, base_combination, samples, measures, results_dir, summary_dir, seeds, significance_results_path


def get_final_tests_significance_tests_config():
    analysed_combinations = [
        'moead;bpg_sq_tel_pp;rbm_rcm_brm_bcpm_wri;ppc;rrm;100;50;50',
        'moead;tel_bpg_strict;rbm_rcm_brm_bcpm_nrii;ppc;rrm;100;50;50',
        'moead;sq_bpg;rbm_rcm_brm_bcpm_nrii;ppc;rrm;110;50;60',
        'moead;sq_bpg;rbm_rcm_brm_bcpm_nrii;ppc;rrm;100;50;50',
        'nsgaii;sq_bpg_50x50_tel_bgp_strict_pr;rbm_rcm_brm_bcpm_wri;ppc_fuo;brm;340;100;10',
        'moead;spg;rbm_rcm_brm_bcpm_wri;ac;rrm;100;50;100',
        'nsgaii;sq_bpg_50x50_tel_bgp_strict_pr;rbm_rcm_brm_bcpm_nrii;ppc;brm;300;100;10',
        'nsgaii;sq_bpg;rbm_rcm_brm_bcpm_nrii;ppc;rrm;120;90;50',
        'nsgaii;sq_bpg_50x50_tel_bgp_strict_pr;rbm_rcm_brm_bcpm_nrii;ppc;rrm;100;50;50',
    ]
    
    base_combination = 'nsgaii;spg;rbm_rcm_brm_bcpm_wri;ac;rrm;100;50;100' # nsgaiiBaseline = ["nsgaii", "spg", "rbm_rcm_brm_bcpm_wri", "ac", "rrm", 100, 0.5, 1.0]

    samples = ["Dubendorf", "Meilen", "Volketswil", "Bassersdorf", "Oberglatt", "Pfaffikon", "Bulach",
                             "Nurensdorf", "Fehraltorf", "Rumlang", "Wetzikon (ZH)", "Hedingen", "Uster",
                             "four_muni_FPUV"]

    results_dir = 'tests_results\\100000_n_pop\\1737136140_fianl_tests'

    summary_dir = 'summaries_results\\FS_FinalTests_19-01-2025'

    measures = ['igd', 'hv']


    (_,
        _,
        _, _,
        seeds,
        _,
        _, _, _, _) = get_final_tests_config()

    significance_results_path = 'summaries_results\\FS_FinalTests_19-01-2025\\final_significance_tests.csv'

    return analysed_combinations, base_combination, samples, measures, results_dir, summary_dir, seeds, significance_results_path


def get_initial_tests_base_and_crossovers_significance_test_config():
    analysed_combinations = [
        [
            'moead_nt_combined;moead;spg;rbm_rcm_brm_bcpm_wri;ac;brm',
            'moead_nt_combined;moead;spg;rbm_rcm_brm_bcpm_wri;spc;brm',
            'moead_nt_combined;moead;spg;rbm_rcm_brm_bcpm_wri;ppc;brm',
            'moead_nt_combined;moead;spg;rbm_rcm_brm_bcpm_wri;ppc_fuo;brm'
        ],
        [
            'nsgaii_nt_combined;nsgaii;spg;rbm_rcm_brm_bcpm_wri;ac;brm',
            'nsgaii_nt_combined;nsgaii;spg;rbm_rcm_brm_bcpm_wri;spc;brm',
            'nsgaii_nt_combined;nsgaii;spg;rbm_rcm_brm_bcpm_wri;ppc;brm',
            'nsgaii_nt_combined;nsgaii;spg;rbm_rcm_brm_bcpm_wri;ppc_fuo;brm'
        ],
        [
            '1736640671_baseline;moead;spg;rbm_rcm_brm_bcpm_wri;ac;brm',
            '1736640671_baseline;nsgaii;spg;rbm_rcm_brm_bcpm_wri;ac;brm'
        ]
    ]

    base_combination = '1736640671_baseline;nsgaii;spg;rbm_rcm_brm_bcpm_wri;ac;brm'

    dataSourceDir = [
        'tests_results\\100000_100\\moead_nt_combined',
        'tests_results\\100000_100\\nsgaii_nt_combined',
        'tests_results\\100000_100\\1736640671_baseline'
    ]

    samples = ["Hedingen", "Uster", "four_muni_FPUV"]

    summary_dir = 'summaries_results\\FS_InitialTests_19-01-2025'

    measures = ['igd', 'hv']

    (_,
     _,
     _, _,
     seeds,
     _,
     _, _, _, _) = get_final_tests_config()

    significance_results_path = 'summaries_results\\FS_InitialTests_19-01-2025\\initial_crossovers_significance_tests.csv'

    return analysed_combinations, base_combination, samples, measures, dataSourceDir, summary_dir, seeds, significance_results_path
