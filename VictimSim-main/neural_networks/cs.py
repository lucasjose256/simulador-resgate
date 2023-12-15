import pandas as pd

class CSVColumnExtractor:
    def __init__(self, csv_path, output_csv_path='gravidades.csv'):
        self.csv_path = csv_path
        self.output_csv_path = output_csv_path

    def extract_6th_column(self):
        df = pd.read_csv(self.csv_path)

        column_6 = df.iloc[:, 6]

        result_df = pd.DataFrame({'6th_column': column_6})

        result_df.to_csv(self.output_csv_path, index=False)

csv_path = str(input("Digite o nome do arquivo para o extrair as gravidades: "))
extractor = CSVColumnExtractor(csv_path)
extractor.extract_6th_column()
