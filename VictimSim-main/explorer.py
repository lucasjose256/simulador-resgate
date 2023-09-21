## EXPLORER AGENT
### @Author: Tacla, UTFPR
### It walks randomly in the environment looking for victims.

import sys
import os
import random
import math

from ExplorerDrawnMap import ExplorerDrawnMap
from abstract_agent import AbstractAgent
from physical_agent import PhysAgent
from abc import ABC, abstractmethod

from stack import stack
from StringQueue import StringQueue
from staticExplorer import staticExplorer


class Explorer(AbstractAgent):
    def __init__(self, env, config_file, resc, direcao):
        """ Construtor do agente random on-line
        @param env referencia o ambiente
        @config_file: the absolute path to the explorer's config file
        @param resc referencia o rescuer para poder acorda-lo
        """

        super().__init__(env, config_file)

        # Specific initialization for the rescuer
        staticExplorer.addAgent()
        self.c = False #FLAG QUE AVISA QUE O EXPLORADOR CHEGOU NA BASE NO FINAL DO ALGORITMO A*
        self.resc = resc  # reference to the rescuer agent
        self.rtime = self.TLIM  # remaining time to explore
        self.explorer_map = ExplorerDrawnMap()
        self.explorer_map.draw(0, 0, 0, 0, "NONE")
        self.row = 0
        self.column = 0
        self.rowA = 0 #SALVA A POSIÇAO DE INICIO PARA A*
        self.columnA = 0 #SALVA A POSIÇAO DE INICIO PARA A*
        self.stack = stack()
        self.a = False #FLAG PARA AVISAR PARA IF PROXIMO QUE COMEÇOU A* em DELIBERATE E QUE NAO PODE IR PARA O CODIGO DFS ONLINE
        self.verde = StringQueue()
        self.vermelho = StringQueue()
        self.head = 0 #SALVA O NO QUE ENCONTRO [0, 0] EM A*
        self.index = 0 #FLAG PARA DIZER SE [0, 0] FOI ENCONTRADO EM A*
        self.b = False #FLAG PARA AVISAR PARA IF PROXIMO QUE COMEÇOU A* em DELIBERATE E QUE NAO PODE IR PARA O CODIGO DFS ONLINE
        self.finalQueue = StringQueue()
        self.la = 0
        self.cb = 0
        self.finalStack = stack()
        self.finalDirectionsQueue = StringQueue()
        self.dir = direcao
        self.vit = []
        self.TIMEMAX = 1
        self.contRow = 1
        self.d = False #FLAG QUE REPETE A FUNÇAO DELIBERATE ATE TODOS EXPLORADORES CHEGARAM AI CHAMANDO OS RESCUERS
        #static agents += 1

    #def score(self, lc):
    #    l = lc[0]
    #    c = lc[1]
    #    return (min(abs(l), abs(c)) * 1.5 + (max(abs(l), abs(c)) - (min(abs(l), abs(c))))) + (
    #                min(abs(l - self.rowA), abs(c - self.columnA)) * 1.5
    #                + (max(abs(l - self.rowA), abs(c - self.columnA)) - min(abs(l - self.rowA), abs(c - self.columnA))))

    def score(self, lc):
        l = lc[0]
        c = lc[1]
        return (min(abs(l), abs(c)) * 1.5 + (max(abs(l), abs(c)) - (min(abs(l), abs(c))))) + (
                    min(abs(l - self.rowA), abs(c - self.columnA)) * 1.5
                    + (max(abs(l - self.rowA), abs(c - self.columnA)) - min(abs(l - self.rowA), abs(c - self.columnA))))


    def adicionar_elementos(self, vetor):
        self.vit.append(vetor)
        #print(self.vit)

    def vizinhos(self, lc):
        l = lc[0]
        c = lc[1]
        # print(l, c)
        # self.explorer_map.print_matrix()
        # print(l, c, "DEPOIS", self.rowA, self.columnA)
        #self.alreadyA.print_elements()
        if not (l == self.rowA and c == self.columnA):
            # print("------------------------------------------------------------------")
            #self.queueA.print_elements()
            # print("Achou ", self.queueA.get_element_by_index(self.queueA.find_index_by_values(l, c)))
            # print("-----------")
            self.vet = self.verde.get_element_by_index(self.verde.find_index_by_values(l, c))
            # print("Achou vet ", self.vet)
            self.vermelho.enqueue([l, c, self.vet[3], self.vet[4]])
            self.verde.dequeue()
        else:
            self.verde.dequeue()
        fila = StringQueue()
        if self.explorer_map.find_row_with_right([l - 1, c - 1]) != "FALSE":
            if [l - 1, c - 1] != [0, 0]:
                if (self.vermelho.find_index_by_values(l - 1, c - 1)) == -1:
                    self.verde.enqueueNotEqual([l - 1, c - 1, self.score([l - 1, c - 1]), l, c], self.vermelho)
            else:
                self.index += 1
                self.head = [l, c]
        if self.explorer_map.find_row_with_right([l - 1, c]) != "FALSE":
            if [l - 1, c] != [0, 0]:
                if (self.vermelho.find_index_by_values(l - 1, c)) == -1:
                    self.verde.enqueueNotEqual([l - 1, c, self.score([l - 1, c]), l, c], self.vermelho)
            else:
                self.index += 1
                self.head = [l, c]
        if self.explorer_map.find_row_with_right([l - 1, c + 1]) != "FALSE":
            if [l - 1, c + 1] != [0, 0]:
                if (self.vermelho.find_index_by_values(l - 1, c + 1)) == -1:
                    self.verde.enqueueNotEqual([l - 1, c + 1, self.score([l - 1, c + 1]), l, c], self.vermelho)
            else:
                self.index += 1
                self.head = [l, c]
        if self.explorer_map.find_row_with_right([l, c - 1]) != "FALSE":
            if [l, c - 1] != [0, 0]:
                if (self.vermelho.find_index_by_values(l, c - 1)) == -1:
                    self.verde.enqueueNotEqual([l, c - 1, self.score([l, c - 1]), l, c], self.vermelho)
            else:
                self.index += 1
                self.head = [l, c]
        if self.explorer_map.find_row_with_right([l, c + 1]) != "FALSE":
            if [l, c + 1] != [0, 0]:
                if (self.vermelho.find_index_by_values(l, c + 1)) == -1:
                    self.verde.enqueueNotEqual([l, c + 1, self.score([l, c + 1]), l, c], self.vermelho)
            else:
                self.index += 1
                self.head = [l, c]
        if self.explorer_map.find_row_with_right([l + 1, c - 1]) != "FALSE":
            if [l + 1, c - 1] != [0, 0]:
                if (self.vermelho.find_index_by_values(l + 1, c - 1)) == -1:
                    self.verde.enqueueNotEqual([l + 1, c - 1, self.score([l + 1, c - 1]), l, c], self.vermelho)
            else:
                self.index += 1
                self.head = [l, c]
        if self.explorer_map.find_row_with_right([l + 1, c]) != "FALSE":
            if [l + 1, c] != [0, 0]:
                if (self.vermelho.find_index_by_values(l + 1, c)) == -1:
                    self.verde.enqueueNotEqual([l + 1, c, self.score([l + 1, c]), l, c], self.vermelho)
            else:
                self.index += 1
                self.head = [l, c]
        if self.explorer_map.find_row_with_right([l + 1, c + 1]) != "FALSE":
            if [l + 1, c + 1] != [0, 0]:
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
        self.verde.merge_sort()
        #print("Depois do merge")
        #self.verde.print_elements()
        #print("-------------------")

    def caminhoA(self):
        self.explorer_map.remove_rows_with_incorrect_columns()
        self.verde.enqueue([self.rowA, self.columnA, self.score([self.rowA, self.columnA]), None, None], self.vermelho)
        self.index = 0

        while self.index <= 0:
            self.vizinhos(self.verde.get_element_by_index(0))
            #print("loop")

        self.la = self.head[0] #LINHA DO NO QUE CONECTA [0, 0]
        self.cb = self.head[1] #COLUNA DO NO QUE CONECTA [0, 0]
        self.finalStack.push([0, 0]) #IGNORA POR ENQUANTO
        self.finalQueue.enqueue([0, 0])
        while self.la != self.rowA or self.cb != self.columnA:
            # print("lugar", self.la, self.rowA)
            self.finalQueue.enqueue([self.la, self.cb])
            self.finalStack.push([self.la, self.cb]) #IGNORA POR ENQUANTO
            self.loop()
        self.finalQueue.enqueue([self.rowA, self.columnA])
        #self.finalQueue.print_elements()

    def loop(self):
        # print(self.la, self.cb)
        aux = self.vermelho.get_element_by_index(self.vermelho.find_index_by_values(self.la, self.cb))
        # print(aux)
        self.la = aux[2]
        self.cb = aux[3]
        #print(self.la, self.cb)

    @property
    def deliberate(self) -> bool:
        """ The agent chooses the next action. The simulator calls this
        method at each cycle. Must be implemented in every agent"""
        if self.d and staticExplorer.checked():
            # self.resc.adicionar_coluna_sem_duplicatas(self.explorer_map.matrix_list)]
            print("Decisao: ", self.dir, "Vitimas: ", len(self.vit))
            staticExplorer.addFinalMap(self.explorer_map.matrix_list)
            self.resc.go_save_victims([], [])
            staticExplorer.addVitimas(self.vit)
            #self.resc.adicionar_vitimas(self.vit)
            return False
        elif (self.d):
            return True
        # No more actions, time almost ended
        if self.c:
            # time to wake up the rescuer
            # pass the walls and the victims (here, they're empty)
            staticExplorer.agentArrived()
            self.d = True
            print(f"{self.NAME} I believe I've remaining time of {self.rtime:.1f}")
            return True
       # elif self.c and not staticExplorer.checked():
        #    self.body.walk(0, 0)
        #    return True

        if self.rtime < ((min(abs(self.row), abs(self.column)) * 1.5 + (max(abs(self.row), abs(self.column)) - (min(abs(self.row), abs(self.column))))))*2 and not self.a:


            #ALGORITMO A*
            self.rowA = self.row   #SALVA A LINHA QUE ELE ESTÁ NO MOMENTO QUE PAROU O DFS ONLINE
            self.columnA = self.column   #SALVA A COLUNA QUE ELE ESTÁ NO MOMENTO QUE PAROU O DFS ONLINE
            self.a = True #FLAG PARA AVISAR PARA IF PROXIMO QUE COMEÇOU A* em DELIBERATE
            self.b = True #FLAG PARA AVISAR PARA IF PROXIMO QUE COMEÇOU A* em DELIBERATE
            self.caminhoA() #COMEÇA PRIMEIRA PARTE DO A* DE EXPLORAR CAMINHOS COM BASE NO "SCORE"

            #PARA FAZER O ALGORITMO ANALISAR AS 5 LINHAS ACIMA + CAMINHOA() + VIZINHOS() + LOOPS()

            #---------------------------------------------------------------------------------------------------



            #print(self.head)
            #self.vermelho.print_elements()
            #print("-------------------------------")
            #self.finalQueue.print_elements()
            self.finalStack.push([self.rowA, self.columnA])
            aux1 = self.finalStack.pop()

            while not self.finalStack.is_empty():
                aux2 = self.finalStack.pop()
                #print("aux1: ", aux1, "aux2: ", aux2)
                way = [aux1[0] - aux2[0], aux1[1] - aux2[1]]
                #print("aux1: ", aux1, "aux2: ", aux2, "way:", way)
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
                #print("Decisao:", decisao)
                aux1 = aux2
                self.finalDirectionsQueue.enqueue(decisao)

        if self.a and self.b:
         if not self.finalDirectionsQueue.is_empty():
            dx = 0
            dy = 0
            dec = self.finalDirectionsQueue.dequeue()
            if self.finalDirectionsQueue.is_empty():
                self.c = True
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

            result = self.body.walk(dx, dy)
            # Update remaining time
            if dx != 0 and dy != 0:
                self.rtime -= self.COST_DIAG
            else:
                self.rtime -= self.COST_LINE

            return True
         else:
             return True

        decision = self.explorer_map.information(self.row, self.column, self.dir)
        # print(decision)
        if decision is None:
            decision = self.stack.pop()
            # print(decision)
        if decision == "UP" or decision == "UP STACK":
            dy = -1
            dx = 0
        elif decision == "DOWN" or decision == "DOWN STACK":
            dy = 1
            dx = 0
        elif decision == "RIGHT" or decision == "RIGHT STACK":
            dx = 1
            dy = 0
        elif decision == "LEFT" or decision == "LEFT STACK":
            dx = -1
            dy = 0
        else:
            dx = 0
            dy = 0

        # dx = random.choice([-1, 0, 1])

        # if dx == 0:
        #   dy = random.choice([-1, 1])
        # else:
        #   dy = random.choice([-1, 0, 1])

        # Check the neighborhood obstacles
        obstacles = self.body.check_obstacles()

        # Moves the body to another position
        result = self.body.walk(dx, dy)
        aux3 = self.explorer_map.contar_linhas_colunas()
        # Update remaining time
        if dx != 0 and dy != 0:
            self.rtime -= self.COST_DIAG
            self.TIMEMAX += 0.23*(aux3 - self.contRow)
        else:
            self.rtime -= self.COST_LINE
            self.TIMEMAX += 0.1*(aux3 - self.contRow)

        self.contRow = aux3
        # Test the result of the walk action
        if result == PhysAgent.BUMPED:
            walls = 1  # build the map- to do
            # print(self.name() + ": wall or grid limit reached")
            if dy == 1:
                self.explorer_map.draw(self.row, self.column, self.row + 1, "NULL", "DOWN")
            elif dy == -1:
                self.explorer_map.draw(self.row, self.column, self.row - 1, "NULL", "UP")
            if dx == 1:
                self.explorer_map.draw(self.row, self.column, "NULL", self.column + 1, "RIGHT")
            elif dx == -1:
                self.explorer_map.draw(self.row, self.column, "NULL", self.column - 1, "LEFT")

        if result == PhysAgent.EXECUTED:
            if decision == "DOWN":
                self.stack.push("UP STACK")
            elif decision == "UP":
                self.stack.push("DOWN STACK")
            if decision == "RIGHT":
                self.stack.push("LEFT STACK")
            elif decision == "LEFT":
                self.stack.push("RIGHT STACK")
            # check for victim returns -1 if there is no victim or the sequential
            # the sequential number of a found victim
            aux = False
            seq = self.body.check_for_victim()
            if seq >= 0:
                aux = True
                vs = self.body.read_vital_signals(seq)
                self.rtime -= self.COST_READ
                # print("exp: read vital signals of " + str(seq))
                # print(vs)
            if dy == 1:
                self.explorer_map.draw(self.row, self.column, self.row + 1, self.column, "DOWN")
                self.row += 1
            elif dy == -1:
                self.explorer_map.draw(self.row, self.column, self.row - 1, self.column, "UP")
                self.row -= 1
            if dx == 1:
                self.explorer_map.draw(self.row, self.column, self.row, self.column + 1, "RIGHT")
                self.column += 1
            elif dx == -1:
                self.explorer_map.draw(self.row, self.column, self.row, self.column - 1, "LEFT")
                self.column -= 1
            if(aux):
                self.adicionar_elementos([self.row, self.column , vs])
        # print("-------------------------------------------\n")
        # self.explorer_map.print_matrix()
        # print("-------------------------------------------\n")

        return True

