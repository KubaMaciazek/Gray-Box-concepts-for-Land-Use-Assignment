import os
import csv

def rank_param_combos_by_avg_hv(input_folder, output_file):
    """
    Reads all .txt files from 'input_folder'. Each file has columns:
      filename;alg;init;mut;cross;repair;n_pop;cxpb;mutpb;min_hv;avg_hv;median_hv;max_hv;std_hv
    Creates a CSV 'output_file' where:
      - The first column is the concatenation of (alg|init|mut|cross|repair|n_pop|cxpb|mutpb)
        using the pipe character '|'.
      - The subsequent columns (one per input file) are named '<basename>_RHV' (basename = file without .txt).
      - Each cell shows the rank of that combo by avg_hv in the corresponding file (1 = highest, 2 = next, etc.).
    """

    # Gather all .txt files from the folder
    files = [f for f in os.listdir(input_folder) if f.endswith('.txt')]
    # Sort files for consistent column order (optional)
    files.sort()

    # We will store the rank information in a dictionary:
    #     rank_by_file[file_name][param_combo] = rank
    rank_by_file = {}

    # A helper dict to map original filenames -> "basename_RHV"
    # e.g. "test1.txt" -> "test1_RHV"
    file_column_map = {}

    # 1) Read each file, parse and sort by avg_hv
    for file_name in files:
        file_path = os.path.join(input_folder, file_name)

        # Derive the column name, e.g. "myfile.txt" -> "myfile_RHV"
        base_name = os.path.splitext(file_name)[0]  # e.g. "myfile"
        col_name = f"{base_name}_RHV"
        file_column_map[file_name] = col_name

        combos_in_file = []

        with open(file_path, 'r', newline='', encoding='utf-8') as f_in:
            reader = csv.DictReader(f_in, delimiter=';')

            for row in reader:
                # Build the param_combo with '|'
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

                # Convert avg_hv to float for sorting
                avg_hv = float(row['avg_hv']) if row['avg_hv'] else 0.0
                combos_in_file.append((param_combo, avg_hv))

        # Sort combos by avg_hv (descending: highest first)
        combos_in_file.sort(key=lambda x: x[1], reverse=True)

        # Assign ranks (1 = highest avg_hv)
        rank_dict = {}
        current_rank = 1
        for combo, _ in combos_in_file:
            if combo not in rank_dict:  # in case of duplicates
                rank_dict[combo] = current_rank
                current_rank += 1

        # Store the rank info in the master dictionary
        rank_by_file[file_name] = rank_dict

    # 2) Collect all unique param_combos across *all* files
    all_combos = set()
    for f in files:
        all_combos.update(rank_by_file[f].keys())
    all_combos = sorted(all_combos)

    # 3) Write the output CSV with ';' as delimiter
    with open(output_file, 'w', newline='', encoding='utf-8') as out_csv:
        writer = csv.writer(out_csv, delimiter=';')

        # Header row: "param_combo" + <basename>_RHV for each file
        header = ["param_combo"] + [file_column_map[f] for f in files]
        writer.writerow(header)

        # Each row corresponds to one param_combo
        for combo in all_combos:
            # Build row: param_combo + ranks from each file
            ranks_for_combo = []
            for f in files:
                rank = rank_by_file[f].get(combo, "")
                ranks_for_combo.append(rank)
            row = [combo] + ranks_for_combo
            writer.writerow(row)

    print(f"Output written to {output_file}")


# --- Example usage ---
if __name__ == "__main__":
    folder_with_txt_files = "summaries_results/FS_FinalTests_19-01-2025/hvs_summary"
    output_csv_file =       "summaries_results/FS_FinalTests_19-01-2025/hvs_summary/hvs_ranks.csv"
    rank_param_combos_by_avg_hv(folder_with_txt_files, output_csv_file)
