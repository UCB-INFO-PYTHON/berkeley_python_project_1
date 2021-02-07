import copy

import chessPiece
from player import *

class chessGame():
    """Game definition class, designed to work for a state-based game
    which can be run on various RL algorithms
    The game start, end, play are defined here"""
    def __init__(self):
        self.board = [["r", "n", "b", "q", "k", "b", "n", "r"],
                      ["p","p","p","p","p","p","p","p"],
                      [" "," "," "," "," "," "," "," "],
                      [" "," "," "," "," "," "," "," "],
                      [" "," "," "," "," "," "," "," "],
                      [" "," "," "," "," "," "," "," "],
                      ["P","P","P","P","P","P","P","P"],
                      ["R","N","B","Q","K","B","N","R"]]
        self.history = []    # history of all moves
        self.half_move_clock = 0

    def startState(self):
        """Defines a start state and should be called at the beginning of a game,
        as it copies the values from the self.board object"""
        return (1,      # 0 white moves first
            [sr.copy() for sr in self.board],    #2 board
            None,   #2 en passant coords
            {'Q': 1, 'K': 1, 'q': 1, 'k': 1},   #3 castle_rights
            False,  #4 check_w,
            False,  #5 check_b,
            False,  #6 check_mate_w,
            False,  #7 check_mate_b,
            0,      #8  number of half moves
            0,)      #9  number of full moves

    def isEnd(self, state):
        """checks if either player is checkmated and returns true if so"""
        if state[6] or state[7] or self.half_move_clock > 50 or state[9] > 500:    # more than 500 moves means something is wrong
            return True

    def utility(self, state):
        """if black wins, the agent (white) loses, so utility is -10000,
        otherwise +10000 if the agent (white) wins.
        This skews any evaluation function to go for a CheckMate"""
        white_checkmated, black_checkmated = state[6], state[7]
        if white_checkmated:
            return float('-10000')
        elif black_checkmated:
            return float('+10000')
        else:
            return 0

    def eval(self, state):
        """returns interim utility for limited depth search.
         the utility value is based on some features, such as material, captures, mobility etc"""
        material, b_mat, w_mat = 0, 0, 0
        # set material value
        piece_dict = {}
        for row in range(len(state[1])):
            for col in range(len(state[1][row])):
                piece = state[1][row][col]
                piece_dict[piece] = piece_dict.get(piece, 0) + 1
        for ch in chessPiece.chessPiece.black_pieces:
            b_mat += piece_dict.get(ch, 0) * chessPiece.chessPiece.piece_values[ch]
        for ch in chessPiece.chessPiece.white_pieces:
            w_mat += piece_dict.get(ch, 0) * chessPiece.chessPiece.piece_values[ch]
        material = w_mat - b_mat

        # get check value
        check_value = 0
        if boardUtil.boardUtil.isCheck(1, state[1], state[2]):
            check_value = 5
        elif boardUtil.boardUtil.isCheck(-1, state[1], state[2]):
            check_value = -5

        # mobility
        mobility = 0
        mob_p1 = 0.1 * len(boardUtil.boardUtil.getLegalCaptureMoves(1, state[1], state[2])) \
            + 0.01 * len(boardUtil.boardUtil.getLegalMoves(1, state[1], state[2]))
        mob_p2 = 0.1 * len(boardUtil.boardUtil.getLegalCaptureMoves(-1, state[1], state[2])) \
                 + 0.01 * len(boardUtil.boardUtil.getLegalMoves(-1, state[1], state[2]))
        mobility = mob_p1 - mob_p2

        return material + check_value + mobility

    def actions(self, state):
        """returns a list with two lists, a list of legal capture moves and a list of legal non-capture moves,
        given a state"""
        return [boardUtil.boardUtil.getLegalCaptureMoves(state[0], state[1], state[2]),
                 boardUtil.boardUtil.getLegalMoves(state[0], state[1], state[2], state[3])]

    def player(self, state):
        """Just returns the turn value of the state
        1 for agent, -1 for opponent"""
        return state[0]

    def successor(self, state, action):
        """returns an updated state given an action (move from coord1 to coord2)"""
        updated_state = boardUtil.boardUtil.executeMoveAction(state, action)
        return updated_state

    def play(self, players: dict):
        """Runs the actual game loop, calling the player objects in the player dictionary
        for each turn, until either side quits or no more moves are possible"""
        state = self.startState()
        recent_action = None
        while not self.isEnd(state):
            boardUtil.boardUtil.printGameStatePretty(state, recent_action, self.history)
            cur_player = self.player(state)
            policy = players[cur_player]
            action = policy.getAction(state)
            if action is None:  # exit game
                print("STALEMATE! Ending game")
                break
            if action == 'quit':
                print('Player', cur_player, 'resigns')
                break

            orig = state[1][action[0][0]][action[0][1]]    # piece moved
            dest = state[1][action[1][0]][action[1][1]]    # piece captured

            state = self.successor(state, action)
            self.history.append(chessPiece.chessPiece.piece_symbols[orig] + (' x' if dest is not ' ' else ' ')
                                + boardUtil.boardUtil.coordToPos(action[1])
                                + (chessPiece.chessPiece.piece_symbols[dest] if dest is not ' ' else ' '))
            recent_action = action
        return state
