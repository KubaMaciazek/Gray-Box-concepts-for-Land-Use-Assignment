import os
import shutil

def copy_and_rename_folders(src_folder, dest_folder, suffix):
    """
    Copy the contents of src_folder to dest_folder and rename the subfolders based on suffix.
    """
    for root, dirs, files in os.walk(src_folder):
        # Determine the subfolder structure
        subfolder_structure = os.path.relpath(root, src_folder)

        # Modify the folder name based on the suffix (wri/nrii)
        new_folder_name = subfolder_structure.replace('rbm_rcm_brm_bcpm', f'rbm_rcm_brm_bcpm_{suffix}')

        # Create the destination path
        dest_subfolder_path = os.path.join(dest_folder, new_folder_name)

        # Create the new subfolder structure in the destination folder if it doesn't exist
        os.makedirs(dest_subfolder_path, exist_ok=True)

        # Copy all files from the current folder to the destination
        for file in files:
            src_file = os.path.join(root, file)
            dest_file = os.path.join(dest_subfolder_path, file)
            shutil.copy(src_file, dest_file)
            print(f"Copied {src_file} to {dest_file}")

def combine_folders():
    # Define the source and destination folders
    path = 'publication/tests_results/100000_100/'
    folder1 = path + '1724932224_nsgaii_nt_wr'
    folder2 = path + '1725000833_nsgaii_nt_nr_2055_end'
    combined_folder = path + 'nsgaii_nt_combined'

    # Ensure the combined folder exists
    os.makedirs(combined_folder, exist_ok=True)

    # Copy and rename folders from the first source folder, appending 'wri'
    copy_and_rename_folders(folder1, combined_folder, 'wri')

    # Copy and rename folders from the second source folder, appending 'nrii'
    copy_and_rename_folders(folder2, combined_folder, 'nrii')

# Call the combine_folders function to start the process
combine_folders()
