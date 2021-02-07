from chessPiece import chessPiece

class knight():
    """Computes all possible moves for a given knight piece"""
    @staticmethod
    def getNormalMoves(piece, position: tuple, board: list):
        """returns list of potential non-capture moves from a given position"""
        row, col = position
        potential_moves = []

        chessPiece.moveUpdate(2, 1, row, col, board, potential_moves, 2)
        chessPiece.moveUpdate(2, -1, row, col, board, potential_moves, 2)
        chessPiece.moveUpdate(1, 2, row, col, board, potential_moves, 2)
        chessPiece.moveUpdate(1, -2, row, col, board, potential_moves, 2)
        chessPiece.moveUpdate(-1, 2, row, col, board, potential_moves, 2)
        chessPiece.moveUpdate(-1, -2, row, col, board, potential_moves, 2)
        chessPiece.moveUpdate(-2, 1, row, col, board, potential_moves, 2)
        chessPiece.moveUpdate(-2, -1, row, col, board, potential_moves, 2)

        return potential_moves

    @staticmethod
    def getCaptureMoves(piece, position: tuple, board: list):
        """returns list of potential capture moves from a given position"""
        color_sign = 1 if piece == 'N' else -1
        row, col = position
        potential_moves = []

        chessPiece.captureUpdate(2, 1, color_sign, row, col, board, potential_moves, 2)
        chessPiece.captureUpdate(2, -1, color_sign, row, col, board, potential_moves, 2)
        chessPiece.captureUpdate(1, 2, color_sign, row, col, board, potential_moves, 2)
        chessPiece.captureUpdate(1, -2, color_sign, row, col, board, potential_moves, 2)
        chessPiece.captureUpdate(-1, 2, color_sign, row, col, board, potential_moves, 2)
        chessPiece.captureUpdate(-1, -2, color_sign, row, col, board, potential_moves, 2)
        chessPiece.captureUpdate(-2, 1, color_sign, row, col, board, potential_moves, 2)
        chessPiece.captureUpdate(-2, -1, color_sign, row, col, board, potential_moves, 2)

        return potential_moves