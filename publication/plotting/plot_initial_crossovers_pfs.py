import os

import numpy as np
from matplotlib import pyplot as plt

from publication.common.convert_combination_naming_convention import convert_combination_naming_convention
from publication.statistics.load_results import load_results


def plot_initial_crossovers_pf(plotTitle, sample, combinations, seed, dataSourceDir, resultsDestinationDir):
    cmap = plt.get_cmap('gist_rainbow')

    # Increase the figure size
    plt.figure(figsize=(8, 10))

    nrOfCombinations = 0

    for j, sublist in enumerate(combinations):
        for i, combination in enumerate(sublist):
            nrOfCombinations += 1

    doneComb = 0
    for j, sublist in enumerate(combinations):
        for i, combination in enumerate(sublist):
            doneComb += 1
            color = cmap(1 - doneComb / nrOfCombinations)

            seedfile = os.path.join(dataSourceDir[j], sample, combination, seed + '.txt')

            result = load_results(seedfile)
            combination_final_pareto_front = result['pfs'][-1]
            sqlX = []
            telY = []
            for point in combination_final_pareto_front:
                sqlX.append(float(point[0]))
                telY.append(float(point[1]))

            # Plot combination pareto front result and min achieved values
            plt.scatter(sqlX, telY, color=color, label=(convert_combination_naming_convention(combination) + (';100;50;50' if j < 2 else ';100;50;100')))
            plt.axvline(x=(np.min(sqlX)), color=color, linestyle=(0, (3, 5, 1, 5)))
            plt.axhline(y=(np.min(telY)), color=color, linestyle=(0, (3, 5, 1, 5)))

    plt.xlabel('Absolute soil quality loss')
    plt.ylabel('Total edge length')
    plt.title(plotTitle)

    # plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1))
    # plt.tight_layout()
    plt.legend(loc='upper right')

    plt.savefig(os.path.join(resultsDestinationDir, 'initial_crossovers_pfs'), bbox_inches='tight')  # Save the figure with the legend box fully displayed
    plt.show()
    plt.clf()
