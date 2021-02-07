class chessPiece():
    """Class for common operations made by chess pieces when computing moves
    Also holds meta data for chess pieces"""
    white_pieces = 'PRNBQK'
    black_pieces = 'prnbqk'

    white_king = '\u265A'
    white_queen = '\u265B'
    white_rook = '\u265C'
    white_bishop = '\u265D'
    white_knight = '\u265E'
    white_pawn = '\u265F'

    black_bishop = '\u2657'
    black_knight = '\u2658'
    black_pawn = '\u2659'
    black_king = '\u2654'
    black_queen = '\u2655'
    black_rook = '\u2656'

    piece_values = {'k':1000, 'q':9, 'r':5, 'b':3, 'n':3, 'p':1, 'K': 1000, 'Q': 9, 'R': 5, 'B': 3, 'N': 3, 'P': 1}
    piece_symbols = {'k': black_king, 'q': black_queen, 'r': black_rook, 'b': black_bishop, 'n': black_knight, 'p': black_pawn,
                    'K': white_king, 'Q': white_queen, 'R': white_rook, 'B': white_bishop, 'N': white_knight, 'P': black_pawn}

    @staticmethod
    def cellIsValidAndEmpty(row, col, board):
        """Returns true if the row and col are valid positions and the board space is empty"""
        if 0 <= row < 8 and 0 <= col < 8:
            if board[row][col] == ' ':
                return True
        return False

    @staticmethod
    def evalCaptureCell(my_color_sign, row, col, board) -> (bool, str, tuple):
        """checks if enemy piece is in cell and returns True/False, enemy piece code, move tuple"""
        if 0 <= row < 8 and 0 <= col < 8:
            dest = board[row][col]
            if my_color_sign == 1:
                if dest in chessPiece.black_pieces:
                    return True, dest, (row, col)
            elif my_color_sign == -1:
                if dest in chessPiece.white_pieces:
                    return True, dest, (row, col)
        return False, None, None

    @staticmethod
    def captureUpdate(mult1, mult2, color_sign, row, col, board, potential_moves, upper_bound=8):
        """Closure to update potential moves array"""
        for k in range(1, upper_bound):
            r, c = row + k * mult1, col + k * mult2
            if chessPiece.cellIsValidAndEmpty(r, c, board):
                continue
            else:
                is_enemy, piece, move = chessPiece.evalCaptureCell(color_sign, r, c, board)
                if is_enemy:
                    potential_moves.append(((row, col), move))
                break    # blocked by some piece no matter what

    @staticmethod
    def moveUpdate(mult1, mult2, row, col, board, potential_moves, upper_bound=8):
        """Closure to update potential moves array"""
        for k in range(1, upper_bound):
            r, c = row + k * mult1, col + k * mult2
            if chessPiece.cellIsValidAndEmpty(r, c, board):
                potential_moves.append(((row, col), (r, c)))
            else:
                break
