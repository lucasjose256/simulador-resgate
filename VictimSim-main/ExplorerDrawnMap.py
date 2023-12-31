class ExplorerDrawnMap:
    def __init__(self):
        self.matrix_list = []

    def find_row_with_right(self, content):
        for row_index, row in enumerate(self.matrix_list):
            if row[0] == content:
                return row_index
        return False

    def information(self, current_positionROW, current_positionCOLUMN):
        rowAUX = self.find_row_with_right([current_positionROW, current_positionCOLUMN])
        if isinstance(self.matrix_list[rowAUX][1], int):
            if self.matrix_list[rowAUX][1] == 0:
                return "UP"
        elif isinstance(self.matrix_list[rowAUX][2], int):
            if self.matrix_list[rowAUX][2] == 0:
                print("Downn")
                return "DOWN"
        elif isinstance(self.matrix_list[rowAUX][3], int):
            if self.matrix_list[rowAUX][3] == 0:
                return "RIGHT"
        elif isinstance(self.matrix_list[rowAUX][4], int):
            if self.matrix_list[rowAUX][4] == 0:
                return "LEFT"



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
        if current_positionROW != "NULL" and current_positionCOLUMN != "NULL" and not self.find_row_with_right([current_positionROW, current_positionCOLUMN]):
            row = len(self.matrix_list)
            if not self.is_valid_position(row, 4):
                while len(self.matrix_list) <= row:
                    self.matrix_list.append([])

            while len(self.matrix_list[row]) <= 4:
                self.matrix_list[row].append(0)

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


def main():
    mapa = ExplorerDrawnMap()
    mapa.draw(0, 0, 0, 0, "NONE")
    mapa.draw(0, 0, 1, 0, "UP")
    mapa.draw(0, 0, 0, -1, "LEFT")
    # mapa.draw(1, 0, 2, 0, "UP")
    # mapa.draw(2, 0, 2, -1, "LEFT")
    mapa.print_matrix()

    # mapa.draw(0, 1)
    # mapa.draw(0, 2)
    # mapa.draw(1, 2)

    print(mapa.is_valid_position(0, 1))


if __name__ == "__main__":
    main()
