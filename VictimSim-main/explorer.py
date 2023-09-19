## EXPLORER AGENT
### @Author: Tacla, UTFPR
### It walks randomly in the environment looking for victims.

import sys
import os
import random


from ExplorerDrawnMap import ExplorerDrawnMap
from abstract_agent import AbstractAgent
from physical_agent import PhysAgent
from abc import ABC, abstractmethod

from stack import stack
from StringQueue import StringQueue



class Explorer(AbstractAgent):
    def __init__(self, env, config_file, resc):
        """ Construtor do agente random on-line
        @param env referencia o ambiente
        @config_file: the absolute path to the explorer's config file
        @param resc referencia o rescuer para poder acorda-lo
        """

        super().__init__(env, config_file)

        # Specific initialization for the rescuer
        self.resc = resc           # reference to the rescuer agent
        self.rtime = self.TLIM     # remaining time to explore
        self.explorer_map = ExplorerDrawnMap()
        self.explorer_map.draw(0, 0, 0, 0, "NONE")
        self.row = 0
        self.column = 0
        self.rowA = 0
        self.columnA = 0
        self.stack = stack()
        self.a = False
        self.queueA = StringQueue()
        self.alreadyA = StringQueue()
        self.head = 0
        self.index = 0
        self.b = True
        self.finalQueue = StringQueue()
        self.la = 0
        self.cb = 0

    def score(self ,lc):
        l = lc[0]
        c = lc[1]
        return (min(abs(l), abs(c))*1.5 + (max(abs(l),abs(c)) - (min(abs(l), abs(c))))) + (min(abs(l - self.rowA), abs(c - self.columnA))*1.5
        + (max(abs(l - self.rowA), abs(c - self.columnA)) - min(abs(l - self.rowA), abs(c - self.columnA))))

    def vizinhos(self, lc):
        l = lc[0]
        c = lc[1]
        print(l, c)
        self.explorer_map.print_matrix()
        #print(l, c, "DEPOIS", self.rowA, self.columnA)
        if l != self.rowA or c != self.columnA:
             #print("------------------------------------------------------------------")
             self.queueA.print_elements()
             #print("Achou ", self.queueA.get_element_by_index(self.queueA.find_index_by_values(l, c)))
             #print("-----------")
             self.vet = self.queueA.get_element_by_index(self.queueA.find_index_by_values(l, c))
             #print("Achou vet ", self.vet)
             self.alreadyA.enqueue([l, c, self.vet[3], self.vet[4]])
             self.queueA.dequeue()
        else:
            self.queueA.dequeue()
        fila = StringQueue()
        if self.explorer_map.find_row_with_right([l - 1, c - 1]) != "FALSE":
            if [l -1, c -1] != [0, 0]:
                if(self.alreadyA.find_index_by_values(l -1, c - 1)) != -1:
                     self.queueA.enqueue([l - 1, c - 1, self.score([l - 1, c - 1]), l, c], self.alreadyA)
            else:
                self.index += 1
                self.head = [l, c]
        if self.explorer_map.find_row_with_right([l - 1, c ]) != "FALSE":
            if [l -1, c] != [0, 0]:
                if(self.alreadyA.find_index_by_values(l -1, c)) != -1:
                     self.queueA.enqueue([l -1, c , self.score([l -1, c ]), l, c], self.alreadyA)
            else:
                self.index += 1
                self.head = [l, c]
        if self.explorer_map.find_row_with_right([l -1, c +1]) != "FALSE":
            if [l -1, c +1] != [0, 0]:
                if(self.alreadyA.find_index_by_values(l -1, c + 1)) != -1:
                     self.queueA.enqueue([l -1, c +1, self.score([l -1, c +1]), l, c], self.alreadyA)
            else:
                self.index += 1
                self.head = [l, c]
        if self.explorer_map.find_row_with_right([l, c -1]) != "FALSE":
            if [l , c -1] != [0, 0]:
                if(self.alreadyA.find_index_by_values(l, c-1)) != -1:
                     self.queueA.enqueue([l, c -1, self.score([l, c -1]), l, c], self.alreadyA)
            else:
                self.index += 1
                self.head = [l, c]
        if self.explorer_map.find_row_with_right([l, c + 1]) != "FALSE":
            if [l , c +1] != [0, 0]:
                if(self.alreadyA.find_index_by_values(l , c+1)) != -1:
                     self.queueA.enqueue([l, c + 1, self.score([l, c + 1]), l, c], self.alreadyA)
            else:
                self.index += 1
                self.head = [l, c]
        if self.explorer_map.find_row_with_right([l +1, c -1]) != "FALSE":
            if [l + 1, c - 1] != [0, 0]:
                if(self.alreadyA.find_index_by_values(l +1, c-1)) != -1:
                     self.queueA.enqueue([l +1, c -1, self.score([l +1, c -1]), l, c], self.alreadyA)
            else:
                self.index += 1
                self.head = [l, c]
        if self.explorer_map.find_row_with_right([l +1, c]) != "FALSE":
            if [l + 1, c] != [0, 0]:
                if(self.alreadyA.find_index_by_values(l +1, c)) != -1:
                     self.queueA.enqueue([l +1, c, self.score([l +1, c]), l, c], self.alreadyA)
            else:
                self.index += 1
                self.head = [l, c]
        if self.explorer_map.find_row_with_right([l +1, c +1]) != "FALSE":
            if [l + 1, c + 1] != [0, 0]:
                if(self.alreadyA.find_index_by_values(l +1, c+ 1)) != -1:
                     self.queueA.enqueue([l +1, c +1, self.score([l +1, c +1]), l, c], self.alreadyA)
            else:
                self.index += 1
                self.head = [l, c]
        #print("Antes do merge")
        self.queueA.print_elements()
        self.queueA.merge_sort()
        #print("Depois do merge")
        #self.queueA.print_elements()

    def caminhoA(self):
        self.explorer_map.remove_string_rows()
        self.queueA.enqueue([self.rowA, self.columnA, self.score([self.rowA, self.columnA]), None, None], self.alreadyA)
        self.index = 0

        while self.index <= 0:
            self.vizinhos(self.queueA.get_element_by_index(0))


        self.la = self.head[0]
        self.cb = self.head[1]
        while self.la != self.rowA and self.cb != self.columnA:
            self.finalQueue.enqueue([self.la, self.cb])
            self.loop()
        print("final")
        self.finalQueue.print_elements()

    def loop(self):
        #print(self.la, self.cb)
        aux = self.alreadyA.get_element_by_index(self.alreadyA.find_index_by_values(self.la, self.cb))
        #print(aux)
        la = aux[2]
        cb = aux[3]

    @property
    def deliberate(self) -> bool:
        """ The agent chooses the next action. The simulator calls this
        method at each cycle. Must be implemented in every agent"""

        # No more actions, time almost ended
        if self.rtime < 10.0:
            # time to wake up the rescuer
            # pass the walls and the victims (here, they're empty)
            print(f"{self.NAME} I believe I've remaining time of {self.rtime:.1f}")
            self.resc.go_save_victims([],[])
            return False

        if self.rtime < 100.0 and not self.a:
            self.rowA = self.row
            self.columnA = self.column
            self.a = True
            self.caminhoA()

            return True
        if self.a and self.b:
            self.alreadyA.print_elements()
            self.b = False
            return True

        decision = self.explorer_map.information(self.row, self.column)
        #print(decision)
        if decision is None:
            decision = self.stack.pop()
            #print(decision)
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
        #dx = random.choice([-1, 0, 1])

        #if dx == 0:
        #   dy = random.choice([-1, 1])
        #else:
        #   dy = random.choice([-1, 0, 1])

        # Check the neighborhood obstacles
        obstacles = self.body.check_obstacles()


        # Moves the body to another position
        result = self.body.walk(dx, dy)
        # Update remaining time
        if dx != 0 and dy != 0:
            self.rtime -= self.COST_DIAG
        else:
            self.rtime -= self.COST_LINE

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
            seq = self.body.check_for_victim()
            if seq >= 0:
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
        #print("-------------------------------------------\n")
        #self.explorer_map.print_matrix()
        #print("-------------------------------------------\n")


                
        return True

