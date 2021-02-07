# Console Chess with AI

Author: Peter (Young Ha) Kim

Semester: Fall 2020

Contact information: vasthorizon@gmail.com

## Program Overview

A simple console chess program with Human vs AI (Minimax with Alpha-Beta pruning, or just Random AI).   Also supports a demo mode of Random AI vs Minimax AI

## Running the program

After cloning/downloading, simply run main.py using python from the command line.

```bash
python ./main.py
```

## Usage

1. OS: Built for Windows 10, Python 3.8.  I have also tested on MacOS.  Not sure if it will run on linux.

2. Screen fonts:  It is recommended to enlarge the font size to at least 16 points for the chess pieces to be well visible (or enlarge screen using Command+ on Mac).  Depending on the system and the font, the bishop and pawn may look very similar.  

3. You can choose between 6 different modes of play:

* 1. Human vs Human
* 2. Human vs Random AI
* 3. Human vs AlphaBeta AI
* 4. Human vs AlphaBeta AI depth+1
* 5. Random AI vs AlphaBeta AI
* 6. Random AI vs AlphaBeta AI depth+1

Random AI: makes moves instantly since it just chooses a move at random, unless there is a capture move available.  If a capture can be done, random AI will prioritize the capture over other moves.

AlphaBeta AI: makes a move depending on the board evaluation function at the leaf node of a given depth of the search tree.  To make gameplay faster, the depth is only 2.  This usually means a move is made within 1-2 seconds for most cases.

AlphaBeta AI depth+1 : same as AlphaBeta AI, but searches to 3 moves ahead.  Each move takes 5-20 seconds at a time and is a bit more challenging to play.

## Movement
On your turn, type in the command as a four letter sequence with no spaces, in the format [a-h][1-8][a-h][1-8].  For instance, if you want to move the piece on coordinate 'e2' to 'e4', you can simply type 'e2e4'

The program will automatically determine if the move is valid based on what piece is selected on the cell and the state of the board.  If you get a message 'Invalid Move', make sure you have the right coordinates and that your move will not result in the King being captured.


## Saving History
You can save the game history at the end of the game.  Just press 'y' when asked if you want to save.  Note that this will overwrite any existing history file in the directory.


## Contributing
I am very much a beginner at chess and thus have a hard time playing against AlphaBeta AI depth+1 ( option 4).  If you are good at chess and beat the computer in this mode, please do share the history with me so that I can incorporate it as a learning case.  Thanks!

## Errata
I realize that chess can have certain corner cases.  I tried my best to run over 1 hundred games to make sure nothing was wrong, but if you see any behavior which is not legal under the rules of chess, please do let me know.
