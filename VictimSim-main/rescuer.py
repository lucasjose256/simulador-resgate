##  RESCUER AGENT
### @Author: Tacla (UTFPR)
### Demo of use of VictimSim

import os
import random
from abstract_agent import AbstractAgent
from physical_agent import PhysAgent
from abc import ABC, abstractmethod
import clustering
from static_explorer import staticExplorer
from string_queue import StringQueue
from stack import stack
from rescuer_issues import rescuerIssues

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
                    min(abs(l - self.rowAtual), abs(c - self.columnAtual)) * 1.5
                    + (max(abs(l - self.rowAtual), abs(c - self.columnAtual)) - min(abs(l - self.rowAtual), abs(c - self.columnAtual))))

    def vizinhos(self, lc, l_final, c_final, verde, vermelho):
        l = lc[0]
        c = lc[1]
        if not (l == self.rowAtual and c == self.columnAtual):
            vet = verde.get_element_by_index(verde.find_index_by_values(l, c))
            vermelho.enqueue([l, c, vet[3], vet[4]])
            verde.dequeue()
        else:
            verde.dequeue()
        if rescuerIssues.procuraFinalMap([l - 1, c - 1]):
            if [l - 1, c - 1] != [l_final, c_final]:
                if (vermelho.find_index_by_values(l - 1, c - 1)) == -1:
                    verde.enqueueNotEqual([l - 1, c - 1, self.score([l - 1, c - 1]), l, c], vermelho)
            else:
                self.index += 1
                self.head = [l, c]
        if rescuerIssues.procuraFinalMap([l - 1, c]):
            if [l - 1, c] != [l_final, c_final]:
                if (vermelho.find_index_by_values(l - 1, c)) == -1:
                    verde.enqueueNotEqual([l - 1, c, self.score([l - 1, c]), l, c], vermelho)
            else:
                self.index += 1
                self.head = [l, c]
        if rescuerIssues.procuraFinalMap([l - 1, c + 1]):
            if [l - 1, c + 1] != [l_final, c_final]:
                if (vermelho.find_index_by_values(l - 1, c + 1)) == -1:
                    verde.enqueueNotEqual([l - 1, c + 1, self.score([l - 1, c + 1]), l, c], vermelho)
            else:
                self.index += 1
                self.head = [l, c]
        if rescuerIssues.procuraFinalMap([l, c - 1]):
            if [l, c - 1] != [l_final, c_final]:
                if (vermelho.find_index_by_values(l, c - 1)) == -1:
                    verde.enqueueNotEqual([l, c - 1, self.score([l, c - 1]), l, c], vermelho)
            else:
                self.index += 1
                self.head = [l, c]
        if rescuerIssues.procuraFinalMap([l, c + 1]):
            if [l, c + 1] != [l_final, c_final]:
                if (vermelho.find_index_by_values(l, c + 1)) == -1:
                    verde.enqueueNotEqual([l, c + 1, self.score([l, c + 1]), l, c], vermelho)
            else:
                self.index += 1
                self.head = [l, c]
        if rescuerIssues.procuraFinalMap([l + 1, c - 1]):
            if [l + 1, c - 1] != [l_final, c_final]:
                if (vermelho.find_index_by_values(l + 1, c - 1)) == -1:
                    verde.enqueueNotEqual([l + 1, c - 1, self.score([l + 1, c - 1]), l, c], vermelho)
            else:
                self.index += 1
                self.head = [l, c]
        if rescuerIssues.procuraFinalMap([l + 1, c]):
            if [l + 1, c] != [l_final, c_final]:
                if (vermelho.find_index_by_values(l + 1, c)) == -1:
                    verde.enqueueNotEqual([l + 1, c, self.score([l + 1, c]), l, c], vermelho)
            else:
                self.index += 1
                self.head = [l, c]
        if rescuerIssues.procuraFinalMap([l + 1, c + 1]):
            if [l + 1, c + 1] != [l_final, c_final]:
                if (vermelho.find_index_by_values(l + 1, c + 1)) == -1:
                    verde.enqueueNotEqual([l + 1, c + 1, self.score([l + 1, c + 1]), l, c], vermelho)
            else:
                self.index += 1
                self.head = [l, c]
        verde.merge_sort()

    def caminhoA(self, x, y):
        l_final = x
        c_final = y
        verde = StringQueue()
        vermelho = StringQueue()
        self.rowAtual = self.x_atual
        self.columnAtual = self.y_atual
        self.index = 0
        self.head[0] = 0
        self.head[1] = 0
        verde.enqueue([self.rowAtual, self.columnAtual, self.score([self.rowAtual, self.columnAtual]), None, None], vermelho)
        while self.index <= 0:
            self.vizinhos(verde.get_element_by_index(0), l_final, c_final, verde, vermelho)
            #print(self.verde.get_element_by_index(0))

        self.l_last = self.head[0] #LINHA DO NO QUE CONECTA [0, 0]
        self.c_last = self.head[1] #COLUNA DO NO QUE CONECTA [0, 0]
        self.finalStack.push([l_final, c_final]) #IGNORA POR ENQUANTO
        # self.finalQueue.enqueue([l_final, c_final])
        while self.l_last != self.rowAtual or self.c_last != self.columnAtual:
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
        pilha.push([self.rowAtual, self.columnAtual])
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
        """ This is the choice of the next action. The simulator calls this
        method at each reasonning cycle if the agent is ACTIVE.
        Must be implemented in every agent
        @return True: there's one or more actions to do
        @return False: there's no more action to do """

        if staticExplorer.checked():
            if not clustering.retornaCalculado():
                rescuerIssues.retirarVitimasRepetidas()
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
                        self.vitimas_cluster.append(rescuerIssues.retornaFinalVitimas()[i])
                self.printou_cluster = True
                #print(f"VITIMAS PARA SEREM RESGASTADAS: {len(self.vitimas_cluster)}")
                #for i, vitimas in enumerate(self.vitimas_cluster):
                #    print(f"({vitimas[0]}, {vitimas[1]})")
                #print("-" * 15)

                self.iniciar_socorro = True

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
                if (self.rtime < (abs(self.x_atual) + abs(self.y_atual)) * 1.75 + 10) and (self.x_atual != 0 or self.y_atual != 0) and not self.voltar_base:
                    # print(f"RESCUER PAROU EM {self.x_atual}, {self.y_atual}")
                    # print(f"RESCUER {self.clt} VOLTANDO PARA BASE")
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
                

                if not self.caminhoA_calculado and not self.voltar_base:
                    self.quantidade_vitimas = len(self.vitimas_cluster)
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
                    elif self.quantidade_vitimas == 1:
                        # PEGA ESSA UNICA VITIMA E CALCULA O MENOR CAMINHO ATE ELA
                        self.finalStack.esvaziar_pilha()
                        self.caminhoA(self.vitimas_cluster[0][0], self.vitimas_cluster[0][1])
                        self.x_vitima = self.vitimas_cluster[0][0]
                        self.y_vitima = self.vitimas_cluster[0][1]
                    else:
                        # TUDO MAIOR QUE 1, TEM QUE CALCULAR O MENOR CAMINHOS ENTRE AS N VITIMAS QUE ELE PRECISA SOCORRER
                        self.x_vitima, self.y_vitima = self.encontraMenorCaminhoEntreVitimas()
                    #self.finalQueue.print_elements()
                    self.caminhoA_calculado = True
                    #print(f"PILHA PARA A VITIMA ({self.x_vitima}, {self.y_vitima})")
                    #self.finalStack.imprimir_pilha()

                if self.voltar_base and not self.imprimiu_volta:
                    #print("PILHA DA VOLTA")
                    #self.finalStack.imprimir_pilha()
                    self.imprimiu_volta = True

                if self.caminhoA_calculado and not self.direcao_adicionada:
                    self.finalStack.push([self.rowAtual, self.columnAtual])
                    aux1 = self.finalStack.pop()
                    while not self.finalStack.is_empty():
                        aux2 = self.finalStack.pop()
                        way = [aux1[0] - aux2[0], aux1[1] - aux2[1]]
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
                        #self.finalDirectionsQueue.print_elements()
                    self.direcao_adicionada = True

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
                        self.plan.append((dx, dy))
                    else:
                        self.plano_adicionado = True

                if self.caminhoA_calculado and self.direcao_adicionada and self.plano_adicionado:
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
                        self.x_atual += dy
                        self.y_atual += dx
                        seq = self.body.check_for_victim()
                        if seq >= 0:
                            self.rtime -= self.COST_FIRST_AID
                            res = self.body.first_aid(seq)  # True when rescued
                        if (self.x_atual == self.x_vitima and self.y_atual == self.y_vitima):
                            self.retira_vitima(self.x_vitima, self.y_vitima)
                            #print("-" * 15)
                            #print(f"RESCUER {self.clt}")
                            #print(f"VITIMAS PARA SEREM RESGASTADAS: {len(self.vitimas_cluster)}")
                            #for i, vitimas in enumerate(self.vitimas_cluster):
                            #    print(f"({vitimas[0]}, {vitimas[1]})")
                            #print("-" * 15)
                            self.caminhoA_calculado = False
                            self.direcao_adicionada = False
                            self.plano_adicionado = False

        return True