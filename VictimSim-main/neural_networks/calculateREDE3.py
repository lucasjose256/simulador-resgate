import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from keras.models import load_model

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

    def apply_formula_to_dataframe(self, df):
        for index, row in df.iterrows():
            input_data = np.array([row.iloc[3], row.iloc[4], row.iloc[5]])
            gravidade = self.calculate_gravidade(input_data)
            df.at[index, df.columns[6]] = gravidade

        return df

csv_path = str(input("Digite o nome do arquivo para o teste: "))
df = pd.read_csv(csv_path)

X_train = df.iloc[:, 3:6].values

calculator = GravidadeCalculator('gravidade_model_rede3.h5')

calculator.train_scaler(X_train)

result_df = calculator.apply_formula_to_dataframe(df)

result_df.to_csv('rede3resultado.csv', index=False)
