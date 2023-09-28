class rescuerIssues:
    vitimas = [] #VÍTIMAS PODEM ESTAR REPETIDAS SE ACHADAS POR MAIS DE UM AGENTE
    finalVitimas = [] #VÍTIMAS NÃO REPETIDAS
    finalMapa = [] #MAPA FINAL A PARTIR DA JUNÇÃO DO MAPA DE CADA EXPLORADOR

    @staticmethod
    def retornaVitimas():
        return rescuerIssues.vitimas

    @staticmethod
    def retornaFinalVitimas():
        return rescuerIssues.finalVitimas

    @staticmethod
    def retornaFinalMap():
        return rescuerIssues.finalMapa

    @staticmethod
    def adicionaVitimas(vetor):
        rescuerIssues.vitimas.extend(vetor)

    @staticmethod
    def retirarVitimasRepetidas():
        for x in rescuerIssues.vitimas:
            if x not in rescuerIssues.finalVitimas:
                #print(f"{x[0]}, {x[1]}")
                rescuerIssues.finalVitimas.append(x)

    @staticmethod
    def adicionaFinalMap(matriz):
        coluna_0 = [linha[0] for linha in matriz]
        for posicao in coluna_0:
            if posicao not in rescuerIssues.finalMapa:
                rescuerIssues.finalMapa.append(posicao)

    @staticmethod
    def procuraFinalMap(pos):
        for posicao in rescuerIssues.finalMapa:
            if posicao == pos:
                return True
        return False
