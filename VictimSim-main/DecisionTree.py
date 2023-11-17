from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import pandas as pd
from rescuer_issues import rescuerIssues

class DecisionTree:
    def __init__(self, file_path):
        self.file_path = file_path
        self.df = self.load_data() #tranforma o arquivo selecionado em um dataframe
        self.X = self.df[['qPA', 'pulso', 'resp']]
        self.y = self.df['classe']
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.X, self.y, test_size=0.2, random_state=42)
        self.clf = DecisionTreeClassifier(random_state=42)
        self.clf.fit(self.X_train, self.y_train)

    def load_data(self):
        with open(self.file_path, 'r') as arquivo:
            linhas = arquivo.readlines()

        matriz = []
        for linha in linhas:
            elementos = linha.strip().split(',')
            linha_da_matriz = [float(elemento) for elemento in elementos]
            matriz.append(linha_da_matriz)

        colunas = ["id", "pSist", "pDiast", "qPA", "pulso", "resp", "gravid", "classe"]
        df = pd.DataFrame(matriz, columns=colunas)
        return df

    def test_tree(self):
        y_pred = self.clf.predict(self.X_test)
        accuracy = accuracy_score(self.y_test, y_pred)
        precision = precision_score(self.y_test, y_pred, average='weighted')
        recall = recall_score(self.y_test, y_pred, average='weighted')
        f1 = f1_score(self.y_test, y_pred, average='weighted')
        print("Acurácia:", accuracy)
        print("Precisão:", precision)
        print("Recall:", recall)
        print("F1-Score:", f1)
        return accuracy, precision, recall, f1

    def classify(self):
        matriz = []
        colunas = ["id", "pSist", "pDiast", "qPA", "pulso", "resp", "gravid", "classe"]
        for i in range(len(rescuerIssues.finalVitimas)):
            matriz.append(rescuerIssues.finalVitimas[i][2])
        dataframe = pd.DataFrame(matriz, columns=colunas)
        result = dataframe[['qPA', 'pulso', 'resp']]

        return self.clf.predict(result)
