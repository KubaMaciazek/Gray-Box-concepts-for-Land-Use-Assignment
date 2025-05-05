import os

# STATS_PATH = 'summaries_results/Final_Summary_19-11-2024'
# STATS_PATH = 'summaries_results/Final_Summary_12-01-2025'
# igds_by_run_path = os.path.join(STATS_PATH, 'igds_by_run')


def get_sample_igd_file(sample, summary_path):
    igds_by_run_path = os.path.join(summary_path, 'igds_by_run')
    os.makedirs(igds_by_run_path, exist_ok=True)
    final_path = os.path.join(igds_by_run_path, sample + '.txt')
    return final_path
