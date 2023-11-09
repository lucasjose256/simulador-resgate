##  RESCUER AGENT
### @Author: Tacla (UTFPR)
### Demo of use of VictimSim

import os
import random
import sys
from math import floor

from abstract_agent import AbstractAgent
from physical_agent import PhysAgent
from abc import ABC, abstractmethod
import clustering
from static_explorer import staticExplorer
from string_queue import StringQueue
from stack import stack
from rescuer_issues import rescuerIssues
from DecisionTree import DecisionTree
import csv

## Classe que define o Agente Rescuer com um plano fixo
class Rescuer(AbstractAgent):
    def __init__(self, env, config_file, cluster):
        """
        @param env: a reference to an instance of the environment class
        @param config_file: the absolute path to the agent's config file"""

        super().__init__(env, config_file)

        # Specific initialization for the rescuer
        self.plan = []  # a list of planned actions
        self.rtime = self.TLIM  # for controlling the remaining time
        self.clt = cluster  # GRUPO DO CLUSTERING
        self.iniciar_socorro = False # QUANDO O ALGORITMO DE CLUSTERING TERMINAR, OS SOCORRISTAS PODEM INICIAR SUAS AÇÕES
        self.quantidade_vitimas = 0 # QUANTIDADE DE VÍTIMAS QUE O SOCORRISTA DEVE ATENDER
        self.x_atual = 0 # POSIÇÃO X ATUAL
        self.y_atual = 0 # POSIÇÃO Y ATUAL
        self.caminhoA_calculado = False # FLAG PARA SABER SE JÁ EXISTE UM CAMINHO A* CALCULADO
        self.direcao_adicionada = False # FLAG PARA SABER SE AS DIREÇÕES DO MOVIMENTO JÁ FORAM ADICIONADAS
        self.plano_adicionado = False # FLAG PARA SABER SE O PLANO JÁ ESTÁ DEFINIDO PARA O AGENTE SE MOVER
        self.voltar_base = False # FLAG INDICANDO SE O AGENTE PRECISA VOLTAR PARA A BASE
        self.score_volta = 0 # VARIÁVEL QUE ARMAZENA O TEMPO QUE DEMORA PRA VOLTAR PARA A BASE DA POSIÇÃO ATUAL
        self.x_vitima = 0 # POSIÇÃO X DA VÍTIMA QUE O AGENTE DESEJA IR
        self.y_vitima = 0 # POSIÇÃO Y DA VÍTIMA QUE O AGENTE DESEJA IR
        self.imprimiu_volta = False
        self.vitimas_cluster = [] # LISTA DAS VÍTIMAS DO GRUPO DO AGENTE
        self.printou_cluster = False
        self.index = 0
        self.head = [0, 0]
        self.rowAtual = 0 # GUARDA A POSIÇÃO X QUE O AGENTE SE ENCONTRA PARA REALIZAR O A*
        self.columnAtual = 0 # GUARDA A POSIÇÃO Y QUE O AGENTE SE ENCONTRA PARA REALIZAR O A*
        self.l_last = 0
        self.c_last = 0
        self.finalStack = stack()
        self.finalDirectionsQueue = StringQueue()
        self.stackAux = stack()
        self.pRight = 1.0
        self.pLeft = 1.0
        self.pUp = 1.0
        self.pDown = 1.0
        self.pDRU = 1.0
        self.pDRD = 1.0
        self.pDLU = 1.0
        self.pDLD = 1.0
        self.pT = 1.0
        self.firstVictim = True
        self.lAtual = 0
        self.cAtual = 0
        self.grupo = None
        self.lMenor = 0
        self.cMenor = 0
        self.lMaior = 0
        self.cMaior = 0
        self.check = False
        self.visitas = StringQueue()
        self.stop = False
        self.kit = []
        self.avarageL = 0
        self.avarageC = 0
        self.tree = DecisionTree(r"C:\Users\ferna\Documents\Faculdade\6º Período\Sistemas Inteligentes\Tarefa 1 - Busca Exploratória x Explotação\simulador-resgate\VictimSim-main\datasets\sinais_vitais.txt")
        self.pessoasClustering = []
        self.nome_arquivo = ""
        self.salvas = []






        # Starts in IDLE state.
        # It changes to ACTIVE when the map arrives
        self.body.set_state(PhysAgent.IDLE)

        # planning
        self.__planner()

    def go_save_victims(self, walls, victims):
        """ The explorer sends the map containing the walls and
        victims' location. The rescuer becomes ACTIVE. From now,
        the deliberate method is called by the environment"""
        self.body.set_state(PhysAgent.ACTIVE)

    def retira_vitima(self, x, y):
        self.vitimas_cluster = [vitima for vitima in self.vitimas_cluster if vitima[0] != x or vitima[1] != y]


    def score(self, lc):
        l = lc[0]
        c = lc[1]

        return (min(abs(l), abs(c)) * 1.5 + (max(abs(l), abs(c)) - (min(abs(l), abs(c))))) + (
                    min(abs(l - self.y_atual), abs(c - self.x_atual)) * 1.5
                    + (max(abs(l - self.y_atual), abs(c - self.x_atual)) - min(abs(l - self.y_atual), abs(c - self.x_atual))))

    def vizinhos(self, lc, l_final, c_final, verde, vermelho):
        l = lc[0]
        c = lc[1]
        #print(l)
        #print(c)
        #rescuerIssues.printFinalMap()
        #if isinstance(l, str):
        #    l = self.y_atual
        #if isinstance(c, str):
        #    c = self.x_atual

        if not (l == self.y_atual and c == self.x_atual):
               vet = verde.get_element_by_index(verde.find_index_by_values(l, c))
               vermelho.enqueue([l, c, vet[3], vet[4]])
               verde.dequeue()
               #if(lx == )
        else:
            verde.dequeue()
        if rescuerIssues.procuraFinalMap([l - 1, c - 1]):
            #print("esta1")
            if [l - 1, c - 1] != [0, 0]:
                if (vermelho.find_index_by_values(l - 1, c - 1)) == -1:
                    verde.enqueueNotEqual([l - 1, c - 1, self.score([l - 1, c - 1]), l, c], vermelho)
            else:
                self.index += 1
                self.head = [l, c]
        if rescuerIssues.procuraFinalMap([l - 1, c]):
            #print("esta1.5")
            if [l - 1, c] != [0, 0]:
                if (vermelho.find_index_by_values(l - 1, c)) == -1:
                    verde.enqueueNotEqual([l - 1, c, self.score([l - 1, c]), l, c], vermelho)
            else:
                self.index += 1
                self.head = [l, c]
        if rescuerIssues.procuraFinalMap([l - 1, c + 1]):
            #print("esta2")
            if [l - 1, c + 1] != [0, 0]:
                if (vermelho.find_index_by_values(l - 1, c + 1)) == -1:
                    verde.enqueueNotEqual([l - 1, c + 1, self.score([l - 1, c + 1]), l, c], vermelho)
            else:
                self.index += 1
                self.head = [l, c]
        if rescuerIssues.procuraFinalMap([l, c - 1]):
            #print("esta3")
            if [l, c - 1] != [0, 0]:
                if (vermelho.find_index_by_values(l, c - 1)) == -1:
                    verde.enqueueNotEqual([l, c - 1, self.score([l, c - 1]), l, c], vermelho)
            else:
                self.index += 1
                self.head = [l, c]
        if rescuerIssues.procuraFinalMap([l, c + 1]):
            #print("esta4")
            if [l, c + 1] != [0, 0]:
                if (vermelho.find_index_by_values(l, c + 1)) == -1:
                    verde.enqueueNotEqual([l, c + 1, self.score([l, c + 1]), l, c], vermelho)
            else:
                self.index += 1
                self.head = [l, c]
        if rescuerIssues.procuraFinalMap([l + 1, c - 1]):
            #print("esta5")
            if [l + 1, c - 1] != [0, 0]:
                if (vermelho.find_index_by_values(l + 1, c - 1)) == -1:
                    verde.enqueueNotEqual([l + 1, c - 1, self.score([l + 1, c - 1]), l, c], vermelho)
            else:

                self.index += 1
                self.head = [l, c]
        if rescuerIssues.procuraFinalMap([l + 1, c]):
            #print("esta6")
            if [l + 1, c] != [0, 0]:
                if (vermelho.find_index_by_values(l + 1, c)) == -1:
                    verde.enqueueNotEqual([l + 1, c, self.score([l + 1, c]), l, c], vermelho)
            else:
                self.index += 1
                self.head = [l, c]
        if rescuerIssues.procuraFinalMap([l + 1, c + 1]):
            #print("esta7")
            if [l + 1, c + 1] != [0, 0]:
                if (vermelho.find_index_by_values(l + 1, c + 1)) == -1:
                    verde.enqueueNotEqual([l + 1, c + 1, self.score([l + 1, c + 1]), l, c], vermelho)
            else:
                self.index += 1
                self.head = [l, c]

        verde.merge_sortR(l_final, c_final)
        if(self.index == 1):
            verde.clear()
        #if(verde.size() > 20):
        #    verde.remove_elements_after_half()

        #verde.merge_sort()

        #print("--------------------")
        #print("--------------------")
        #print(l_final)
        #print(c_final)
        #vermelho.print_elements()
        #print("--------------------")
        #verde.print_elements()
        #print("--------------------")
        #print("--------------------")

    def caminhoA(self, x, y):
        l_final = x
        c_final = y
        verde = StringQueue()
        vermelho = StringQueue()
        self.rowAtual = self.x_atual
        self.columnAtual = self.y_atual
        #print("Atual: " + str(self.rowAtual) + " , " + str(self.columnAtual))
        self.index = 0
        self.head[0] = 0
        self.head[1] = 0
        verde.enqueue([self.y_atual, self.x_atual, self.score([self.y_atual, self.x_atual]), None, None], vermelho)
        while self.index <= 0:
            self.vizinhos(verde.get_element_by_index(0), l_final, c_final, verde, vermelho)
            #print(self.verde.get_element_by_index(0))

        self.l_last = self.head[0] #LINHA DO NO QUE CONECTA [0, 0]
        self.c_last = self.head[1] #COLUNA DO NO QUE CONECTA [0, 0]
        self.finalStack.push([l_final, c_final]) #IGNORA POR ENQUANTO
        # self.finalQueue.enqueue([l_final, c_final])
        while self.l_last != self.y_atual or self.c_last != self.x_atual:
            # print("lugar", self.la, self.rowA)
            #self.finalQueue.enqueue([self.l_last, self.c_last])
            self.finalStack.push([self.l_last, self.c_last]) #IGNORA POR ENQUANTO
            self.loop(vermelho)
        #self.finalQueue.enqueue([self.rowAtual, self.columnAtual])
        #print("-------------")
        #print(self.vitimas_cluster)
        #print(self.rowAtual, self.columnAtual)
        #print("FINAL")
        #print("FILA")
        #self.finalQueue.print_elements()
        #print("PILHA")
        #self.finalStack.imprimir_pilha()
        #print("-------------")

    def loop(self, vermelho):
        aux = vermelho.get_element_by_index(vermelho.find_index_by_values(self.l_last, self.c_last))
        self.l_last = aux[2]
        self.c_last = aux[3]
        #print(self.l_last, self.c_last)

    def calculaScorePilha(self):
        pilha = stack()
        score = 0
        pilha = stack.copiar_pilha(self.finalStack)
        pilha.push([self.y_atual, self.x_atual])
        #print("PILHA PARA SCORE")
        #pilha.imprimir_pilha()
        aux1 = pilha.pop()
        while not pilha.is_empty():
            aux2 = pilha.pop()
            way = [aux1[0] - aux2[0], aux1[1] - aux2[1]]
            if (way == [0, 1]):
                score += 1
            elif (way == [0, -1]):
                score += 1
            elif (way == [1, 0]):
                score += 1
            elif (way == [-1, 0]):
                score += 1
            elif (way == [1, 1]):
                score += 1.5
            elif (way == [1, -1]):
                score += 1.5
            elif (way == [-1, 1]):
                score += 1.5
            elif (way == [-1, -1]):
                score += 1.5
            aux1 = aux2
        #print(f"{score}")

        return score

    def encontraMenorCaminhoEntreVitimas(self):
        # AQUI VOCE TEM QUE FAZER UM FOR PARA CALCULAR O SCORE DE CADA CAMINHO DAS VITIMAS
        # E RETORNAR A POSICAO DA VITIMA COM MENOR CAMINHO
        x_final = 0
        y_final = 0
        i = 0
        menor_score = 0
        for i in range(len(self.vitimas_cluster)):
            #print(f"SCORE PARA A VITIMA {self.vitimas_cluster[i][0]}, {self.vitimas_cluster[i][1]}")
            if i == 0:
                x_final = self.vitimas_cluster[i][0]
                y_final = self.vitimas_cluster[i][1]
                self.finalStack.esvaziar_pilha()
                self.caminhoA(self.vitimas_cluster[i][0], self.vitimas_cluster[i][1])
                #print(f"PILHA {i+1} VITIMA {self.vitimas_cluster[i][0]}, {self.vitimas_cluster[i][1]}")
                #self.finalStack.imprimir_pilha()
                self.auxStack = stack.copiar_pilha(self.finalStack)
                menor_score = self.calculaScorePilha()
                #print(menor_score)
            else:
                self.finalStack.esvaziar_pilha()
                self.caminhoA(self.vitimas_cluster[i][0], self.vitimas_cluster[i][1])
                #print(f"PILHA {i+1} VITIMA {self.vitimas_cluster[i][0]}, {self.vitimas_cluster[i][1]}")
                #self.finalStack.imprimir_pilha()
                #print(self.calculaScorePilha())
                if menor_score > self.calculaScorePilha():
                    x_final = self.vitimas_cluster[i][0]
                    y_final = self.vitimas_cluster[i][1]
                    self.auxStack = stack.copiar_pilha(self.finalStack)
                    menor_score = self.calculaScorePilha()


        self.finalStack = stack.copiar_pilha(self.auxStack)

        return x_final, y_final

    def isInCluster(self, l, c):
        for i in range(len(self.grupo)):
            if(self.grupo[i][0] == l and self.grupo[i][1] == c):
                #self.grupo[i][0] = sys.maxsize
                #self.grupo[i][1] = sys.maxsize
                return True
        return False

    """def isInClusterKIT(self, l, c):
        print("RECEBI: " + str(l) + " , " + str(c))
        t = False
        for i in range(len(self.kit)):
            print("TENHO: " + str(self.kit[i][0]) + " , " + str(self.kit[i][1]))
            if(self.kit[i][0] == l and self.kit[i][1] == c):
                print("ACHEI")
                #self.kit[i][0] = sys.maxsize
                #self.kit[i][1] = sys.maxsize
                return True
        return False"""

    def encontraGenetica(self):

        # AQUI VOCE TEM QUE FAZER UM FOR PARA CALCULAR O SCORE DE CADA CAMINHO DAS VITIMAS
        # E RETORNAR A POSICAO DA VITIMA COM MENOR CAMINHO
        x_final = 0
        y_final = 0
        i = 0
        menor_score = 0

        #print(f"SCORE PARA A VITIMA {self.vitimas_cluster[i][0]}, {self.vitimas_cluster[i][1]}")
        #pRight = 1.0
        #pLeft = 1.0
        #pUp = 1.0
        #pDown = 1.0
        #pDRU = 1.0
        #pDRD = 1.0
        #pDLU = 1.0
        #pDLD = 1.0
        #t = pRight + pLeft + pUp + pDown + pDRU + pDRD + pDLU + pDLD
        decision = "None"
        if(self.firstVictim):
            self.lAtual = 0
            self.cAtual = 0
            la = 0
            ca = 0
            lC = self.grupo[0][0]
            cC = self.grupo[0][1]
            pL = lC - la
            pC = cC - ca
            self.probabilityC(floor(self.avarageL), floor(self.avarageC), "st")
            self.firstVictim = False
        victimFound = False
        self.finalStack.esvaziar_pilha()
        while decision == "None":
            re = 0
            total = 0
            re += 1
            self.fixProb()
            """print ("--------------")
            #print("1º vitima: " + str(lC) + "," + str(cC))
            print("time: " + str(self.rtime))
            print ("Probability Right: " + str (self.pRight / self.pT))
            print ("Probability Left: " + str (self.pLeft / self.pT))
            print ("Probability Down: " + str (self.pDown / self.pT))
            print ("Probability Up: " + str (self.pUp / self.pT))
            print ("Probability UpRight: " + str (self.pDRU / self.pT))
            print ("Probability UpLeft: " + str (self.pDLU / self.pT))
            print ("Probability DownRight: " + str (self.pDRD / self.pT))
            print ("Probability DownLeft: " + str (self.pDLD / self.pT))
            print ("LMenor: " + str (self.lMenor) + " LMaior: " + str (self.lMaior) + " CMenor: " + str (
                self.cMenor) + " CMaior: " + str (self.cMaior))"""
            position = self.probababilitySelector ()
            re = True
            # if re > 8:
            #    exit(1)
            # MELHORAR PARA BAIXAR PRIORIDADE DE JA VISITADO (CRIAR UMA MATRIZ DE VERTICES JA VISITADAS)
            self.visitas.enqueueNotEqual ([0, 0])
            if position == "UP":
                self.visitas.enqueueNotEqual ([self.lAtual - 1, self.cAtual])
                if (rescuerIssues.procuraFinalMap ([self.lAtual - 1, self.cAtual])):
                    #print("passei UP")
                    if (self.isInCluster (self.lAtual - 1, self.cAtual)):
                        self.probabilityC (-1, 0, "victim")
                        victimFound = True
                        x_final = self.lAtual - 1
                        y_final = self.cAtual
                    else:
                        self.probabilityC (-1, 0, "nonVictim")
                        #self.finalStack.push (([self.lAtual - 1, self.cAtual]))
                        total += 1
                    decision = "UP"
                    self.lAtual = self.lAtual - 1
                    self.cAtual = self.cAtual
                else:
                    if (
                            self.lAtual - 1 > self.lMaior or self.lAtual - 1 < self.lMenor or self.cAtual > self.cMaior or self.cAtual < self.cMenor):
                        self.probabilityC (-1, 0, "Wall")
                    else:
                        self.probabilityC (-1, 0, "Obstacle")
            elif position == "DOWN":
                self.visitas.enqueueNotEqual ([self.lAtual + 1, self.cAtual])
                if (rescuerIssues.procuraFinalMap ([self.lAtual + 1, self.cAtual])):
                    #print("Passei DOWN")
                    if (self.isInCluster (self.lAtual + 1, self.cAtual)):
                        self.probabilityC (1, 0, "victim")
                        victimFound = True
                        x_final = self.lAtual + 1
                        y_final = self.cAtual
                    else:
                        self.probabilityC (1, 0, "nonVictim")
                        #self.finalStack.push (([self.lAtual + 1, self.cAtual]))
                        total += 1
                    decision = "DOWN"
                    self.lAtual = self.lAtual + 1
                    self.cAtual = self.cAtual
                else:
                    if (
                            self.lAtual + 1 > self.lMaior or self.lAtual + 1 < self.lMenor or self.cAtual > self.cMaior or self.cAtual < self.cMenor):
                        self.probabilityC (1, 0, "Wall")
                    else:
                        self.probabilityC (1, 0, "Obstacle")
            elif position == "RIGHT":
                self.visitas.enqueueNotEqual ([self.lAtual, self.cAtual + 1])
                if (rescuerIssues.procuraFinalMap ([self.lAtual, self.cAtual + 1])):
                    #print("passei RIGHT")
                    if (self.isInCluster (self.lAtual, self.cAtual + 1)):
                        self.probabilityC (0, 1, "victim")
                        victimFound = True
                        x_final = self.lAtual
                        y_final = self.cAtual + 1
                    else:
                        self.probabilityC (0, 1, "nonVictim")
                        #self.finalStack.push (([self.lAtual, self.cAtual + 1]))
                        total += 1
                    decision = "RIGHT"
                    self.lAtual = self.lAtual
                    self.cAtual = self.cAtual + 1
                else:
                    if (
                            self.lAtual > self.lMaior or self.lAtual < self.lMenor or self.cAtual + 1 > self.cMaior or self.cAtual + 1 < self.cMenor):
                        self.probabilityC (0, 1, "Wall")
                    else:
                        self.probabilityC (0, 1, "Obstacle")
            elif position == "LEFT":
                self.visitas.enqueueNotEqual ([self.lAtual, self.cAtual - 1])
                if (rescuerIssues.procuraFinalMap ([self.lAtual, self.cAtual - 1])):
                    #print("passei LEFT")
                    if (self.isInCluster (self.lAtual, self.cAtual - 1)):
                        self.probabilityC (0, -1, "victim")
                        victimFound = True
                        x_final = self.lAtual
                        y_final = self.cAtual - 1
                    else:
                        self.probabilityC (0, -1, "nonVictim")
                        #self.finalStack.push (([self.lAtual, self.cAtual - 1]))
                        total += 1
                    decision = "LEFT"
                    self.lAtual = self.lAtual
                    self.cAtual = self.cAtual - 1
                else:
                    if (
                            self.lAtual > self.lMaior or self.lAtual < self.lMenor or self.cAtual - 1 > self.cMaior or self.cAtual - 1 < self.cMenor):
                        self.probabilityC (0, -1, "Wall")
                    else:
                        self.probabilityC (0, -1, "Obstacle")
            elif position == "DiagonalLU":
                self.visitas.enqueueNotEqual ([self.lAtual - 1, self.cAtual - 1])
                if (rescuerIssues.procuraFinalMap ([self.lAtual - 1, self.cAtual - 1])):
                    #print("passei DiagonalLU")
                    if (self.isInCluster (self.lAtual - 1, self.cAtual - 1)):
                        self.probabilityC (-1, -1, "victim")
                        victimFound = True
                        x_final = self.lAtual - 1
                        y_final = self.cAtual - 1
                    else:
                        self.probabilityC (-1, -1, "nonVictim")
                        #self.finalStack.push (([self.lAtual - 1, self.cAtual - 1]))
                        total += 1.5
                    decision = "diagonalUL"
                    self.lAtual = self.lAtual - 1
                    self.cAtual = self.cAtual - 1
                else:
                    if (
                            self.lAtual - 1 > self.lMaior or self.lAtual - 1 < self.lMenor or self.cAtual - 1 > self.cMaior or self.cAtual - 1 < self.cMenor):
                        self.probabilityC (-1, -1, "Wall")
                    else:
                        self.probabilityC (-1, -1, "Obstacle")
            elif position == "DiagonalRU":
                self.visitas.enqueueNotEqual ([self.lAtual - 1, self.cAtual + 1])
                if (rescuerIssues.procuraFinalMap ([self.lAtual - 1, self.cAtual + 1])):
                    #print("passei DiagonalRU")
                    if (self.isInCluster (self.lAtual - 1, self.cAtual + 1)):
                        self.probabilityC (-1, 1, "victim")
                        victimFound = True
                        x_final = self.lAtual - 1
                        y_final = self.cAtual + 1
                    else:
                        self.probabilityC (-1, 1, "nonVictim")
                        #self.finalStack.push (([self.lAtual - 1, self.cAtual + 1]))
                        decision = "diagonalUR"
                        total += 1.5
                    decision = "diagonalUR"
                    self.lAtual = self.lAtual - 1
                    self.cAtual = self.cAtual + 1
                else:
                    if (
                            self.lAtual - 1 > self.lMaior or self.lAtual - 1 < self.lMenor or self.cAtual + 1 > self.cMaior or self.cAtual + 1 < self.cMenor):
                        self.probabilityC (-1, 1, "Wall")
                    else:
                        self.probabilityC (-1, 1, "Obstacle")
            elif position == "DiagonalLD":
                self.visitas.enqueueNotEqual ([self.lAtual + 1, self.cAtual - 1])
                if (rescuerIssues.procuraFinalMap ([self.lAtual + 1, self.cAtual - 1])):
                    #print("passei DiagonalLD")
                    if (self.isInCluster (self.lAtual + 1, self.cAtual - 1)):
                        self.probabilityC (1, -1, "victim")
                        victimFound = True
                        x_final = self.lAtual + 1
                        y_final = self.cAtual - 1
                    else:
                        self.probabilityC (1, -1, "nonVictim")
                        #self.finalStack.push (([self.lAtual + 1, self.cAtual - 1]))
                        total += 1.5
                    decision = "diagonalDL"
                    self.lAtual = self.lAtual + 1
                    self.cAtual = self.cAtual - 1
                else:
                    if (
                            self.lAtual + 1 > self.lMaior or self.lAtual + 1 < self.lMenor or self.cAtual - 1 > self.cMaior or self.cAtual - 1 < self.cMenor):
                        self.probabilityC (1, -1, "Wall")
                    else:
                        self.probabilityC (1, -1, "Obstacle")
            elif position == "DiagonalRD":
                self.visitas.enqueueNotEqual ([self.lAtual + 1, self.cAtual + 1])
                if (rescuerIssues.procuraFinalMap ([self.lAtual + 1, self.cAtual + 1])):
                    #print("passei DiagonalRD")
                    if (self.isInCluster (self.lAtual + 1, self.cAtual + 1)):
                        self.probabilityC (1, 1, "victim")
                        victimFound = True
                        x_final = self.lAtual + 1
                        y_final = self.cAtual + 1
                    else:
                        self.probabilityC (1, 1, "nonVictim")
                        #self.finalStack.push (([self.lAtual + 1, self.cAtual + 1]))
                        total += 1.5
                    decision = "diagonalDR"
                    self.lAtual = self.lAtual + 1
                    self.cAtual = self.cAtual + 1
                else:
                    if (
                            self.lAtual + 1 > self.lMaior or self.lAtual + 1 < self.lMenor or self.cAtual + 1 > self.cMaior or self.cAtual + 1 < self.cMenor):
                        self.probabilityC (1, 1, "Wall")
                    else:
                        self.probabilityC (1, 1, "Obstacle")
            #print("LATUAL: " + str(x_final) + " CATUAL: " + str(y_final))
            #if ((self.rtime - total) < (abs(self.lAtual) + abs(self.cAtual)) * 1.75 + 10) and (self.lAtual != 0 or self.cAtual != 0):
                #self.stop = True



            """
            if i == 0:
                x_final = self.vitimas_cluster[i][0]
                y_final = self.vitimas_cluster[i][1]
                self.finalStack.esvaziar_pilha()
                self.caminhoA(self.vitimas_cluster[i][0], self.vitimas_cluster[i][1])
                #print(f"PILHA {i+1} VITIMA {self.vitimas_cluster[i][0]}, {self.vitimas_cluster[i][1]}")
                #self.finalStack.imprimir_pilha()
                self.auxStack = stack.copiar_pilha(self.finalStack)
                menor_score = self.calculaScorePilha()
                #print(menor_score)
            else:
                self.finalStack.esvaziar_pilha()
                self.caminhoA(self.vitimas_cluster[i][0], self.vitimas_cluster[i][1])
                #print(f"PILHA {i+1} VITIMA {self.vitimas_cluster[i][0]}, {self.vitimas_cluster[i][1]}")
                #self.finalStack.imprimir_pilha()
                #print(self.calculaScorePilha())
                if menor_score > self.calculaScorePilha():
                    x_final = self.vitimas_cluster[i][0]
                    y_final = self.vitimas_cluster[i][1]
                    self.auxStack = stack.copiar_pilha(self.finalStack)
                    menor_score = self.calculaScorePilha()
                """

        #print("--------PILHA-------------")
        #self.finalStack.imprimir_pilha()
        #print("---------------------")
        #print ("Position 1: " + decision)
        return decision

    def probabilityC(self, pL, pC, st):
        #print("Esc: " + st)
            #pRight = 1.0
            #pLeft = 1.0
            #pUp = 1.0
            #pDown = 1.0
            #pDRU = 1.0
            #pDRD = 1.0
            #pDLU = 1.0
            #pDLD = 1.0
        stBoost = 10
        victimBoost = 5
        nonVictimBoost = 0.94
        wallVictimBoost = 0.1
        obstacleVictimBoost = 0.85
        if(st == "st"):
          if(pL > 0):
            self.pDown = self.pDown*stBoost
          elif(pL < 0):
            self.pUp = self.pUp*stBoost
          if(pC > 0):
            self.pRight = self.pRight*stBoost
          elif(pC < 0):
            self.pLeft = self.pLeft*stBoost
          #DIAGONAIS
          if(pL > 0 and pC > 0):
            self.pDRD = self.pDRD*stBoost
          elif(pL < 0 and pC > 0):
            self.pDRU = self.pDRU*stBoost
          if(pL > 0 and pC < 0):
            self.pDLD = self.pDLD*stBoost
          elif(pL < 0 and pC < 0):
            self.pDLU = self.pDLU*stBoost
        elif (st == "victim"):
          if(pL > 0):
            self.pDown = self.pDown*victimBoost
          elif(pL < 0):
            self.pUp = self.pUp*victimBoost
          if(pC > 0):
            self.pRight = self.pRight*victimBoost
          elif(pC < 0):
            self.pLeft = self.pLeft*victimBoost
          #DIAGONAIS
          if(pL > 0 and pC > 0):
            self.pDRD = self.pDRD*victimBoost
          elif(pL < 0 and pC > 0):
            self.pDRU = self.pDRU*victimBoost
          if(pL > 0 and pC < 0):
            self.pDLD = self.pDLD*victimBoost
          elif(pL < 0 and pC < 0):
            self.pDLU = self.pDLU*victimBoost
        elif(st == "nonVictim"):
          if(pL > 0):
            self.pDown = self.pDown*nonVictimBoost
          elif(pL < 0):
            self.pUp = self.pUp*nonVictimBoost
          if(pC > 0):
            self.pRight = self.pRight*nonVictimBoost
          elif(pC < 0):
            self.pLeft = self.pLeft*nonVictimBoost
          #DIAGONAIS
          if(pL > 0 and pC > 0):
            self.pDRD = self.pDRD*nonVictimBoost
          elif(pL < 0 and pC > 0):
            self.pDRU = self.pDRU*nonVictimBoost
          if(pL > 0 and pC < 0):
            self.pDLD = self.pDLD*nonVictimBoost
          elif(pL < 0 and pC < 0):
            self.pDLU = self.pDLU*nonVictimBoost
        elif(st == "Wall"):
          if(pL > 0):
            self.pDown = self.pDown*wallVictimBoost
          elif(pL < 0):
            self.pUp = self.pUp*wallVictimBoost
          if(pC > 0):
            self.pRight = self.pRight*wallVictimBoost
          elif(pC < 0):
            self.pLeft = self.pLeft*wallVictimBoost
          #DIAGONAIS
          if(pL > 0 and pC > 0):
            self.pDRD = self.pDRD*wallVictimBoost
          elif(pL < 0 and pC > 0):
            self.pDRU = self.pDRU*wallVictimBoost
          if(pL > 0 and pC < 0):
            self.pDLD = self.pDLD*wallVictimBoost
          elif(pL < 0 and pC < 0):
            self.pDLU = self.pDLU*wallVictimBoost
        elif(st == "Obstacle"):
          if(pL > 0):
            self.pDown = self.pDown*obstacleVictimBoost
          elif(pL < 0):
            self.pUp = self.pUp*obstacleVictimBoost
          if(pC > 0):
            self.pRight = self.pRight*obstacleVictimBoost
          elif(pC < 0):
            self.pLeft = self.pLeft*obstacleVictimBoost
          #DIAGONAIS
          if(pL > 0 and pC > 0):
            self.pDRD = self.pDRD*obstacleVictimBoost
          elif(pL < 0 and pC > 0):
            self.pDRU = self.pDRU*obstacleVictimBoost
          if(pL > 0 and pC < 0):
            self.pDLD = self.pDLD*obstacleVictimBoost
          elif(pL < 0 and pC < 0):
            self.pDLU = self.pDLU*obstacleVictimBoost

        self.pT = self.pRight+self.pLeft+self.pUp+self.pDown+self.pDRU+self.pDRD+self.pDLU+self.pDLD
        if(self.pT > 1000):
            self.pDown = self.pDown*0.001
            self.pUp = self.pUp*0.001
            self.pRight = self.pRight*0.001
            self.pLeft = self.pLeft*0.001
            self.pDRD = self.pDRD*0.001
            self.pDRU = self.pDRU*0.001
            self.pDLD = self.pDLD*0.001
            self.pDLU = self.pDLU*0.001

        if(self.pT < 0.01):
            self.pDown = self.pDown*100
            self.pUp = self.pUp*100
            self.pRight = self.pRight*100
            self.pLeft = self.pLeft*100
            self.pDRD = self.pDRD*100
            self.pDRU = self.pDRU*100
            self.pDLD = self.pDLD*100
            self.pDLU = self.pDLU*100

        self.fixProb()
    def fixProbability(self):
            self.pT = self.pRight+self.pLeft+self.pUp+self.pDown+self.pDRU+self.pDRD+self.pDLU+self.pDLD
            self.pLeft = (self.pLeft/self.pT)
            self.pDown = (self.pDown/self.pT)
            self.pUp = (self.pUp/self.pT)
            self.pDRU = (self.pDRU/self.pT)
            self.pDLU = (self.pDLU/self.pT)
            self.pDRD =(self.pDRD/self.pT)
            self.pDLD = (self.pDLD/self.pT)
            self.pT = self.pRight+self.pLeft+self.pUp+self.pDown+self.pDRU+self.pDRD+self.pDLU+self.pDLD


    def fixProb(self):
        self.pT = self.pRight+self.pLeft+self.pUp+self.pDown+self.pDRU+self.pDRD+self.pDLU+self.pDLD
        pDown = 0.04
        pLimit = 0.94
        pMin = 0.05
        pMax = 0.94


        if (self.pRight/self.pT) < pDown:
                self.fixProbability()
                self.pRight = pMin
        if (self.pLeft/self.pT) < pDown:
                self.fixProbability()
                self.pLeft = pMin
        if (self.pDown/self.pT) < pDown:
                self.fixProbability()
                self.pDown = pMin
        if (self.pUp/self.pT) < pDown:
                self.fixProbability()
                self.pUp = pMin
        if (self.pDRD/self.pT) < pDown:
                self.fixProbability()
                self.pDRD = pMin
        if (self.pDLU/self.pT) < pDown:
                self.fixProbability()
                self.pDLU = pMin
        if (self.pDRU/self.pT) < pDown:
                self.fixProbability()
                self.pDRU = pMin
        if (self.pDLD/self.pT) < pDown:
                self.fixProbability()
                self.pDLD = pMin
        if (self.pRight/self.pT) > pLimit:
                self.fixProbability()
                self.pRight = pMax
        if (self.pLeft/self.pT) > pLimit:
                self.fixProbability()
                self.pLeft = pMax
        if (self.pDown/self.pT) > pLimit:
                self.fixProbability()
                self.pDown = pMax
        if (self.pUp/self.pT) > pLimit:
                self.fixProbability()
                self.pUp = pMax
        if (self.pDRD/self.pT) > pLimit:
                self.fixProbability()
                self.pDRD = pMax
        if (self.pDLU/self.pT) > pLimit:
                self.fixProbability()
                self.pDLU = pMax
        if (self.pDRU/self.pT) > pLimit:
                self.fixProbability()
                self.pDRU = pMax
        if (self.pDLD/self.pT) > pLimit:
                self.fixProbability()
                self.pDLD = pMax
        self.pT = self.pRight+self.pLeft+self.pUp+self.pDown+self.pDRU+self.pDRD+self.pDLU+self.pDLD

    def boostCenter(self):
        if(self.lAtual - self.avarageL < 0):
            self.pDown = self.pDown*abs(1 + abs(self.lAtual - self.avarageL))*1.2
            if(self.cAtual - self.avarageC < 0):
                self.pDRD = self.pDRD*abs(1 + abs(self.lAtual - self.avarageL)/2)
            if(self.cAtual - self.avarageC > 0):
                self.pDLD = self.pDLD*abs(1 + abs(self.lAtual - self.avarageL)/2)
        if(self.lAtual - self.avarageL > 0):
            self.pUp = self.pUp*abs(1 + abs(self.lAtual - self.avarageL))*1.2
            if(self.cAtual - self.avarageC < 0):
                self.pDRU = self.pDRU*abs(1 + abs(self.lAtual - self.avarageL)/2)
            if(self.cAtual - self.avarageC > 0):
                self.pDLU = self.pDLU*abs(1 + abs(self.lAtual - self.avarageL)/2)
        if(self.cAtual - self.avarageC < 0):
            self.pRight = self.pRight*abs(1 + abs(self.cAtual - self.avarageC))*1.2
            if(self.lAtual - self.avarageL < 0):
                self.pDRD = self.pDRD*abs(1 + abs(self.cAtual - self.avarageC)/2)
            if(self.lAtual - self.avarageL > 0):
                self.pDRU = self.pDRU*abs(1 + abs(self.cAtual - self.avarageC)/2)
        if(self.cAtual - self.avarageC > 0):
            self.pLeft = self.pRight*abs(1 + abs(self.cAtual - self.avarageC))*1.2
            if(self.lAtual - self.avarageL < 0):
                self.pDLD = self.pDRD*abs(1 + abs(self.cAtual - self.avarageC)/2)
            if(self.lAtual - self.avarageL > 0):
                self.pDLU = self.pDRU*abs(1 + abs(self.cAtual - self.avarageC)/2)
        self.pT = self.pRight+self.pLeft+self.pUp+self.pDown+self.pDRU+self.pDRD+self.pDLU+self.pDLD
    def probababilitySelector(self):
        self.pT = self.pRight+self.pLeft+self.pUp+self.pDown+self.pDRU+self.pDRD+self.pDLU+self.pDLD
        if(self.pT > 1000):
            self.pDown = self.pDown*0.001
            self.pUp = self.pUp*0.001
            self.pRight = self.pRight*0.001
            self.pLeft = self.pLeft*0.001
            self.pDRD = self.pDRD*0.001
            self.pDRU = self.pDRU*0.001
            self.pDLD = self.pDLD*0.001
            self.pDLU = self.pDLU*0.001

        if(self.pT < 0.01):
            self.pDown = self.pDown*100
            self.pUp = self.pUp*100
            self.pRight = self.pRight*100
            self.pLeft = self.pLeft*100
            self.pDRD = self.pDRD*100
            self.pDRU = self.pDRU*100
            self.pDLD = self.pDLD*100
            self.pDLU = self.pDLU*100

        self.fixProb()

        self.boostCenter()
        self.pT = self.pRight+self.pLeft+self.pUp+self.pDown+self.pDRU+self.pDRD+self.pDLU+self.pDLD
        rand = random.uniform(0, self.pT)

        """print("RAND: " + str(rand))
        print("TOTAL: " + str(self.pT))
        print("Right: " + str(self.pRight))
        print("Left: " + str(self.pLeft))
        print("Down: " + str(self.pDown))
        print("Up: " + str(self.pUp))
        print("UpRight: " + str(self.pDRU))
        print("UpLeft: " + str(self.pDLU))
        print("DownRight: " + str(self.pDRU))
        print("DownLeft: " + str(self.pDLD))"""
        elementos = ["UP", "DOWN", "RIGHT", "LEFT", "DiagonalLU", "DiagonalRU", "DiagonalLD", "DiagonalRD"]

        #"DiagonalRD", "DiagonalRU", "DiagonalLD", "DiagonalLU"]
        no = False
        pesos = [0.000001, 0.000001, 0.000001, 0.000001, 0.000001, 0.000001, 0.000001, 0.000001]
        #print("--------------")
        #print("ATUAL: " + str(self.lAtual) + " , " + str(self.cAtual))
        #self.visitas.print_elements()
        #print("--------------")
        if self.visitas.find_index_by_values(self.lAtual - 1, self.cAtual) == -1:
              pesos[0] = self.pUp
              no = True
              #print("0")
        if self.visitas.find_index_by_values(self.lAtual + 1, self.cAtual) == -1:
              pesos[1] = self.pDown
              no = True
              #print("1")
        if self.visitas.find_index_by_values(self.lAtual, self.cAtual + 1) == -1:
              pesos[2] = self.pRight
              no = True
              #print("2")
        if self.visitas.find_index_by_values(self.lAtual, self.cAtual - 1) == -1:
              pesos[3] = self.pLeft
              no = True
              #print("3")
        if self.visitas.find_index_by_values(self.lAtual - 1, self.cAtual - 1) == -1:
              pesos[4] = self.pDLU
              no = True
              #print("4")
        if self.visitas.find_index_by_values(self.lAtual - 1, self.cAtual + 1) == -1:
              pesos[5] = self.pDRU
              no = True
              #print("5")
        if self.visitas.find_index_by_values(self.lAtual + 1, self.cAtual - 1) == -1:
              pesos[6] = self.pDLD
              no = True
              #print("6")
        if self.visitas.find_index_by_values(self.lAtual + 1, self.cAtual + 1) == -1:
              pesos[7] = self.pDRD
              no = True
              #print("7")
        if not no:
          if(rand < self.pDown):#BAIXO
              return "DOWN"
          elif(rand > self.pDown and rand < (self.pDown + self.pUp)):#CIMA
            return "UP"
          elif((rand > (self.pDown + self.pUp) and rand < (self.pDown + self.pUp + self.pRight))): #DIREITA
            return "RIGHT"
          elif((rand > (self.pDown + self.pUp + self.pRight) and rand < (self.pDown + self.pUp + self.pRight + self.pLeft))): #ESQUERDA
            return "LEFT"
          elif((rand > (self.pDown + self.pUp + self.pRight + self.pLeft) and rand < (self.pDown + self.pUp + self.pRight + self.pLeft + self.pDRD))): #Diagonal DIREITABAIXO
            return "DiagonalRD"
          elif((rand > (self.pDown + self.pUp + self.pRight + self.pLeft + self.pDRD) and rand < (self.pDown + self.pUp + self.pRight + self.pLeft + self.pDRD + self.pDRU))): #Diagonal DIREITACIMA
            return "DiagonalRU"
          elif((rand > (self.pDown + self.pUp + self.pRight + self.pLeft + self.pDRD + self.pDRU) and rand < (self.pDown + self.pUp + self.pRight + self.pLeft + self.pDRD + self.pDRU + self.pDLD))): #Diagonal ESQUERDABAIXO
            return "DiagonalLD"
          else: #ESQUERDACIMA
            return "DiagonalLU"
        else:
          elemento = (self.sortear_com_pesos(elementos, pesos))
          #print(elemento)
          return elemento

    def sortear_com_pesos(self, elementos, pesos):
    # Verifica se os vetores têm o mesmo tamanho
        if len(elementos) != len(pesos):
           raise ValueError("Os vetores de elementos e pesos devem ter o mesmo tamanho.")

    # Cria uma lista de intervalos cumulativos com base nos pesos
        intervalos_cumulativos = []
        soma_pesos = sum(pesos)
        intervalo_acumulado = 0
        for peso in pesos:
           intervalo_acumulado += peso / soma_pesos
           intervalos_cumulativos.append(intervalo_acumulado)

    # Gera um número aleatório entre 0 e 1
        numero_aleatorio = random.random()

    # Encontra o índice do intervalo correspondente
        for i, intervalo in enumerate(intervalos_cumulativos):
          if numero_aleatorio < intervalo:
            return elementos[i]


    def __planner(self):
        """ A private method that calculates the walk actions to rescue the
        victims. Further actions may be necessary and should be added in the
        deliberata method"""

        # This is a off-line trajectory plan, each element of the list is
        # a pair dx, dy that do the agent walk in the x-axis and/or y-axis
        '''
        if (self.clt == 1):
            self.plan.append((0, 1))
            self.plan.append((1, 1))
            self.plan.append((1, 0))
            self.plan.append((1, -1))
            self.plan.append((0, -1))
            self.plan.append((-1, 0))
            self.plan.append((-1, -1))
            self.plan.append((-1, -1))
            self.plan.append((-1, 1))
            self.plan.append((1, 1))
        '''

    @property
    def deliberate(self) -> bool:
        #print("DiferençaL: " + str(self.y_atual - self.lAtual) + " sendo self.y_atual = " + str(self.y_atual) + " e self.lAtual) = " + str(self.lAtual))
        #print("DiferençaC: " + str(self.x_atual - self.cAtual) + " sendo self.x_atual = " + str(self.x_atual) + " e self.cAtual) = " + str(self.cAtual))
        decis = "None"
        volta = False
        """ This is the choice of the next action. The simulator calls this
        method at each reasonning cycle if the agent is ACTIVE.
        Must be implemented in every agent
        @return True: there's one or more actions to do
        @return False: there's no more action to do """

        if staticExplorer.checked():
            if not clustering.retornaCalculado():
                rescuerIssues.retirarVitimasRepetidas()
                #for i in range(len(rescuerIssues.finalVitimas)):
                #    print(rescuerIssues.finalVitimas[i][2][0])
                #print("-"*15)
                rescuerIssues.defineClasses(self.tree.classify().tolist())
                #for i in range(len(rescuerIssues.finalVitimas)):
                #    print(f"{i+1}: {rescuerIssues.retornaClasses()[i]}")
                self.tree.test_tree()
                clustering.k_means()

            if not self.printou_cluster:
                centroides_finais = clustering.retornaCentroides()
                atribuicoes_finais = clustering.retornaAtribuicoes()
                vitimas_sem_duplicatas = rescuerIssues.retornaFinalVitimas()

                #print("-" * 15)
                #print(f"RESCUER: {self.clt}")
                #for i, vitimas in enumerate(vitimas_sem_duplicatas):
                #    print(f"Vítima {i + 1}: ({vitimas[0]}, {vitimas[1]})")

                #print("Coordenadas dos centroides finais:")
                #for i, centroide in enumerate(centroides_finais):
                #    print(f"Centroide {i + 1}: ({centroide[0]}, {centroide[1]})")
                for i, atribuicoes in enumerate(atribuicoes_finais):
                    #print(f"Vítima {i + 1}: {atribuicoes+1}")
                    if atribuicoes+1 == self.clt:
                        # print("GUARDOU")
                        # print(f"({rescuerIssues.retornaFinalVitimas()[i][0]}, {rescuerIssues.retornaFinalVitimas()[i][1]})")
                        pessoa = [rescuerIssues.retornaFinalVitimas()[i][2][0], rescuerIssues.retornaFinalVitimas()[i][0],
                                  rescuerIssues.retornaFinalVitimas()[i][1], 0, rescuerIssues.retornaClasses()[i]]
                        self.vitimas_cluster.append(rescuerIssues.retornaFinalVitimas()[i])
                        self.pessoasClustering.append(pessoa)
                        self.kit.append(rescuerIssues.retornaFinalVitimas()[i])
                self.printou_cluster = True
                for i in range(len(self.vitimas_cluster)):
                    print(self.vitimas_cluster[i][2])
                if self.clt == 1:
                    self.nome_arquivo = "cluster1.txt"
                elif self.clt == 2:
                    self.nome_arquivo = "cluster2.txt"
                elif self.clt == 3:
                    self.nome_arquivo = "cluster3.txt"
                elif self.clt == 4:
                    self.nome_arquivo = "cluster4.txt"

                with open(self.nome_arquivo, mode='w', newline='') as arquivo:
                    writer = csv.writer(arquivo)

                    for pessoa in self.pessoasClustering:
                        writer.writerow(pessoa)

                #print(f"VITIMAS PARA SEREM RESGASTADAS: {len(self.vitimas_cluster)}")
                #for i, vitimas in enumerate(self.vitimas_cluster):
                #    print(f"({vitimas[0]}, {vitimas[1]})")
                #print("-" * 15)

                self.iniciar_socorro = True

            if(not self.check):
                  self.lMenor, self.lMaior = rescuerIssues.menorMaiorL()
                  self.cMenor, self.cMaior = rescuerIssues.menorMaiorC()
                  self.check = True
                  self.grupo = self.vitimas_cluster
                  #self.kit =  (self.vitimas_cluster).copy()


                  q = 0
                  qL = 0
                  qC = 0
                  for pos in (self.kit):
                      qL += pos[0]
                      qC += pos[1]
                      q += 1
                  self.avarageL = qL/q
                  self.avarageC = qC/q
                  print("MediaL: " + str(self.avarageL) + " MediaC: " + str(self.avarageC))
            if self.iniciar_socorro:
                '''
                if (self.x_atual != 0 or self.y_atual != 0) and not self.voltar_base:
                    self.finalStack.esvaziar_pilha()
                    self.caminhoA(0, 0)
                    self.score_volta = self.calculaScorePilha()
                    if self.rtime < (self.score_volta - 3.5):
                        print(f"Posição que parou para voltar {self.x_atual} {self.y_atual}")
                        if self.caminhoA_calculado and self.direcao_adicionada and self.plano_adicionado:
                            print("EU ESTAVA A CAMINHO DA VITIMA")
                        self.finalDirectionsQueue.clear()
                        self.plan.clear()
                        print(f"O tempo para voltar é {self.score_volta} e tenho {self.rtime}")
                        self.voltar_base = True
                        self.caminhoA_calculado = True
                        self.direcao_adicionada = False
                        self.plano_adicionado = False
                '''
                if ((self.rtime) < (abs(self.lAtual) + abs(self.cAtual)) * 3 + 15) and (self.lAtual != 0 or self.cAtual != 0) and not self.plano_adicionado:
                    #print("Esta em C: " + str(self.cAtual) + " E L: " + str(self.lAtual))
                    # print(f"RESCUER PAROU EM {self.x_atual}, {self.y_atual}")
                    # print(f"RESCUER {self.clt} VOLTANDO PARA BASE")
                    #print("base")
                    self.voltar_base = True
                    if self.caminhoA_calculado and self.direcao_adicionada and self.plano_adicionado:
                        print("EU ESTAVA A CAMINHO DA VITIMA")
                    self.finalStack.esvaziar_pilha()
                    self.finalDirectionsQueue.clear()
                    self.plan.clear()
                    self.caminhoA(0, 0)
                    self.score_volta = self.calculaScorePilha()
                    print(f"O tempo para voltar é {self.score_volta} e tenho {self.rtime}")
                    self.caminhoA_calculado = True
                    self.direcao_adicionada = False
                    self.plano_adicionado = False
                    volta = True
                elif not self.voltar_base:
                    decis = self.encontraGenetica()
                    self.finalStack.esvaziar_pilha()
                    """self.quantidade_vitimas = len(self.vitimas_cluster)
                    #print(f"RESCUER {self.clt} AINDA TEM {self.quantidade_vitimas} PARA RECUAR")
                    if self.quantidade_vitimas == 0:
                        # ELE TEM QUE VOLTAR PARA A BASE SE ELE NÃO ESTIVER NELA
                        # print(f"RESCUER PAROU EM {self.x_atual}, {self.y_atual}")
                        if self.x_atual != 0 or self.y_atual != 0:
                            self.finalStack.esvaziar_pilha()
                            # print(f"RESCUER {self.clt} VOLTANDO PARA BASE")
                            print(f"RESCUER {self.clt} salvou todas as Vítimas dele")
                            self.voltar_base = True
                            self.caminhoA(0, 0)
                    else:"""
                    # TUDO MAIOR QUE 1, TEM QUE CALCULAR O MENOR CAMINHOS ENTRE AS N VITIMAS QUE ELE PRECISA SOCORRER
                    #self.x_vitima, self.y_vitima = self.encontraMenorCaminhoEntreVitimas()
                        #self.x_vitima = self.lAtual
                        #self.y_vitima = self.cAtual
                        #self.finalStack.imprimir_pilha()

                    #self.finalQueue.print_elements()
                #self.caminhoA_calculado = True


                    #print(f"PILHA PARA A VITIMA ({self.x_vitima}, {self.y_vitima})")
                    #self.finalStack.imprimir_pilha()

                if self.voltar_base and not self.imprimiu_volta:
                    #print("PILHA DA VOLTA")
                    #self.finalStack.imprimir_pilha()
                    self.imprimiu_volta = True

                if self.caminhoA_calculado and not self.direcao_adicionada and volta:
                    """if not volta:
                        stackAux = stack()
                        while not self.finalStack.is_empty():
                            stackAux.push(self.finalStack.pop())
                        self.finalStack = stackAux
                        print("---PILHA---")
                        self.finalStack.imprimir_pilha()
                        print("----------")
                    else:"""

                    #self.finalStack.push([self.rowAtual, self.columnAtual])
                    #print("Estou em X: " + str(self.y_atual) + " Y: " + str(self.x_atual))
                    self.finalStack.push([self.y_atual, self.x_atual])
                    #print("---------")
                    #self.finalStack.imprimir_pilha()
                   # print("---------")
                    aux1 = self.finalStack.pop()
                    while not self.finalStack.is_empty():
                        aux2 = self.finalStack.pop()
                        way = [aux1[0] - aux2[0], aux1[1] - aux2[1]]
                        #print("aux1: " + str(aux1) + " aux2: " + str(aux2))
                        decisao = ""
                        if (way == [0, 1]):
                            decisao = "LEFT"
                        elif (way == [0, -1]):
                            decisao = "RIGHT"
                        elif (way == [1, 0]):
                            decisao = "UP"
                        elif (way == [-1, 0]):
                            decisao = "DOWN"
                        elif (way == [1, 1]):
                            decisao = "diagonalUL"
                        elif (way == [1, -1]):
                            decisao = "diagonalUR"
                        elif (way == [-1, 1]):
                            decisao = "diagonalDL"
                        elif (way == [-1, -1]):
                            decisao = "diagonalDR"
                        aux1 = aux2
                        self.finalDirectionsQueue.enqueue(decisao)
                    #print("------D--------")
                    #self.finalDirectionsQueue.print_elements()
                    #print("------D--------")
                    self.direcao_adicionada = True
                if not self.voltar_base:
                    #print ("Position 2: " + decis)
                    dx = 0
                    dy = 0
                    if decis == "UP":
                        dy = -1
                        dx = 0
                    elif decis == "DOWN":
                        dy = 1
                        dx = 0
                    elif decis == "RIGHT":
                        dx = 1
                        dy = 0
                    elif decis == "LEFT":
                        dx = -1
                        dy = 0
                    elif decis == "diagonalUL":
                        dy = -1
                        dx = -1
                    elif decis == "diagonalUR":
                        dy = -1
                        dx = 1
                    elif decis == "diagonalDL":
                        dy = 1
                        dx = -1
                    elif decis == "diagonalDR":
                        dy = 1
                        dx = 1
                    else:
                        print("Não existe: " + decis)
                   # self.plan.append((dx, dy))
                    result = self.body.walk(dx, dy)
                    if dx != 0 and dy != 0:
                        self.rtime -= self.COST_DIAG
                    else:
                        self.rtime -= self.COST_LINE



                    # Rescue the victim at the current position
                    if result == PhysAgent.EXECUTED:
                        self.x_atual += dx
                        self.y_atual += dy
                        # check if there is a victim at the current position
                        seq = self.body.check_for_victim()
                        if seq >= 0:
                            self.rtime -= self.COST_FIRST_AID
                            res = self.body.first_aid(seq)  # True when rescued
                            if (res):
                                string = str(seq) + ", " + str(self.x_atual)  + ", " + str(self.y_atual) + ", " + str(0) + ", " + str(0)
                                rescuerIssues.vitimaSalva(string)

                        #if (self.x_atual == self.x_vitima and self.y_atual == self.y_vitima):
                        #    self.retira_vitima(self.x_vitima, self.y_vitima)
                    return True









                #elif self.caminhoA_calculado and not self.direcao_adicionada:
                #    stackAux = StringQueue()
                #    while not self.finalStack.is_empty():
                #        queueAux

                if self.caminhoA_calculado and self.direcao_adicionada and not self.plano_adicionado:
                    while not self.finalDirectionsQueue.is_empty():
                        dx = 0
                        dy = 0
                        dec = self.finalDirectionsQueue.dequeue()
                        if dec == "UP":
                            dy = -1
                            dx = 0
                        elif dec == "DOWN":
                            dy = 1
                            dx = 0
                        elif dec == "RIGHT":
                            dx = 1
                            dy = 0
                        elif dec == "LEFT":
                            dx = -1
                            dy = 0
                        elif dec == "diagonalUL":
                            dy = -1
                            dx = -1
                        elif dec == "diagonalUR":
                            dy = -1
                            dx = 1
                        elif dec == "diagonalDL":
                            dy = 1
                            dx = -1
                        elif dec == "diagonalDR":
                            dy = 1
                            dx = 1
                        else:
                            print("Não existe: " + dec)
                        self.plan.append((dx, dy))
                    self.plano_adicionado = True

                if self.caminhoA_calculado and self.direcao_adicionada and self.plano_adicionado:
                    if self.plan == []:  # empty list, no more actions to do
                        #print("false1")
                        return False


                    # Takes the first action of the plan (walk action) and removes it from the plan
                    dx, dy = self.plan.pop(0)

                    # Walk - just one step per deliberation
                    result = self.body.walk(dx, dy)
                    if dx != 0 and dy != 0:
                        self.rtime -= self.COST_DIAG
                    else:
                        self.rtime -= self.COST_LINE

                    self.x_atual += dx
                    self.y_atual += dy
                    #print("Esta em C: " + str(self.x_atual) + " E L: " + str(self.y_atual))
                    # Rescue the victim at the current position
                    #if result == PhysAgent.EXECUTED:
                        # check if there is a victim at the current position

                        #seq = self.body.check_for_victim()
                        #if seq >= 0:
                        #    self.rtime -= self.COST_FIRST_AID
                        #    res = self.body.first_aid(seq)  # True when rescued
                        #if (self.x_atual == self.x_vitima and self.y_atual == self.y_vitima):
                        #    self.retira_vitima(self.x_vitima, self.y_vitima)
                            #print("-" * 15)
                            #print(f"RESCUER {self.clt}")
                            #print(f"VITIMAS PARA SEREM RESGASTADAS: {len(self.vitimas_cluster)}")
                            #for i, vitimas in enumerate(self.vitimas_cluster):
                            #    print(f"({vitimas[0]}, {vitimas[1]})")
                            #print("-" * 15)
                        #    self.caminhoA_calculado = False
                        #    self.direcao_adicionada = False
                        #    self.plano_adicionado = False
                    if self.x_atual == 0 and self.y_atual == 0:
                        #print("false2")
                        return False

        return True

    """def addVictim(self, l, c):
        for pos in self.salvas:
            #print("L: " + str(pos[0]) + " C: " + str(pos[1]))
            if pos[0] == l and pos[1] == c:
                return False
        self.salvas.append([l, c])
        return True"""
