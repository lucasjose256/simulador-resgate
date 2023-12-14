import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from keras.models import Sequential, load_model

class GravidadeCalculator:
    def __init__(self, model_path):
        self.model = load_model(model_path)
        self.scaler = StandardScaler()

    def train_scaler(self, X_train):
        self.scaler.fit(X_train)

    def calculate_gravidade(self, input_data):

        input_data = self.scaler.transform(np.array([input_data]))

        gravidade = self.model.predict(input_data)[0][0]
        return gravidade

    def apply_formula_to_csv(self, csv_path):
        df = pd.read_csv(csv_path)

        for index, row in df.iterrows():
            if np.isclose(row.iloc[6], 0.0, atol=1e-8):
                input_data = np.array([row.iloc[3], row.iloc[4], row.iloc[5]])
                gravidade = self.calculate_gravidade(input_data)
                df.at[index, df.columns[6]] = gravidade
        df.to_csv('rede2resultado.csv', index=False)


csv_path = r"C:\Users\Rodrigo\PycharmProjects\simulador-resgate\VictimSim-main\neural_networks\sinais_vitais_teste.txt"  # Replace with the actual path to your CSV file
df = pd.read_csv(csv_path)


X_train = df.iloc[:, 3:6].values


calculator = GravidadeCalculator('gravidade_model_rede2.h5')


calculator.train_scaler(X_train)


calculator.apply_formula_to_csv(r'C:\Users\Rodrigo\PycharmProjects\simulador-resgate\VictimSim-main\neural_networks\sinais_vitais_teste.txt')
