import csv
import os

def read_config(config_file): #Extract source and destination files for comparision and store as dictionary
    config_data = []
    with open(config_file, 'r', newline='') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            config_data.append({
                'sl_no': row[0],
                'source_file': row[1],
                'destination_file': row[2]
            })
    return config_data

def compare_csv(source_file, destination_file, differences):
    count = 0
    with open(source_file, 'r', newline='') as source_csv, \
            open(destination_file, 'r', newline='') as destination_csv:
        source_reader = csv.reader(source_csv)
        destination_reader = csv.reader(destination_csv)
        
        for row_num, (source_row, destination_row) in enumerate(zip(source_reader, destination_reader), start=1):
            for i, (source_value, destination_value) in enumerate(zip(source_row, destination_row)):
                if source_value != destination_value:
                    differences.append([f'Row {row_num}', f'Column {i+1}', source_value, destination_value])
                    count += 1
    return count

def generate_comparison_result(config_data):
    results = []
    for config_entry in config_data:
        sl_no = config_entry['sl_no']
        source_file = config_entry['source_file']
        destination_file = config_entry['destination_file']
        differences = []
        count = compare_csv(source_file, destination_file, differences)
        result = 'Pass' if count == 0 else 'Failed'
        results.append([sl_no, source_file, destination_file, result, count])
    return results

def main(config_file):
    config_data = read_config(config_file)
    current_directory = os.getcwd()
    
    # Generate differences report
    all_differences = []
    for config_entry in config_data:
        sl_no = config_entry['sl_no']
        source_file = config_entry['source_file']
        destination_file = config_entry['destination_file']
        compare_csv(source_file, destination_file, all_differences)

    # Write all differences to a single report file
    differences_report_path = os.path.join(current_directory, 'all_differences_report.csv')
    with open(differences_report_path, 'w', newline='') as report:
        report_writer = csv.writer(report)
        report_writer.writerow(['Row', 'Column', 'Source Value', 'Destination Value'])
        report_writer.writerows(all_differences)
        
    # Generate comparison result report
    comparison_result = generate_comparison_result(config_data)
    comparison_result_report_path = os.path.join(current_directory, 'comparison_result_report.csv')
    with open(comparison_result_report_path, 'w', newline='') as result_report:
        result_writer = csv.writer(result_report)
        result_writer.writerow(['Sl No', 'Source File', 'Destination File', 'Result', 'Count'])
        result_writer.writerows(comparison_result)

if __name__ == "__main__":
    main("D:/pythonWorkspace/CSV_files/CSV_compare_config.csv")
