import os

# STATS_PATH = 'summaries_results\Final_Summary_19-11-2024'
# TPFS_STATS_PATH = os.path.join(STATS_PATH, 'tpfs')


def load_tpf_sampla(sample, summary_path):
    TPFS_STATS_PATH = os.path.join(summary_path, 'tpfs')

    hv = 0
    tpf = []

    final_path = os.path.join(TPFS_STATS_PATH, sample + '.txt')

    with open(final_path, 'r') as file:
        hv = float(file.readline().strip())

        for line in file:
            values = line.strip().split()
            (x, y) = tuple(map(float, values))
            tpf.append((x, y))

    return hv, tpf
