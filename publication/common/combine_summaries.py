import os
import csv


def combine_csv_files(input_folder, output_file):
    # Get all files in the folder
    files = [f for f in os.listdir(input_folder) if f.endswith('.txt')]

    # Open the output file in write mode
    with open(output_file, 'w', newline='') as output_csv:
        csv_writer = csv.writer(output_csv, delimiter=';')

        # Flag to check if the header has been written
        header_written = False

        # Loop through all files
        for file in files:
            file_path = os.path.join(input_folder, file)

            with open(file_path, 'r') as input_csv:
                csv_reader = csv.reader(input_csv, delimiter=';')

                # Read the header (first line)
                header = next(csv_reader)

                # If the header hasn't been written yet, write it to the output file
                if not header_written:
                    # Add the new column for the filename in the header
                    csv_writer.writerow(['filename'] + header)  # Add 'filename' as the first column in header
                    header_written = True

                # Write the rows from this file, adding the filename as the first column
                for row in csv_reader:
                    csv_writer.writerow([file] + row)  # Add the filename as the first element of the row

    print(f"All files have been combined into {output_file}.")


# # Test usage:
# # sample = 'Hedingen'
# # sample = 'Uster'
# # sample = 'four_muni_FPUV'
# input_folder = f'publication/summaries_results/Final_Summary_12-01-2025/hvs_summary/{sample}'  # Folder containing the CSV files
# output_file = f'publication/summaries_results/Final_Summary_12-01-2025/hvs_summary/{sample}_FS_12-01-2025.csv'  # Name of the output combined file
#
# combine_csv_files(input_folder, output_file)


# # ------------------- FS_FinalTests_19-01-2025 19.01.2025----------------------------------
# samples = ["Dubendorf", "Meilen", "Volketswil", "Bassersdorf", "Oberglatt", "Pfaffikon", "Bulach", "Nurensdorf", "Fehraltorf", "Rumlang", "Wetzikon (ZH)", "Hedingen", "Uster", "four_muni_FPUV"]
# for sample in samples:
#     input_folder = f'summaries_results/FS_FinalTests_19-01-2025/hvs_summary/{sample}'  # Folder containing the CSV files
#     output_file = f'summaries_results/FS_FinalTests_19-01-2025/hvs_summary/{sample}.txt'  # Name of the output combined file
#     combine_csv_files(input_folder, output_file)

# # ------------------- FS_AfterTunningTests_19-01-2025 19.01.2025----------------------------------
# samples = ["Hedingen", "Uster", "four_muni_FPUV"]
# for sample in samples:
#     input_folder = f'summaries_results/FS_AfterTunningTests_19-01-2025/hvs_summary/{sample}'  # Folder containing the CSV files
#     output_file = f'summaries_results/FS_AfterTunningTests_19-01-2025/hvs_summary/{sample}.txt'  # Name of the output combined file
#     combine_csv_files(input_folder, output_file)

# # ------------------- FS_InitialTests_19-01-2025 19.01.2025----------------------------------
# samples = ["Hedingen", "Uster", "four_muni_FPUV"]
# for sample in samples:
#     input_folder = f'summaries_results/FS_InitialTests_19-01-2025/hvs_summary/{sample}'  # Folder containing the CSV files
#     output_file = f'summaries_results/FS_InitialTests_19-01-2025/hvs_summary/{sample}.txt'  # Name of the output combined file
#     combine_csv_files(input_folder, output_file)
