from chessPiece import chessPiece

class pawn(chessPiece):
    """Computes all possible moves for a given pawn piece"""
    @staticmethod
    def getNormalMoves(piece, position: tuple, board: list) -> list:
        """returns list of potential non-capture moves from a given position"""
        color_sign = 1 if piece == 'P' else -1
        row, col = position
        rank = row + 1 if color_sign == -1 else 8 - row
        potential_moves = []

        def updateMoves(r, c):
            if chessPiece.cellIsValidAndEmpty(r, c, board):
                potential_moves.append((position, (r, c)))    # 1 space forward

        updateMoves(row - 1 * color_sign, col)
        if rank == 2:    # can move 2 spaces from rank 2 only
            if chessPiece.cellIsValidAndEmpty(row - 1 * color_sign, col, board):
                updateMoves(row - 2 * color_sign, col)

        return potential_moves

    @staticmethod
    def getCaptureMoves(piece, position: tuple, board: list, en_passant_coords) -> list:
        """returns list of potential capture moves from a given position"""
        color_sign = 1 if piece == 'P' else -1
        row, col = position
        potential_capture_moves = []

        def updateCapture(r, c):
            isEnemy, piece, move = chessPiece.evalCaptureCell(color_sign, r, c, board)
            if isEnemy:
                potential_capture_moves.append((position, move))
            # check en passant capture, assumes parameter en passant coords is computed as square
            # the enemy pawn will land on after an en passant capture
            if chessPiece.cellIsValidAndEmpty(r, c, board) and (r, c) == en_passant_coords:
                potential_capture_moves.append((position, (r, c)))

        updateCapture(row - 1 * color_sign, col - 1)
        updateCapture(row - 1 * color_sign, col + 1)

        return potential_capture_moves