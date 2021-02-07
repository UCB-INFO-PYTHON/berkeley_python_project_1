import boardUtil
from chessPiece import chessPiece

class king():
    """Computes all possible moves for a given king piece"""
    @staticmethod
    def getNormalMoves(piece, position: tuple, board: list, castle_rights, isCheck):
        """returns list of potential non-capture moves from a given position"""
        color_sign = 1 if piece == 'K' else -1
        row, col = position
        potential_moves = []

        def update(mult1, mult2):
            """Closure to update potential moves array"""
            k = 1
            if chessPiece.cellIsValidAndEmpty(row + k * mult1, col + k * mult2, board):
                potential_moves.append((position, (row + k * mult1, col + k * mult2)))

        # diagonals
        update(-1, -1)
        update(1, 1)
        update(-1, 1)
        update(1, -1)

        # horizontals verticals
        update(-1, 0)
        update(1, 0)
        update(0, 1)
        update(0, -1)

        # Check castle moves
        def updateCastle(direction_mult, king_char):
            # for each cell on path to move: king moves three places left
            can_castle = True
            # check if piece is on knights place for queenside castle
            if direction_mult == -1:
                if not chessPiece.cellIsValidAndEmpty(row, col + 3 * direction_mult, board):
                    can_castle = False

            for i in range(1, 3):  # just two spaces
                newCol = col + i * direction_mult
                # check if cells to move are empty
                if not chessPiece.cellIsValidAndEmpty(row, newCol, board):
                    can_castle = False
                    break
                # check if king is in check on each cell
                board_copy = [sr.copy() for sr in board]
                board_copy[row][newCol], board_copy[row][col] = king_char, ' '
                if boardUtil.boardUtil.isCheck(color_sign, board_copy, None):
                    can_castle = False
                    break
            if can_castle:
                potential_moves.append((position, (row, col + 2 * direction_mult)))

        if not isCheck:
            if color_sign == 1:
                if castle_rights.get('Q', 0) == 1:
                    updateCastle(-1, 'K')
                if castle_rights.get('K', 0) == 1:
                    updateCastle(1, 'K')
            else:
                if castle_rights.get('q', 0) == 1:
                    updateCastle(-1, 'k')
                if castle_rights.get('k', 0) == 1:
                    updateCastle(1, 'k')

        return potential_moves

    @staticmethod
    def getCaptureMoves(piece, position: tuple, board: list):
        """returns list of potential capture moves from a given position"""
        color_sign = 1 if piece == 'K' else -1
        row, col = position
        potential_moves = []

        def update(mult1, mult2):
            """Closure to update potential moves array"""
            k = 1
            is_enemy, piece, move = chessPiece.evalCaptureCell(color_sign, row + k * mult1, col + k * mult2, board)
            if is_enemy:
                potential_moves.append((position, move))

        # diagonals
        update(-1, -1)
        update(1, 1)
        update(-1, 1)
        update(1, -1)

        # horizontals verticals
        update(-1, 0)
        update(1, 0)
        update(0, 1)
        update(0, -1)

        return potential_moves