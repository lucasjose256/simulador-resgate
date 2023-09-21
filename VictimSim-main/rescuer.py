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
        self.clt = cluster
        self.finalMap = []
        self.vitimas = []
        self.vitimas_cluster = []


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

        print("------------------")
        #self.print_matrix()
        print("------------------")


    def print_matrix(self):
        for row in staticExplorer.finalMap:
            for element in row:
                print(element, end=" ")  # Imprime o elemento e um espaço em branco
            print()

    def adicionar_vitimas(self, vetor):
        #self.vitimas.extend(vetor)
        #print(staticExplorer.vitimas)
        staticExplorer.adicionar_vitimas(vetor)
        #staticExplorer.print_matrix()


        if staticExplorer.checked():
            clustering.tirar_duplicatas(staticExplorer.vitimas)
            #print(clustering.ret_vitimas_sem_duplicatas())
            clustering.k_means()
            #vitimas_sem_duplicatas = []
            #[vitimas_sem_duplicatas.append(x) for x in self.vitimas if x not in vitimas_sem_duplicatas]

            '''for i in range(len(vitimas_sem_duplicatas)):
                print(f"Vítima {i + 1}: {vitimas_sem_duplicatas[i]}")
                i += 1'''


            #k = 4
            #pontos = [(vitimas_sem_duplicatas[i][0], vitimas_sem_duplicatas[i][1]) for i in range(len(vitimas_sem_duplicatas))]
            #centroides_finais, atribuicoes_finais = clustering.k_means(pontos, k)

            centroides_finais = clustering.ret_centroides()
            atribuicoes_finais = clustering.ret_atribuicoes()
            vitimas_sem_duplicatas = clustering.ret_vitimas_sem_duplicatas()

            print(centroides_finais)
            print(atribuicoes_finais)
            print("Coordenadas dos centroides finais:")
            for i, centroide in enumerate(centroides_finais):
                print(f"Centroide {i + 1}: ({centroide[0]}, {centroide[1]})")
            for i, atribuicoes in enumerate(atribuicoes_finais):
                print(f"Vítima {i + 1}: {atribuicoes+1}")
                if atribuicoes+1 == self.clt:
                    print("Adicionado")
                    print(vitimas_sem_duplicatas[i])
                    self.vitimas_cluster.append(vitimas_sem_duplicatas[i])


    def go_save_victims(self, walls, victims):
        """ The explorer sends the map containing the walls and
        victims' location. The rescuer becomes ACTIVE. From now,
        the deliberate method is called by the environment"""
        self.body.set_state(PhysAgent.ACTIVE)

    def __planner(self):
        """ A private method that calculates the walk actions to rescue the
        victims. Further actions may be necessary and should be added in the
        deliberata method"""

        # This is a off-line trajectory plan, each element of the list is
        # a pair dx, dy that do the agent walk in the x-axis and/or y-axis
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

    @property
    def deliberate(self) -> bool:
        """ This is the choice of the next action. The simulator calls this
        method at each reasonning cycle if the agent is ACTIVE.
        Must be implemented in every agent
        @return True: there's one or more actions to do
        @return False: there's no more action to do """


        for i, vitimas in enumerate(self.vitimas_cluster):
            print(f"Vítima {i + 1}: ({vitimas[0]}, {vitimas[1]})")
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
