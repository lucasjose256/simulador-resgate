import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Perceptron
from sklearn.metrics import mean_squared_error

# Carregar dados
df_train = pd.read_csv( r'C:\Users\lucas\PycharmProjects\simulador-resgate\VictimSim-main\neural_networks\dataset.csv',usecols=["id", "pSist", "pDiast", "qPA", "pulso", "resp", "gravid", "classe"])
#df_test = pd.read_csv('caminho/do/seu/arquivo/teste_cego.csv')

# Separar dados de entrada (X) e saída (y)
X_train = df_train[['qPA', 'pulso', 'frequencia_respiratoria']]
y_train = df_train['gravidade']

#X_test = df_test[['qPA', 'pulso', 'frequencia_respiratoria']]
#y_test = df_test['gravidade']

# Padronizar os dados
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
#X_test_scaled = scaler.transform(X_test)

# Criar e treinar o Perceptron
perceptron = Perceptron(max_iter=1000, random_state=42)
perceptron.fit(X_train_scaled, y_train)

# Prever no conjunto de teste cego
#y_test_pred = perceptron.predict(X_test_scaled)

# Avaliar o modelo
#rmse_test = mean_squared_error(y_test, y_test_pred, squared=False)
print(perceptron.fit(X_train_scaled, y_train))