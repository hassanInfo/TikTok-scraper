import os
import pandas as pd

def merge_csv_files(input_dir, output_file):
    """
    Merge multiple CSV files from a directory into a single CSV file.

    Parameters:
    - input_dir (str): Path to the directory containing CSV files.
    - output_file (str): Path to the output CSV file.
    """
    # Get a list of CSV files in the input directory
    csv_files = [file for file in os.listdir(input_dir) if file.endswith('.csv')]

    # Check if there are any CSV files in the directory
    if not csv_files:
        print("No CSV files found in the specified directory.")
        return

    # Initialize an empty DataFrame to store the merged data
    merged_df = pd.DataFrame()

    # Read each CSV file and append its contents to the merged DataFrame
    for csv_file in csv_files:
        file_path = os.path.join(input_dir, csv_file)
        df = pd.read_csv(file_path)
        merged_df = merged_df.append(df, ignore_index=True)

    # Write the merged DataFrame to a new CSV file
    merged_df.to_csv(output_file, index=False)
    print(f"Merged data saved to {output_file}")