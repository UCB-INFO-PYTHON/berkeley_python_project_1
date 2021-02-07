from chessPiece import chessPiece

class bishop():
    """Computes all possible moves for bishop pieces"""
    @staticmethod
    def getNormalMoves(piece, position: tuple, board: list):
        """returns list of potential non-capture moves from a given position"""
        row, col = position
        potential_moves = []

        chessPiece.moveUpdate(-1, -1, row, col, board, potential_moves, 8)
        chessPiece.moveUpdate(1, 1, row, col, board, potential_moves, 8)
        chessPiece.moveUpdate(-1, 1, row, col, board, potential_moves, 8)
        chessPiece.moveUpdate(1, -1, row, col, board, potential_moves, 8)

        return potential_moves

    @staticmethod
    def getCaptureMoves(piece, position: tuple, board: list):
        """returns list of potential capture moves from a given position"""
        color_sign = 1 if piece == 'B' else -1
        row, col = position
        potential_moves = []

        chessPiece.captureUpdate(1, 1, color_sign, row, col, board, potential_moves, 8)
        chessPiece.captureUpdate(1, -1, color_sign, row, col, board, potential_moves, 8)
        chessPiece.captureUpdate(-1, 1, color_sign, row, col, board, potential_moves, 8)
        chessPiece.captureUpdate(-1, -1, color_sign, row, col, board, potential_moves, 8)

        return potential_moves