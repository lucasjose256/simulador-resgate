import pandas as pd
import numpy as np
from sklearn.model_selection import KFold
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from keras.models import Sequential
from keras.layers import SimpleRNN, Dense
from sklearn.metrics import mean_squared_error

# Carregar dados de treinamento
train_data = pd.read_csv('dados_treinamento.txt', header=None, names=['id', 'pSist', 'pDiast', 'qPA', 'pulso', 'freq_resp', 'gravidade', 'classe_gravidade'])

# Selecionar atributos relevantes para treinamento
features = train_data[['qPA', 'pulso', 'freq_resp']].values
labels = train_data['gravidade'].values

# Normalizar os dados
#scaler = MinMaxScaler()
scaler = StandardScaler()
features_scaled = scaler.fit_transform(features)

# Criar modelo da RNN
model = Sequential()
model.add(SimpleRNN(units=32, input_shape=(features.shape[1], 1), activation='relu'))
model.add(Dense(units=1, activation='linear'))

# Compilar o modelo
model.compile(optimizer='adam', loss='mean_squared_error')

# Realizar K-fold cross-validation
kfold = KFold(n_splits=5, shuffle=True, random_state=42)
for train_index, val_index in kfold.split(features_scaled):
    X_train, X_val = features_scaled[train_index], features_scaled[val_index]
    y_train, y_val = labels[train_index], labels[val_index]

    # Treinar o modelo
    model.fit(X_train.reshape(X_train.shape[0], X_train.shape[1], 1), y_train, epochs=100, batch_size=32, verbose=1)

    # Avaliar o modelo
    val_loss = model.evaluate(X_val.reshape(X_val.shape[0], X_val.shape[1], 1), y_val, verbose=0)
    print(f'Validation Loss: {val_loss}')

# Carregar dados de teste
test_data = pd.read_csv('dados_teste.txt', header=None, names=['id', 'pSist', 'pDiast', 'qPA', 'pulso', 'freq_resp', 'gravidade', 'classe_gravidade'])

# Selecionar atributos relevantes para teste
test_features = test_data[['qPA', 'pulso', 'freq_resp']].values
y_test = test_data[['gravidade']].values

# Normalizar os dados de teste
test_features_scaled = scaler.transform(test_features)

# Prever gravidade para os dados de teste
predicted_gravity = model.predict(test_features_scaled.reshape(test_features_scaled.shape[0], test_features_scaled.shape[1], 1))

rmse = np.sqrt(mean_squared_error(y_test, predicted_gravity))
print(f'Root Mean Squared Error (RMSE): {rmse}')

np.savetxt('gravidade_predita.csv', predicted_gravity, delimiter=',', fmt='%.6f')

# Adicionar os resultados ao DataFrame de teste
test_data['gravidade_predita'] = predicted_gravity

# Salvar os resultados em um arquivo CSV
test_data.to_csv('resultados.csv', index=False)
