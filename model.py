MOVES = [
    (2, -1),
    (1, -2),
    (-1, -2),
    (-2, -1),
    (-2, 1),
    (-1, 2),
    (1, 2),
    (2, 1)]


class Board:
    BOARD_SIZE = 7

    def __init__(self):
        self.fields = [[0 for x in range(Board.BOARD_SIZE)] for y in range(Board.BOARD_SIZE)]

    def get_field(self, x, y):
        return self.fields[x][y]

    def mark_field(self, x, y, v):
        self.fields[x][y] = v

    def __str__(self):
        output = ''
        for y in range(Board.BOARD_SIZE):
            ar = [str(self.fields[x][y]) + "\t\t" for x in range(Board.BOARD_SIZE)]
            output += ''.join(ar) + "\n\n\n"
        return output

    def board_size(self):
        return Board.BOARD_SIZE


class Knight:
    def __init__(self, x=0, y=0, marker=0):
        self.x = x
        self.y = y
        self.marker = marker

    def move(self, mv):
        self.x += mv[0]
        self.y += mv[1]
        self.marker += 1
        return self.x, self.y, self.marker


class Coord:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Move:
    def __init__(self, knight, move):
        self.old_position = Coord(knight.x, knight.y)
        self.new_position = Coord(knight.x + move[0], knight.y + move[1])
        self.move = Coord(move[0], move[1])


class MoveHistory:
    def __init__(self, moves, knight, board):
        self.moves = moves
        self.moves_number = len(moves)
        self.knight = knight
        self.board = board
