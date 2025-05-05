import os

from publication.statistics.load_results import load_results
from publication.summary.igds.get_sample_igd_file import get_sample_igd_file
from publication.summary.igds.my_igd import my_igd
from publication.summary.tpfs.load_tpf import load_tpf_sampla


def calculate_igds_by_run(analyzed_tests_paths, sample, summary_path):
    sample_igd_file_path = get_sample_igd_file(sample, summary_path)
    _, sample_tpf = load_tpf_sampla(sample, summary_path)

    with open(sample_igd_file_path, 'w') as igd_file:
        # calculate_igd_by_run(test_result_sample_root_path, sample, combinations, igd_file, sample_tpf)

        for test_path in analyzed_tests_paths:
            test = test_path.split('\\')[-1]
            test_sample_path = os.path.join(test_path, sample)
            combinations = [d for d in os.listdir(test_sample_path) if os.path.isdir(os.path.join(test_sample_path, d))]

            for combination in combinations:
                # sample combination path
                scp = os.path.join(test_sample_path, combination)
                # sample combination seeds results
                scsr = []
                for seedfile in os.listdir(scp):
                    scsr.append(load_results(os.path.join(scp, seedfile)))

                combination_igds = []
                for result in scsr:
                    apf = result['pfs'][-1]
                    # print(apf)
                    apf = [tuple(map(float, values)) for values in apf]
                    # apf = np.array(apf)
                    # apf = np.transpose(apf)
                    # print(apf)
                    # igd = indicator(apf)
                    igd = my_igd(apf, sample_tpf)
                    # print(igd)
                    combination_igds.append(float(igd))

                # print(combination_igds)
                igd_file.write(test + ';' + combination + ';' + ';'.join(map(str, combination_igds)) + '\n')
