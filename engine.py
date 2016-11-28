from model import Board, Knight, Move, DIRECTIONS
from random import randint, choice


def can_move(knight, board, move):
    x = knight.x + move.x
    y = knight.y + move.y
    return not (are_out_of_board(x, y, board) or is_field_marked(x, y, board))


def is_out_of_board(v, board):
    return v < 0 or v >= board.board_size()


def are_out_of_board(a, b, board):
    return is_out_of_board(a, board) or is_out_of_board(b, board)


def are_in_board(a, b, board):
    return not are_out_of_board(a, b, board)


def is_field_marked(x, y, board):
    return board.fields[x][y] != 0


def is_field_not_marked(x, y, board):
    return not is_field_marked(x, y, board)


def move(knight, board, mv):
    move_to_return = Move(knight, mv)
    board.mark_field(*(knight.move(mv)))
    return move_to_return


def get_random_location(max):
    return randint(0, max - 1), randint(0, max - 1)


def get_possible_moves(knight, board):
    return [m for m in DIRECTIONS if can_move(knight, board, m)]


def get_next_random_possible_move(knight, board):
    possible_moves = get_possible_moves(knight, board)
    if possible_moves:
        return choice(possible_moves)
    else:
        return None
