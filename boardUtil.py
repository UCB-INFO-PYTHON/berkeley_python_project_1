from os import system, name

import chessPrint
from rook import rook
from pawn import pawn
from bishop import bishop
from knight import knight
from queen import queen
from king import king
from chessPiece import chessPiece


class boardUtil():
    """Static class with methods for chess board game play
    Methods:
        1. Computes all legal moves given a state
        2. Updates a board state with a given move
        3. Performs game rules checks
        4. Supports board printing to screen
    """
    move_cache = {}     # cache moves for a board state as str:tuple
    capt_cache = {}     # cache capture moves for a board state as str:tuple

    @staticmethod
    def executeMoveAction(state: tuple, action: tuple):
        """creates and returns updated game state based on the action given.
        assumes all actions are legal actions

        input state and action should be as defined in game.py
        input state should have turn, board, en_passant, castle, check_w, check_b, checkM_w, checkM_b
        action should be a tuple of tuples source(row,col), dest(row, col)"""

        r1, c1 = action[0]
        r2, c2 = action[1]

        # input check, remove later
        if not (0 <= r1 < 8 and 0 <= r2 < 8 and 0 <= c1 < 8 and 0 <= c2 < 8):
            return False, "Row and Col is wrong! Should be between a-h and 1-8"

        player_sign = state[0]
        board = state[1]
        en_passant_coord = state[2]
        u_castle = state[3].copy()

        # update new state
        new_board = [sr.copy() for sr in state[1]]
        new_en_passant = None
        check_w, check_b, checkM_w, checkM_b, half_moves = state[4], state[5], state[6], state[7], state[8]

        piece = board[r1][c1]
        target_space = board[r2][c2]

        # if en passant capture
        if en_passant_coord and (r2, c2) == en_passant_coord:
            new_board[r1][c1], new_board[r2][c2] = ' ', board[r1][c1]
            # if player is white, capturing black pawn so delete pawn below square
            new_board[en_passant_coord[0] \
                      + (1 if player_sign == 1 else -1)][en_passant_coord[1]] = ' '
            success, msg = True, "Captured en passant! "
            half_moves = 0
        elif target_space == ' ':    # not a capture move
            new_board[r1][c1], new_board[r2][c2] = ' ', board[r1][c1]
            # check if castle:
            if piece == 'K' and c2 - c1 == -2 and board[7][0] == 'R':  # White queenside castle
                new_board[7][0], new_board[7][3] = ' ', 'R'
            elif piece == 'K' and c2 - c1 == 2 and board[7][7] == 'R':  # White kingside castle
                new_board[7][7], new_board[7][5] = ' ', 'R'
            elif piece == 'k' and c2 - c1 == -2 and board[0][0] == 'r':  # Black queenside castle
                new_board[0][0], new_board[0][3] = ' ', 'r'
            elif piece == 'k' and c2 - c1 == 2 and board[0][7] == 'r':  # Black kingside castle
                new_board[0][7], new_board[0][5] = ' ', 'r'

            success, msg = True, "Move Success"
            # half move clock
            if piece.lower() == 'p':
                half_moves = 0
            else:
                half_moves += 1
        else:    # is a capture move
            capturedPiece = board[r2][c2]
            new_board[r1][c1], new_board[r2][c2] = ' ', board[r1][c1]
            success, msg = True, "Captured " + capturedPiece
            half_moves = 0


        # update en passant square
        if success:  # update en passant square if pawn moved 2 spaces
            if ((piece == 'p' and player_sign == -1) \
                or (piece == 'P' and player_sign == 1)) \
                    and abs(r2 - r1) == 2:  # pawn moved 2 spaces
                new_en_passant = (r2 - 1 if player_sign == -1 else r2 + 1, c2)
            else:
                new_en_passant = None

        # CHECK check for check or checkmate
        if success:  # only update check states if move was successful
            other_player = player_sign * -1
            if boardUtil.isCheck(other_player, new_board, en_passant_coord):
                possible_move_count \
                    = len(boardUtil.getLegalMoves(other_player, new_board, en_passant_coord, u_castle)) \
                    + len(boardUtil.getLegalCaptureMoves(other_player, new_board, en_passant_coord))
                if other_player == 1:
                    check_w, msg = True, 'White in CHECK'
                    # if white has no moves to relieve check then checkmate
                    if possible_move_count == 0:
                        checkM_w, msg = True, 'CHECKMATE'
                else:
                    check_b, msg = True, 'Black in CHECK'
                    # if black has no moves to relieve check then checkmate
                    if possible_move_count == 0:
                        checkM_b, msg = True, 'CHECKMATE'
            else:
                check_w, check_b = False, False

        # Update Castle rights
        if success:
            u_castle = state[3].copy()
            if piece == 'K':  # white king moved
                u_castle['K'], u_castle['Q'] = 0, 0
            elif piece == 'k':  # black king moved
                u_castle['k'], u_castle['q'] = 0, 0
            elif piece == 'r' and (r1, c1) == (0, 0):  # black queenside rook moved
                u_castle['q'] = 0
            elif piece == 'r' and (r1, c1) == (0, 7):  # black kingside rook moved
                u_castle['k'] = 0
            elif piece == 'R' and (r1, c1) == (7, 0):  # white queenside rook moved
                u_castle['Q'] = 0
            elif piece == 'R' and (r1, c1) == (7, 7):  # white kingside rook moved
                u_castle['K'] = 0

        # Pawn promotion
        if success:
            if piece == 'P' and r2 == 0:  # white has reached 8th rank
                new_board[r2][c2] = 'Q'
            if piece == 'p' and r2 == 7:
                new_board[r2][c2] = 'q'

        updated_state = (player_sign * -1, new_board, new_en_passant, u_castle,
                         check_w, check_b, checkM_w, checkM_b, half_moves,
                         state[9] + 1 if player_sign == -1 else state[9])

        return updated_state

    @staticmethod
    def getLegalMoves(player_sign, board, en_passant_coords: tuple, castle_rights=None) -> list:
        """Gets all legally possible moves for player"""

        if castle_rights is None:
            castle_rights = {}

        potential_moves = []
        for row in range(len(board)):
            for col in range(len(board)):
                piece = board[row][col]
                if (player_sign == -1 and piece in chessPiece.black_pieces) \
                        or (player_sign == 1 and piece in chessPiece.white_pieces):
                    piece_moves = \
                        boardUtil.getPieceLegalMoves(piece, (row, col), board, en_passant_coords, castle_rights)
                    potential_moves.extend(piece_moves)

        movesList = [move for move in potential_moves
                     if boardUtil.moveRelievesCheck(player_sign, move, board, en_passant_coords)]

        return movesList

    @staticmethod
    def getPotentialCaptureMoves(player_sign, board, en_passant_coord: tuple):
        """Get a list of all potential capture moves.  Only considers movement and does not
        verify if move results in player being in CHECK"""
        potential_moves = []
        for row in range(len(board)):
            for col in range(len(board)):
                piece = board[row][col]
                if (player_sign == -1 and piece in chessPiece.black_pieces) \
                        or (player_sign == 1 and piece in chessPiece.white_pieces):
                    piece_moves = \
                        boardUtil.getPieceCaptureMoves(piece, (row, col), board, en_passant_coord)
                    potential_moves.extend(piece_moves)
        return potential_moves

    @staticmethod
    def getLegalCaptureMoves(player_sign, board, en_passant_coord: tuple):
        """Get a list of all possible capture moves for the player given a board and en passant coordinates.
        Difference from getPotentialCaptureMoves is that we make sure a move does not result in being in CHECK
        """
        potential_moves = boardUtil.getPotentialCaptureMoves(player_sign, board, en_passant_coord)
        movesList = [move for move in potential_moves
                     if boardUtil.moveRelievesCheck(player_sign, move, board, en_passant_coord)]
        return movesList

    @staticmethod
    def getPieceLegalMoves(piece, position: tuple, board: list, en_passant_coords: tuple, castle_rights=None):
        """returns list of legal move instructions given board etc"""
        if castle_rights is None:
            castle_rights = {}

        if piece == 'P' or piece == 'p':
            return pawn.getNormalMoves(piece, position, board)
        elif piece == 'R' or piece == 'r':
            return rook.getNormalMoves(piece, position, board)
        elif piece == 'B' or piece == 'b':
            return bishop.getNormalMoves(piece, position, board)
        elif piece == 'Q' or piece == 'q':
            return queen.getNormalMoves(piece, position, board)
        elif piece == 'K' or piece == 'k':
            player_sign = 1 if piece == 'K' else -1
            return king.getNormalMoves(piece, position, board, castle_rights,
                                       boardUtil.isCheck(player_sign, board, en_passant_coords))
        elif piece == 'N' or piece == 'n':
            return knight.getNormalMoves(piece, position, board)
        else:
            return []

    @staticmethod
    def getPieceCaptureMoves(piece, position: tuple, board: list, en_passant_coords: tuple):
        """returns list of potential capture move instructions given board"""
        if piece == 'P' or piece == 'p':
            return pawn.getCaptureMoves(piece, position, board, en_passant_coords)
        elif piece == 'R' or piece == 'r':
            return rook.getCaptureMoves(piece, position, board)
        elif piece == 'B' or piece == 'b':
            return bishop.getCaptureMoves(piece, position, board)
        elif piece == 'Q' or piece == 'q':
            return queen.getCaptureMoves(piece, position, board)
        elif piece == 'K' or piece == 'k':
            return king.getCaptureMoves(piece, position, board)
        elif piece == 'N' or piece == 'n':
            return knight.getCaptureMoves(piece, position, board)
        else:
            return []

    @staticmethod
    def getKingPos(sign, board):
        """returns king position, assuming white king is usually at bottom and black king at top of board"""
        if sign == -1:
            for i in range(len(board)):
                for j in range(len(board)):
                    if board[i][j] == 'k':
                        return i, j
        elif sign == 1:
            for i in range(len(board) - 1, -1, -1):
                for j in range(len(board)):
                    if board[i][j] == 'K':
                        return i, j
        return -1, -1

    @staticmethod
    def isCheck(player_sign, board, en_passant_coords):
        """Checks if the given player's king is under attack"""
        capture_moves = boardUtil.getPotentialCaptureMoves(player_sign * -1, board, en_passant_coords)
        # if any moves will capture king, return True
        k_pos = boardUtil.getKingPos(player_sign, board)
        for move in capture_moves:
            if move[1] == k_pos:
                return True
        return False

    @staticmethod
    def moveRelievesCheck(player_sign: int, move: tuple, board: list, en_passant_coords: tuple):
        """Checks if any potential move will relieve the current check placed on player_sign"""
        board_copy = [sr.copy() for sr in board]
        x1, y1 = move[0]
        x2, y2 = move[1]
        board_copy[x1][y1], board_copy[x2][y2] = ' ', board_copy[x1][y1]
        if boardUtil.isCheck(player_sign, board_copy, en_passant_coords):
            return False
        else:
            return True

    @staticmethod
    def getPieceAtCoords(row: int, col: int, board: list):
        """returns the piece at board array row, col, None for invalid board positions"""
        if 0 <= row < len(board) and 0 <= col < len(board):
            return board[row][col]
        else:
            return None

    @staticmethod
    def getPieceAtPos(pos, board: list):
        x1, y1 = boardUtil.posToCoord(pos)
        return boardUtil.getPieceAtCoords(x1, y1, board)

    @staticmethod
    def posToCoord(pos):
        """returns array row index and col index of pos in the array
        ex: a1 returns 7, 0, meaning 7th row, 0th item, so last row first item in terms of array indexing """
        return 8 - int(pos[1]), boardUtil.colToNum(pos[0])    # row, col

    @staticmethod
    def coordToPos(coord: tuple):
        """takes array index coordinates and converts to chess board grid notation"""
        return chr(97 + coord[1]) + str(8 - coord[0])

    @staticmethod
    def colToNum(col):
        """Takes column letter and converts to array index"""
        return ord(col.lower()) - 97    # ord('a') == 97

    @staticmethod
    def clearScreen():
        if name == 'nt':    # for windows
            system('cls')
        else:    # for mac and linux(here, os.name is 'posix')
            system('clear')

    @staticmethod
    def printGameStatePretty(state: tuple, recent_action: tuple, game_history: list):
        """prints game state as ascii"""

        boardUtil.clearScreen()
        board = state[1]

        left_buff, right_buff = 5, 7
        big_seperator = ' || '
        big_row_divider = '=' * (8 * 5 + right_buff)
        small_row_divider = '-' * (8 * 5 + right_buff)
        ref_characters = ' ' * left_buff + '  | '.join([ch for ch in 'abcdefgh'])

        chessPrint.screenPrinter.printCyan(ref_characters)
        chessPrint.screenPrinter.printCyan(big_row_divider)

        for row in range(8):
            rank = str(8 - row)

            if row % 2 == 1:
                chessPrint.screenPrinter.printGray(rank + big_seperator, end='')
            else:
                print(rank + big_seperator, end='')

            for col in range(8):
                if recent_action is not None and (row, col) == recent_action[1]:
                    chessPrint.screenPrinter.printRed(
                        chessPiece.piece_symbols[board[row][col]] + ' ', end='')
                elif board[row][col] in chessPiece.white_pieces:
                    chessPrint.screenPrinter.printYellow(
                        chessPiece.piece_symbols[board[row][col]] + ' ', end='')
                elif board[row][col] in chessPiece.black_pieces:
                    chessPrint.screenPrinter.printGreen(
                        chessPiece.piece_symbols[board[row][col]] + ' ', end='')
                else:
                    print('  ', end='')

                if col != 7:
                    if (row % 2 == 0 and col % 2 == 0) \
                        or (row % 2 == 1 and col % 2 == 1):
                        chessPrint.screenPrinter.printGray(' | ', end='')
                    else:
                        print(' | ', end='')
                else:
                    if row % 2 == 1:
                        chessPrint.screenPrinter.printGray(big_seperator + rank)
                    else:
                        print(big_seperator + rank)


            if row < 8 - 1:
                if row % 2 == 1:
                    print(small_row_divider)
                else:
                    chessPrint.screenPrinter.printGray(small_row_divider)
            else:
                chessPrint.screenPrinter.printCyan(big_row_divider)

        chessPrint.screenPrinter.printCyan(ref_characters)

        if state[2] is not None:
            print("En passant square:", state[2])
        if state[3]:
            print("Castle rights:", state[3])

        print('\nHistory:', str(game_history))

        if game_history:
            print('Most Recent Move: ', str(game_history[-1]))

        if state[4]:
            chessPrint.screenPrinter.printYellow("YELLOW is CHECKED")
        if state[5]:
            chessPrint.screenPrinter.printGreen("GREEN is CHECKED")
        if state[6]:
            chessPrint.screenPrinter.printYellow("YELLOW is CHECKMATED!")
        if state[7]:
            chessPrint.screenPrinter.printGreen("GREEN is CHECKMATED!")