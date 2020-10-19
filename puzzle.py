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
	# print("{} is a {}x{} grid".format(str(filepath),dimensions,dimensions))
	state = flatten(state)

	return state

	# WE need an error thing to detect wrong things

# Prints game state
def DebugPrint(fileToPrint):
	dimensions = int(math.sqrt(len(fileToPrint)))
	state = fileToPrint
	print("")
	for split in range(dimensions):
		for digit in range(dimensions):
			index = dimensions * split + digit
			print(" {}\t".format(state[index]), end = '')

		print("")

	print("")





# moving up
def MoveUp(state):
	modified = copy.deepcopy(state)
	dimensions = int(math.sqrt(len(state)))
	index = state.index("*")

	bottom = True if (index > (dimensions**2 - dimensions)) else False

	if not bottom:
		modified[index] = modified[index+dimensions]
		modified[index+dimensions] = "*"

	return modified

# moving down
def MoveDown(state):
	modified = copy.deepcopy(state)
	dimensions = int(math.sqrt(len(state)))
	index = state.index("*")

	top = True if (index < dimensions) else False

	if not top:
		modified[index] = modified[index-dimensions]
		modified[index-dimensions] = "*"

	return modified

# moving right
def MoveRight(state):
	modified = copy.deepcopy(state)
	dimensions = int(math.sqrt(len(state)))
	index = state.index("*")

	left = True if (index % dimensions == 0) else False

	if not left:
		modified[index] = modified[index-1]
		modified[index-1] = "*"

	return modified

# moving left
def MoveLeft(state):
	modified = copy.deepcopy(state)
	dimensions = int(math.sqrt(len(state)))
	index = state.index("*")

	right = True if ((index + 1) % dimensions == 0) else False

	if not right:
		modified[index] = modified[index+1]
		modified[index+1] = "*"

	return modified




# Takes game state, returns iterable containing adjacent states
def ComputeNeighbors(state):
	dimensions = int(math.sqrt(len(state)))
	index = state.index("*")
	possibleStates = []

	if not MoveRight(state) == state:
		yes = (MoveRight(state)[index], MoveRight(state))
		possibleStates.append(yes)
		# DebugPrint(MoveRight(state))
	if not MoveLeft(state) == state:
		yes = (MoveLeft(state)[index], MoveLeft(state))
		possibleStates.append(yes)
		# DebugPrint(MoveLeft(state))
	if not MoveUp(state) == state:
		yes = (MoveUp(state)[index], MoveUp(state))
		possibleStates.append(yes)
		# DebugPrint(MoveUp(state))
	if not MoveDown(state) == state:
		yes = (MoveDown(state)[index], MoveDown(state))
		possibleStates.append(yes)
		# DebugPrint(MoveDown(state))

	print(possibleStates)

def IsGoal(state):
	goal = [str(n+1) for n in range(len(state)-1)]
	goal.append("*")
	return True if state == goal else False


pee = LoadFromFile("Test.txt")

DebugPrint(pee)
print(IsGoal(pee))
