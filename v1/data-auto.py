import pandas as pd

# Function to filter the dataset
def data_auto(data):
    return data[['Name', 'License State', 'License Type']]

# Main script
def main(input_file, output_file):
    # Read the Excel file
    data = pd.read_excel(input_file)

    # Filter the dataset
    filtered_data = data_auto(data)

    # Save the filtered data back to Excel
    filtered_data.to_excel(output_file, index=False)
    print(f"Filtered data saved to {output_file}")

# Example usage
input_file = 'Dataset.xlsx'  # Replace with your input file name
output_file = 'filtered_data.xlsx'  # Replace with your desired output file name
main(input_file, output_file)
