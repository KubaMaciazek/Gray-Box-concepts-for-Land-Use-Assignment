import os

# STATS_PATH = 'summaries_results\Final_Summary_19-11-2024'
# TPFS_STATS_PATH = os.path.join(STATS_PATH, 'tpfs')


def save_tpf(sample, tpf, summary_path):
    TPFS_STATS_PATH = os.path.join(summary_path, 'tpfs')

    os.makedirs(TPFS_STATS_PATH, exist_ok=True)
    final_path = os.path.join(TPFS_STATS_PATH, sample + '.txt')

    with open(final_path, 'w') as file:
        file.write(f"{tpf['hv']}\n")

        for point in tpf['pf']:
            line = ' '.join(map(str, point)) + '\n'
            file.write(line)
