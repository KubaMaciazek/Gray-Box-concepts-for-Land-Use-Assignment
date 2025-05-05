import numpy as np

file_path = 'tests_results/'


def load_results(seedfile):
    '''
    :param seedfile: file path of specific test_sample_seed experiment
    :return: object with total execution time, list of x'th hvs and list of x'th pfs (in publication, only final ones)
    '''
    result = {}
    total_exec_time = 0
    hvs = []
    pfs = []

    with open(seedfile, 'r') as file:
        total_exec_time = float(file.readline().strip())

        while True:
            line = file.readline().strip()
            if line == '_front_':
                break
            hvs.append(float(line))
            # print(line)

        pf = []
        for line in file:
            values = line.strip().split()
            if len(values) == 1:
                # print(values)
                pfs.append(np.copy(pf))
                pf = []
            else:
                (x, y) = tuple(map(float, values))
                pf.append((x, y))
        pfs.append(np.copy(pf))

    # print(total_exec_time)
    # print(hvs)
    # print(len(pfs[-1]))
    result['total_exec_time'] = total_exec_time
    result['hvs'] = hvs
    result['pfs'] = pfs

    return result
