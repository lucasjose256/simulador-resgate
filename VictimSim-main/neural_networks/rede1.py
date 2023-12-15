import pandas as pd
import numpy as np
from sklearn.model_selection import KFold
from sklearn.preprocessing import StandardScaler
from keras.models import Sequential, load_model
from keras.layers import SimpleRNN, Dense
from keras.callbacks import ModelCheckpoint

csv_path = str(input("Digite o nome do arquivo para o treinamento: "))
df = pd.read_csv(csv_path)

X = df.iloc[:, 3:6].values
y = df.iloc[:, 6].values

scaler = StandardScaler()
X = scaler.fit_transform(X)
X = X.reshape((X.shape[0], 1, X.shape[1]))

kf = KFold(n_splits=5, shuffle=True, random_state=42)

best_loss = float('inf')
best_model_filename = 'best_model_rede1.h5'

for fold, (train_index, val_index) in enumerate(kf.split(X)):
    X_train, X_val = X[train_index], X[val_index]
    y_train, y_val = y[train_index], y[val_index]

    model = Sequential()
    model.add(SimpleRNN(units=64, activation='relu', input_shape=(1, 3), return_sequences=True))
    model.add(SimpleRNN(units=32, activation='relu'))
    model.add(Dense(units=1, activation='linear'))
    model.compile(optimizer='adam', loss='mean_squared_error')

    checkpoint = ModelCheckpoint(best_model_filename, monitor='val_loss', save_best_only=True, mode='min', verbose=1)

    model.fit(X_train, y_train, epochs=4000, batch_size=32, validation_data=(X_val, y_val), callbacks=[checkpoint])

    loss = model.evaluate(X_val, y_val)
    print(f'Fold {fold + 1}, Validation Loss: {loss}')

    if loss < best_loss:
        best_loss = loss
        best_model_filename = f'best_model_rede1_fold_{fold + 1}.h5'

best_model = load_model(best_model_filename)
best_model.save('gravidade_model_rede1.h5')
