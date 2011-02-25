Title: PyConnect4
Author: Yohei YASUKAWA
Date: Feb. 25

How To Run
-----------
To run PyConnect4, you need to get python 2.6.x.
After getting the python, you can run the program by typing following command.

	$ python main.py WIDTH HEIGHT CONNECT_N PLAY_STYLE FIRST_PLAYER
	
WIDTH	= a width of board
HEIGHT	= a height of board
CONNECT_N = How many connects players should get to win
PLAY_STYLE:
	'human' = Player vs. Player
	'cpu' 	= Player vs. CPU
FIRST_PLAYER:
	'p1' = Player1(you) plays first.
	'p2' = Player2(human or cpu) plays first.
	
Example Command:

	$ python main.py 3 3 3 cpu p1



How AI Runs
-----------
This AI program runs on a mini-max algorithm,
and scores in the following way.

- If a terminal node shows you win, return 1.
- If a terminal node shows you lose, return -1.
- If a terminal node shows drawn game, return 0.

But the basic mini-max algorithm spends so much time
if a board is equal to or larger than 4x4 with connect 3.
So, I added the algorithm that do pruning a tree that
is needless to calculate, with alpha-beta algorithm.

Thanks to the algorithm, this AI calculates how to
win with less time than before. But there are still
2 concerns on this AI.

First, if AI thinks that it never wins in the given
board, it gives up playing a game. For example,
if a given board is 4x4 with connect 3 and AI is the
last turn, it notices that it cannot win by calculation.
So, all possible moves have -1 score; thereby,
AI gives up and always inserts a coin at the most left,
which seems that AI does not run appropriately.
In other words, if using same board with connect 3 and
AI is the first player, you never win the AI.

This problem is caused by simple scoring function,
return 1, 0, or -1. So, revising the function will be
able to solve the problem.

The other concern is that if a board is much larger,
such as 5x5 with connect 4, the AI does not work
appropriately because AI needs tons of time to
calculate next move. Even though alpha-beta algorithm
helps to reduce calculating time, it is still difficult
for AI to calculate tons of trees. In particular, it needs
tons of time at the first turn in the game.

If I will solve the problem, I will make AI able to evaluate
not-terminal trees. For, AI does not have to calculate up to
terminal nodes if it can evaluate the non-terminal trees. So,
with that function, AI will be able to much larger board.

In conclusion, implementing those functions to this AI
will make it smarter and more functional, and users can
play connect4 with more various board size they need.






