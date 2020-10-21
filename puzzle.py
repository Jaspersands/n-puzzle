#Japer Dan Colin maybe Akis n Kunde
import math
import copy # I import this because without it, the Move functions weren't Pure

# Takes a nested list and flattens it. We coded this in class at one point
def flatten(nested_list):
    flat_list = []

    def flatten_func(sublist):
        for element in sublist:
            if isinstance(element, list):
                flatten_func(element)
            else:
                flat_list.append(element)


    flatten_func(nested_list)
    return flat_list

# Makes tuple (dimensions, empty location, state)
def LoadFromFile(filepath):
	state = []
	f = open(filepath, "r")
	for i in f:
		state.append(i.strip().split("\t" or "\n"))
	dimensions = int(state.pop(0)[0])

	state = flatten(state)

	valid = True

	# Troubleshooting errors
	if len(state) != dimensions**2: # Not proper rows and columns
		valid = False
		print("You don't have {} rows and {} columns".format(dimensions,dimensions))
		return None
	if state.count("*") == 0: # No empty spaces
		valid = False
		print("You need an empty space")
	if state.count("*") > 1: # both "0" and "*"
		valid = False
		print("You have too many empty spaces")

	return ("*", state) if valid else None



# Prints game state
def DebugPrint(fileToPrint):
	if(fileToPrint == None):
		print("Gimme a proper game state ya dipshit")
		return
	dimensions = int(math.sqrt(len(fileToPrint[1])))
	state = fileToPrint[1]
	print()
	print("")
	for split in range(dimensions):
		for digit in range(dimensions):
			index = dimensions * split + digit
			print(" {}\t".format(state[index]), end = '')

		print("")

	print("")





# moving up
def MoveUp(state):
	modified = copy.deepcopy(state[1])
	dimensions = int(math.sqrt(len(modified)))
	index = modified.index("*")

	bottom = True if (index > (dimensions**2 - dimensions)) else False
	if not bottom:
		modified[index] = modified[index+dimensions]
		modified[index+dimensions] = "*"
		return modified[index], modified
	else:
		return None



# moving down
def MoveDown(state):
	board = state[1]
	modified = copy.deepcopy(board)
	dimensions = int(math.sqrt(len(board)))
	index = board.index("*")

	top = True if (index < dimensions) else False

	if not top:
		modified[index] = modified[index-dimensions]
		modified[index-dimensions] = "*"
		return modified[index], modified
	else:
		return None

# moving right
def MoveRight(state):
	board = state[1]
	modified = copy.deepcopy(board)
	dimensions = int(math.sqrt(len(board)))
	index = board.index("*")

	left = True if (index % dimensions == 0) else False

	if not left:
		modified[index] = modified[index-1]
		modified[index-1] = "*"
		return modified[index], modified
	else:
		return None

# moving left
def MoveLeft(state):
	board = state[1]
	modified = copy.deepcopy(board)
	dimensions = int(math.sqrt(len(board)))
	index = board.index("*")

	right = True if ((index + 1) % dimensions == 0) else False

	if not right:
		modified[index] = modified[index+1]
		modified[index+1] = "*"
		return modified[index], modified
	else:
		return None



# Takes tuple of (last_move, state), returns iterable containing adjacent states
def ComputeNeighbors(state):
	if(state == None):
		print("Gimme a proper game state ya dipshit")
		return
	dimensions = int(math.sqrt(len(state[1])))
	last = state[0]
	board = copy.deepcopy(state)
	index = board.index("*")
	possibleStates = []


	if not MoveRight(board) == None:
		possibleStates.append(MoveRight(board))
		DebugPrint(MoveRight(board))
	if not MoveLeft(board) == None:
		possibleStates.append(MoveLeft(board))
		DebugPrint(MoveLeft(board))
	if not MoveUp(board) == None:
		possibleStates.append(MoveUp(board))
		DebugPrint(MoveUp(board))
	if not MoveDown(board) == None:
		possibleStates.append(MoveDown(board))
		DebugPrint(MoveDown(board))

	print(possibleStates)

# is this the goal state
def IsGoal(state):
	goal = [str(n+1) for n in range(len(state)-1)]
	goal.append("*")
	return True if state == goal else False

# Breadth first search
def BFS(state):
	frontier = [state]
	discovered = set(state)
	parents = {state: None} # dict

	while frontier is not None:
		current_state = frontier.pop(0)
		discovered.add(current_state)

		if IsGoal(current_state):
			# return the path you need by backtracking in parents
			return parents

		for neighbor in ComputeNeighbors(current_state):
			if neighbor not in discovered:
				frontier.append(neighbor)
				discovered.add(neighbor)
				parents[neighbor] = current_state





pee = LoadFromFile("Test.txt")



ComputeNeighbors(pee)
BFS(pee)
