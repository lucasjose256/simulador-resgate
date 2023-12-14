import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from keras.models import load_model

class Calculate:
    def __init__(self, model_path, scaler):
        self.model = load_model(model_path)
        self.scaler = scaler

    def calculate_gravidade(self, input_data):
        # Standardize input data
        input_data = self.scaler.transform(np.array([input_data]))
        # Predict using the trained model
        gravidade = self.model.predict(input_data)[0][0]
        return gravidade

    def apply_formula_to_csv(self, csv_path, output_csv_path='rede3resultado.csv'):
        df = pd.read_csv(csv_path)

        # Extract relevant columns (4th, 5th, 6th)
        input_data = df.iloc[:, 3:6].values

        # Standardize input data using the trained scaler
        input_data_standardized = self.scaler.transform(input_data)

        # Predict gravidade using the trained model
        gravidade_predictions = self.model.predict(input_data_standardized)

        # Update the 'gravidade' column in the DataFrame
        df['gravidade'] = gravidade_predictions

        # Save the updated CSV
        df.to_csv(output_csv_path, index=False)

# Load your CSV data
csv_path = r"C:\Users\Rodrigo\PycharmProjects\simulador-resgate\VictimSim-main\neural_networks\sinais_vitais_teste.txt"
df = pd.read_csv(csv_path)

# Extract relevant columns (4th, 5th, 6th)
X_train = df.iloc[:, 3:6].values

# Create an instance of StandardScaler and train it on your data
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)

# Create an instance of the Calculate class
calculator = Calculate('gravidade_model_rede3.h5', scaler)

# Apply the formula to the CSV file and save the updated CSV
calculator.apply_formula_to_csv(csv_path, output_csv_path='C:\Users\Rodrigo\PycharmProjects\simulador-resgate\VictimSim-main\neural_networks\sinais_vitais_teste.txt')
