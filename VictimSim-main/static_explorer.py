class staticExplorer:
    total = 0
    agentes = 0
    vitimas = []
    vitFinal = []
    finalMap = []

    @staticmethod
    def addFinalMap(matriz):
        coluna_0 = [linha[0] for linha in matriz]

        for elemento in coluna_0:
            if elemento not in staticExplorer.finalMap:
                staticExplorer.finalMap.append(elemento)

    @staticmethod
    def retornaNumLinhas():
        i = 0
        for row in staticExplorer.finalMap:
            i += 1
        return i

    @staticmethod
    def print_matrix():
        for row in staticExplorer.finalMap:
            for element in row:
                print(element, end=" ")  # Imprime o elemento e um espaço em branco
            print()

    @staticmethod
    def procura_matrix(vet):
        for row in staticExplorer.finalMap:
            if row == vet:
                return True
        return False

    @staticmethod
    def addVitimas(vetor):
        staticExplorer.vitimas.extend(vetor)

    @staticmethod
    def returnVitFinal():
        return staticExplorer.vitFinal

    @staticmethod
    def remover_duplicatas():
        for x in staticExplorer.vitimas:
            if x not in staticExplorer.vitFinal:
                staticExplorer.vitFinal.append(x)

    @staticmethod
    def imprimeVitimas():
        print(staticExplorer.vitimas)

    @staticmethod
    def agentArrived():
        staticExplorer.total += 1

    @staticmethod
    def addAgent():
        staticExplorer.agentes += 1

    @staticmethod
    def checked():
        return staticExplorer.total == staticExplorer.agentes
