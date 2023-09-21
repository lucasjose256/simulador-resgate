class staticExplorer:
    total = 0
    agentes = 0
    vitimas = []
    finalMap = []

    @staticmethod
    def adicionar_coluna_sem_duplicatas(matriz):
        coluna_0 = [linha[0] for linha in matriz]

        for elemento in coluna_0:
            if elemento not in staticExplorer.finalMap:
                staticExplorer.finalMap.append(elemento)

    @staticmethod
    def print_matrix():
        for row in staticExplorer.finalMap:
            for element in row:
                print(element, end=" ")  # Imprime o elemento e um espaço em branco
            print()

    @staticmethod
    def adicionar_vitimas(vetor):
        staticExplorer.vitimas.extend(vetor)

    @staticmethod
    def imprime_vitimas():
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
