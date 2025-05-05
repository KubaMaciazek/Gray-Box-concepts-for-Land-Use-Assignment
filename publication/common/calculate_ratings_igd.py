import os
import csv
import os.path

def rank_param_combos_by_avg_igd(input_folder, output_file):
    """
    Reads all .txt files from 'input_folder'. Each file has columns like:
      filename;alg;init;mut;cross;repair;n_pop;cxpb;mutpb;min_igd;avg_igd;median_igd;max_igd;std_igd
    Creates a CSV 'output_file' where:
      - The first column is the concatenation of (alg|init|mut|cross|repair|n_pop|cxpb|mutpb)
        using the pipe character '|'.
      - The subsequent columns (one per .txt file) are named '<basename>_IGDR', where <basename>
        is the file name without '.txt'.
      - Each cell shows the rank of that combo by 'avg_igd' in the corresponding file
        (1 = best/lowest IGD, 2 = next, etc.).
    """

    # Gather all .txt files from the folder
    files = [f for f in os.listdir(input_folder) if f.endswith('.txt')]
    # (Optional) Sort files for consistent column order
    files.sort()

    # Dictionary to store rank info, by file:
    # rank_by_file[file_name][param_combo] = rank
    rank_by_file = {}

    # A helper map: original filename -> "basename_IGDR"
    # e.g. "example.txt" -> "example_IGDR"
    file_column_map = {}

    # 1) Read each file, parse rows, sort by avg_igd (ascending, because smaller IGD is better)
    for file_name in files:
        file_path = os.path.join(input_folder, file_name)

        # Build the column name (e.g. "example_IGDR")
        base_name = os.path.splitext(file_name)[0]
        col_name = f"{base_name}_IGDR"
        file_column_map[file_name] = col_name

        combos_in_file = []
        with open(file_path, 'r', newline='', encoding='utf-8') as f_in:
            # Read using DictReader with delimiter=';'
            reader = csv.DictReader(f_in, delimiter=';')

            for row in reader:
                # Build the param_combo using '|'
                param_combo = "|".join([
                    row['alg'],
                    row['init'],
                    row['mut'],
                    row['cross'],
                    row['repair'],
                    row['n_pop'],
                    row['cxpb'],
                    row['mutpb']
                ])

                # Parse avg_igd as float for sorting (default to 0.0 if missing or invalid)
                try:
                    avg_igd = float(row['avg_igd'])
                except (ValueError, KeyError):
                    avg_igd = 0.0

                combos_in_file.append((param_combo, avg_igd))

        # Sort by avg_igd in ascending order (lowest = best)
        combos_in_file.sort(key=lambda x: x[1], reverse=False)

        # Assign ranks (1 = lowest avg_igd)
        rank_dict = {}
        current_rank = 1
        for combo, _ in combos_in_file:
            # Only assign if not already present (in case of duplicates)
            if combo not in rank_dict:
                rank_dict[combo] = current_rank
                current_rank += 1

        # Store the rank dictionary for this file
        rank_by_file[file_name] = rank_dict

    # 2) Collect all unique param_combos across *all* files
    all_combos = set()
    for f in files:
        all_combos.update(rank_by_file[f].keys())

    # Sort combos alphabetically for a consistent row order
    all_combos = sorted(all_combos)

    # 3) Write the output CSV with ';' as the delimiter
    with open(output_file, 'w', newline='', encoding='utf-8') as out_csv:
        writer = csv.writer(out_csv, delimiter=';')

        # Header row: param_combo + one column per file, named <basename>_IGDR
        header = ["param_combo"] + [file_column_map[f] for f in files]
        writer.writerow(header)

        # Each row corresponds to one param_combo
        for combo in all_combos:
            ranks_for_combo = []
            for f in files:
                rank = rank_by_file[f].get(combo, "")
                ranks_for_combo.append(rank)
            row = [combo] + ranks_for_combo
            writer.writerow(row)

    print(f"Done! Output written to: {output_file}")


# Example usage
if __name__ == "__main__":
    folder_with_txt_files = "summaries_results/FS_FinalTests_19-01-2025/igds_summary"
    output_csv_file =       "summaries_results/FS_FinalTests_19-01-2025/igds_summary/igds_ranks.csv"
rank_param_combos_by_avg_igd(folder_with_txt_files, output_csv_file)
