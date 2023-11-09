import random
from rescuer_issues import rescuerIssues

class clustering:
    centroides = []
    atribuicoes = []
    k = 0
    max_iteracoes = 100
    calculado = False

@staticmethod
def retornaCalculado():
    return clustering.calculado

@staticmethod
def retornaCentroides():
    return clustering.centroides

@staticmethod
def retornaAtribuicoes():
    return clustering.atribuicoes

# Função para calcular a distância euclidiana entre dois pontos inteiros
@staticmethod
def distancia(ponto1, ponto2):
    x1, y1, classe1 = ponto1
    x2, y2, classe2 = ponto2
    distancia_posicao = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
    distancia_classe = abs(classe1 - classe2)
    distancia_ponderada = 0.8 * distancia_posicao + 0.2 * distancia_classe
    return distancia_ponderada


# Função para encontrar o centróide mais próximo de um ponto
@staticmethod
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
        soma_classe = 0
        count = 0
        for j, ponto in enumerate(pontos):
            if atribuicoes[j] == i:
                x, y, classe = ponto
                soma_x += x
                soma_y += y
                soma_classe += classe
                count += 1
        if count > 0:
            novo_centroide = (soma_x // count, soma_y // count, soma_classe // count)  # Use divisão inteira
            novos_centroides.append(novo_centroide)
    return novos_centroides

# Função para executar o algoritmo K-means
@staticmethod
def k_means():
    #pontos = [(staticExplorer.staticExplorer.returnVitFinal()[i][0], staticExplorer.staticExplorer.returnVitFinal()[i][1]) for i in
    #                     range(len(staticExplorer.staticExplorer.returnVitFinal()))]
    pontos = [(rescuerIssues.retornaFinalVitimas()[i][0], rescuerIssues.retornaFinalVitimas()[i][1], rescuerIssues.retornaClasses()[i]) for i in range(len(rescuerIssues.retornaFinalVitimas()))]
    if len(pontos) == 1:
        clustering.k = 1
    elif len(pontos) == 2:
        clustering.k = 2
    elif len(pontos) == 3:
        clustering.k = 3
    else:
        clustering.k = 4
    # print(f"QUANTIDADE DE VITIMAS AO TODO NO CLUSTERING: {len(pontos)}")
    # Inicialização aleatória dos centroides
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

    clustering.calculado = True
