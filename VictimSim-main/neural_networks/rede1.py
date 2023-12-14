import pandas as pd
import numpy as np
from sklearn.model_selection import KFold
from sklearn.preprocessing import StandardScaler
from keras.models import Sequential
from keras.layers import SimpleRNN, Dense


csv_path = r"C:\Users\Rodrigo\PycharmProjects\simulador-resgate\VictimSim-main\neural_networks\dataset.csv"  # Replace with the actual path to your CSV file
df = pd.read_csv(csv_path)


X = df.iloc[:, 3:6].values
y = df.iloc[:, 6].values


scaler = StandardScaler()
X = scaler.fit_transform(X)

X = X.reshape((X.shape[0], 1, X.shape[1]))

model = Sequential()
model.add(SimpleRNN(units=64, activation='relu', input_shape=(1, 3), return_sequences=True))
model.add(SimpleRNN(units=32, activation='relu'))
model.add(Dense(units=1, activation='linear'))

model.compile(optimizer='adam', loss='mean_squared_error')

kf = KFold(n_splits=5, shuffle=True, random_state=42)
for train_index, val_index in kf.split(X):
    X_train, X_val = X[train_index], X[val_index]
    y_train, y_val = y[train_index], y[val_index]

    model.fit(X_train, y_train, epochs=4000, batch_size=32, validation_data=(X_val, y_val))

model.save('gravidade_model_rede1.h5')
