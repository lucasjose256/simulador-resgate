import pandas as pd

class CSVColumnExtractor:
    def __init__(self, csv_path, output_csv_path='extracted_column.csv'):
        self.csv_path = csv_path
        self.output_csv_path = output_csv_path

    def extract_6th_column(self):
        # Read the CSV file
        df = pd.read_csv(self.csv_path)

        # Extract the 6th column
        column_6 = df.iloc[:, 6]

        # Create a new DataFrame with only the 6th column
        result_df = pd.DataFrame({'6th_column': column_6})

        # Save the extracted column to a new CSV file
        result_df.to_csv(self.output_csv_path, index=False)

# Example usage:
csv_path = r"C:\Users\Rodrigo\PycharmProjects\simulador-resgate\VictimSim-main\neural_networks\rede1resultado.csv"  # Replace with the actual path to your CSV file
extractor = CSVColumnExtractor(csv_path)
extractor.extract_6th_column()
