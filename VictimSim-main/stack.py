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
