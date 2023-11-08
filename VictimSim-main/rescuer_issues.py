import sys


class rescuerIssues:
    vitimas = [] #PODE CONTER VITIMAS REPETIDAS, SE ENCONTRADAS POR MAIS DE UM EXPLORADOR
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

    @staticmethod
    def printFinalMap():
        print("finalMap")
        for posicao in rescuerIssues.finalMapa:
            print(posicao)
        print("---FIM---")
        return False

    @staticmethod
    def menorMaiorL():
        menor = sys.maxsize
        maior = -sys.maxsize
        for posicao in rescuerIssues.finalMapa:
            if menor > posicao[0]:
                menor = posicao[0]
            if maior < posicao[0]:
                maior = posicao[0]
        return menor, maior

    @staticmethod
    def menorMaiorC():
        menor = sys.maxsize
        maior = -sys.maxsize
        for posicao in rescuerIssues.finalMapa:
            if menor > posicao[1]:
                menor = posicao[1]
            if maior < posicao[1]:
                maior = posicao[1]
        return menor, maior
