# Connect4-MiniMaxAI
This uses minimax algorithm to create an AI which plays Connect4

Connect 4: A simple two player game in which each player takes turns placing coloured pieces into a 6 row by 7 column grids. The turn player chooses a column to place their piece, and the piece falls to the lowest position in the column not already occupied by another piece. The goal for each player is to be the first player to create a horizontal, vertical, or diagonal line of 4 or more of their pieces in an adjacent line.

The AI plays with using the minimax algorithm to determine what move to make. User can determine speed by defining a cutoff in the game tree. Depth for AI: 4 = less than a sec, 5 = 5 sec, 6 = 40 sec, 7 = approx 3 min. Higher the depth better the solution.
A better algorithm with Minimax is alpha beta prunning which I will implement in my chess game, published in a separate repositary.

To play the game click on file with name "Connect4.cpython-37". You can select to play with human by pressing 1 or 2 for AI.
