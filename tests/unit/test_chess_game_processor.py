import unittest
import chess


class ChessGameProcessor:
    def __init__(self, board_data, move_data):
        self.board = self.create_board(board_data)
        self.move = self.parse_move(move_data)

    def create_board(self, board_data):
        fen_notation = []
        for row in board_data:
            row_notation = []
            empty_squares = 0
            for piece in row:
                if piece is None:
                    empty_squares += 1
                else:
                    if empty_squares > 0:
                        row_notation.append(str(empty_squares))
                        empty_squares = 0
                    row_notation.append(piece)
            if empty_squares > 0:
                row_notation.append(str(empty_squares))
            fen_notation.append("".join(row_notation))
        fen_notation = "/".join(fen_notation)
        fen_notation += " w KQkq - 0 1"  # default values for active color, castling, en passant, halfmove clock, and fullmove number
        return chess.Board(fen_notation)

    def parse_move(self, move_data):
        columns = ["a", "b", "c", "d", "e", "f", "g", "h"]
        from_file = ord(columns[move_data["from"][0]-1].lower()) - ord('a')
        from_rank = int(move_data["from"][1]) - 1
        to_file = ord(columns[move_data["to"][0]-1].lower()) - ord('a')
        to_rank = int(move_data["to"][1]) - 1

        from_square = chess.square(from_file, from_rank)
        to_square = chess.square(to_file, to_rank)
        return chess.Move(from_square, to_square)

    def is_valid_move(self):
        return self.move in self.board.legal_moves

    def make_move(self):
        if self.is_valid_move():
            self.board.push(self.move)
        else:
            raise ValueError("Invalid move")

    def is_game_over(self):
        return self.board.is_game_over()

    def get_game_result(self):
        return self.board.result()

    def get_fen(self):
        return self.board.fen()


class TestChessGameProcessor(unittest.TestCase):
    def setUp(self):
        self.board_data = [
            ["r", "n", "b", "q", "k", "b", "n", "r"],
            ["p", "p", "p", "p", "p", "p", "p", "p"],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            ["P", "P", "P", "P", "P", "P", "P", "P"],
            ["R", "N", "B", "Q", "K", "B", "N", "R"]
        ]
        self.move_data = {"from": [5, 2], "to": [5, 4]}
        self.processor = ChessGameProcessor(self.board_data, self.move_data)

    def test_create_board(self):
        self.assertIsInstance(self.processor.board, chess.Board)
        self.assertEqual(self.processor.board.fen(), "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")

    def test_parse_move(self):
        self.assertIsInstance(self.processor.move, chess.Move)
        self.assertEqual(self.processor.move.from_square, chess.square(4, 1))
        self.assertEqual(self.processor.move.to_square, chess.square(4, 3))

    def test_is_valid_move(self):
        self.assertTrue(self.processor.is_valid_move())

    def test_make_move(self):
        self.processor.make_move()
        self.assertEqual(self.processor.board.fen(), "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1")

    def test_is_game_over(self):
        self.assertFalse(self.processor.is_game_over())

    '''def test_get_game_result_draw(self):
        self.processor.make_move()
        self.processor.board.push(chess.Move(chess.square(4, 3), chess.square(4, 4)))
        self.processor.board.push(chess.Move(chess.square(4, 4), chess.square(4, 5)))
        self.processor.board.push(chess.Move(chess.square(4, 5), chess.square(4, 6)))
        self.processor.board.push(chess.Move(chess.square(4, 6), chess.square(4, 7)))
        self.processor.board.push(chess.Move(chess.square(4, 7), chess.square(4, 6)))
        self.processor.board.push(chess.Move(chess.square(4, 6), chess.square(4, 5)))
        self.processor.board.push(chess.Move(chess.square(4, 5), chess.square(4, 4)))
        self.processor.board.push(chess.Move(chess.square(4, 4), chess.square(4, 3)))
        self.assertTrue(self.processor.board.is_stalemate() or self.processor.board.is_fivefold_repetition())
        result = self.processor.get_game_result()
        self.assertEqual(result, "1/2-1/2")'''
