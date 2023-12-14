import csv

def substitute_column(file_path, column_index, substitution_value):
    # Read the CSV file
    with open(file_path, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        rows = list(reader)

    # Modify the 7th column in each row
    for row in rows:
        if len(row) > column_index:
            row[column_index] = substitution_value

    # Write the modified data back to the CSV file
    with open(file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(rows)

# Replace 'your_file.csv' with the actual file path
file_path = r'C:\Users\Rodrigo\PycharmProjects\simulador-resgate\VictimSim-main\neural_networks\rede1resultado.csv'

# Specify the column index (0-based) and the substitution value
column_index_to_substitute = 6  # 7th column (0-based index)
substitution_value = '0.0'

# Call the function
substitute_column(file_path, column_index_to_substitute, substitution_value)
