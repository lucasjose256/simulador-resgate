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
        # Standardize input data
        input_data = self.scaler.transform(np.array([input_data]))
        # Predict gravidade using the trained model
        gravidade = self.model.predict(input_data)[0][0]
        return gravidade

    def apply_formula_to_csv(self, csv_path):
        df = pd.read_csv(csv_path)
        mat =[4050]
        i = 0
        for index, row in df.iterrows():
            if np.isclose(row.iloc[6], 0.0, atol=1e-8):  # Use the position instead of column name
                # Extract input features
                input_data = np.array([row.iloc[3], row.iloc[4], row.iloc[5]])  # Use positions
                # Calculate gravidade
                gravidade = self.calculate_gravidade(input_data)
                # Update the 'gravidade' column
                df.at[index, df.columns[6]] = gravidade  # Use the position of 'gravidade' column
                #mat[i] = gravidade
                i += 1

        # Save the updated CSV
        df.to_csv('updated_data.csv', index=False)
        df_save = df[6]
        df_save.to_csv('LucasBarszcz.csv', header=None, index=False)
        #df.columns[6].to_csv('LucasBarszcz.csv', index=False)

# Load your CSV data
csv_path = r"/Users/lucasbarszcz/PycharmProjects/simulador-resgate/VictimSim-main/neural_networks/datasetCompare.csv"  # Replace with the actual path to your CSV file
df = pd.read_csv(csv_path)

# Extract relevant columns (4th, 5th, 6th)
X_train = df.iloc[:, 3:6].values

# Create an instance of the GravidadeCalculator
calculator = GravidadeCalculator('gravidade_model_cross_val.h5')

# Train the scaler
calculator.train_scaler(X_train)

# Apply the formula to the CSV file
calculator.apply_formula_to_csv(r'/Users/lucasbarszcz/PycharmProjects/simulador-resgate/VictimSim-main/neural_networks/datasetCompare.csv')
