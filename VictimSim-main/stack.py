class stack:
    def __init__(self):
        self.stack = []

    def push(self, string):
        self.stack.append(string)

    def pop(self):
        if not self.is_empty():
            return self.stack.pop()
        else:
            return "A pilha está vazia."

    def is_empty(self):
        return len(self.stack) == 0

    def peek(self):
        if not self.is_empty():
            return self.stack[-1]
        else:
            return "A pilha está vazia."

    def size(self):
        return len(self.stack)

    def copiar_pilha(pilha_original):
        pilha_copia = stack()  # Cria uma nova pilha vazia (uma instância da classe stack)

        # Copia os elementos da pilha original para a pilha de cópia
        for elemento in pilha_original.stack:
            pilha_copia.push(elemento)

        return pilha_copia

    # Função para esvaziar uma pilha
    def esvaziar_pilha(self):
        while not self.is_empty():
            self.pop()

    def imprimir_pilha(self):
        for elemento in self.stack:
            print(elemento)