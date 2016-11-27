from model import Knight, Board, MoveHistory, Move
from engine import get_random_location, get_next_random_possible_move, move


def create_random_knight():
    return Knight(*(get_random_location(Board.BOARD_SIZE)))


if __name__ == "__main__":
    history = []
    while True:
        board = Board()
        knight = create_random_knight()
        moves_so_far = []
        next_move = get_next_random_possible_move(knight, board)
        while next_move is not None:
            moves_so_far.append(move(knight, board, next_move))
            next_move = get_next_random_possible_move(knight, board)
        current_history = MoveHistory(moves_so_far, knight, board)
        history.append(current_history)
    pass
