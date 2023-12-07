import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from keras.models import Sequential, load_model

class GravidadeCalculator:
    def __init__(self, model_path):
        # Load the trained model
        self.model = load_model(model_path)
        # Initialize the scaler
        self.scaler = StandardScaler()

    def train_scaler(self, X_train):
        # Fit the scaler on the training data
        self.scaler.fit(X_train)

    def calculate_gravidade(self, input_data):
        # Standardize input data
        input_data = self.scaler.transform(np.array([input_data]))
        # Reshape input data for RNN input (batch_size, time_steps, features)
        input_data = input_data.reshape((input_data.shape[0], 1, input_data.shape[1]))
        # Predict gravidade using the trained model
        gravidade = self.model.predict(input_data)[0][0]
        return gravidade

    def apply_formula_to_csv(self, csv_path):
        df = pd.read_csv(csv_path)

        for index, row in df.iterrows():
            if row.iloc[6] == 0.0:  # Use the position instead of column name
                # Extract input features
                input_data = np.array([row.iloc[3], row.iloc[4], row.iloc[5]])  # Use positions
                # Calculate gravidade
                gravidade = self.calculate_gravidade(input_data)
                # Update the 'gravidade' column
                df.at[index, df.columns[6]] = gravidade  # Use the position of 'gravidade' column

        # Save the updated CSV
        df.to_csv('updated_dataRNN.csv', index=False)

# Load your CSV data
csv_path = r"\Users\lucasbarszcz\PycharmProjects\simulador-resgate\VictimSim-main\neural_networks\datasetCompare.csv"  # Replace with the actual path to your CSV file
df = pd.read_csv(csv_path)

# Extract relevant columns (4th, 5th, 6th)
X_train = df.iloc[:, 3:6].values

# Create an instance of the GravidadeCalculator
calculator = GravidadeCalculator('gravidade_model_rnn.h5')

# Train the scaler
calculator.train_scaler(X_train)

# Apply the formula to the CSV file
calculator.apply_formula_to_csv(r'C:\Users\Rodrigo\PycharmProjects\simulador-resgate\VictimSim-main\neural_networks\datasetCompare.csv')
