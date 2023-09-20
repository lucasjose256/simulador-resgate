class StringQueue:
    def __init__(self):
        self.queue = []

    def enqueueNotEqual(self, string, blacklist_queue=None):
        # if blacklist_queue and string in blacklist_queue.queue:
        #    print(f"Elemento '{string}' está na blacklist e não pode ser adicionado.")
        # if blacklist_queue is not None:
        #   if (blacklist_queue.find_index_by_values(string[0], string[1])) == -1:
        #        return None
        # elif string not in self.queue:
        if string not in self.queue:
            self.queue.append(string)

    def enqueue(self, string, blacklist_queue=None):
        self.queue.append(string)

    def dequeue(self):
        if not self.is_empty():
            return self.queue.pop(0)
        else:
            return "A fila está vazia."

    def is_empty(self):
        return len(self.queue) == 0

    def peek(self):
        if not self.is_empty():
            return self.queue[0]
        else:
            return "A fila está vazia."

    def size(self):
        return len(self.queue)

    def get_element_by_index(self, index):
        if 0 <= index < len(self.queue):
            return self.queue[index]
        else:
            return "Índice fora dos limites da fila."

    def find_index_by_values(self, value_0, value_1):
        for index, vetor in enumerate(self.queue):
            if isinstance(vetor, list) and len(vetor) >= 2 and vetor[0] == value_0 and vetor[1] == value_1:
                return index
        return -1

    def print_elements(self):
        for string in self.queue:
            if isinstance(string, list):
                print(string)
            else:
                print("Elemento não é uma lista:", string)

    def merge_sort(self):
        self.queue = self._merge_sort_helper(self.queue)

    def _merge_sort_helper(self, arr):
        if len(arr) > 1:
            mid = len(arr) // 2
            left_half = arr[:mid]
            right_half = arr[mid:]

            self._merge_sort_helper(left_half)
            self._merge_sort_helper(right_half)

            i = j = k = 0

            while i < len(left_half) and j < len(right_half):
                # Comparação considerando [2] como primeiro critério
                if left_half[i][2] < right_half[j][2]:
                    arr[k] = left_half[i]
                    i += 1
                elif left_half[i][2] > right_half[j][2]:
                    arr[k] = right_half[j]
                    j += 1
                else:
                    # Em caso de empate em [2], comparar a soma de [0] e [1]
                    sum_left = left_half[i][0] + left_half[i][1]
                    sum_right = right_half[j][0] + right_half[j][1]

                    if sum_left < sum_right:
                        arr[k] = left_half[i]
                        i += 1
                    elif sum_left > sum_right:
                        arr[k] = right_half[j]
                        j += 1
                    else:
                        # Em caso de empate em [2] e soma de [0] e [1], verificar [0] e [1]
                        if left_half[i][0] == right_half[j][0]:
                            arr[k] = left_half[i]
                            i += 1
                        elif left_half[i][1] == right_half[j][1]:
                            arr[k] = right_half[j]
                            j += 1
                        else:
                            # Se tudo empatar, manter a ordem original
                            arr[k] = left_half[i]
                            i += 1

                k += 1

            while i < len(left_half):
                arr[k] = left_half[i]
                i += 1
                k += 1

            while j < len(right_half):
                arr[k] = right_half[j]
                j += 1
                k += 1

        return arr
