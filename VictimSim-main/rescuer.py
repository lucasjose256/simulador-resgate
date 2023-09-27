##  RESCUER AGENT
### @Author: Tacla (UTFPR)
### Demo of use of VictimSim

import os
import random
from abstract_agent import AbstractAgent
from physical_agent import PhysAgent
from abc import ABC, abstractmethod
import clustering
from staticExplorer import staticExplorer
from StringQueue import StringQueue
from stack import stack

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
        self.clt = cluster  # grupo do cluster
        self.a = False
        self.b = False
        self.finalMap = []
        self.vitimas = []
        self.vitimas_cluster = []
        self.printou_cluster = False
        self.iniciou_a = False
        self.voltar = False
        self.index = 0
        self.TIMEMAX = 1
        self.row = 0
        self.column = 0
        self.rowAtual = 0
        self.columnAtual = 0
        self.l_last = 0
        self.c_last = 0
        self.verde = StringQueue()
        self.vermelho = StringQueue()
        self.finalQueue = StringQueue()
        self.finalStack = stack()
        self.finalDirectionsQueue = StringQueue()
        self.stackAux = stack()
        self.stackA = stack()
        self.stackB = stack()
        self.stackA_calculado = False
        self.stackB_calculado = False
        self.somaA = 0
        self.somaB = 0
        self.xA = 0
        self.yA = 0
        self.xB = 0
        self.yB = 0
        self.rowB = 0
        self.columnB = 0


        # Starts in IDLE state.
        # It changes to ACTIVE when the map arrives
        self.body.set_state(PhysAgent.IDLE)

        # planning
        self.__planner()

    def adicionar_coluna_sem_duplicatas(self, matriz):
        coluna_0 = [linha[0] for linha in matriz]

        for elemento in coluna_0:
            if elemento not in self.finalMap:
                self.finalMap.append(elemento)

        #print("------------------")
        #self.print_matrix()
        #print("------------------")


    def print_matrix(self):
        for row in staticExplorer.finalMap:
            for element in row:
                print(element, end=" ")  # Imprime o elemento e um espaço em branco
            print()

    def adicionar_vitimas(self, vetor):
        #self.vitimas.extend(vetor)
        #print(staticExplorer.vitimas)
        #print(self.clt)
        #staticExplorer.print_matrix()
        #print("----------------------")
        #staticExplorer.imprimeVitimas()

        '''
        for i, vitimas in enumerate(staticExplorer.vitimas):
            print(f"Vítima {i + 1}: ({vitimas[0]}, {vitimas[1]})")
        '''


    def go_save_victims(self, walls, victims):
        """ The explorer sends the map containing the walls and
        victims' location. The rescuer becomes ACTIVE. From now,
        the deliberate method is called by the environment"""
        self.body.set_state(PhysAgent.ACTIVE)

    def retira_vitima(self, x, y):
        #print(len(self.vitimas_cluster))
        self.vitimas_cluster = [vitima for vitima in self.vitimas_cluster if vitima[0] != x or vitima[1] != y]

    def score(self, lc):
        l = lc[0]
        c = lc[1]
        return (min(abs(l), abs(c)) * 1.5 + (max(abs(l), abs(c)) - (min(abs(l), abs(c))))) + (
                    min(abs(l - self.rowAtual), abs(c - self.columnAtual)) * 1.5
                    + (max(abs(l - self.rowAtual), abs(c - self.columnAtual)) - min(abs(l - self.rowAtual), abs(c - self.columnAtual))))

    def vizinhos(self, lc, l_final, c_final):
        l = lc[0]
        c = lc[1]
        if not (l == self.rowAtual and c == self.columnAtual):
            self.vet = self.verde.get_element_by_index(self.verde.find_index_by_values(l, c))
            self.vermelho.enqueue([l, c, self.vet[3], self.vet[4]])
            self.verde.dequeue()
        else:
            self.verde.dequeue()
        fila = StringQueue()
        if staticExplorer.procura_matrix([l - 1, c - 1]):
            if [l - 1, c - 1] != [l_final, c_final]:
                if (self.vermelho.find_index_by_values(l - 1, c - 1)) == -1:
                    self.verde.enqueueNotEqual([l - 1, c - 1, self.score([l - 1, c - 1]), l, c], self.vermelho)
            else:
                self.index += 1
                self.head = [l, c]
        if staticExplorer.procura_matrix([l - 1, c]):
            if [l - 1, c] != [l_final, c_final]:
                if (self.vermelho.find_index_by_values(l - 1, c)) == -1:
                    self.verde.enqueueNotEqual([l - 1, c, self.score([l - 1, c]), l, c], self.vermelho)
            else:
                self.index += 1
                self.head = [l, c]
        if staticExplorer.procura_matrix([l - 1, c + 1]):
            if [l - 1, c + 1] != [l_final, c_final]:
                if (self.vermelho.find_index_by_values(l - 1, c + 1)) == -1:
                    self.verde.enqueueNotEqual([l - 1, c + 1, self.score([l - 1, c + 1]), l, c], self.vermelho)
            else:
                self.index += 1
                self.head = [l, c]
        if staticExplorer.procura_matrix([l, c - 1]):
            if [l, c - 1] != [l_final, c_final]:
                if (self.vermelho.find_index_by_values(l, c - 1)) == -1:
                    self.verde.enqueueNotEqual([l, c - 1, self.score([l, c - 1]), l, c], self.vermelho)
            else:
                self.index += 1
                self.head = [l, c]
        if staticExplorer.procura_matrix([l, c + 1]):
            if [l, c + 1] != [l_final, c_final]:
                if (self.vermelho.find_index_by_values(l, c + 1)) == -1:
                    self.verde.enqueueNotEqual([l, c + 1, self.score([l, c + 1]), l, c], self.vermelho)
            else:
                self.index += 1
                self.head = [l, c]
        if staticExplorer.procura_matrix([l + 1, c - 1]):
            if [l + 1, c - 1] != [l_final, c_final]:
                if (self.vermelho.find_index_by_values(l + 1, c - 1)) == -1:
                    self.verde.enqueueNotEqual([l + 1, c - 1, self.score([l + 1, c - 1]), l, c], self.vermelho)
            else:
                self.index += 1
                self.head = [l, c]
        if staticExplorer.procura_matrix([l + 1, c]):
            if [l + 1, c] != [l_final, c_final]:
                if (self.vermelho.find_index_by_values(l + 1, c)) == -1:
                    self.verde.enqueueNotEqual([l + 1, c, self.score([l + 1, c]), l, c], self.vermelho)
            else:
                self.index += 1
                self.head = [l, c]
        if staticExplorer.procura_matrix([l + 1, c + 1]):
            if [l + 1, c + 1] != [l_final, c_final]:
                if (self.vermelho.find_index_by_values(l + 1, c + 1)) == -1:
                    self.verde.enqueueNotEqual([l + 1, c + 1, self.score([l + 1, c + 1]), l, c], self.vermelho)
            else:
                self.index += 1
                self.head = [l, c]

        #print("-----------------ALREADY")
        #self.alreadyA.print_elements()
        #print("-------------------")
        #print("Antes do merge")
        #self.verde.print_elements()
        #self.verde.merge_sort()
        #print("Depois do merge")
        #self.verde.print_elements()
        #print("-------------------")

    def caminhoA(self, x, y):
        l_final = x
        c_final = y
        self.verde.enqueue([self.rowAtual, self.columnAtual, self.score([self.rowAtual, self.columnAtual]), None, None], self.vermelho)
        while self.index <= 0:
            self.vizinhos(self.verde.get_element_by_index(0), l_final, c_final)
            #print(self.verde.get_element_by_index(0))

        self.l_last = self.head[0] #LINHA DO NO QUE CONECTA [0, 0]
        self.c_last = self.head[1] #COLUNA DO NO QUE CONECTA [0, 0]
        self.finalStack.push([l_final, c_final]) #IGNORA POR ENQUANTO
        self.finalQueue.enqueue([l_final, c_final])
        while self.l_last != self.rowAtual or self.c_last != self.columnAtual:
            # print("lugar", self.la, self.rowA)
            self.finalQueue.enqueue([self.l_last, self.c_last])
            self.finalStack.push([self.l_last, self.c_last]) #IGNORA POR ENQUANTO
            self.loop()
        self.finalQueue.enqueue([self.rowAtual, self.columnAtual])
        #print("-------------")
        #print(self.vitimas_cluster)
        #print(self.rowAtual, self.columnAtual)
        #print("FINAL")
        #print("FILA")
        #self.finalQueue.print_elements()
        #print("PILHA")
        #self.finalStack.imprimir_pilha()
        #print("-------------")

    def loop(self):
        aux = self.vermelho.get_element_by_index(self.vermelho.find_index_by_values(self.l_last, self.c_last))
        self.l_last = aux[2]
        self.c_last = aux[3]
        #print(self.l_last, self.c_last)

    def calcula_dois_menor(self, x1, y1, x2, y2):
        self.rowAtual = self.row
        self.columnAtual = self.column
        self.caminhoA(x1, y1)
        #self.finalStack.push([self.rowAtual, self.columnAtual])
        #self.finalStack.imprimir_pilha()
        self.stackAux = stack.copiar_pilha(self.finalStack)
        aux1 = self.finalStack.pop()
        soma = 0
        while not self.finalStack.is_empty():
            aux2 = self.finalStack.pop()
            way = [aux1[0] - aux2[0], aux1[1] - aux2[1]]
            if (way == [0, 1]):
                soma += 1
            elif (way == [0, -1]):
                soma += 1
            elif (way == [1, 0]):
                soma += 1
            elif (way == [-1, 0]):
                soma += 1
            elif (way == [1, 1]):
                soma += 1.5
            elif (way == [1, -1]):
                soma += 1.5
            elif (way == [-1, 1]):
                soma += 1.5
            elif (way == [-1, -1]):
                soma += 1.5
            aux1 = aux2
        self.stackA = stack.copiar_pilha(self.stackAux)

        stack.esvaziar_pilha(self.stackAux)
        stack.esvaziar_pilha(self.finalStack)

        self.caminhoA(x2, y2)
        #self.finalStack.push([self.rowAtual, self.columnAtual])
        #self.finalStack.imprimir_pilha()
        self.stackAux = stack.copiar_pilha(self.finalStack)
        aux1 = self.finalStack.pop()
        soma = 0
        while not self.finalStack.is_empty():
            aux2 = self.finalStack.pop()
            way = [aux1[0] - aux2[0], aux1[1] - aux2[1]]
            if (way == [0, 1]):
                soma += 1
            elif (way == [0, -1]):
                soma += 1
            elif (way == [1, 0]):
                soma += 1
            elif (way == [-1, 0]):
                soma += 1
            elif (way == [1, 1]):
                soma += 1.5
            elif (way == [1, -1]):
                soma += 1.5
            elif (way == [-1, 1]):
                soma += 1.5
            elif (way == [-1, -1]):
                soma += 1.5
            aux1 = aux2
        self.stackB = stack.copiar_pilha(self.stackAux)

        stack.esvaziar_pilha(self.stackAux)
        stack.esvaziar_pilha(self.finalStack)

        if self.somaA > self.somaB:
            self.stackB_calculado = True
            stack.esvaziar_pilha(self.stackA)
            self.xB = x2
            self.yB = y2
            self.rowVatual = x2
            self.columnVatual = y2
            return "B"
        else:
            self.stackA_calculado = True
            stack.esvaziar_pilha(self.stackB)
            self.xA = x1
            self.yA = y1
            self.rowVatual = x1
            self.columnVatual = y1
            return "A"

    def calcular_um_menor(self, x1, y1):
        self.rowAtual = self.row
        self.columnAtual = self.column
        self.caminhoA(x1, y1)
        #self.finalStack.push([self.rowAtual, self.columnAtual])
        #self.finalStack.imprimir_pilha()
        self.stackAux = stack.copiar_pilha(self.finalStack)
        aux1 = self.finalStack.pop()
        soma = 0
        while not self.finalStack.is_empty():
            aux2 = self.finalStack.pop()
            way = [aux1[0] - aux2[0], aux1[1] - aux2[1]]
            if (way == [0, 1]):
                soma += 1
            elif (way == [0, -1]):
                soma += 1
            elif (way == [1, 0]):
                soma += 1
            elif (way == [-1, 0]):
                soma += 1
            elif (way == [1, 1]):
                soma += 1.5
            elif (way == [1, -1]):
                soma += 1.5
            elif (way == [-1, 1]):
                soma += 1.5
            elif (way == [-1, -1]):
                soma += 1.5
            aux1 = aux2
        if self.stackB_calculado:
            self.stackA = stack.copiar_pilha(self.stackAux)
            self.somaA = soma
            self.xA = x1
            self.yA = y1
            self.rowVatual = x1
            self.columnVatual = y1
            self.stackA_calculado = True

        if self.stackA_calculado:
            self.stackB = stack.copiar_pilha(self.stackAux)
            self.somaB = soma
            self.xB = x1
            self.yB = y1
            self.rowVatual = x1
            self.columnVatual = y1
            self.stackB_calculado = True

        stack.esvaziar_pilha(self.stackAux)
        stack.esvaziar_pilha(self.finalStack)

        if self.somaA > self.somaB:
            self.stackA_calculado = False
            stack.esvaziar_pilha(self.stackA)
            return "B"
        else:
            self.stackB_calculado = False
            stack.esvaziar_pilha(self.stackB)
            return "A"

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
        elif (self.clt == 2):
            self.plan.append((0, 1))
            self.plan.append((0, 1))
            self.plan.append((0, 1))
            self.plan.append((0, 1))
            self.plan.append((0, 1))
        '''

    @property
    def deliberate(self) -> bool:
        """ This is the choice of the next action. The simulator calls this
        method at each reasonning cycle if the agent is ACTIVE.
        Must be implemented in every agent
        @return True: there's one or more actions to do
        @return False: there's no more action to do """

        
        #for i, vitimas in enumerate(self.vitimas_cluster):
        #    print(f"Vítima {i + 1}: ({vitimas[0]}, {vitimas[1]})")
        

        if staticExplorer.checked():
            staticExplorer.remover_duplicatas()
            if not clustering.ret_calculado():
                clustering.k_means()
                clustering.clustering_calculado()
            #for i, vitimas in enumerate(staticExplorer.vitFinal):
            #    print(f"Vítima {i + 1}: ({vitimas[0]}, {vitimas[1]})")

            if not self.printou_cluster:
                centroides_finais = clustering.ret_centroides()
                atribuicoes_finais = clustering.ret_atribuicoes()
                vitimas_sem_duplicatas = staticExplorer.returnVitFinal()

                print("-------------------------------------------")
                print(f"RESCUER: {self.clt}")
                for i, vitimas in enumerate(vitimas_sem_duplicatas):
                    print(f"Vítima {i + 1}: ({vitimas[0]}, {vitimas[1]})")

                print("Coordenadas dos centroides finais:")
                for i, centroide in enumerate(centroides_finais):
                    print(f"Centroide {i + 1}: ({centroide[0]}, {centroide[1]})")
                for i, atribuicoes in enumerate(atribuicoes_finais):
                    print(f"Vítima {i + 1}: {atribuicoes+1}")
                    if atribuicoes+1 == self.clt:
                        print("GUARDOU")
                        print(staticExplorer.returnVitFinal()[i])
                        self.vitimas_cluster.append(staticExplorer.returnVitFinal()[i])
                #for i, vitimas in enumerate(self.vitimas_cluster):
                #    print(f"Vítima {i + 1}: ({vitimas[0]}, {vitimas[1]})")
                #print("--------------------------------")
                self.printou_cluster = True
        print(self.vitimas_cluster)
        '''
        if not self.iniciou_a:
            i = 0
            menor = ''
            if self.voltar:
                self.caminhoA(0, 0)

            else:
                for i in range(len(self.vitimas_cluster)):
                    if i == 0 and len(self.vitimas_cluster) > 1:
                        menor = self.calcula_dois_menor(self.vitimas_cluster[i][0], self.vitimas_cluster[i][1], self.vitimas_cluster[i+1][0], self.vitimas_cluster[i+1][1])
                        i += 2
                    elif i == 0 and len(self.vitimas_cluster) == 1:
                        menor == "C"
                        self.rowVatual = self.vitimas_cluster[i][1]
                        self.columnVatual = self.vitimas_cluster[i][1]
                        self.caminhoA(self.vitimas_cluster[i][0], self.vitimas_cluster[i][1])
                    else:
                        menor = self.calcular_um_menor(self.vitimas_cluster[i][0], self.vitimas_cluster[i][1])
                        i += 1

                if menor == "A":
                    self.finalStack = stack.copiar_pilha(self.stackA)
                elif menor == "B":
                    self.finalStack = stack.copiar_pilha(self.stackB)
                #elif menor == "C":
                    #self.finalStack.push([self.rowAtual, self.columnAtual])

            #self.finalStack.push([self.rowAtual, self.columnAtual])
            #self.finalStack.imprimir_pilha()
            #print("------------------")

            aux1 = self.finalStack.pop()
            while not self.finalStack.is_empty():
                aux2 = self.finalStack.pop()
                # print("aux1: ", aux1, "aux2: ", aux2)
                way = [aux1[0] - aux2[0], aux1[1] - aux2[1]]
                # print("aux1: ", aux1, "aux2: ", aux2, "way:", way)
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
                # print("Decisao:", decisao)
                aux1 = aux2
                self.finalDirectionsQueue.enqueue(decisao)
            self.iniciou_a = True
            self.a = True
            #self.finalDirectionsQueue.print_elements()
            #print("-------------------------")

        if self.a:
            if not self.finalDirectionsQueue.is_empty():
                dx = 0
                dy = 0
                dec = self.finalDirectionsQueue.dequeue()
                if self.finalDirectionsQueue.is_empty():
                    self.a = False
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
                self.plan.append((dx, dy))
            self.b = True


        # No more actions to do
        if self.b:
            if self.plan == []:  # empty list, no more actions to do
                return False

            # Takes the first action of the plan (walk action) and removes it from the plan
            dx, dy = self.plan.pop(0)

            # Walk - just one step per deliberation
            result = self.body.walk(dx, dy)
            if dx != 0 and dy != 0:
                self.rtime -= self.COST_DIAG
            else:
                self.rtime -= self.COST_LINE

            # Rescue the victim at the current position
            if result == PhysAgent.EXECUTED:
                # check if there is a victim at the current position
                self.rowB += dx
                self.columnB += dy
                aux3 = staticExplorer.retornaNumLinhas()
                self.contRow = aux3
                seq = self.body.check_for_victim()
                if seq >= 0:
                    self.rtime -= self.COST_FIRST_AID
                    res = self.body.first_aid(seq)  # True when rescued
                    self.retira_vitima(self.rowB, self.columnB)
                if (self.rowVatual == self.rowB and self.columnVatual == self.rowB):
                    self.b = False
                    self.iniciou_a = False
                    self.voltar = True

            return True
        '''

        # No more actions to do
        if self.plan == []:  # empty list, no more actions to do
            return False

        # Takes the first action of the plan (walk action) and removes it from the plan
        dx, dy = self.plan.pop(0)

        # Walk - just one step per deliberation
        result = self.body.walk(dx, dy)

        # Rescue the victim at the current position
        if result == PhysAgent.EXECUTED:
            # check if there is a victim at the current position
            seq = self.body.check_for_victim()
            if seq >= 0:
                res = self.body.first_aid(seq)  # True when rescued

        return True