import itertools
import random
import re
import time

import boardUtil


class player():
    """Base class for all types of policy agents that can play the game"""
    def __init__(self, name):
        self.name = name

    def getAction(self, state):
        """All child classes must implement this method"""
        pass


class alphabetaAIPlayer(player):
    """Minimax policy player (AI) with alpha beta pruning of the search tree.
    Does a limited depth search for possible moves and evaluates leaf nodes with chessGame.eval()"""
    def __init__(self, name, my_sign, depth=2):
        super().__init__(name)
        self.my_sign = my_sign
        self.search_depth = depth
        self.gameClass = None
        self.explored = 0

    def setGame(self, gameClass):
        self.gameClass = gameClass

    def getAction(self, gameState):
        """Runs recursion for AlphaBeta minimax algorithm and returns an action"""
        print(self.name, 'is thinking...')
        self.explored = 0
        start = time.time()

        def alphabeta(state, d, a, b, isMax):
            self.explored += 1

            if self.gameClass.isEnd(state):
                return (self.gameClass.utility(state), None)
            elif d == 0:
                return (self.gameClass.eval(state), None)

            actions = self.gameClass.actions(state)
            all_moves = list(itertools.chain.from_iterable(actions))

            if isMax:    # 1 is maximizing player
                value = float('-inf')
                act = None
                for move in all_moves:
                    v, ac = alphabeta(self.gameClass.successor(state, move), d - 1, a, b, False)
                    if v > value:
                        value, act = v, move
                    a = max(a, value)
                    if a >= b:
                        break
                return value, act
            else:
                value = float('+inf')
                act = None
                for move in all_moves:
                    v, ac = alphabeta(self.gameClass.successor(state, move), d - 1, a, b, True)
                    if v < value:
                        value, act = v, move
                    b = min(b, value)
                    if a >= b:
                        break
                return value, act

        value, action = alphabeta(gameState, self.search_depth, float('-inf'), float('+inf'),
                                  False if self.my_sign == -1 else True)
        print('Alphabeta AI action', action, 'explored states:', self.explored, 'time:{:.2f}'.format(time.time() - start))
        time.sleep(1)
        return action


class randomAIPlayer(player):
    """Random AI player that does random moves, but with priority for capture moves"""
    def __init__(self, name):
        super().__init__(name)

    def getAction(self, state):
        """Chooses an action at random, but prioritizes capture moves"""
        legalMoves = boardUtil.boardUtil.getLegalMoves(state[0], state[1], state[2], state[3])
        capturelegalMoves = boardUtil.boardUtil.getLegalCaptureMoves(state[0], state[1], state[2])

        if len(capturelegalMoves) > 0:
            move_choice = random.choice(capturelegalMoves)
            print(self.name, 'made move:', move_choice)
            time.sleep(1)
            return move_choice
        elif len(legalMoves) > 0:
            move_choice = random.choice(legalMoves)
            print(self.name, 'made move:', move_choice)
            time.sleep(1)
            return move_choice


class humanPlayer(player):
    """Class for getting input from a human player
    Includes input validation"""
    def __init__(self, name):
        super().__init__(name)
        self.cmd_pattern = re.compile(r'[abcdefgh]\d[abcdefgh]\d')

    def getAction(self, state):
        """Takes human input from command line, checks for validation and returns a move action
        Valid chess moves are also checked against the current state"""
        while True:
            cmd = input('\n' + self.name + "'s turn, Enter Move ('quit' to exit, 'help' for list of legal moves):")

            if cmd.lower() == 'quit':
                return 'quit'

            # make sure input is a valid move!
            legalMoves = boardUtil.boardUtil.getLegalMoves(state[0], state[1], state[2], state[3])
            capturelegalMoves = boardUtil.boardUtil.getLegalCaptureMoves(state[0], state[1], state[2])

            if cmd.lower() == 'help':
                legal_coords = [boardUtil.boardUtil.coordToPos(move[0]) + boardUtil.boardUtil.coordToPos(move[1]) for move in legalMoves]
                legal_capture_coords = [boardUtil.boardUtil.coordToPos(move[0]) + boardUtil.boardUtil.coordToPos(move[1]) for move in capturelegalMoves]
                print('Legal Moves:', end='')
                for move in legal_coords:
                    print(str(move), end=',')
                print('\nLegal capture Moves:', end='')
                for move in legal_capture_coords:
                    print(str(move), end=',')
                print('\n')
                continue

            if len(cmd) != 4:
                print("Error, Command should be of length 4!")
                continue

            if not self.cmd_pattern.match(cmd):
                print("Error, Command should be of format [a-h][digit][a-h][digit]")
                continue

            pos1, pos2 = cmd[0:2], cmd[2:]
            r1, c1 = boardUtil.boardUtil.posToCoord(pos1)
            r2, c2 = boardUtil.boardUtil.posToCoord(pos2)

            if not (0 <= r1 < 8 and 0 <= r2 < 8 and 0 <= c1 < 8 and 0 <= c2 < 8):
                print("Row and Col is wrong! Should be between a-h and 1-8")
                continue


            move = (r1, c1), (r2, c2)
            if move not in legalMoves and move not in capturelegalMoves:
                print("Invalid Move!")
                continue

            return move