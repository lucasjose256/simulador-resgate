class ExplorerDrawnMap:
    def __init__(self):
        self.matrix_list = []
        self.rowA = 4
        self.columnA = 2

    def find_row_with_right(self, content):
        for row_index, row in enumerate(self.matrix_list):
            if row[0] == content:
                return row_index
        return "FALSE"

    def information(self, current_positionROW, current_positionCOLUMN, direcao):
        priority = False
        task = False
        rowAUX = self.find_row_with_right([current_positionROW, current_positionCOLUMN])
        if(direcao == 1):
            while(not priority):
                if isinstance(self.matrix_list[rowAUX][4], int):
                   if self.matrix_list[rowAUX][4] == 0:
                      if(self.find_row_with_right([current_positionROW, current_positionCOLUMN - 1]) == "FALSE" or task):
                        return "LEFT"
                if isinstance(self.matrix_list[rowAUX][1], int):
                   if self.matrix_list[rowAUX][1] == 0:
                       if(self.find_row_with_right([current_positionROW - 1, current_positionCOLUMN])  == "FALSE" or task):
                         return "UP"
                if isinstance(self.matrix_list[rowAUX][3], int):
                   if self.matrix_list[rowAUX][3] == 0:
                      if((self.find_row_with_right([current_positionROW, current_positionCOLUMN + 1])  == "FALSE") or task):
                        return "RIGHT"
                if isinstance(self.matrix_list[rowAUX][2], int):
                   if self.matrix_list[rowAUX][2] == 0:
                       if(self.find_row_with_right([current_positionROW + 1, current_positionCOLUMN]) == "FALSE" or task):
                        return "DOWN"
                if task:
                    break
                task = True
        elif(direcao == 2):
            while(not priority):
                if isinstance(self.matrix_list[rowAUX][3], int):
                   if self.matrix_list[rowAUX][3] == 0:
                      if((self.find_row_with_right([current_positionROW, current_positionCOLUMN + 1])  == "FALSE") or task):
                        return "RIGHT"
                if isinstance(self.matrix_list[rowAUX][4], int):
                   if self.matrix_list[rowAUX][4] == 0:
                      if(self.find_row_with_right([current_positionROW, current_positionCOLUMN - 1]) == "FALSE" or task):
                        return "LEFT"
                if isinstance(self.matrix_list[rowAUX][2], int):
                   if self.matrix_list[rowAUX][2] == 0:
                       if(self.find_row_with_right([current_positionROW + 1, current_positionCOLUMN]) == "FALSE" or task):
                        return "DOWN"
                if isinstance(self.matrix_list[rowAUX][1], int):
                   if self.matrix_list[rowAUX][1] == 0:
                       if(self.find_row_with_right([current_positionROW - 1, current_positionCOLUMN])  == "FALSE" or task):
                        return "UP"
                if task:
                    break
                task = True
        elif(direcao == 3):
            while(not priority):
                if isinstance(self.matrix_list[rowAUX][2], int):
                   if self.matrix_list[rowAUX][2] == 0:
                       if(self.find_row_with_right([current_positionROW + 1, current_positionCOLUMN]) == "FALSE" or task):
                        return "DOWN"
                if isinstance(self.matrix_list[rowAUX][1], int):
                   if self.matrix_list[rowAUX][1] == 0:
                       if(self.find_row_with_right([current_positionROW - 1, current_positionCOLUMN])  == "FALSE" or task):
                        return "UP"
                if isinstance(self.matrix_list[rowAUX][3], int):
                   if self.matrix_list[rowAUX][3] == 0:
                      if((self.find_row_with_right([current_positionROW, current_positionCOLUMN + 1])  == "FALSE") or task):
                        return "RIGHT"
                if isinstance(self.matrix_list[rowAUX][4], int):
                   if self.matrix_list[rowAUX][4] == 0:
                      if(self.find_row_with_right([current_positionROW, current_positionCOLUMN - 1]) == "FALSE" or task):
                        return "LEFT"
                if task:
                    break
                task = True
        elif(direcao == 4):
            while(not priority):
                if isinstance(self.matrix_list[rowAUX][1], int):
                   if self.matrix_list[rowAUX][1] == 0:
                       if(self.find_row_with_right([current_positionROW - 1, current_positionCOLUMN])  == "FALSE" or task):
                        return "UP"
                if isinstance(self.matrix_list[rowAUX][4], int):
                   if self.matrix_list[rowAUX][4] == 0:
                      if(self.find_row_with_right([current_positionROW, current_positionCOLUMN - 1]) == "FALSE" or task):
                        return "LEFT"
                if isinstance(self.matrix_list[rowAUX][3], int):
                   if self.matrix_list[rowAUX][3] == 0:
                      if((self.find_row_with_right([current_positionROW, current_positionCOLUMN + 1])  == "FALSE") or task):
                        return "RIGHT"
                if isinstance(self.matrix_list[rowAUX][2], int):
                   if self.matrix_list[rowAUX][2] == 0:
                       if(self.find_row_with_right([current_positionROW + 1, current_positionCOLUMN]) == "FALSE" or task):
                        return "DOWN"
                if task:
                    break
                task = True

    def draw(self, later_positionROW, later_positionCOLUMN, current_positionROW, current_positionCOLUMN, decision):
        rowAUX = self.find_row_with_right([later_positionROW, later_positionCOLUMN])

        if current_positionROW != "NULL" and current_positionCOLUMN != "NULL":
            if decision == "UP":
                self.matrix_list[rowAUX][1] = [current_positionROW, current_positionCOLUMN]
            elif decision == "DOWN":
                self.matrix_list[rowAUX][2] = [current_positionROW, current_positionCOLUMN]
            elif decision == "RIGHT":
                self.matrix_list[rowAUX][3] = [current_positionROW, current_positionCOLUMN]
            elif decision == "LEFT":
                self.matrix_list[rowAUX][4] = [current_positionROW, current_positionCOLUMN]

        else:
            if decision == "UP":
                self.matrix_list[rowAUX][1] = "WALL/BORDER"
            elif decision == "DOWN":
                self.matrix_list[rowAUX][2] = "WALL/BORDER"
            elif decision == "RIGHT":
                self.matrix_list[rowAUX][3] = "WALL/BORDER"
            elif decision == "LEFT":
                self.matrix_list[rowAUX][4] = "WALL/BORDER"
        if current_positionROW != "NULL" and current_positionCOLUMN != "NULL" and self.find_row_with_right(
                [current_positionROW, current_positionCOLUMN]) == "FALSE":
            row = len(self.matrix_list)
            if not self.is_valid_position(row, 4):
                while len(self.matrix_list) <= row:
                    self.matrix_list.append([])

            while len(self.matrix_list[row]) <= 4:
                self.matrix_list[row].append(0)

            if (current_positionROW != "Í"):
                self.matrix_list[row][0] = [current_positionROW, current_positionCOLUMN]

    # def decision_point(self, current_positionX, current_positionY):
    #     if self.matrix_list[current_positionX][0] == [1, 1, 1, 1]:
    #         self.matrix_list[current_positionX][0] = [0, 1, 1, 1]
    #         return "UP"
    #     elif self.matrix_list[current_positionX][0] == [0, 1, 1, 1]:
    #         self.matrix_list[current_positionX][0] = [0, 0, 1, 1]
    #         return "DOWN"
    #     elif self.matrix_list[current_positionX][0] == [0, 0, 1, 1]:
    #        self.matrix_list[current_positionX][0] = [0, 0, 0, 1]
    #        return "RIGHT"
    #    elif self.matrix_list[current_positionX][0] == [0, 0, 0, 1]:
    #        self.matrix_list[current_positionX][0] = [0, 0, 0, 0]
    #        return "LEFT"
    #    else:
    #       return "NONE"

    def is_valid_position(self, x, y):
        return 0 <= x < len(self.matrix_list) and 0 <= y < len(self.matrix_list[x]) and self.matrix_list[x][y] != 0

    def print_matrix(self):
        for row in self.matrix_list:
            for element in row:
                print(element, end=" ")  # Imprime o elemento e um espaço em branco
            print()

    # def score(self ,lc):
    #    l = lc[0]
    #    c = lc[1]
    #    return (min(abs(l),abs(c))*1.5 + (max(abs(l),abs(c)) - (min(abs(l),abs(c))))) + (min(abs(l - self.rowA), abs(c - self.columnA))*1.5
    #    + (max(abs(l - self.rowA), abs(c - self.columnA)) - min(abs(l - self.rowA), abs(c - self.columnA))))
    def remove_rows_with_incorrect_columns(self, expected_columns=5):
        self.matrix_list = [row for row in self.matrix_list if len(row) == expected_columns]

    def print_matrix_types(self):
        for row in self.matrix_list:
            for element in row:
                element_type = type(element).__name__
                print(f"Tipo: {element_type}", end="\t")
            print()

    def contar_linhas_colunas(self):
        num_linhas = len(self.matrix_list)

        return num_linhas

def main():
    mapa = ExplorerDrawnMap()
    print(mapa.score([1, 1]))
    # mapa.draw(1, 0, 2, 0, "UP")
    # mapa.draw(2, 0, 2, -1, "LEFT")

    # mapa.draw(0, 1)
    # mapa.draw(0, 2)
    # mapa.draw(1, 2)


if __name__ == "__main__":
    main()
