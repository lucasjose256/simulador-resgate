import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error

#test_data = pd.read_csv('resultados.csv', header=None, names=['id', 'pSist', 'pDiast', 'qPA', 'pulso', 'freq_resp', 'gravidade', 'classe_gravidade', 'gravidade_predita'])
test_data = pd.read_csv('rede1gravidade.csv', header=None, names=['gravidade'])
#test_data = pd.read_csv('rede2gravidade.csv', header=None, names=['gravidade'])
#test_data = pd.read_csv('rede3gravidade.csv', header=None, names=['gravidade'])
#y_test = test_data[['gravidade_predita']].values
y_test = test_data[['gravidade']].values
predicted_gravity_data = pd.read_csv('gravidade_predita.txt', header=None, names=['id', 'pSist', 'pDiast', 'qPA', 'pulso', 'freq_resp', 'gravidade', 'classe_gravidade'])
# predicted_gravity_data = pd.read_csv('gravidade_predita.csv', header=None, names=['gravidade_predita'])
predicted_gravity = predicted_gravity_data[['gravidade']].values

rmse = np.sqrt(mean_squared_error(y_test, predicted_gravity))
print(f'Root Mean Squared Error (RMSE): {rmse}')
