import pandas as pd
import numpy as np
from sklearn.model_selection import KFold
from sklearn.preprocessing import StandardScaler
from keras.models import Sequential
from keras.layers import Dense

pasta = r"C:\Users\Rodrigo\PycharmProjects\simulador-resgate\VictimSim-main\neural_networks\dataset.csv"
df = pd.read_csv(pasta)
X = df.iloc[:, 3:6].values
y = df.iloc[:, 6].values

scaler = StandardScaler()
X = scaler.fit_transform(X)


kf = KFold(n_splits=5, shuffle=True, random_state=42)
for train_index, test_index in kf.split(X):
    X_train, X_test = X[train_index], X[test_index]
    y_train, y_test = y[train_index], y[test_index]

    model = Sequential()
    model.add(Dense(units=64, activation='relu', input_dim=3))
    model.add(Dense(units=32, activation='relu'))
    model.add(Dense(units=1, activation='linear'))
    model.compile(optimizer='adam', loss='mean_squared_error')
    model.fit(X_train, y_train, epochs=20000, batch_size=32, validation_data=(X_test, y_test))

    mse = model.evaluate(X_test, y_test)
    print(f'Squared error: {mse}')


model.save('gravidade_model_cross_val.h5')
