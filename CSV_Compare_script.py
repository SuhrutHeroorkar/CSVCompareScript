import os
import pandas as pd
import csv

def compare_csv_files(source_folder, destination_file):
    source_files = [file for file in os.listdir(source_folder) if file.endswith('.csv')] #get csv files in source folder
    df_destination = pd.read_csv(destination_file) #read destination file data in pandas df
    differences_count = {} #structure to count differences
    for source_file in source_files:
        df_source = pd.read_csv(os.path.join(source_folder, source_file)) #read source file data in pandas df
        diff1 = df_source[~df_source.isin(df_destination)].dropna() #item in source not in destination
        diff2 = df_destination[~df_destination.isin(df_source)].dropna() #item in destination not in source


        differences_count[source_file] = {'Items in Source Not in Destination': len(diff1),
                                          'Items in Destination Not in Source': len(diff2)}

        output_file1 = os.path.join(source_folder, f'differences_{source_file}_source_not_in_destination.csv')
        output_file2 = os.path.join(source_folder, f'differences_{source_file}_destination_not_in_source.csv')
        diff1.to_csv(output_file1, index=False)
        diff2.to_csv(output_file2, index=False)

    summary_file = os.path.join(source_folder, 'comparison_summary.csv') #summary file
    with open(summary_file, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['CSV File', 'Items in Source Not in Destination', 'Items in Destination Not in Source'])
        writer.writeheader()
        for csv_file, diff_count in differences_count.items():
            writer.writerow({'CSV File': csv_file,
                             'Items in Source Not in Destination': diff_count['Items in Source Not in Destination'],
                             'Items in Destination Not in Source': diff_count['Items in Destination Not in Source']})

source_folder = 'D:/pythonWorkspace/CSV_files'
destination_file = "D:/pythonWorkspace/CSV_files/Magnetometer_edit1.csv"

compare_csv_files(source_folder, destination_file)
