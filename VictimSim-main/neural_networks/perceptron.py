import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Perceptron
from sklearn.metrics import accuracy_score

# Carregue os dados do CSV
file_path = r'C:\Users\lucas\PycharmProjects\simulador-resgate\VictimSim-main\neural_networks\dataset.csv'  # Substitua pelo caminho do seu arquivo CSV
colunas = ["id", "pSist", "pDiast", "qPA", "pulso", "resp", "gravid", "classe"]
data = pd.read_csv(file_path,)

# Divida os dados em features (X) e rótulos (y)
X = data.iloc[:, [2,3,4]].values  # Todas as colunas, exceto a última
y = data.iloc[:, 7].values   # Última coluna

# Divida os dados em conjuntos de treinamento e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Padronize os dados (média=0 e desvio padrão=1)
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Crie um perceptron e treine-o
perceptron = Perceptron()
perceptron.fit(X_train, y_train)

# Faça previsões no conjunto de teste
y_pred = perceptron.predict(X_test)

# Avalie a precisão do modelo
accuracy = accuracy_score(y_test, y_pred)
print(f'Acurácia: {accuracy * 100:.2f}%')
