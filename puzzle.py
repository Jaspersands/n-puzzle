#revised 10/22 to use correct gamestate structure
import math
import copy
import re

#is necessary?
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

#is goal?
def IsGoal(state):
	return True if state[2] == goal[2] else False

#bfs algorithm for path search
def BFS(state):
	return FS(state, True)

#dfs algorithm for path search
def DFS(state):
	return FS(state, False)

#____ first search algorithm for path search - dfs and bfs call
def FS(state, bfs):
	frontier = [state]
	discovered = set(str(state[2]))
	parents = {state: '0'}

	while frontier: #while len(frontier) > 0
		current_state = frontier.pop(0) if bfs else frontier.pop()
		if str(current_state[2]) not in discovered:
			discovered.add(str(current_state[2]))
		if IsGoal(current_state):
			return parents[current_state].split(',')[1:]
		for neighbor_state in ComputeNeighbors(current_state):
			if str(neighbor_state[2]) not in discovered:
				print("neighbor_state" + str(neighbor_state))
				frontier.append(neighbor_state)
				discovered.add(str(neighbor_state[2]))
				parents[neighbor_state] = parents[current_state]+','+neighbor_state[1]
	return None

def IsIntersecting(discovered1, discovered2):
	for i in discovered1.union(discovered2):
		if i in discovered1 and i in discovered2:
			return i
	return None

def BidirectionalSearch(state):
	fwFrontier = [state]
	bwFrontier = [goal]
	fwDiscovered = set()
	fwDiscovered.add(state)
	bwDiscovered = set()
	bwDiscovered.add(goal)
	fwParents = {state: '0'}
	bwParents = {goal: '0'}
	while fwFrontier and bwFrontier: #while len whatever > 0 and len whatever > 0
		#forward
		currFwState = fwFrontier.pop(0)
		if currFwState not in fwDiscovered:
			fwDiscovered.add(currFwState)
		for fwNeighbor in ComputeNeighbors(currFwState):
			if fwNeighbor not in fwDiscovered:
				print("fwNeighbor" + str(fwNeighbor))
				fwFrontier.append(fwNeighbor)
				fwDiscovered.add(fwNeighbor)
				fwParents[fwNeighbor] = fwParents[currFwState]+','+fwNeighbor[1]

		#backward
		currBwState = bwFrontier.pop(0)
		if currBwState not in bwDiscovered:
			bwDiscovered.add(currBwState)
		for bwNeighbor in ComputeNeighbors(currBwState):
			if bwNeighbor not in bwDiscovered:
				print("bwNeighbor" + str(bwNeighbor))
				bwFrontier.append(bwNeighbor)
				bwDiscovered.add(bwNeighbor)
				bwParents[bwNeighbor] = bwParents[currBwState]+','+bwNeighbor[1]

		#check solve
		intersection = IsIntersecting(fwDiscovered, bwDiscovered)
		if intersection:
			fwList = fwParents[intersection].split(',')[1:]
			bwList = bwParents[intersection].split(',')[1:]
			if fwList[-1:] == bwList[-1:]:
				fwList.pop()
				bwList.pop()
			fwList += bwList[::-1]
			return fwList

	return None

pee = LoadFromFile("Test copy.txt")
#print(BFS(pee))
print(BidirectionalSearch(pee))
