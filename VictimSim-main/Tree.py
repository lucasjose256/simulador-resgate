from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, export_text, export_graphviz
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn import tree
import pandas as pd

with open('/Users/lucasbarszcz/PycharmProjects/simulador-resgate/VictimSim-main/vital_signs_132v.txt', 'r') as arquivo:
    # Lê as linhas do arquivo
    linhas = arquivo.readlines()

matriz = []

for linha in linhas:
    # Divide a linha em elementos separados por vírgula
    elementos = linha.strip().split(',')
    # Converte os elementos em números de ponto flutuante e os adiciona à matriz
    linha_da_matriz = [float(elemento) for elemento in elementos]
    matriz.append(linha_da_matriz)

df = pd.DataFrame(matriz)

colunas = ["id", "pSist", "pDiast", "qPA", "pulso", "resp", "gravid", "classe", ]
df.columns = colunas
print(df)
X = df[['qPA', 'pulso', 'resp']]
y = df['classe']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
clf = tree.DecisionTreeClassifier(random_state=42,)
clf.fit(X_train, y_train)

print(clf.predict(X))
y_pred = clf.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, average='weighted')
recall = recall_score(y_test, y_pred, average='weighted')
f1 = f1_score(y_test, y_pred, average='weighted')

print("Acurácia:", accuracy)
print("Precisão:", precision)
print("Recall:", recall)
print("F1-Score:", f1)
