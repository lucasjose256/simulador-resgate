import random
import staticExplorer

class clustering:
    vitimas_sem_duplicatas = []
    centroides = []
    atribuicoes = []
    k = 4
    max_iteracoes = 100
    calculado = False

@staticmethod
def clustering_calculado():
    clustering.calculado = True

@staticmethod
def ret_calculado():
    return clustering.calculado

@staticmethod
def ret_centroides():
    return clustering.centroides

@staticmethod
def ret_atribuicoes():
    return clustering.atribuicoes

@staticmethod
def ret_vitimas_sem_duplicatas():
    return clustering.vitimas_sem_duplicatas

@staticmethod
def tirar_duplicatas(vitimas):
    for x in vitimas:
        if x not in clustering.vitimas_sem_duplicatas:
            clustering.vitimas_sem_duplicatas.append(x)

@staticmethod
def define_pontos():
    clustering.pontos = [(clustering.vitimas_sem_duplicatas[i][0], clustering.vitimas_sem_duplicatas[i][1]) for i in range(len(clustering.vitimas_sem_duplicatas))]

# Função para calcular a distância euclidiana entre dois pontos inteiros
def distancia(ponto1, ponto2):
    x1, y1 = ponto1
    x2, y2 = ponto2
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5


# Função para encontrar o centróide mais próximo de um ponto
def encontrar_centroide_mais_proximo(ponto, centroides):
    distancia_minima = float('inf')
    centroide_mais_proximo = None
    for i, centroide in enumerate(centroides):
        d = distancia(ponto, centroide)
        if d < distancia_minima:
            distancia_minima = d
            centroide_mais_proximo = i
    return centroide_mais_proximo


# Função para atualizar os centroides com base nas atribuições
@staticmethod
def atualizar_centroides(pontos, atribuicoes, k):
    novos_centroides = []
    for i in range(k):
        soma_x = 0
        soma_y = 0
        count = 0
        for j, ponto in enumerate(pontos):
            if atribuicoes[j] == i:
                x, y = ponto
                soma_x += x
                soma_y += y
                count += 1
        if count > 0:
            novo_centroide = (soma_x // count, soma_y // count)  # Use divisão inteira
            novos_centroides.append(novo_centroide)
    return novos_centroides


# Função para executar o algoritmo K-means
@staticmethod
def k_means():
    pontos = [(staticExplorer.staticExplorer.returnVitFinal()[i][0], staticExplorer.staticExplorer.returnVitFinal()[i][1]) for i in
                         range(len(staticExplorer.staticExplorer.returnVitFinal()))]
    # Inicialização aleatória dos centroides
    while len(pontos) < clustering.k:
        clustering.k -= 1

    clustering.centroides = random.sample(pontos, clustering.k)
    for _ in range(clustering.max_iteracoes):
        # Atribuir cada ponto ao centróide mais próximo
        clustering.atribuicoes = [encontrar_centroide_mais_proximo(pontos, clustering.centroides)
                                    for pontos in pontos]
        # Atualizar os centroides
        novos_centroides = atualizar_centroides(pontos, clustering.atribuicoes, clustering.k)

        # Verificar a convergência
        if clustering.centroides == novos_centroides:
            break

        clustering.centroides = novos_centroides
