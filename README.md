# This is a GO - like game.

Author: Bernard Śniegowski

For information about the original GO game see https://en.wikipedia.org/wiki/Go_(game)


# ABOUT GAME AND RULES

The game uses pygame library


## Board:
- the game board is a grid of dimension n x n
- one can draw circles (which is called "placing stones")
- stones can be placed only on the intersection points of the grid
- two stones are considered adjacent if there is a straight line connecting them and there is no other stone or no intersection point between them

## Players and game window:
- there are two players, WHITE and BLACK
- their score is at the top of the window ("WHITE:" and "BLACK")
- WHITE takes first turn
- each player has limited time - the timers are ("Time left:") in the top of the program window
- for each turn there is a limited time to make a move shown by timer "Time left in this turn:"
- if a player does not make a move in time, his turn is over and the other player makes a move
- the score of a given player is the number of his stones on the board

## Killing enemy's stones:
If after placing a stone there is a group of opponent stones such that
1. no stone of this group has an empy field as a neighbour
2. the stones in the group form a connected graph
3. at least one stone in the group has as a neighbour the stone recently placed
then this group is deleted and the opponent's score is updated


## End of game
The game ends, when one player runs out of time or when the board is full with stones



## How to win the game
There are two ways to win the game
1. If the board is full and both players have some time left then the player with higher score wins
2. If one player runs out of time then the other player wins ONLY IF he has higher score. OTHERWISE the result is a DRAW


# CODE DESCRIPTION
Code consist of three main parts:
1. Block of global variable definitions. Some of them are
	- board dimensions - by changing it you decide whether your board has dimensions 9x9, 17x17 and so on
	- size of window
	- size of offset - the distance between board edge and the edge of the window
	- definitions of some colors - you can change them to change the looks of your game
	- radius of circles representing stones
	- an array (list of lists) representing board
2. main() function, which starts the game
3. Some helper functions to maintain the game changes and apply game rules

## Functions description
* -- main() --
As explained above, this is the main function of our program which runs the pygame window

* -- redrawGameWindow() --
Function that constantly redraws window and updates all the changes

* -- drawBoard() --
Functions that draws board on the window surface

* -- closest(x, A) --
Function that finds element in list A that is the closest to X.
A - list of floats (either X or Y coordinates of grid lines
x - X or Y coordinate of a middle of point we want to draw

* -- drawCircle(i, j, COLOR) --
Functions that draws a circle on window surface
i, j - indices of stone on board
COLOR - color of stone to be drawn

* -- find_dead(i, j) --
Checks whether a give group of stones is dead and returns them all (or an empty list if a given group is not dead). It uses BFS to traverse through the group.
i, j - indices of a stone to be checked if it is contained in a dead group of stones

* -- kill_enemies(i, j) --
Tries to kill all opponent neighbours of a given stone using find_dead function
i, j - indices of a given stone

* -- get_neighbours(i, j) --
Function to get all neighbours of a given stone
