import chessPrint
from game import chessGame
import player
import boardUtil

class chess():
    """Class that holds the game instance, displays welcome screens
    sets up and runs the game loop"""
    def __init__(self):
        self.startMsg = """Welcome to Peter's Chess!
        
    In this game, you can choose to play another human
    or try your skills against the computer AI
    
    -- Playing Instructions --    
    Due to the poor visibility of black pieces on a console window,
    pieces in chess originally in BLACK are displayed in GREEN,        
    and pieces in chess originally in WHITE are displayed in YELLOW,        
    
    Certain systems have different fonts so 
    if you find it hard to distinguish the following pieces,
    try enlarging your terminal fonts or 
    switching to a different font before moving on.
    ♖ ♘ ♗ ♕ ♔ ♗ ♘ ♖  
    ♙ ♙ ♙ ♙ ♙ ♙ ♙ ♙ 
    ♟ ♟ ♟ ♟ ♟ ♟ ♟ ♟ 
    ♜ ♞ ♝ ♛ ♚ ♝ ♞ ♜ 
    
    """
        self.moveMsg = """
    -- Moving Instructions --
    
    The grid is displayed in the following format:
     a  | b  | c  | d  | e  | f  | g  | h
===============================================
8 || ♖  | ♘  | ♗  |    | ♔  |    | ♘  | ♖  || 8
-----------------------------------------------
7 || ♙  | ♙  | ♙  | ♙  |    | ♙  | ♙  | ♙  || 7
-----------------------------------------------
6 ||    |    |    |    | ♙  |    |    |    || 6
-----------------------------------------------
5 ||    |    |    |    |    |    |    |    || 5
-----------------------------------------------
4 || ♟  |    |    |    |    | ♕  |    |    || 4
    ...
    
    to move a piece, type in the current location of the piece,
    immediately followed by the destination location
    
    For instance, to move the pawn at d7 -> d5, type d7d5
    You can type 'quit' on your turn to quit the game
    """
        self.playerSelectionMsg = """Select Opponent:
    
    You will be playing as YELLOW (White), and will go first.
    The opponent will be playing as GREEN (Black).
    Type in the number of your opponent from the following:
    
    1. Another human player
    
    There are 3 computer agents to choose from.
    
    2. Random AI - Makes moves at random unless there is a capture move, 
    in which case a random capture move will be chosen
        
    3. Alpha-Beta AI - A Minimax AI where the Computer will try to minimize your expected value 
    of the game state for every move it makes. The search space is slightly more optimized, 
    meaning the AI can search one more depth than normal minimax in the same time.
    
    4. Alpha-Beta AI, depth+1 - same as 3 but searches one more depth.  
    NOTE: The time taken for each move will be around 10-20 seconds in this mode. 
    
    DEMO Mode
    5. Demo Mode - Choose this mode if you want the computer to play against itself. 
    In this case, YELLOW is Random AI, while GREEN is played by Alpha-Beta AI
    
    6. Slow Demo - YELLOW Alpha-Beta vs GREEN Alpha-Beta depth+1.  
    Observe the effect of increasing search depth.
    
    """
        self.game = None

    def run(self):
        """Shows welcome messages and gets input to determine
         how to instantiate and execute the chess game"""

        # Welcome messages
        boardUtil.boardUtil.clearScreen()
        chessPrint.screenPrinter.printReplace(self.startMsg)
        input("\nPress Enter to Continue")

        boardUtil.boardUtil.clearScreen()
        chessPrint.screenPrinter.printReplace(self.moveMsg)
        input("\nPress Enter to Continue")

        boardUtil.boardUtil.clearScreen()
        chessPrint.screenPrinter.printReplace(self.playerSelectionMsg)

        # Select game type
        oppType = 0
        while True:
            playerChoice = input("Enter a number for the type of opponent (1-6):")
            if playerChoice.isnumeric():
                if 1 <= int(playerChoice) <= 6:
                    oppType = int(playerChoice)
                    break
            print("Error, input a choice from 1-6")

        human1 = player.humanPlayer('Human YELLOW')
        random1 = player.randomAIPlayer('Random AI YELLOW')
        human2 = player.humanPlayer('Human GREEN')
        random2 = player.randomAIPlayer('Random AI GREEN')
        alphaBeta1 = player.alphabetaAIPlayer('AlphaBeta AI YELLOW', 1, 2)
        alphaBeta2 = player.alphabetaAIPlayer('AlphaBeta AI GREEN', -1, 2)
        alphaBeta3 = player.alphabetaAIPlayer('AlphaBeta depth+1 AI GREEN', -1, 3)

        # instantiate game
        self.game = chessGame()
        alphaBeta1.setGame(self.game)
        alphaBeta2.setGame(self.game)
        alphaBeta3.setGame(self.game)

        # set players according to input
        players = {+1: random1, -1: alphaBeta2}
        if oppType == 1:
            players = {+1: human1, -1: human2}
        elif oppType == 2:
            players = {+1: human1, -1: random2}
        elif oppType == 3:
            players = {+1: human1, -1: alphaBeta2}
        elif oppType == 4:
            players = {+1: human1, -1: alphaBeta3}
        elif oppType == 6:
            players = {+1: alphaBeta1, -1: alphaBeta3}

        # PLAY the game!
        endState = self.game.play(players)

        # print final state once game is over
        boardUtil.boardUtil.printGameStatePretty(endState, None, self.game.history)
        print('Game over, \nPlayer1=', players[1].name, '\nPlayer2:', players[-1].name)


# Run / Save the game on game end
my_chess = chess()
my_chess.run()
save = input('save game to file? (y/n)')
if save.lower() == 'y':
    saved_game = open('my_game.txt', 'wt', encoding='utf-8')
    saved_game.writelines('\n'.join(my_chess.game.history))
    saved_game.close()
    print("saved game to my_game.txt")