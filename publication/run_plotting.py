from publication.plotting.plot_final_pfs import plot_final_pfs
from publication.plotting.plot_initial_crossovers_pfs import plot_initial_crossovers_pf
from publication.plotting.plotting_configs import get_final_combinations_plotting_config, \
    get_initial_crossovers_plotting_config


def run_plotting():
    # PLot final PFS
    plotTitle, sample, combinations, seed, dataSourceDir, resultsDestinationDir = get_final_combinations_plotting_config()
    plot_final_pfs(plotTitle, sample, combinations, seed, dataSourceDir, resultsDestinationDir)

    # Plot initial crossovers and baselines pfs
    plotTitle, sample, combinations, seed, dataSourceDir, resultsDestinationDir = get_initial_crossovers_plotting_config()
    plot_initial_crossovers_pf(plotTitle, sample, combinations, seed, dataSourceDir, resultsDestinationDir)

run_plotting()
