import csv
import sys


class rescuerIssues:
    vitimas = [] #PODE CONTER VITIMAS REPETIDAS, SE ENCONTRADAS POR MAIS DE UM EXPLORADOR
    finalVitimas = [] #VÍTIMAS NÃO REPETIDAS
    finalMapa = [] #MAPA FINAL A PARTIR DA JUNÇÃO DO MAPA DE CADA EXPLORADOR
    finalClasses = [] #CLASSES FINAIS PARA CADA VÍTIMAS, EM ORDEM EM RELAÇÃO À finalVitimas
    salvas = []
    cluster = 1

    @staticmethod
    def retornaVitimas():
        return rescuerIssues.vitimas

    @staticmethod
    def vitimaSalva(string):
        if not string in rescuerIssues.salvas:
            rescuerIssues.salvas.append(string)


    @staticmethod
    def salvar_vetor_em_csv(nome_arquivo):
        if True:
            with open("cluster " + str(rescuerIssues.cluster), 'w', newline='') as arquivo_csv:
                escritor = csv.writer(arquivo_csv)
                for item in rescuerIssues.salvas:
                    escritor.writerow(item)
            rescuerIssues.cluster += 1

    @staticmethod
    def retornaFinalVitimas():
        return rescuerIssues.finalVitimas

    @staticmethod
    def retornaFinalMap():
        return rescuerIssues.finalMapa

    @staticmethod
    def retornaClasses():
        return rescuerIssues.finalClasses

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
    def defineClasses(vetor):
        rescuerIssues.finalClasses = vetor

    @staticmethod
    def retornaLinhaClasses(id):
        linha = 0
        for i in range(len(rescuerIssues.finalVitimas)):
            if rescuerIssues.finalVitimas[i][2][0] == id:
                return linha
            linha += 1
        return -1

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
