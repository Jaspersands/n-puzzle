#revised 10/22 to use correct gamestate structure
import math
import copy
import re

def flatten(nList):
	return [item for temp in nList for item in flatten(temp)] if isinstance(nList, list) else [nList]

#note ALL GAMESTATES SAVED IN TUPLE AS (dimensions, last tile moved, current board list)
def LoadFromFile(filepath):
	global goal
	state = []
	f = open(filepath, "r")
	for value in f:
		state.append(value.strip().split("\t" or "\n"))
	dimensions = int(state.pop(0)[0])
	state = flatten(state)
	valid = True

	# Catch error
	if len(state) != dimensions**2:
		valid = False
		print("You don't have {} rows and {} columns".format(dimensions,dimensions))
		return None
	if state.count("*") == 0:
		valid = False
		print("You need an empty space")
	if state.count("*") > 1:
		valid = False
		print("You have too many empty spaces")

	goalBoard = [str(n+1) for n in range(len(state)-1)]
	goalBoard.append("*")
	goal = dimensions, None, tuple(goalBoard)

	return dimensions, None, tuple(state) if valid else None #is packaged into tuple by default on return with [0] = dims, [1] = move tile, [2] = board

#helper function for board-position rearrangement
def movePlace(board, index, dimensions):
	board = list(board)
	board[index] = board[index+dimensions]
	board[index+dimensions] = "*"
	return tuple(board)

#move 4d functions
def move(state, dir):
	board = copy.deepcopy(state[2])
	emptIndex = board.index("*")
	if dir == "up":
		if emptIndex >= (state[0]**2 - state[0]):
			return "bad"
		else:
			return state[0], board[emptIndex + state[0]], movePlace(board, emptIndex, state[0])
	elif dir == "down":
		if emptIndex < state[0]:
			return "bad"
		else:
			return state[0], board[emptIndex - state[0]], movePlace(board, emptIndex, -state[0])
	elif dir == "right":
		if emptIndex % state[0] == 0:
			return "bad"
		else:
			return state[0], board[emptIndex - 1], movePlace(board, emptIndex, -1)
	elif dir == "left":
		if (emptIndex + 1) % state[0] == 0:
			return "bad"
		else:
			return state[0], board[emptIndex + 1], movePlace(board, emptIndex, 1)
	#catch error
	print("not valid direction")
	return None

#checks validity of move() in 4 cardinal directions and returns possible moves
def ComputeNeighbors(state):
	return tuple([item for item in [move(state, "up"), move(state, "down"), move(state, "right"), move(state, "left")] if item != "bad"])

#comprehensive search function
def search(state, mode, frontier, discovered, parents):
	if mode == "Bidirectional":
		fFrontier = [state]
		bFrontier = [goal]
		fDisc = set()
		fDisc.add(state)
		bDisc = set()
		bDisc.add(state)
		while fFrontier and bFrontier:
			fList, fDisc = search(state, "BFS", fFrontier, fDisc, {state: '0'})
			bList, bDisc = search(goal, "BFS", bFrontier, bDisc, {goal: '0'})
			for i in fDisc.union(bDisc):
				if i in fDisc and i in bDisc:
					return fList[:-1] + bList[:-1:-1] if fList[-1:] == bList[-1:] else fList + bList[::-1]
			return None
	else:
		while frontier:
			cstate = frontier.pop(0) if mode == "BFS" else frontier.pop()
			if cstate not in discovered:
				discovered.add(cstate)
			if cstate[2] == goal[2]:
				return parents[cstate].split(',')[1:], discovered
			for nstate in ComputeNeighbors(cstate):
				if nstate not in discovered:
					print("nstate" + str(nstate))
					frontier.append(nstate)
					discovered.add(nstate)
					parents[nstate] = parents[cstate]+','+nstate[1]
		return None

#bfs
def BFS(state):
	temp = set()
	temp.add(state)
	return search(state, "BFS", [state], temp, {state: '0'})[0]

#dfs
def DFS(state):
	temp = set()
	temp.add(state)
	return search(state, "DFS", [state], temp, {state: '0'})[0]

#bidirectional
def BidirectionalSearch(state):
	return search(state, "Bidirectional", None, None, None)

pee = LoadFromFile("Test copy.txt")
#print(BFS(pee))
print(BidirectionalSearch(pee))
