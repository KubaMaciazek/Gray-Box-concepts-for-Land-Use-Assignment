# Gray-Box-concepts-for-Land-Use-Assignment

Following repository contains materials regarding paper *Seeking and leveraging alternative variable dependency concepts in gray-box-elusive bimodal land-use allocation problems* by Jakub Maciążek, Michal W. Przewozniczek and Jonas Schwaab, published at GECCO 2025 conference.  
Full paper is available at **ADD_PAPER_WEBSITE_LINK**.

## Repository content

- publication
    - data/data_gemeinde_zuerich - __samples used in research__. All are based on real life data from canton of Zuerich, Switzerland. Each sample consists of 3 files, which can be previewed with [QGIS software](https://qgis.org):
        - areal_4_09.tif - land use map of given region represented as matrix of number corresponding to categories under consideration (1 - urban, 2 - agricultural, 3 - forest, 4 - lakes and rivers). Each square represents area of 100m by 100m.
        - areal_4_09_majfilter.tif - simplified land use land cover representation
        - sq.tif - Soil quality in given area, represented by a matrix of integer values. Higher value coresponds with higher fertility of given 100m by 100m section.
    - operators - implementation of __operators used in research__. Operators presented in the paper can be found under different, more concise name. Those are:
        - SP-I : SPG
        - SQ-I : SQ_BPG
        - TEL-I : TEL_BPG_STRICT
        - HYB-I : BPG_SQ_TEL_PP
        - HAL-I : SQ_BPG_50x50_TEL_BGP_STRICT_PR
        - MutC : RBM_RCM_BRM_BCPM_WRI
        - MutC2 : RBM_RCM_BRM_BCPM_NRII
        - SRC : SPC
        - DRC : PPC
        - IDRC : PPC_FUO
    - algorithyms - implementation of a single run optimization of MOEA/D and NSGAII, iteration and evaluation number based.
    - summary - calculation of True Pareto Front and Inverted Generational Distance
    - tunning - tunning functions and results of mutpb and cxpb parameters tunning
    - tests_results - single optimization results for each test run.
    - summaries_results - summarized tests statistics calculated based on tests_results
    - common, general_test, objective_functions, plotting, significqnce_tests, statistics - utility purposes
    - __*SCRIPTS*__ - starting point of tests, tunning and other operations

## Execution scripts

General tests:
- run_general_tests_baseline.py - run tests for configuration reflecting baseline setup
- run_general_tests_seed_threaded.py - run tests for all possible configurations of operators with base parameters and NSGAII selection mechanism
- run_general_tests_seed_threaded_moead.py - run tests for all possible configurations of operators with base parameters and MOEAD selection mechanism

Tunning:
- run_tunning.py - run tunning for NSGAII
- run_tunning_moead.py - run tunning for MOEAD

Final tests for tunned best:
- run_tests_for_tunned_best.py - for NSGAII
- run_tests_for_tunned_best_moead.py - for MOEAD

## Technologies required to run code:
- [Python ^3](https://www.python.org/downloads/)
- [GDAL](https://pypi.org/project/GDAL/)
- [DEAP](https://deap.readthedocs.io/en/master/)
