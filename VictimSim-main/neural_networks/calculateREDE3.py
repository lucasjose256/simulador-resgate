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

# Load your CSV data
csv_path = r"C:\Users\Rodrigo\PycharmProjects\simulador-resgate\VictimSim-main\neural_networks\sinais_vitais_teste.txt"
df = pd.read_csv(csv_path)

# Extract relevant columns (4th, 5th, 6th)
X_train = df.iloc[:, 3:6].values

# Create an instance of GravidadeCalculator
calculator = GravidadeCalculator('gravidade_model_rede3.h5')

# Train the scaler
calculator.train_scaler(X_train)

# Apply the formula to the DataFrame
result_df = calculator.apply_formula_to_dataframe(df)

# Save the updated DataFrame to a new CSV file
result_df.to_csv('updated_dataset.csv', index=False)
