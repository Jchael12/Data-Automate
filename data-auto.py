import pandas as pd

def data_auto(data, checker_lists):
    # Normalize case for comparison
    data['License'] = (data['License State'] + ' ' + data['License Type']).str.lower()
    
    # Combine all checker lists into one set
    checker_set = set()
    for checker_list in checker_lists:
        checker_set.update(license.lower() for license in checker_list)
    
    # Initialize the Result column
    data['Result'] = 'MISSING'
    
    # Update Result for licenses found in the checker set
    data.loc[data['License'].isin(checker_set), 'Result'] = 'ACTIVE'
    
    # Identify licenses in the dataset but not in the checker list
    dataset_set = set(data['License'])
    missing_from_checker = dataset_set - checker_set
    
    # Identify licenses in the checker list but not in the dataset
    missing_from_dataset = checker_set - dataset_set
    
    # Create DataFrame for missing licenses from checker
    missing_checker_data = pd.DataFrame(list(missing_from_checker), columns=['License'])
    missing_checker_data['Result'] = 'MISSING (Dataset)'
    missing_checker_data[['License State', 'License Type']] = missing_checker_data['License'].str.split(' ', 1, expand=True)
    
    # Create DataFrame for missing licenses from dataset
    missing_dataset_data = pd.DataFrame(list(missing_from_dataset), columns=['License'])
    missing_dataset_data['Result'] = 'MISSING (Checker)'
    missing_dataset_data[['License State', 'License Type']] = missing_dataset_data['License'].str.split(' ', 1, expand=True)
    
    # Drop the auxiliary lower-case column and keep original case for License
    final_data = data[['License State', 'License Type', 'Result']]
    final_data['License'] = final_data['License State'] + ' ' + final_data['License Type']
    final_data = final_data[['License', 'Result']]
    
    # Append the missing licenses to the final data
    missing_checker_data['License'] = missing_checker_data['License State'] + ' ' + missing_checker_data['License Type']
    missing_checker_data = missing_checker_data[['License', 'Result']]
    
    missing_dataset_data['License'] = missing_dataset_data['License State'] + ' ' + missing_dataset_data['License Type']
    missing_dataset_data = missing_dataset_data[['License', 'Result']]
    
    final_data = pd.concat([final_data, missing_checker_data, missing_dataset_data], ignore_index=True)
    
    return final_data

def main(input_file, checker_files, output_file):
    # Read the dataset file
    data = pd.read_excel(input_file)
    
    # Read and combine all checker files
    checker_lists = []
    for checker_file in checker_files:
        checker_df = pd.read_excel(checker_file, header=None)
        checker_list = checker_df.iloc[:, 0].dropna().tolist()
        checker_lists.append(checker_list)
    
    # Validate and create the final output
    updated_data = data_auto(data, checker_lists)
    
    # Save the updated data back to Excel
    updated_data.to_excel(output_file, index=False)
    print(f"Updated data saved to {output_file}")

# Example usage
input_file = 'oceo.xlsx'  # Replace with your dataset file name
checker_files = [
    #'fraud_checker.xlsx'
     '51pc_checker.xlsx',
    # 'ASG_checker.xlsx',
    # '37pc_checker.xlsx',
    # 'RAM_NL_checker.xlsx'
]  # Replace with the paths to your checker data files
output_file = 'updated_data.xlsx'  # Replace with your desired output file name
main(input_file, checker_files, output_file)
