import os

import numpy as np
from matplotlib import pyplot as plt

from publication.common.convert_combination_naming_convention import convert_combination_naming_convention
from publication.data.get_community_data import get_community_min_tel_possible, get_community_min_sq_loss_possible
from publication.statistics.load_results import load_results


def plot_final_pfs(plotTitle, sample, combinations, seed, dataSourceDir, resultsDestinationDir):
    """
    Like plot_final_hofs from maciazek/testy/general/plot_general_tests_statistics.py
    """

    # Get: sample name -> sample min sqloss and tel. combinations, seed, results dir, image_destination_dir, plot_title

    # Set colour palette
    cmap = plt.get_cmap('gist_rainbow')

    # Increase the figure size
    plt.figure(figsize=(8, 10))

    # Get final pareto front per combination + add it to plot
    for i, combination in enumerate(combinations):
        # calculate data series colour
        color = cmap(1 - i / len(combinations))

        # Get combination data
        seedfile = os.path.join(dataSourceDir, sample, combination, seed + '.txt')
        result = load_results(seedfile)
        combination_final_pareto_front = result['pfs'][-1]
        sqlX = []
        telY = []
        for point in combination_final_pareto_front:
            sqlX.append(float(point[0]))
            telY.append(float(point[1]))

        # Plot combination pareto front result and min achieved values
        plt.scatter(sqlX, telY, color=color, label=convert_combination_naming_convention(combination))
        plt.axvline(x=(np.min(sqlX)), color=color, linestyle=(0, (3, 5, 1, 5)))
        plt.axhline(y=(np.min(telY)), color=color, linestyle=(0, (3, 5, 1, 5)))

    # Plot Sample minimum possible values, legend and descriptions

    # pmin_sq = get_community_min_sq_loss_possible(sample)
    # pmin_tel = get_community_min_tel_possible(sample)
    # plt.axvline(x=pmin_sq, color='black', linestyle='--')
    # plt.axhline(y=pmin_tel, color='black', linestyle='--')

    plt.xlabel('Absolute soil quality loss')
    plt.ylabel('Total edge length')
    plt.title(plotTitle)

    # # plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, mode="expand", borderaxespad=0.)
    # plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1))
    # plt.tight_layout()
    # # plt.subplots_adjust(bottom=0.2)
    plt.legend(loc='upper right')

    # plt.savefig(RESULTS_PATH + "/" + 'final_pf_comparison___' + name, bbox_inches='tight')  # Save the figure with the legend box fully displayed
    plt.savefig(os.path.join(resultsDestinationDir, 'final_combinations_pfs'), bbox_inches='tight')  # Save the figure with the legend box fully displayed
    plt.show()
    plt.clf()
